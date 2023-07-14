import datetime
import uuid

from flask import Flask, request, make_response, render_template, Response

from ..generation.gen_ppt_outline import GenBody, GenTitle, GenOutline
from ..mdtree.tree2ppt import Tree2PPT
import logging



app = Flask(__name__)
# 设置日志级别
app.logger.setLevel(logging.INFO)

# 创建日志处理器
handler = logging.FileHandler('app.log', encoding='utf-8')
handler.setLevel(logging.INFO)

# 创建日志格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# 添加日志处理器到应用程序记录器
app.logger.addHandler(handler)
# from flask_cors import CORS

app = Flask(__name__)


# 允许跨域
# CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/auto-ppt/gen-uuid', methods=['GET'])
def get_uuid():
    random_uuid = str(uuid.uuid4())
    # todo 将ip地址和uuid 在redis缓存 对话历史记录
    return random_uuid


@app.route('/auto-ppt/gen-title', methods=['POST'])
def gen_title():
    title = request.json["title"]
    uuid = request.json["uuid"]
    ip_address = request.remote_addr
    app.logger.info(f'ip地址为 {ip_address}\t uuid 为 {uuid}\t生成了标题')
    gen_title = GenTitle(uuid)
    stream = gen_title.predict_title(title)
    return Response(stream, mimetype='application/octet-stream')


@app.route('/auto-ppt/gen-outline', methods=['POST'])
def gen_outline():
    num = request.json["num"]
    uuid = request.json["uuid"]
    ip_address = request.remote_addr
    app.logger.info(f'ip地址为 {ip_address}\t uuid 为 {uuid}\t生成了大纲')
    gen_outline1 = GenOutline(uuid)
    stream = gen_outline1.predict_outline(num)
    return Response(stream, mimetype='application/octet-stream')


@app.route('/auto-ppt/gen-body', methods=['POST'])
def gen_body():
    uuid = request.json["uuid"]
    ip_address = request.remote_addr
    app.logger.info(f'ip地址为 {ip_address}\t uuid 为 {uuid}\t生成了全文')
    gen_body1 = GenBody(uuid)
    stream = gen_body1.predict_body("")
    return Response(stream, mimetype='application/octet-stream')


@app.route('/auto-ppt/gen-ppt', methods=['POST'])
def gen_ppt():
    markdown_data = request.data
    if not markdown_data:
        return 'No data provided', 400
    markdown_str = request.data.decode('utf-8').replace('\r', '\n')
    print(markdown_str)
    ip_address = request.remote_addr
    app.logger.info(f'ip地址为 {ip_address}\t uuid md转换生成了ppt')
    ppt = Tree2PPT(markdown_str)
    stream = ppt.save_stream()
    response = make_response(stream)
    now = datetime.datetime.now().timestamp()
    response.headers['Content-Disposition'] = 'attachment; filename=' + str(now) + '.pptx'
    return response


# old outdated
@app.route('/ppt', methods=['GET'])
def stream():
    title1 = request.args.get('title')  # 获取title参数的值

    session_id = str(uuid.uuid4())

    title = GenTitle(session_id)
    title.predict_title(title1)

    outline = GenOutline(session_id)
    outline.predict_outline("1")

    body = GenBody(session_id)
    md = body.predict_body("")

    ppt = Tree2PPT(md)
    stream = ppt.save_stream()
    response = make_response(stream)
    response.headers['Content-Disposition'] = 'attachment; filename=file.pptx_static'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
