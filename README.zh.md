[**English**](./README.md)

# [学术文件转换器](https://github.com/GetRD/academic-file-converter)

[![从PyPI下载](https://img.shields.io/pypi/v/academic.svg?style=for-the-badge)](https://pypi.python.org/pypi/academic)
[![Discord](https://img.shields.io/discord/722225264733716590?style=for-the-badge)](https://discord.com/channels/722225264733716590/742892432458252370/742895548159492138)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/gcushen?label=%E2%9D%A4%EF%B8%8F%20sponsor&style=for-the-badge)](https://github.com/sponsors/gcushen)
[![Twitter Follow](https://img.shields.io/twitter/follow/georgecushen?label=Follow%20on%20Twitter&style=for-the-badge)](https://twitter.com/GeorgeCushen)
[![GitHub followers](https://img.shields.io/github/followers/gcushen?label=Follow%20on%20GH&style=for-the-badge)](https://github.com/gcushen)


### 📚 将出版物和Jupyter笔记本轻松导入到您的Markdown格式的网站或书籍中

![](.github/media/demo.gif)

**特性**

* 将 **Jupyter笔记本**导入为博客文章或书籍章节
* 将出版物（如**书籍、会议论文集和期刊**）从您的参考文献管理器导入到您的Markdown格式的网站或书籍中
  * 只需从参考文献管理器（例如[Zotero](https://www.zotero.org)）导出BibTeX文件，并将此文件作为转换工具的输入
* **兼容所有静态网站生成器**，如Next、Astro、Gatsby、Hugo等
* **易于使用** - 100% Python，无需依赖Pandoc等复杂软件
* 使用[GitHub Action](https://github.com/HugoBlox/hugo-blox-builder/blob/main/starters/blog/.github/workflows/import-notebooks.yml) **自动化** 文件转换

**社区**

- 📚 [查看以下的**文档**](#安装)
- 💬 [在Discord上与**社区**实时聊天](https://discord.gg/z8wNYzb)
- 🐦 推特：[@GetResearchDev](https://twitter.com/GetResearchDev) [@GeorgeCushen](https://twitter.com/GeorgeCushen) [#MadeWithAcademic](https://twitter.com/search?q=%23MadeWithAcademic&src=typed_query)

## ❤️ 支持开放研究和开源软件

我们的使命是通过开发像这样的**开源**工具来促进**开放研究**。

为了帮助我们根据MIT许可证在可持续地进行这个开源软件的开发，我们请求所有使用它的个人和企业支持它的维护和发展，通过赞助和贡献来实现。

支持开放研究运动：

  - ⭐️ [在GitHub上给这个项目**加星标**](https://github.com/GetRD/academic-file-converter)
  - ❤️ [成为**GitHub赞助商**并**解锁特权**](https://github.com/sponsors/gcushen)
  - ☕️ [**捐赠一杯咖啡**](https://github.com/sponsors/gcushen?frequency=one-time)
  - 👩‍💻 [**贡献**](#contribute)

## 安装

打开您的**终端**或**命令提示符**应用程序并输入以下的安装命令之一。

### 使用Pipx

对于**最简单**的安装，使用[Pipx](https://pypa.github.io/pipx/)进行安装：

    pipx install academic

Pipx将会**自动在一个专用环境中为您安装所需的Python版本**。

### 使用Pip

使用Python的Pip工具进行安装，请确保您已安装[Python 3.11+](https://realpython.com/installing-python/)，然后运行：

    pip3 install -U academic

## 使用方式

打开您的命令行或终端应用程序，使用`cd`命令导航至包含您希望转换的文件的文件夹，例如：

    cd ~/Documents/my_website

### 导入出版物

从您的参考文献管理器中（例如Zotero）下载参考文献，使用Bibtex格式。

假设我们将我们的出版物下载到了网站文件夹内名为`my_publications.bib`的文件中，让我们将它们导入到 `content/publication/`文件夹中：

    academic import my_publications.bib content/publication/ --compact

可选参数：

* `--compact` 生成没有注释或空键的最小化markdown
* `--overwrite` 覆盖输出文件夹中的任何现有出版物
* `--normalize` 标准化标签，将其转换为小写并将第一个字母大写（例如 "sciEnCE" -> "Science"）
* `--featured` 将这些出版物标记为*特色出版物*（以便在您的网站的*特色出版物*部分显示）
* `--verbose` 或 `-v`显示详细消息
* `--help` 帮助

### 导入全文和封面图像

导入出版物后，我们建议您：
- 编辑每个出版物的Markdown正文，直接在页面上添加全文（如果出版物是开放访问的），或者添加每个出版物的补充笔记
- 将名为`featured`的图像添加到每个出版物的文件夹中，以在页面上可视化地代表您的出版物，并用于在社交媒体上分享
- 将出版物的PDF添加到每个出版物的文件夹中（对于开放访问的出版物），以便您的网站访问者可以下载您的出版物
  
[在Hugo Blox文档中学习更多知识](https://docs.hugoblox.com/reference/content-types/).

### 从Jupyter笔记本中导入博客文章

设想我们有一个笔记本在网站文件夹中的`notebooks`文件夹中，让我们将它们导入到`content/post/`文件夹中：

    academic import 'notebooks/*.ipynb' content/post/ --verbose

可选参数:

* `--overwrite` 覆盖输出文件夹中的任何现有博客文章
* `--verbose` 或 `-v` 显示详细消息
* `--help` 帮助

## 贡献

对贡献**开源**和**开放研究**感兴趣吗？

了解[Github上如何贡献代码](https://codeburst.io/a-step-by-step-guide-to-making-your-first-github-contribution-5302260a2940)。

查看[开放的问题](https://github.com/GetRD/academic-file-converter/issues)，并贡献一个[Pull Request](https://github.com/GetRD/academic-file-converter/pulls)。

对于本地开发，克隆此存储库并使用诗(Poetry)安装和运行转换器，使用以下命令：    git clone https://github.com/GetRD/academic-file-converter.git
    cd academic-file-converter
    poetry install
    poetry run academic import tests/data/article.bib output/publication/ --overwrite --compact
    poetry run academic import 'tests/data/**/*.ipynb' output/post/ --overwrite --verbose

在准备投稿时，请运行以下检查并确保所有检查都通过：

- Lint：`make lint`
- Format：`make format`
- Test：`make test`
- Type check：`make type`

### 帮助测试开发者版本

您可以通过安装GitHub上的最新`main`分支来帮助测试最新的开发版本：

    pip3 install -U git+https://github.com/GetRD/academic-file-converter.git

## 许可证

版权所有2018-至今 [George Cushen](https://georgecushen.com)。

根据[MIT许可证](https://github.com/GetRD/academic-file-converter/blob/main/LICENSE.md)授权。

![PyPI - 下载次数](https://img.shields.io/pypi/dm/academic?label=PyPi%20Downloads&style=for-the-badge)
[![许可证](https://img.shields.io/pypi/l/academic.svg?style=for-the-badge)](https://github.com/GetRD/academic-file-converter/blob/main/LICENSE.md)
