# -*- coding: utf-8 -*-
# @Time    : 2023/8/17 10:10
# @Author  : limaoyi
# @File    : gen_ppt_md.py
# @Software: PyCharm
# @GitHub  : https://github.com/limaoyi1
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# 将父文件夹路径添加到PYTHONPATH
sys.path.append(parent_dir)