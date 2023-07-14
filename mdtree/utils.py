import os
import random
bg_base_path = "./pptx_static/static/bg"


def get_random_theme():
    root_path = bg_base_path
    # 获取根路径下的所有文件夹
    folders = [folder for folder in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, folder))]

    # 随机选择一个文件夹
    random_folder = random.choice(folders)

    # 返回完整的文件夹路径
    random_folder_path = os.path.join(root_path, random_folder)
    return random_folder_path


def read_md_file(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        content = file.read()
    return content


def get_random_file(path):
    folder_path = path

    # 获取文件夹内所有文件
    files = os.listdir(folder_path)

    # 从文件列表中随机选择一个文件
    random_file = random.choice(files)

    # 返回完整的文件路径
    random_file_path = os.path.join(folder_path, random_file)
    return random_file_path