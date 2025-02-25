# 学术LLM知识库

## 安装

```bash
uv init
uv venv
source .venv/bin/activate # 手动激活虚拟环境，uv可以不手动激活
# 编辑pyproject.toml
uv sync
```

## 运行

- docker

```bash
cd docker/grobid && docker-compose -f docker-compose-cpu.yml up -d # 启动cpu版本
cd docker/milvus && docker-compose -f docker-compose-cpu.yml up -d # 启动cpu版本
cd docker/nebulargraph && docker-compose -f docker-compose-lite.yml up -d # 启动lite版本
```

```bash
uv run python InitDatabase.py --auto_create
```


```bash
# non uv
streamlit run App.py

# uv
uv run streamlit run App.py 
```

