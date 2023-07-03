# Auto_PPT 自动生成你的PPT

## English Guide

> please visit [English Guide](./Readme.en.md)

## 项目介绍

> 通过 gpt-3.5-turbo 和 pptx 生成 指定主题的PPTX文件

## 感谢支持

> 为项目点亮星星吧

## 免费试用

> 生成一个ppt需要3~5分钟 这取决于openai 接口的速度 \
> 这是是一个简单的线上试用版本： [试用网址](http://www.limaoyi.top:5000/) \
> 不提供随机图片服务(本就贫穷的服务器流量雪上加霜),程序会在几张随机配图中生成。

## 项目优势

> 1. 用户只需要输入标题就能够产生一篇新的PPTX.
> 2. 使用gpt-3.5-turbo-16k 接口,让接口稳定生成PPT大纲
> 3. 创造性的使用csv格式生成ppt文本,让pptx更加容易制作和稳定生成
> 4. 使用unsplash来获取插图
> 5. 可以本地化部署,只需要你添加你的openAI的api秘钥 和 unsplash api 秘钥信息

## 部署指南

> 项目运行需要python环境 ，推荐python3以上，作者使用的是python3.9

> 1. 创建虚拟环境

```bash
   python -m venv venv
```

> 2. 激活虚拟环境

```bash
   . venv/bin/activate
```

> 3. 安装要求的python组件

```bash
pip install -r requirements.txt
```

> 4. 在 config.ini 添加你的api key

> 5. 运行项目

```bash
python application.py
```

> 或者 (生产模式) 需要在 类linux 环境运行以下命令

```bash
gunicorn -b 0.0.0.0:5000 --log-level=debug --threads 4 wsgi:application > gunicorn.log 2>&1 &
```

> 6. 访问 http://127.0.0.1:5000

## 下一个版本
> 需要优化的内容 2023/7/3
> 
| 蓝图     | 完成情况       | 存在问题          |
|--------|------------|---------------|
| 部署线上服务 | 已完成        | ui过于简陋        |
| 优化生成格式 | 已经优化段落间距   | 格式过于单一        |
| 优化生成速度 | 已经优化服务启动方式 | openaiapi接口太慢 |

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=limaoyi1/Auto_PPT&type=Timeline)](https://star-history.com/#limaoyi1/Auto_PPT&Timeline)

## Blog 链接

作者博客:[http://www.limaoyi.top/](http://www.limaoyi.top/)
