from flask import Flask, request, make_response, render_template

from saveppt import make_ppt

from flask_cors import CORS

app = Flask(__name__)
# 允许跨域
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ppt')
def stream():
    title = request.args.get('title')  # 获取title参数的值

    ppt = make_ppt(title)

    response = make_response(ppt)
    response.headers['Content-Disposition'] = 'attachment; filename=file.pptx'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)