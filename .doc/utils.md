# 工具类模块 (utils)

## 概述

utils模块包含了一系列辅助工具类和函数，用于支持系统的各种功能，包括文件处理、装饰器、Markdown解析、PDF处理、PMC和PubMed数据获取等。这些工具类为系统的核心功能提供了基础支持。

## 主要组件

### 装饰器 (Decorator.py)

提供了两个主要的装饰器函数：

- `timer`: 用于测量函数执行时间的装饰器，记录函数的执行耗时并输出日志
- `retry`: 为函数提供重试逻辑的装饰器，可配置最大重试次数和延迟时间

### 文件工具 (FileUtil.py)

提供了文件和文本处理的基础功能：

- `format_filename`: 格式化文件名，移除无效字符
- `split_words`: 分割文本中的单词，包括处理括号包围的单词
- `replace_multiple_spaces`: 替换文本中的多个连续空格为单个空格
- `is_en`: 检查文本是否只包含英文和数字

### Grobid工具 (GrobidUtil.py)

集成了Grobid服务，用于PDF文献的结构化解析：

- `GrobidConnector`: 连接Grobid服务的客户端类，提供PDF解析功能
  - `parse_file`: 将PDF文件转换为TEI XML格式
  - `parse_files`: 批量处理PDF文件
- `parse_xml`: 解析XML文件，提取论文相关信息
- 支持多种解析配置选项，如标题合并、引用合并等

### Markdown解析器 (MarkdownPraser.py)

处理Markdown格式的文档，支持文档分割和引用提取：

- `split_markdown`: 分割Markdown文档为多个部分
- `split_markdown_text`: 分割Markdown文本，提取元数据和引用信息
- `split_paper`: 将Paper对象转换为文档列表和引用信息
- `save_to_md`: 将Paper对象保存为Markdown格式文件
- `load_from_md`: 从Markdown文件加载内容，并分割为文档列表和引用信息

### PMC工具 (PMCUtil.py)

处理PMC(PubMed Central)文献的工具：

- `get_pmc_id`: 根据搜索术语获取PMC文章ID
- `download_paper_data`: 下载指定PMC文章的XML数据
- `parse_paper_data`: 从XML文本中解析论文数据
- 支持处理不同格式的引用和章节结构

### PubMed工具 (PubmedUtil.py)

与PubMed API交互的工具：

- `get_paper_info`: 根据PubMed ID获取论文信息
- `get_info_by_term`: 通过标题、DOI号等补全参考文献信息
- 支持多种搜索类型：标题、DOI、PMID

## 数据实体 (entities)

### Paper.py

定义了与论文相关的数据结构：

- `PaperType`: 论文类型枚举（纯Markdown、Grobid解析、PMC论文等）
- `PaperInfo`: 论文基本信息（作者、年份、类型、关键词等）
- `Section`: 论文章节信息（文本内容和层级）
- `Reference`: 引用信息
- `Paper`: 完整论文数据结构，包含基本信息、章节和引用

### TimeZones.py

包含一个完整的时区列表，用于系统中的时区配置。

### UserProfile.py

定义了用户相关的数据结构：

- `UserGroup`: 用户组枚举（访客、作者、文件管理员、管理员）
- `User`: 用户信息（用户名、密码、用户组等）
- `Project`: 项目信息（名称、所有者、最后聊天等）
- `ChatHistory`: 聊天历史记录信息

## 工作流程

1. 文献处理流程：
   - 使用GrobidUtil解析PDF文件获取结构化XML
   - 或使用PMCUtil从PMC下载XML格式论文
   - 使用MarkdownPraser将解析后的数据转换为系统内部使用的格式
   - 支持将处理后的数据保存为Markdown格式

2. 引用处理流程：
   - 从解析的文献中提取引用信息
   - 使用PubmedUtil补充引用的元数据
   - 构建引用关系图

3. 用户管理流程：
   - 使用UserProfile中的数据结构管理用户信息和权限
   - 支持项目关联和聊天历史记录

## 技术特点

1. 模块化设计，各工具类职责明确
2. 使用装饰器实现横切关注点（如重试逻辑、性能监控）
3. 支持多种文献来源和格式
4. 提供丰富的数据实体类，便于系统内部数据交换
5. 错误处理和日志记录机制完善
