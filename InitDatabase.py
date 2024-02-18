import argparse
import json
import os
import shutil

import yaml
from langchain.retrievers import ParentDocumentRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings, HuggingFaceEmbeddings
from langchain_community.vectorstores.milvus import Milvus
from loguru import logger
from tqdm import tqdm

from storage.SqliteStore import SqliteDocStore
from utils.MarkdownPraser import split_markdown_text
from utils.TimeUtil import timer

logger.add('log/init_database.log')


def init_retriever() -> ParentDocumentRetriever:
    logger.info('start building vector database...')
    milvus_cfg = config.milvus_config

    collection = milvus_cfg.get_collection().NAME

    if milvus_cfg.get_collection().LANGUAGE == 'zh':
        model = config.milvus_config.ZH_MODEL

        embedding = HuggingFaceEmbeddings(
            model_name=model,
            model_kwargs={'device': 'cuda'},
            encode_kwargs={'normalize_embeddings': True}
        )
    else:
        model = config.milvus_config.EN_MODEL

        embedding = HuggingFaceBgeEmbeddings(
            model_name=model,
            model_kwargs={'device': 'cuda'},
            encode_kwargs={'normalize_embeddings': True}
        )
    logger.info(f'load collection [{collection}], using model {model}')

    doc_store = SqliteDocStore(
        connection_string=config.get_sqlite_path()
    )

    if milvus_cfg.USING_REMOTE:
        connection_args = {
            'uri': milvus_cfg.REMOTE_DATABASE['url'],
            'user': milvus_cfg.REMOTE_DATABASE['username'],
            'password': milvus_cfg.REMOTE_DATABASE['password'],
            'secure': True,
        }
    else:
        connection_args = {
            'host': milvus_cfg.MILVUS_HOST,
            'port': milvus_cfg.MILVUS_PORT,
        }

    vector_db = Milvus(
        embedding,
        collection_name=collection,
        connection_args=connection_args,
        index_params=milvus_cfg.get_collection().INDEX_PARAM,
        drop_old=True
    )

    logger.info('done')

    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=450,
        chunk_overlap=0,
        separators=['\n\n', '\n'],
        keep_separator=False
    )

    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=10,
        separators=['.', '\n\n', '\n'],
        keep_separator=False
    )

    retriever = ParentDocumentRetriever(
        vectorstore=vector_db,
        docstore=doc_store,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
    )

    return retriever


@timer
def load_md(base_path):
    retriever = init_retriever()
    logger.info('start loading file...')

    for root, dirs, files in os.walk(base_path):
        for _file in tqdm(files, total=len(files)):
            file_path = os.path.join(root, _file)
            file_year = int(os.path.basename(root))
            doi = _file.replace('@', '/').replace('.md', '')

            with open(file_path, 'r', encoding='utf-8') as f:
                md_text = f.read()

            md_docs = split_markdown_text(md_text, file_year, doi)

            try:
                retriever.add_documents(md_docs)
            except Exception as e:
                logger.error(f'loading <{_file}> ({file_year}) fail')
                logger.error(e)

    logger.info(f'done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--collection', '-C', nargs='?', type=int, help='初始化特定collection，从0开始')
    parser.add_argument('--auto_create', '-A', action='store_true', help='根据目录结构自动初始化数据库')
    parser.add_argument('--force', '-F', action='store_true', help='强制覆盖已有配置')
    parser.add_argument('--build_reference', '-R', action='store_true', help='在创建文档时构建引用树')
    args = parser.parse_args()

    if args.auto_create:
        yml_path = 'config.yml'
        if not os.path.exists(yml_path):
            logger.info('config dose not exits')
            shutil.copy('config.example.yml', yml_path)

        with open(file=yml_path, mode='r', encoding='utf-8') as file:
            yml = yaml.load(file, Loader=yaml.FullLoader)
            DATA_ROOT = yml['data_root']
            cfg_path = os.path.join(DATA_ROOT, 'collections.json')

            if not args.force and os.path.exists(cfg_path):
                logger.info('config file exists, use existing config file')
            else:
                cols = [{"collection_name": collection,
                         "language": 'en',
                         "title": collection,
                         "description": f'This is a collection about {collection}',
                         "index_param": {
                             "metric_type": 'L2',
                             "index_type": 'HNSW',
                             "params": {"M": 8, "efConstruction": 64},
                         }}
                        for collection in os.listdir(DATA_ROOT)
                        if os.path.isdir(os.path.join(DATA_ROOT, collection))]

                json.dump({"collections": cols}, open(cfg_path, 'w', encoding='utf-8'))
                logger.info(f'auto create config file {cfg_path}')

    from Config import config

    if args.collection is not None:
        if not args.collection:
            for i in range(len(config.milvus_config.COLLECTIONS)):
                logger.info(f'Start init collection {i}')
                config.set_collection(i)
                load_md(config.get_md_path())
        elif args.collection is True:
            if args.collection >= len(config.milvus_config.COLLECTIONS) or args.collection < 0:
                logger.error(f'collection index {args.collection} out of range')
                exit(1)
            else:
                config.set_collection(args.collection)
                if args.build_reference:
                    pass
                else:
                    logger.info(f'Only init collection {args.collection}')
                    load_md(config.get_md_path())
