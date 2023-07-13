import datetime
import os

from pptx import Presentation
from pptx.enum.text import MSO_AUTO_SIZE, MSO_VERTICAL_ANCHOR
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

from mdtree.parser import parse_string, Out, Heading
from mdtree.utils import get_random_theme, get_random_file, read_md_file


class Tree2PPT:
    prs: Presentation = None
    md_str: str = None
    out: Out = None
    tree: Heading = None
    theme: str = None

    def __init__(self, md_str1):
        self.init_pptx()
        self.init_markdown(md_str1)
        self.traverse_tree(self.tree)
        now = datetime.datetime.now().timestamp()
        path = './../myppt/test' + str(now) + '.pptx'
        if not os.path.exists('./../myppt'):
            os.makedirs('./../myppt')
        self.prs.save(path)
        pass

    def init_pptx(self):
        prs = Presentation()
        self.theme = get_random_theme()
        self.prs = prs

    def init_markdown(self, md_str):
        self.md_str = md_str
        out = parse_string(md_str)
        self.out = out
        self.tree = out.main

    def traverse_tree(self, heading):
        self.make_slide_demo(self.prs, heading.text, heading.source)
        if heading.children is not []:
            for child in heading.children:
                self.traverse_tree(child)

    # 简单demo 后续需要多样化的模板
    def make_slide_demo(self, presentation,title,content):
        slide =presentation.slides.add_slide(presentation.slide_layouts[8])
        # 1、新增母版占位符
        placeholder1 = slide.placeholders[1]
        path = get_random_file(self.theme)
        picture = placeholder1.insert_picture(path)
        placeholder2 = slide.placeholders[2]
        placeholder2.element.getparent().remove(placeholder2.element)
        # 2、设置占位符宽高
        picture.left = 0
        picture.top = 0
        picture.width = presentation.slide_width
        picture.height = presentation.slide_height
        # 3、添加文本框1
        shapes = slide.shapes
        text_box = shapes.add_textbox(Inches(0.3), Inches(0.3), Inches(3), Inches(0.8))
        tf = text_box.text_frame  # TextFrame
        tf.clear()  # Clear existing content
        tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
        tf.vertical_anchor = MSO_VERTICAL_ANCHOR.TOP
        # 添加标题
        paragraph = tf.paragraphs[0]
        text = title
        paragraph.text = text
        paragraph.font.bold = True
        paragraph.font.name = "微软雅黑"
        paragraph.font.color.rgb = RGBColor(51, 0, 102)
        paragraph.font.size = Pt(26)
        paragraph.word_wrap = True
        paragraph.vertical_anchor = MSO_VERTICAL_ANCHOR.TOP
        if content is not None:
            paragraph2 = tf.add_paragraph()
            paragraph2.text = content
            paragraph2.font.bold = True
            paragraph2.font.name = "微软雅黑"
            paragraph2.font.color.rgb = RGBColor(51, 0, 102)
            paragraph2.font.size = Pt(18)
            paragraph2.word_wrap = True
            paragraph2.vertical_anchor = MSO_VERTICAL_ANCHOR.TOP


if __name__ == "__main__":
    md_content = read_md_file("./txt.md")
    out = parse_string(md_content)
    Tree2PPT(md_content)







