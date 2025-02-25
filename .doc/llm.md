# LLM模块文档

## 概述

LLM模块为应用程序提供核心AI能力，实现了各种语言模型集成、检索增强生成(RAG)、嵌入和智能体功能。该模块作为智能层，为应用程序的知识检索、问答和写作辅助功能提供支持。

## 核心组件

### 模型管理
- `ModelCore.py` - 处理各种LLM提供商的模型加载和初始化
  - 支持OpenAI模型(GPT-4, GPT-4o, GPT-4o-mini)
  - 支持智谱模型(GLM-4)
  - 实现缓存以提高模型加载效率
  - 管理API调用的代理配置

### 嵌入和重排序
- `EmbeddingCore.py` - 实现向量嵌入功能
  - `BgeM3Embeddings` - BGE-M3嵌入模型实现
  - `BgeReranker` - 重排序实现，用于提高检索质量
  - 支持本地模型加载和GPU加速

### 检索系统
- `RetrieverCore.py` - 实现各种检索策略
  - `ScoreRetriever` - 具有评分和重排序功能的检索器
  - `ReferenceRetriever` - 跟踪文档之间引用链接的检索器
  - `ExprRetriever` - 支持表达式过滤的检索器
  - `MultiVectorSelfQueryRetriever` - 带元数据过滤的自查询检索器

### RAG实现
- `RagCore.py` - 核心RAG实现
  - 支持双语(中文/英文)问答
  - 实现文档格式化和引用跟踪
  - 提供与Milvus的向量存储集成
  - 在需要时处理语言之间的翻译

### 聊天和对话
- `ChatCore.py` - 对话管理
  - `chat_with_history` - 带历史跟踪的基本聊天功能
  - `write_paper` - 专门用于学术写作辅助的功能
  - `conclude_chat` - 总结聊天对话

### 智能体和工具集成
- `AgentCore.py` - 简单智能体实现
  - 语言之间的翻译功能
- `GraphCore.py` - LangGraph集成，用于更复杂的智能体工作流
  - 实现基于图的智能体，用于与数据库集成的写作
- `ToolCore.py` - 智能体工具实现
  - `VecstoreSearchTool` - 用于搜索向量数据库的工具
  - `WebSearchTool` - 用于网络搜索集成的工具

### 提示模板
- `Template.py` - 包含各种任务的提示模板
  - 问题生成模板
  - 翻译模板
  - RAG系统和用户提示
  - 示例问答模板

## 主要特性

1. **双语支持**
   - 无缝处理英文和中文内容
   - 在需要时自动翻译
   - 特定语言的提示模板

2. **高级检索**
   - 多查询检索以提高召回率
   - 重排序以提高精确度
   - 自查询功能，支持元数据过滤
   - 基于表达式的过滤，用于精确搜索

3. **学术写作重点**
   - 专门针对学术写作的提示
   - 引用跟踪和格式化
   - 与知识库集成

4. **工具集成**
   - 向量存储搜索工具
   - 网络搜索功能
   - 文档处理工具

5. **模型灵活性**
   - 支持多个LLM提供商
   - 可配置的模型参数
   - API访问的代理支持

6. **性能优化**
   - 缓存以提高模型加载效率
   - 嵌入模型的GPU加速
   - 批处理以提高效率

## 技术实现细节

### 嵌入实现
`BgeM3Embeddings`类使用BGE-M3模型实现嵌入功能：
- 支持CPU和GPU推理
- 实现FP16精度以加速GPU推理
- 提供池化方法(CLS和平均池化)
- 处理批处理以提高效率

### 重排序实现
`BgeReranker`类提供文档重排序：
- 对查询相关的文档进行评分
- 过滤低分文档
- 支持批处理以提高效率

### 检索策略
实现了多种检索策略：
- 带多查询扩展的基本检索
- 带元数据过滤的自查询检索
- 基于表达式的检索，用于精确搜索
- 基于引用的检索，用于跟踪文档连接

### RAG流程
RAG实现遵循结构化流程：
1. 查询处理(包括需要时的翻译)
2. 从向量存储中检索文档
3. 带元数据的文档格式化
4. 基于LLM的答案生成，带引用
5. 带引用的响应格式化

### 智能体实现
智能体实现使用LangGraph进行结构化工作流：
1. 为学术写作设置系统消息
2. 集成知识检索工具
3. 基于工具调用的条件路由
4. 使用检索信息生成响应

## 集成点

- **向量数据库**：与Milvus集成，用于向量存储和检索
- **文档存储**：连接SQLite，用于文档元数据和内容
- **网络搜索**：集成搜索API(Serper, DuckDuckGo)，用于网络检索
- **UI**：提供兼容Streamlit的函数，带进度指示器

## 使用示例

### 基本RAG查询
```python
result = get_answer(
    collection_name="my_collection",
    question="什么是transformer架构？",
    llm_name="gpt4o"
)
```

### 学术写作助手
```python
result = write_paper(chat_history)
```

### 带历史的聊天
```python
result = chat_with_history(chat_history, "告诉我更多关于注意力机制的信息")
```

### 翻译
```python
translated = translate_sentence(question, TRANSLATE_TO_EN)
```

## 模块关系

LLM模块是应用程序的核心智能层，与其他模块有以下关系：

1. **与存储模块的关系**：
   - 通过`SqliteStore`获取文档内容和元数据
   - 通过`MilvusConnection`访问向量数据

2. **与UI组件的关系**：
   - 为Streamlit页面提供缓存函数
   - 提供进度指示器以改善用户体验

3. **与配置系统的关系**：
   - 从`Config`获取API密钥和模型设置
   - 通过`StatusBus`获取运行时配置

## 技术栈

- **语言模型**：OpenAI GPT-4/GPT-4o/GPT-4o-mini, 智谱GLM-4
- **嵌入模型**：BGE-M3, BGE-Reranker-v2-m3
- **框架**：LangChain, LangGraph
- **向量数据库**：Milvus
- **工具集成**：Serper API, DuckDuckGo Search
