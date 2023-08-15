import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# 将父文件夹路径添加到PYTHONPATH
sys.path.append(parent_dir)