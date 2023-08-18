import logging

from flask import Flask, render_template, send_from_directory, request, Response
from flask_cors import CORS

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
        title = request.json["title"]
        uuid = request.json["uuid"]
        ip_address = request.remote_addr
        app.logger.info(f'ip地址为 {ip_address}\t uuid 为 {uuid}\t生成了标题')
        role = request.json["role"]
        form = request.json["form"]
        topic_num = 1
        gen_title_v2 = GenTitle(uuid)
        gen_outline_v2 = GenOutline(uuid)
        gen_title_v2.predict_title_v2(form, role, title, 1)
        gen_outline_v2.predict_outline_v3("1", title_requirement="")
        gen_body1 = GenBody(uuid)
        gen_body1.predict_body_v3()
        return Response(gen_body1.predict_body_v3(),
                        mimetype='application/octet-stream')
    elif request.method != "POST":
        return Response("不支持POST请求外的其他请求",
                        mimetype='application/octet-stream')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
