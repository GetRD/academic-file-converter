[**English**](./README.md)

# [Bibtex 转 Markdown 转换器](https://github.com/wowchemy/bibtex-to-markdown)

[![从PyPI下载](https://img.shields.io/pypi/v/academic.svg?style=for-the-badge)](https://pypi.python.org/pypi/academic)
[![Discord](https://img.shields.io/discord/722225264733716590?style=for-the-badge)](https://discord.com/channels/722225264733716590/742892432458252370/742895548159492138)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/gcushen?label=%E2%9D%A4%EF%B8%8F%20赞助&style=for-the-badge)](https://github.com/sponsors/gcushen)
[![Twitter Follow](https://img.shields.io/twitter/follow/georgecushen?label=在%20Twitter%20上关注&style=for-the-badge)](https://twitter.com/GeorgeCushen)
[![GitHub followers](https://img.shields.io/github/followers/gcushen?label=在%20GitHub%20上关注&style=for-the-badge)](https://github.com/gcushen)


### 📚 轻松地将您的参考经理中的出版物导入到您的 Markdown 格式的网站或书籍中

![](.github/media/demo.gif)

**特征**

* 将 Bibtex 出版物（如**书籍，会议记录和期刊**）从您的参考管理器导入到您的 Markdown 格式的网站或书籍
  - 只需从您的参考管理器（如 [Zotero](https://www.zotero.org)）中导出一个 BibTeX 文件，并将其作为转换器工具的输入
* 兼容所有静态网站生成器，如 Next, Astro, Gatsby, Hugo 等。

**社区**

- 📚 [查看**文件**](https://wowchemy.com/docs/content/publications/#import-from-bibtex) 和下面的使用指南
- 💬 [与**社区**交谈](https://discord.gg/z8wNYzb)
- 🐦 Twitter: [@wowchemy](https://twitter.com/wowchemy) [@GeorgeCushen](https://twitter.com/GeorgeCushen) [#MadeWithAcademic](https://twitter.com/search?q=(%23MadeWithWowchemy%20OR%20%23MadeWithAcademic)&src=typed_query)

**❤️ 支持这个开源软件**

为了帮助我们在 MIT 许可下可持续地开发这个转换器工具和相关的 Wowchemy 开源软件，我们要求所有使用它的个人和企业通过赞助和贡献来帮助支持其持续的维护和开发。

支持这个开放科学运动：

  - ⭐️ [在 GitHub 上为这个项目打**星**](https://github.com/wowchemy/bibtex-to-markdown)
  - ❤️ [成为一名**GitHub 赞助者**并**解锁特权**](https://github.com/sponsors/gcushen)
  - ☕️ [**捐赠一杯咖啡**](https://github.com/sponsors/gcushen?frequency=one-time)
  - 👩‍💻 [**贡献**](#贡献)

## 安装

打开您的**终端**或**命令提示符**应用程序，并输入以下安装命令之一。

### 使用 Pipx

对于**最简单**的安装，可使用 [Pipx](https://pypa.github.io/pipx/) 安装： 

    pipx install academic

Pipx 将**自动在专用环境中为您安装所需的 Python 版本**。

### 使用 Pip

要使用 Python 的 Pip 工具进行安装，请确保已安装 [Python 3.11+](https://realpython.com/installing-python/)，然后运行：

    pip3 install -U academic

## 使用

请以 Bibtex 格式从您的参考管理器（如 Zotero）中下载引用。

使用 `cd` 命令导航到包含您的 Bibtex 文件的文件夹：

    cd <MY_BIBTEX_FOLDER>

### 导入出版物

假设我们将出版物下载到网站文件夹中名为 `my_publications.bib` 的文件中，让我们将它们导入到 `content/publication/` 文件夹中：

    academic import my_publications.bib content/publication/ --compact

可选参数：

* `--compact` 生成没有评论或空键的最小 markdown
* `--overwrite` 覆盖输出文件夹中的任何现有出版物
* `--normalize` 通过将它们转换为小写并大写第一个字母来规范标签（例如 "sciEnCE" -> "Science"）
* `--featured` 将这些出版物标记为*精选*（将在您的网站的*精选出版物*部分出现）
* `--verbose` 或 `-v` 显示详细消息
* `--help` 帮助

### 导入全文和封面图像

导入出版物后，我们建议您：
- 编辑每个出版物的 Markdown 正文以将全文直接添加到页面（如果出版物是开放获取的），或其他方式，为每个出版物添加补充笔记
- 将名为 `featured` 的图像添加到每个出版物的文件夹中，以在页面上直观地表示您的出版物并在社交媒体上分享
- 将出版物 PDF 添加到每个出版物文件夹（对于开放获取的出版物），以便您的网站访问者下载您的出版物

[在 Wowchemy 文档中了解更多](https://university.wowchemy.com)。

## 贡献

对贡献**开源**和**开放科学**感兴趣？

学习 [如何在 Github 上贡献代码](https://codeburst.io/a-step-by-step-guide-to-making-your-first-github-contribution-5302260a2940)。

查看 [开放问题](https://github.com/wowchemy/bibtex-to-markdown/issues) 和贡献 [拉取请求](https://github.com/wowchemy/bibtex-to-markdown/pulls)。 

要进行本地开发，请克隆此存储库并使用 Poetry 使用以下命令安装并运行转换器：

    git clone https://github.com/wowchemy/bibtex-to-markdown.git
    cd bibtex-to-markdown
    poetry install
    poetry run academic import tests/data/article.bib output/ --overwrite --compact

准备贡献时，运行以下检查并确保都已通过：

- Lint: `make lint`
- Format: `make format`
- Test: `make test`
- 类型检查: `make type`

### 帮助测试开发版本

您可以通过安装来自 GitHub 的最新 `main` 分支来帮助测试最新的开发版本：

    pip3 install -U git+https://github.com/wowchemy/bibtex-to-markdown.git

## 许可

Copyright 2018-present [George Cushen](https://georgecushen.com).根据[MIT许可证](https://github.com/wowchemy/bibtex-to-markdown/blob/main/LICENSE.md)许可。

![PyPI - Downloads](https://img.shields.io/pypi/dm/academic?label=PyPi%20Downloads&style=for-the-badge)
[![License](https://img.shields.io/pypi/l/academic.svg?style=for-the-badge)](https://github.com/wowchemy/bibtex-to-markdown/blob/main/LICENSE.md)
