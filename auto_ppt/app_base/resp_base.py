# -*- coding: utf-8 -*-
# @Time    : 2023/8/22 17:36
# @Author  : limaoyi
# @File    : resp_base.py
# @Software: PyCharm
# @GitHub  : https://github.com/limaoyi1/GPT-prompt
import json

from flask import make_response, jsonify


def to_dict(obj):
    try:
        json.dumps(obj)
        return obj
    except TypeError:
        pass
    if hasattr(obj, 'to_dict'):
        try:
            json.dumps(obj.to_dict())
            return obj.to_dict()
        except TypeError:
            raise BaseException("类对象不支持json序列化。")


def response(data, message, code, result, *args):
    return make_response(jsonify({'data': to_dict(data),
                                  'message': None if message is None else message.format(*args),
                                  'result': result,
                                  'code': str(code)
                                  }),
                         code)


def response_success(data):
    return response(data, None, 200, "操作成功")


def response_error(message, code, *args):
    return response(None, message, code, "操作失败", *args)
