# Project Structure Overview

## Core Components

### Main Application Files
- `App.py` - 主应用入口，设置Streamlit页面配置和基本UI布局，实现知识库问答功能
- `Config.py` - 配置管理类，处理配置文件的加载和访问，支持运行时配置更新
- `InitDatabase.py` - 数据库初始化脚本，支持指定collection初始化和自动创建

### Storage
- `storage/` - 存储相关实现
  - `SqliteStore.py` - SQLite存储实现，包括文档存储、引用存储和用户配置存储
  - `MilvusConnection.py` - Milvus向量数据库连接管理
  - `NebulaStore.py` - NebulaGraph图数据库存储实现

### Pages
- `pages/` - Streamlit页面组件
  - `WriteAssistant.py` - AI写作助手页面，支持文件上传和写作辅助
  - `FileUpload.py` - 文件上传和处理页面，支持PDF、PMC等多种来源
  - `CollectionManage.py` - 知识库管理页面，支持知识库创建、删除和权限管理

### Preprocessing
- `preprocess/` - 数据预处理模块
  - `ParsePDF.py` - PDF解析工具
  - `LoadCSV.py` - CSV数据加载工具
  - `DownloadFromPMC.py` - PMC文献下载工具

### Utils
- `utils/` - 工具类和辅助函数
  - `MarkdownPraser.py` - Markdown解析工具，支持文档分割和引用提取
  - `GrobidUtil.py` - Grobid工具集成，用于PDF文献结构化解析
  - `PMCUtil.py` - PMC文献处理工具，支持XML格式解析
  - `PubmedUtil.py` - PubMed API工具
  - `entities/` - 数据实体类定义
    - `Paper.py` - 论文相关数据结构
    - `UserProfile.py` - 用户配置相关数据结构
    - `TimeZones.py` - 时区配置

### LLM Integration
- `llm/` - 大语言模型集成
  - `RagCore.py` - RAG检索增强生成核心实现，支持中英双语
  - `ModelCore.py` - 模型加载和初始化
  - `EmbeddingCore.py` - 向量嵌入模型实现
  - `ChatCore.py` - 对话功能实现，支持对话总结
  - `ToolCore.py` - 工具函数集成，包括向量检索等功能
  - `RetrieverCore.py` - 检索器实现
  - `Template.py` - 提示词模板

### UI Components
- `uicomponent/` - UI组件
  - `StComponent.py` - Streamlit通用组件，包括侧边栏等
  - `StatusBus.py` - 状态管理组件，处理用户登录状态等

## Configuration
- `config.example.yml` - 配置文件模板，包含：
  - 数据目录配置
  - 用户登录系统配置
  - 代理设置(HTTP/SOCKS5)
  - 检索系统配置(Milvus)
  - LLM模型配置(OpenAI/Zhipu)
  - 外部工具配置(PubMed/Serper/Grobid)

## Project Features

1. **文献管理**
   - PDF文献解析和存储
   - Markdown格式转换
   - 引用关系管理
   - 多种来源支持(PDF、PMC、PubMed)
   - 引用树构建(仅PDF、PMC支持)

2. **知识库功能**
   - 向量数据库集成(Milvus)
   - 文献检索(支持精准查询和模糊匹配)
   - RAG增强问答(支持中英双语)
   - 知识库权限管理

3. **用户系统**
   - 用户认证和权限管理(ADMIN/USER)
   - 项目管理
   - 对话历史记录
   - 时区配置支持

4. **AI写作辅助**
   - 写作风格分析
   - 文献引用建议
   - 智能写作辅助
   - 支持Markdown格式

5. **系统管理**
   - 知识库管理
     - 知识库创建与删除
     - 权限管理
     - 索引参数配置(支持多种索引类型)
   - 用户管理
     - 用户创建与认证
     - 权限分级(ADMIN/USER)
     - 项目关联
   - 系统配置管理
     - 模型配置
     - 代理设置
     - 外部服务集成

6. **数据存储**
   - 向量数据库(Milvus)存储文献内容
   - SQLite存储
     - 用户信息
     - 项目配置
     - 聊天历史
     - 文献引用关系
   - 本地文件系统
     - PDF原文
     - Markdown转换文本
     - XML中间格式

## Technical Stack
- Python
- Streamlit (Web UI)
- SQLite (本地存储)
- Milvus (向量数据库)
- LangChain (LLM集成)
- GROBID (PDF解析) 
- BGE (Embedding Model)
  - bge-m3 (Embedding)
  - bge-reranker-v2-m3 (Reranker)
- OpenAI API
  - GPT-4
  - GPT-4-Turbo
- Zhipu API (GLM-4)
- PubMed API
- Serper API