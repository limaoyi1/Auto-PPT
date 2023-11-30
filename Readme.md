# <p align="center">Auto_PPT 自动生成你的PPT</p>

<p align="center"><i>你是否厌倦了花费无尽的时间来制作乏味的演示文稿？是否希望有一个魔法工具，能够在几秒钟内为你生成令人惊叹的PPT？别担心，我们为你带来了Auto_PPT！</i></p>

<p align="center">
<a href="https://github.com/limaoyi1/Auto_PPT/fork" target="blank">
<img src="https://img.shields.io/github/forks/limaoyi1/Auto_PPT?style=for-the-badge" alt="Auto_PPT forks"/>
</a>

<a href="https://github.com/limaoyi1/Auto_PPT/stargazers" target="blank">
<img src="https://img.shields.io/github/stars/limaoyi1/Auto_PPT?style=for-the-badge" alt="Auto_PPT stars"/>
</a>
<a href="https://github.com/limaoyi1/Auto_PPT/pulls" target="blank">
<img src="https://img.shields.io/github/issues-pr/limaoyi1/Auto_PPT?style=for-the-badge" alt="Auto_PPT pull-requests"/>
</a>
<a href='https://github.com/limaoyi1/Auto_PPT/blob/main/LICENSE'>
<img src='https://img.shields.io/github/license/limaoyi1/Auto_PPT?&label=Latest&style=for-the-badge' alt="Auto_PPT LICENSE">
</a>
<a href='https://github.com/limaoyi1/Auto_PPT/releases'>
<img src='https://img.shields.io/github/release/limaoyi1/Auto_PPT?&label=Latest&style=for-the-badge' alt="Auto_PPT releases">
</a>
</p>


[//]: # (https://github.com/ikatyang/emoji-cheat-sheet 表情仓库)

## 🔥 [English Guide](./Readme.en.md)

> please visit [English Guide](./Readme.en.md)

## 🎞️ 项目介绍 

> 使用 gpt-3.5-turbo 和 pptx 一站式生成指定主题的PPTX文件。 \
> ![img.png](pptx_static/static/img2.png)
> 以下是通过项目生成的原始示例：
> ![img.png](pptx_static/static/img.png)

## ⭐ 感谢支持

> 通过给项目点亮星星，您展示了对我们的认可，并帮助我们在社区中获得更多关注。\
> 这激励我们不断改进和开发新功能，以提升您使用 Auto_PPT 的体验。

> 鸣谢 [Miraitowa-wsy](https://github.com/Miraitowa-wsy) 老板的赞助.

## 🛸 免费试用

>  新版 试用网址 🔗 ： [试用网址](http://www.limaoyi.top:4399/#)

> 🧭 只需2~3分钟，即可拥有一份专业设计的PPT。生成时间取决于 OpenAI 接口的速度，确保高效和可靠的操作。

> 🔗 立即试用，让我们一同探索 Auto_PPT 的神奇之处！请注意，为了维护有限的服务器流量，我们暂不提供随机图片服务。

## 🧲 项目优势

> 🌟 不再费心思：只需输入标题，Auto_PPT将立即为你创造一份全新的PPTX，无需任何额外努力！

> 🎩 魔法背后的秘密：我们借助强大的gpt-3.5-turbo-16k接口，确保每次生成的PPT大纲都稳定而令人印象深刻。

> 💡 创造性使用md格式：我们独特地运用md格式多步链式地生成PPT文本，使PPTX制作变得更加容易和稳定。告别格式困扰，让你专注于内容的创作！

> 🔗 在v1.0使用langchain对程序进行优化和重构,感谢langchain可以让代码变得简单,轻松和美观!

> 🖼️ 风景图插图：我们与Unsplash合作，提供最精美的插图，让你的PPT瞬间焕发生机与美感。

> 🔒 安全本地部署：如果你担心数据安全问题，不用担心！Auto_PPT支持本地部署，只需添加你的OpenAI API密钥和Unsplash API密钥信息即可。

## 🎨 部署指南

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

> 5. 修改./readconfig/mycofig.py 的base 绝对路径 使其为config.ini的文件夹路径

> 6. 运行项目

> 运行
```bash
python application.py
```

> 或者 (生产模式) 需要在 类linux 环境运行以下命令

```bash
gunicorn -b 0.0.0.0:5000 --log-level=debug --threads 4 app:application > gunicorn.log 2>&1 &
```

> 7. 访问 http://127.0.0.1:5000

## 💡 下一个版本

> 2023/7/3 | v0.5.1 | 一个创意的诞生 | 已经完成 ✔️
>

| 蓝图     | 存在问题          | 完成情况       |
|--------|---------------|------------|
| 部署线上服务 | ui过于简陋        | 已完成        |
| 优化生成格式 | 格式过于单一        | 已经优化段落间距   |
| 优化生成速度 | openaiapi接口太慢 | 已经优化服务启动方式 |

> 2023/7/6 | v1.0 | 用langChain 重构代码 | 已经完成 ✔
>

| 蓝图              | 存在问题               | 完成情况     |
|-----------------|--------------------|----------|
| 优化生成内容          | 生成内容不够详细和准确        | 推迟到下一个版本 |
| 优化生成步骤          | 单一步骤难以一步完成一个优质的PPT | 7.14已完成  |
| 使用langChain优化项目 | 优化为链式调用            | 7.14已完成  |


> 2023/7/15 | v1.5 | 下一个版本需要完成的内容 | 开始 🧭
> 
| 蓝图             | 存在问题           | 完成情况   |
|----------------|----------------|--------|
| 兼容更多md格式       | md的格式工作量很大     | 刚开始    |
| 选用一种前端语言重构前端代码 | 作为后端工程师对前端的不熟悉 | 已经完成 ✔ |
| 优化主题的效果        | 没有美感的ppt模板参考   | 刚开始    |

## 🌟 Star History

<br>

[![Star History Chart](https://api.star-history.com/svg?repos=limaoyi1/Auto_PPT&type=Timeline)](https://star-history.com/#limaoyi1/Auto_PPT&Timeline)

</br>
