import markdown

from mdtree.parser import parse_string
from mdtree.tree2ppt import Tree2PPT
from mdtree.utils import read_md_file

if __name__ == '__main__':
    md_content = read_md_file("./readme.md")
    out = parse_string(md_content)
    Tree2PPT(md_content)
    print("==================================================")
    md = markdown.Markdown()
    html1 = md.convert(md_content)
    with open("some_file.html", "w", errors="xmlcharrefreplace") as output_file:
        output_file.write(html1)
