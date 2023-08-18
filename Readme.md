# <p align="center">Auto-PPT</p>

#### <p align="center"><i>GPT赋能，PPT创作革命</i></p>

<p align="center">
<br> 中文 | <a href="README_en.md">English</a>
</p>

<p align="center">
<a href="https://github.com/limaoyi1/Auto_PPT/stargazers" target="blank">
<img src="https://img.shields.io/github/stars/limaoyi1/Auto_PPT?style=for-the-badge" alt="Auto_PPT stars"/>
</a>
<a href="https://github.com/limaoyi1/Auto_PPT/fork" target="blank">
<img src="https://img.shields.io/github/forks/limaoyi1/Auto_PPT?style=for-the-badge" alt="Auto_PPT forks"/>
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

## 🎞️ 项目介绍

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;制作演示文档常常是许多人繁重的日常任务，琐碎的文案、特效和格式使得这项工作可能每天都成为困扰。然而，随着AI浪潮的席卷，这一现状正在悄然发生着改变，而我恰巧踏上了AIGC应用开发的道路。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在这股AI浪潮中，我开始思考如何创造能够减轻人们负担的解决方案。Auto-PPT便是我首个成熟构想的产物，“登高必自卑，观远必自眇”,通过几个月的尝试和不断的优化，如今它已经越发成熟。

## 💥 重要更新

> 2023/8/18 | v3.0 几乎完成重构项目
> - 重构后端服务,去除对redis的使用,改为sqlite3,去除对python-pptx的依赖
> - 重构前端服务,支持前端编辑Markdown,浏览Markdown,操作PPT
> - 制作在线编辑markdwon2ppt开源组件
> - 支持GPT3.5 ,GPT4 ,百度文心一言
> - 优化大纲和全文的生成效果和质量,优化了langchain的使用
> - 完全支持英语和中文

## ⭐ 感谢支持

> 通过给项目点亮星星，您展示了对我们的认可，并帮助我们在社区中获得更多关注。\
> 这激励我们不断改进和开发新功能，以提升您使用 Auto_PPT 的体验。

> 鸣谢 [Miraitowa-wsy](https://github.com/Miraitowa-wsy) 老板的赞助.

## 🤝 交流

### 微信群
<details>
  <summary>微信群 入群二维码 有效期到2月25日</summary>

  ![微信 WeChat](./static/ql_0825.jpg)
</details>

### 作者微信
<details>
  <summary>作者微信二维码</summary>

  ![微信 WeChat](./static/lmy_wx.jpg)
</details>

### 请我喝咖啡?
<details>
  <summary>作者微信赞赏码</summary>

  ![微信 WeChat](./static/lmy_jz.jpg)
</details>

## 🛸 使用方式

### 在线使用

> 新版 试用网址 🔗 ： [试用网址](http://www.limaoyi.top:4399/#) 只需2~3分钟，即可拥有一份专业设计的PPT。

### 本地部署

#### windows打包软件
> 暂时还没有打包

#### windows
##### 1. 打开cmd或者其他终端,把项目到本地
```bash
git clone https://github.com/limaoyi1/Auto-PPT.git
```
##### 2. 签出main分支
```bash
git checkout main 
```
##### 3. 创建虚拟环境并且激活
```bash
python -m venv myenv
cd .\myenv\Scripts
activate
cd ../../
```
##### 在/auto_ppt/config.ini添加你的秘钥
[config.ini](./auto_ppt/config.ini)

##### 4. Auto-PPT, 启动!
```bash
python application.py
```
##### 访问本地网页
[localhost:5000](http://localhost:5000/)

#### linux
> 同理,不过我推荐使用nginx单独转发静态页面

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=limaoyi1/Auto_PPT&type=Timeline)](https://star-history.com/#limaoyi1/Auto_PPT&Timeline)


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

> 2023/7/15 | v1.5 | 继续优化python转pptx | 已经完成 ✔
>

| 蓝图             | 存在问题           | 完成情况           |
|----------------|----------------|----------------|
| 兼容更多md格式       | md的格式工作量很大     | 前端支持md展示和PPT转换 |
| 选用一种前端语言重构前端代码 | 作为后端工程师对前端的不熟悉 | 已经完成 ✔         |
| 优化主题的效果        | 没有美感的ppt模板参考   | 推迟到下一个版本       |
| 优化部署           | fork后难以快速使用    | 已经完成 ✔         |

> 2023/8/18 | v3.0 几乎完成重构项目 | 已经完成 ✔
>

|           蓝图           |                  优化内容                   | 完成情况 |
|:----------------------:|:---------------------------------------:|:----:|
|         重构后端服务         | 去除对redis的使用，改为sqlite3，去除对python-pptx的依赖 | 完成 ✔ |
|         重构前端服务         |     支持前端编辑Markdown，浏览Markdown，操作PPT     | 完成 ✔ |
| 制作在线编辑markdwon2ppt开源组件 |                                         | 完成 ✔ |
|  支持GPT3.5，GPT4，百度文心一言  |                                         | 完成 ✔ |
|    优化大纲和全文的生成效果和质量     |             优化了langchain的使用             | 完成 ✔ |
|       完全支持英语和中文        |                                         | 完成 ✔ |