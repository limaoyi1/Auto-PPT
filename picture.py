import codecs
import configparser
import os
import random

import pyunsplash
from PIL import Image

config = configparser.ConfigParser()
# 指定编码为 UTF-8
config.read_file(codecs.open('config.ini', 'r', 'utf-8-sig'))
Real_File = config.get('Credentials', 'Real_File')
if Real_File == "Config.ini":
    UNSPLASH_API_KEYS = config.get('Credentials', 'UNSPLASH_API_KEYS').split(',')
    UNSPLASH_ENABLE = config.get('Credentials', 'UNSPLASH_ENABLE')
else:
    config.read_file(codecs.open(Real_File, 'r', 'utf-8-sig'))
    UNSPLASH_API_KEYS = config.get('Credentials', 'UNSPLASH_API_KEYS').split(',')
    UNSPLASH_ENABLE = config.get('Credentials', 'UNSPLASH_ENABLE')


# 免费api
# https://unsplash.com/documentation#get-the-users-profile
# 找到的比较好的包
# https://pyunsplash.readthedocs.io/en/latest/index.html
# 找到好用的素材网站
# https://www.ppt-themes.com/

def get_random_api_key():
    return random.choice(UNSPLASH_API_KEYS)


base_path = "./picture"

bg_base_path = "pptx_static/static/bg"

import requests


def check_same_name_file(directory, filename):
    file_list = os.listdir(directory)
    if filename in file_list:
        print("存在缓存")
        return True
    else:
        print("不存在缓存")
        return False


def download_image(url, save_path):
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"图片已下载并保存为: {save_path}")
    else:
        print("下载失败")


def search(keyword):
    if UNSPLASH_ENABLE == "false":
        #   ################### 图片限流 ###########################
        return get_random_file(base_path)
        #   #######################################################
    new_keyword = keyword.replace("&", " ")
    pu = pyunsplash.PyUnsplash(get_random_api_key())
    collections_page = pu.photos(type_='random', count=1, featured=True, query=new_keyword)
    for photo in collections_page.entries:
        print(photo.id, photo.link_download)
        save_path = base_path + "/" + keyword + ".jpg"
        download_image(photo.link_download, save_path)
        return save_path


def get_random_theme():
    root_path = bg_base_path
    # 获取根路径下的所有文件夹
    folders = [folder for folder in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, folder))]

    # 随机选择一个文件夹
    random_folder = random.choice(folders)

    # 返回完整的文件夹路径
    random_folder_path = os.path.join(root_path, random_folder)
    return random_folder_path


def get_random_file(path):
    folder_path = path

    # 获取文件夹内所有文件
    files = os.listdir(folder_path)

    # 从文件列表中随机选择一个文件
    random_file = random.choice(files)

    # 返回完整的文件路径
    random_file_path = os.path.join(folder_path, random_file)
    return random_file_path


def count_files_in_folder(folder_path):
    if not os.path.isdir(folder_path):
        raise ValueError("Invalid folder path.")

    count = 0
    for _, _, files in os.walk(folder_path):
        count += len(files)

    return count


def get_image_resolution(image_path):
    image = Image.open(image_path)
    width, height = image.size
    return width, height

