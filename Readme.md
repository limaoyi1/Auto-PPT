# Auto_PPT 自动生成你的PPT

## English Guide
> please visit [English Guide](./Readme.en.md)

## 项目介绍

> 通过 gpt-3.5-turbo 和 pptx 生成 指定主题的PPTX文件

## 项目优势

> 1. 用户只需要输入标题就能够产生一篇新的PPTX.
> 2. 使用gpt-3.5-turbo-16k 接口,让接口稳定生成PPT大纲
> 3. 创造性的使用csv格式生成ppt文本,让pptx更加容易制作和稳定生成
> 4. 使用unsplash来获取插图
> 5. 可以本地化部署,只需要你添加你的openAI的api秘钥 和 unsplash api 秘钥信息

## 部署指南

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

> 6. 访问 http://127.0.0.1:5000

## 下一个版本
> 1. 部署线上服务
> 2. 优化生成内容 ,提供更准确的生成服务.
> 3. 优化生成格式 ,可以选择多种风格的样式.
> 4. 添加一个更优美的web-ui
> 5. 优化生成速度,gptApi的速度实在是太慢了

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=limaoyi1/Auto_PPT&type=Timeline)](https://star-history.com/#limaoyi1/Auto_PPT&Timeline)
