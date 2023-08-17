# -*- coding: utf-8 -*-
# @Time    : 2023/8/17 14:56
# @Author  : limaoyi
# @File    : test.py
# @Software: PyCharm
# @GitHub  : https://github.com/limaoyi1/GPT-prompt
from mdtree.parser import Parser

md ="""# 开源之潮：项目管理的新光芒

## 介绍开源项目管理的背景和重要性
### 开源软件的蓬勃发展
### 开源项目管理的优势与挑战

## 开源项目管理的关键要素
### 项目目标与愿景的确立
### 社区参与与协作
### 代码版本控制与版本管理
### 缺陷跟踪与解决
### 文档编写与维护
### 社区治理与决策机制

## 开源项目管理的最佳实践
### 设定明确的项目愿景和目标
### 建立积极的社区参与氛围
### 使用适当的工具和平台
### 采用有效的代码贡献流程
### 着重关注代码质量和测试
### 掌握高效的沟通与协作技巧

## 开源项目管理的挑战与解决方案
### 社区治理与决策的平衡
### 代码维护与贡献者参与的挑战
### 知识传承与文档管理的困扰
### 社区成员的多样性与协作的挑战
### 风险管理与项目可持续性的考量

## 结论
### 开源项目管理的重要性与优势
### 推动开源项目管理的发展和应用
### 开源项目管理的未来展望1. 开源软件的蓬勃发展"""

parser = Parser()
parser.parse(md)
out = parser.out
print("测试熬")
# 获取第一级
main = out.main
if main.level == 1:
    # 获取第二级
    childrens = main.children
    for child in childrens:
        print(child.full_source)
    pass

def get_first_line(input_string):
    lines = input_string.split('\n')
    if lines:
        return lines[0].strip()
    else:
        return ""

input_text = """这是第一行
这是第二行
这是第三行
"""

first_line = get_first_line(input_text)
print(first_line)