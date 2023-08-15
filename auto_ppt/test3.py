# -*- coding: utf-8 -*-
# @Time    : 2023/8/10 15:48
# @Author  : limaoyi
# @File    : test3.py
# @Software: PyCharm
from gpt_prompt.character.advertiser import AdvertiserPrompt

if __name__ == '__main__':
    build = AdvertiserPrompt().build(language="chs")
    print(build)