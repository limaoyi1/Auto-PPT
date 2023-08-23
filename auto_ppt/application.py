# -*- coding: utf-8 -*-
# @Time    : 2023/8/17 10:10
# @Author  : limaoyi
# @File    : gen_ppt_md.py
# @Software: PyCharm
# @GitHub  : https://github.com/limaoyi1
import logging

from flask import Flask, request, Response
from flask_cors import CORS
from flask_restx import Api, fields, Resource
from marshmallow import validate

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

app = Flask(__name__)
api = Api(app, version='3.0', title='Auto PPT API',
          description='Auto PPT TodoMVC API',
          )
# 允许跨域
CORS(app)

# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# @app.route('/static/js/<filename>')
# def serve_js(filename):
#     return send_from_directory('./templates/static/js', filename)
#
#
# @app.route('/static/css/<filename>')
# def serve_css(filename):
#     return send_from_directory('./templates/static/css', filename)
#
#
# @app.route('/static/media/<filename>')
# def serve_media(filename):
#     return send_from_directory('./templates/static/media', filename)
#
#
# @app.route('/<filename>')
# def serve_json(filename):
#     return send_from_directory('./templates/', filename)


generate_markdown_request = api.model('generate_markdown_request', {
    'profession': fields.String(required=True, validate=validate.Length(min=1), description='角色'),
    'topic': fields.String(required=True, validate=validate.Length(min=1), description='话题'),
    'model_name': fields.String(required=True, validate=validate.Length(min=1), description='模型名称'),
    'language': fields.String(required=True, validate=validate.Length(min=1), description='语言'),
})


@api.route('/generate_markdown', methods=['POST'])
class GenMarkdown(Resource):
    @api.expect(api.model('generate_markdown_request', generate_markdown_request), validate=True)
    def post(self):
        profession = request.json["profession"]
        topic = request.json["topic"]
        model_name = request.json["model_name"]
        language = request.json["language"]
        ip_address = request.remote_addr
        app.logger.info(f'ip地址为 {ip_address}\t 请求生成PPT文本')
        gen = GenMd(profession, topic, model_name, language)
        md = gen.run()
        return Response(md, mimetype='application/octet-stream')


smart_rewrite_request = api.model('smart_rewrite_request', {
    'markdown': fields.String(required=True, validate=validate.Length(min=1), description='需要修改的markdown内容'),
    'model_name': fields.String(required=True, validate=validate.Length(min=1), description='模型名称'),
    'language': fields.String(required=True, validate=validate.Length(min=1), description='语言'),
})


@api.route('/smart_rewrite', methods=['POST'])
class SmartRewrite(Resource):

    @api.expect(api.model('smart_rewrite_request', smart_rewrite_request), validate=True)
    def post(self):
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


generate_verbatim_request = api.model('generate_verbatim_request', {
    'markdown': fields.String(required=True, validate=validate.Length(min=1), description='全部的markdown内容'),
    'model_name': fields.String(required=True, validate=validate.Length(min=1), description='模型名称'),
    'language': fields.String(required=True, validate=validate.Length(min=1), description='语言'),
})


@api.route('/generate_verbatim', methods=['POST'])
class GenerateVerbatim(Resource):

    @api.expect(api.model('generate_verbatim_request', generate_verbatim_request), validate=True)
    def post(self):
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


smart_form_request = api.model('smart_form_request', {
    'markdown': fields.String(required=True, validate=validate.Length(min=1), description='需要改写的markdown内容'),
    'model_name': fields.String(required=True, validate=validate.Length(min=1), description='模型名称'),
    'language': fields.String(required=True, validate=validate.Length(min=1), description='语言'),
})


@api.route('/smart_form', methods=['POST'])
class SmartForm(Resource):

    @api.expect(api.model('smart_form_request', smart_form_request), validate=True)
    def post(self):
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
