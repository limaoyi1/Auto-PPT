# -*- coding: utf-8 -*-
# @Time    : 2023/8/17 10:10
# @Author  : limaoyi
# @File    : gen_ppt_md.py
# @Software: PyCharm
# @GitHub  : https://github.com/limaoyi1
import logging

from flask import Flask, render_template, send_from_directory, request, Response
from flask_cors import CORS

from generation.gen_other import OptimizeMd
from generation.gen_ppt_md import GenMd

app = Flask(__name__)
# 设置日志级别
app.logger.setLevel(logging.DEBUG)

# 创建日志处理器
handler = logging.FileHandler('app.log', encoding='utf-8')
handler.setLevel(logging.DEBUG)

# 创建日志格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# 添加日志处理器到应用程序记录器
app.logger.addHandler(handler)
# from flask_cors import CORS

app = Flask(__name__)

# 允许跨域
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/static/js/<filename>')
def serve_js(filename):
    return send_from_directory('./templates/static/js', filename)


@app.route('/static/css/<filename>')
def serve_css(filename):
    return send_from_directory('./templates/static/css', filename)


@app.route('/static/media/<filename>')
def serve_media(filename):
    return send_from_directory('./templates/static/media', filename)


@app.route('/<filename>')
def serve_json(filename):
    return send_from_directory('./templates/', filename)


@app.route('/generate_markdown', methods=['POST'])
def gen_markdown():
    if request.method == "POST":
        profession = request.json["profession"]
        topic = request.json["topic"]
        model_name = request.json["model_name"]
        language = request.json["language"]
        ip_address = request.remote_addr
        app.logger.info(f'ip地址为 {ip_address}\t 请求生成PPT文本')
        gen = GenMd(profession, topic, model_name, language)
        md = gen.run()
        return Response(md, mimetype='application/octet-stream')
    elif request.method != "POST":
        return Response("不支持POST请求外的其他请求", mimetype='application/octet-stream')


@app.route('/smart_rewrite', methods=['POST'])
def smart_rewrite():
    if request.method == "POST":
        markdown = request.json["markdown"]
        model_name = request.json["model_name"]
        language = request.json["language"]
        ip_address = request.remote_addr
        app.logger.info(f'ip地址为 {ip_address}\t 请求智能改写')
        gen = OptimizeMd(model_name, language)
        rewrite = gen.smart_rewrite(markdown)
        return Response(rewrite, mimetype='application/octet-stream')
    elif request.method != "POST":
        return Response("不支持POST请求外的其他请求", mimetype='application/octet-stream')


@app.route('/generate_verbatim', methods=['POST'])
def generate_verbatim():
    if request.method == "POST":
        markdown = request.json["markdown"]
        model_name = request.json["model_name"]
        language = request.json["language"]
        ip_address = request.remote_addr
        app.logger.info(f'ip地址为 {ip_address}\t 请求生成逐字稿')
        gen = OptimizeMd(model_name, language)
        rewrite = gen.generate_verbatim(markdown)
        return Response(rewrite, mimetype='application/octet-stream')
    elif request.method != "POST":
        return Response("不支持POST请求外的其他请求", mimetype='application/octet-stream')


@app.route('/smart_form', methods=['POST'])
def smart_form():
    if request.method == "POST":
        markdown = request.json["markdown"]
        model_name = request.json["model_name"]
        language = request.json["language"]
        ip_address = request.remote_addr
        app.logger.info(f'ip地址为 {ip_address}\t 请求智能改写')
        gen = OptimizeMd(model_name, language)
        rewrite = gen.smart_form(markdown)
        return Response(rewrite, mimetype='application/octet-stream')
    elif request.method != "POST":
        return Response("不支持POST请求外的其他请求", mimetype='application/octet-stream')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
