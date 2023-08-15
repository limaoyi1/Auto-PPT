# import math
# import os
# import re
# from io import StringIO, BytesIO
#
# import pptx
# import pandas as pd
# import datetime
# from pptx.util import Pt, Inches, Inches
# from pptx.dml.color import RGBColor
# from pptx.enum.shapes import MSO_SHAPE_TYPE, MSO_SHAPE
# from pptx.enum.text import MSO_AUTO_SIZE, MSO_ANCHOR, MSO_VERTICAL_ANCHOR, PP_PARAGRAPH_ALIGNMENT, PP_ALIGN
# from aiget import get_gpt_data
# from makepage import make_page_left, make_page_right, get_subtitle_by_index, make_page_cv
# from picture import search, check_same_name_file, get_random_file, get_random_theme
# from pptx import Presentation
#
# import warnings
#
# warnings.filterwarnings('ignore')
#
#
# def make_cover(presentation, theme,title):
#     """
#     制作封面
#     :param theme:
#     :param presentation:
#     :param title: 标题
#     :return:
#     """
#     slide = presentation.slides.add_slide(presentation.slide_layouts[8])
#     # 1、新增母版占位符
#     placeholder1 = slide.placeholders[1]
#     path = get_random_file(theme)
#     picture = placeholder1.insert_picture(path)
#     placeholder2 = slide.placeholders[2]
#     placeholder2.element.getparent().remove(placeholder2.element)
#     # 2、设置占位符宽高
#     picture.left = 0
#     picture.top = 0
#     picture.width = presentation.slide_width
#     picture.height = presentation.slide_height
#     # 3、添加文本框
#     text_box = slide.shapes.add_textbox(Inches(0), Inches(0), presentation.slide_width, presentation.slide_height)
#     tf = text_box.text_frame
#     tf.text = title
#     tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
#     tf.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
#     tf.paragraphs[0].font.size = Pt(46)
#     tf.paragraphs[0].font.bold = True
#     tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
#     tf.paragraphs[0].alignment = PP_ALIGN.CENTER
#     tf.vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE
#     tf.paragraphs[0].vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE
#     pass
#
#
# def make_catalogue(presentation, theme, numbers, titles, indexs):
#     """
#     制作目录
#     :param numbers: 编号数组
#     :param titles: 标题数组
#     :return:
#     """
#     slide = presentation.slides.add_slide(presentation.slide_layouts[8])
#     # 1、新增母版占位符
#     placeholder1 = slide.placeholders[1]
#     path = get_random_file(theme)
#     picture = placeholder1.insert_picture(path)
#     placeholder2 = slide.placeholders[2]
#     placeholder2.element.getparent().remove(placeholder2.element)
#     # 2、设置占位符宽高
#     picture.left = 0
#     picture.top = 0
#     picture.width = presentation.slide_width
#     picture.height = presentation.slide_height
#     # 3、添加group组件
#     group_shape = slide.shapes.add_group_shape()
#     group_shape.height = presentation.slide_height
#     print(presentation.slide_height, '----------------------',
#           presentation.slide_height - Inches(0.8) * 2 - Inches(0.6) * len(indexs))
#     # 4、添加文本框
#     for idx in range(len(indexs)):
#         # 添加图标
#         left = Inches(1.2)
#         top = Inches(0)
#         if len(indexs) <= 1:
#             top = Inches(0.8)
#         elif len(indexs) <= 4:
#             top = Inches(0.8) + idx * (
#                         (presentation.slide_height - Inches(0.8) * 2 - Inches(0.5) * len(indexs)) / (len(indexs) - 1))
#         elif len(indexs) <= 6:
#             top = Inches(0.8) + idx * (
#                         (presentation.slide_height - Inches(0.8) * 2 - Inches(0.3) * len(indexs)) / (len(indexs) - 1))
#         else:
#             top = Inches(0.8) + idx * (
#                         (presentation.slide_height - Inches(0.8) * 2 - Inches(0.1) * len(indexs)) / (len(indexs) - 1))
#         width = height = Inches(0.6)
#         oval_shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, width, height)
#         fill = oval_shape.fill
#         fill.solid()
#         fill.fore_color.rgb = RGBColor(68, 84, 106)
#         oval_shape.text = str(idx + 1)
#         oval_shape.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
#         # 添加目录标题
#         text_box_common = slide.shapes.add_textbox(Inches(1.8), top, Inches(5), height)
#         text_frame_common = text_box_common.text_frame
#         if idx == 0:
#             text_frame_common.paragraphs[0].text = titles[indexs[idx]]
#         else:
#             text_frame_common.paragraphs[0].text = str(numbers[indexs[idx]]) + " " + titles[indexs[idx]]
#         text_frame_common.vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE
#     pass
#
#
# def get_title_levels(title):
#     # 使用正则表达式匹配标题数据
#     levels = re.findall(r'\d+', str(title))
#     levels = [int(level) for level in levels]
#     return levels
#
#
# def get_titles_by_level(numbers, level):
#     """
#     通过标题等级获取index
#     :param numbers:
#     :param level:
#     :return:
#     """
#     match_indexs = []
#     for i in range(numbers.size):
#         levels = get_title_levels(numbers[i])
#         if (len(levels) == level):
#             match_indexs.append(i)
#     return match_indexs
#
#
# def make_page_common(numbers, titles, texts, keywords, index):
#     """
#     制作具体页面
#     :return:
#     """
#     slide = prs.slides.add_slide(prs.slide_layouts[8])
#     # 1、新增母版占位符
#     placeholder1 = slide.placeholders[1]
#     path = get_random_file(theme)
#     picture = placeholder1.insert_picture(path)
#     placeholder2 = slide.placeholders[2]
#     placeholder2.element.getparent().remove(placeholder2.element)
#     # 2、设置占位符宽高
#     picture.left = 0
#     picture.top = 0
#     picture.width = prs.slide_width
#     picture.height = prs.slide_height
#     # 3、添加文本框1
#     shapes = slide.shapes
#     text_box = shapes.add_textbox(Inches(0.3), Inches(0.3), Inches(3), Inches(0.8))
#     tf = text_box.text_frame  # TextFrame
#     tf.clear()  # Clear existing content
#     tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
#     tf.vertical_anchor = MSO_VERTICAL_ANCHOR.TOP
#     # 添加标题
#     paragraph = tf.paragraphs[0]
#     text = str(numbers[index]) + " " + titles[index]
#     paragraph.text = text
#     paragraph.font.bold = True
#     paragraph.font.name = "微软雅黑"
#     paragraph.font.color.rgb = RGBColor(51, 0, 102)
#     paragraph.font.size = Pt(26)
#     paragraph.word_wrap = True
#     paragraph.vertical_anchor = MSO_VERTICAL_ANCHOR.TOP
#     # 3、添加 shape 集合
#     subtitle_by_index = get_subtitle_by_index(numbers, index)
#     print(subtitle_by_index, '=================================')
#     group_shape = slide.shapes.add_group_shape()
#     group_shape.height = prs.slide_height
#
#     for idx in range(len(subtitle_by_index)):
#         if (idx != 0):
#             text_box_common = group_shape.shapes.add_textbox(Inches(0.8), Inches(0.4 + idx * 0.8), Inches(8),
#                                                              Inches(0.8))
#             text_frame_common = text_box_common.text_frame
#             text_frame_common.paragraphs[0].text = titles[subtitle_by_index[idx]]
#             text_frame_common.paragraphs[0].font.bold = True
#             text_frame_common.paragraphs[0].font.name = "微软雅黑"
#             text_frame_common.paragraphs[0].font.color.rgb = RGBColor(0, 0, 102)
#             text_frame_common.paragraphs[0].font.size = Inches(0.25)
#             text_frame_common.paragraphs[0].font.word_wrap = True
#             text_frame_common.vertical_anchor = MSO_VERTICAL_ANCHOR.TOP
#             if texts[subtitle_by_index[idx]] is not None and str(texts[subtitle_by_index[idx]]) != "nan":
#                 text_box_common2 = group_shape.shapes.add_textbox(Inches(0.7), Inches(0.3 + idx * 0.8 + 0.5), Inches(8),
#                                                                   Inches(0.8))
#                 text_frame_common2 = text_box_common2.text_frame
#                 text_frame_common2.paragraphs[0].text = str("\t" + texts[subtitle_by_index[idx]])
#                 text_frame_common2.paragraphs[0].font.name = "微软雅黑"
#                 text_frame_common2.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
#                 text_frame_common2.paragraphs[0].font.size = Inches(0.15)
#                 text_frame_common2.paragraphs[0].font.word_wrap = True
#                 text_frame_common2.word_wrap = True
#                 text_frame_common2.paragraphs[0].space_after = Inches(0.1)
#                 text_frame_common2.vertical_anchor = MSO_VERTICAL_ANCHOR.TOP
#                 text_frame_common2.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
#
#     # 添加插图
#     # 获取二级插图keywords
#     keywords_index_ = keywords[index]
#     if keywords_index_ is None and keywords_index_ == "":
#         pass
#     else:
#         b = check_same_name_file("./picture", str(keywords_index_) + ".jpg")
#         if (b == True):
#             link = "./picture" + "/" + str(keywords_index_) + ".jpg"
#         else:
#             link = search(str(keywords_index_))
#         left = Inches(0)  # 图片左侧距离幻灯片左边缘的距离
#         top = Inches(4.5)  # 图片顶部距离幻灯片上边缘的距离
#         width = Inches(4)  # 图片的宽度
#         height = Inches(3)  # 图片的高度
#         ph_picture = slide.shapes.add_picture(link, prs.slide_width - Inches(3), prs.slide_width - Inches(4.5), width,
#                                               height)
#         ph_picture.rotation = 135.0
#         ph_picture.opacity = 0.5
#
#
# def make_ppt(name1):
#     prs = Presentation()
#     data = get_gpt_data(name1)
#     csv_data = StringIO(data)
#     # 使用read_csv()函数读取CSV字符串
#     df = pd.read_csv(csv_data)
#     theme = get_random_theme()
#
#     make_cover(prs, theme, df["title"][0])
#
#     match_indexs1 = get_titles_by_level(df["index"], 1)
#     print(match_indexs1)
#
#     match_indexs2 = get_titles_by_level(df["index"], 2)
#     print(match_indexs2)
#
#     match_indexs3 = get_titles_by_level(df["index"], 3)
#     print(match_indexs3)
#
#     make_catalogue(prs, theme, df["index"], df["title"], match_indexs2)
#
#     # make_page(df["index"],df["title"],df["content"],1)
#     # 获取所有一级标题
#     level1 = get_titles_by_level(df["index"], 1)
#     level_1 = level1[1:]
#     # 获取所有的二级标题
#     level2 = get_titles_by_level(df["index"], 2)
#     j = 0
#     for i in range(len(level2)):
#         # 简单的小算法
#         if j < len(level_1) and level_1[j] < level2[i]:
#             make_cover(prs, theme, df["title"][level_1[j]])
#             j = j + 1
#         if i % 2 == 1:
#             make_page_left(prs, theme, df["index"], df["title"], df["content"], df["keyword"], level2[i])
#         else:
#             make_page_right(prs, theme, df["index"], df["title"], df["content"], df["keyword"], level2[i])
#
#     stream = BytesIO()
#     prs.save(stream)
#     stream.seek(0)  # Reset the stream position to the beginning
#
#     return stream
#
#
#
# # test 测试
# if __name__ == '__main__':
#     prs = Presentation()
#
#     # 调试模式
#     print("调试模式： 1.节流模式（调用旧数据） \n"
#           "2.仿真模式（请求openai-api）")
#     mode = input("请输入您的模式：")
#     df = pd.read_csv("pptx_static/1.csv")
#     if mode == "1":
#         df = pd.read_csv("pptx_static/1.csv")
#     elif mode == "2":
#         name = input("请输入您的主题：")
#         data = get_gpt_data(name)
#         print(data)
#         # 通过StringIO对象读取CSV字符串
#         csv_data = StringIO(data)
#
#         # 使用read_csv()函数读取CSV字符串
#         df = pd.read_csv(csv_data)
#
#     theme = get_random_theme()
#
#     make_cover(prs, theme, df["title"][0])
#
#     match_indexs1 = get_titles_by_level(df["index"], 1)
#     print(match_indexs1)
#
#     match_indexs2 = get_titles_by_level(df["index"], 2)
#     print(match_indexs2)
#
#     match_indexs3 = get_titles_by_level(df["index"], 3)
#     print(match_indexs3)
#
#     make_catalogue(prs,theme, df["index"], df["title"], match_indexs2)
#
#     # make_page(df["index"],df["title"],df["content"],1)
#     # 获取所有一级标题
#     level1 = get_titles_by_level(df["index"], 1)
#     level_1 = level1[1:]
#     # 获取所有的二级标题
#     level2 = get_titles_by_level(df["index"], 2)
#     j = 0
#     for i in range(len(level2)):
#         # 简单的小算法
#         if j < len(level_1) and level_1[j] < level2[i]:
#             make_cover(prs, theme, df["title"][level_1[j]])
#             j = j + 1
#         if i % 2 == 1:
#             make_page_left(prs, theme, df["index"], df["title"], df["content"], df["keyword"], level2[i])
#         else:
#             make_page_right(prs, theme, df["index"], df["title"], df["content"], df["keyword"], level2[i])
#
#     now = datetime.datetime.now().timestamp()
#     path = './myppt/test' + str(now) + '.pptx_static'
#     if not os.path.exists('./myppt'):
#         os.makedirs('./myppt')
#     prs.save(path)
