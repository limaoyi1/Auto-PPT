import datetime
import logging
import uuid

from flask import Flask, request, make_response, render_template, Response, send_from_directory
from flask_cors import CORS

from generation.gen_ppt_outline import GenBody, GenTitle, GenOutline
from mdtree.tree2ppt import Tree2PPT

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


@app.route('/auto-ppt/gen-uuid', methods=['GET'])
def get_uuid():
    random_uuid = str(uuid.uuid4())
    # todo 将ip地址和uuid 在redis缓存 对话历史记录
    return random_uuid


@app.route('/generate_title', methods=("GET", "POST"))
def stream1():
    if request.method == "POST":
        title = request.json["title"]
        uuid = request.json["uuid"]
        ip_address = request.remote_addr
        app.logger.info(f'ip地址为 {ip_address}\t uuid 为 {uuid}\t生成了标题')
        role = request.json["role"]
        form = request.json["form"]
        topic_num = request.json["topic_num"]
        gen_title_v2 = GenTitle(uuid)
        return Response(gen_title_v2.predict_title_v2(form, role, title, topic_num),
                        mimetype='application/octet-stream')


@app.route('/generate_outline', methods=['POST'])
def stream2():
    if request.method == "POST":
        uuid = request.json["uuid"]
        title = request.json["title"]
        ip_address = request.remote_addr
        app.logger.info(f'ip地址为 {ip_address}\t uuid 为 {uuid}\t生成了大纲')
        requirement = request.json["requirement"]
        gen_outline_v2 = GenOutline(uuid)
        return Response(gen_outline_v2.predict_outline_v2(title, requirement), mimetype='application/octet-stream')


@app.route('/generate_body', methods=['POST'])
def stream3():
    if request.method == "POST":
        uuid = request.json["uuid"]
        outline = request.json["outline"]
        ip_address = request.remote_addr
        app.logger.info(f'ip地址为 {ip_address}\t uuid 为 {uuid}\t生成了全文')
        requirement = request.json["requirement"]
        gen_body1 = GenBody(uuid)
        # 以流的方式返回结果
        return Response(gen_body1.predict_body(outline, requirement), mimetype='application/octet-stream')


@app.route('/generate_ppt', methods=['POST'])
def gen_ppt():
    if request.method == "POST":
        markdown_data = request.json["paper"]
        if not markdown_data:
            return 'No data provided', 400
        markdown_str = markdown_data.replace('\r', '\n')
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
    app.run(host='0.0.0.0', port=5000, debug=True)
