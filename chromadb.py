
# chromaDB

import chromadb
from dotenv import load_dotenv
import json
import os
import pandas as pd
from langchain.docstore.document import Document
from langchain.prompts import ChatPromptTemplate
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
from langchain_upstage import UpstageEmbeddings
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")

upstage_api_key_env_name = "UPSTAGE_API_KEY"
tavily_api_key_env_name = "TAVILY_API_KEY"

def load_env():
    # Running in Google Colab
    if "google.colab" in str(get_ipython()):
        from google.colab import userdata
        upstage_api_key = userdata.get(upstage_api_key_env_name)
        tavily_api_key = userdata.get(tavily_api_key_env_name)
        return (os.environ.setdefault("UPSTAGE_API_KEY", upstage_api_key),
        # os.environ.setdefault("LANGCHAIN_API_KEY", langchain_api_key),
        os.environ.setdefault("TAVILY_API_KEY", tavily_api_key))
    else:
        # Running in local Jupyter Notebook
        from dotenv import load_dotenv
        load_dotenv()
        return (os.environ.get(upstage_api_key_env_name),
        os.environ.get(tavily_api_key_env_name))

UPSTAGE_API_KEY, TAVILY_API_KEY = load_env()


upstage_api_key_env_name = "UPSTAGE_API_KEY"
tavily_api_key_env_name = "TAVILY_API_KEY"

def load_env():
    # Running in Google Colab
    if "google.colab" in str(get_ipython()):
        from google.colab import userdata
        upstage_api_key = userdata.get(upstage_api_key_env_name)
        tavily_api_key = userdata.get(tavily_api_key_env_name)
        return (os.environ.setdefault("UPSTAGE_API_KEY", upstage_api_key),
        # os.environ.setdefault("LANGCHAIN_API_KEY", langchain_api_key),
        os.environ.setdefault("TAVILY_API_KEY", tavily_api_key))
    else:
        # Running in local Jupyter Notebook
        from dotenv import load_dotenv
        load_dotenv()
        return (os.environ.get(upstage_api_key_env_name),
        os.environ.get(tavily_api_key_env_name))

UPSTAGE_API_KEY, TAVILY_API_KEY = load_env()

# sample
sample_text = [
    "Korea is a beautiful country to visit in the spring.",
    "The best time to visit Korea is in the fall.",
    "Best way to find bug is using unit test.",
    "Python is a great programming language for beginners.",
    "Sung Kim is a great teacher.",
]

splits = RecursiveCharacterTextSplitter().create_documents(sample_text)

print(splits)

vectorstore = Chroma.from_documents(
    documents=splits,
    ids=[doc.page_content for doc in splits],
    embedding=UpstageEmbeddings(model="solar-embedding-1-large"),
)


## 사진, pdf 정보 json 파일 병합

# Load JSON files
with open(r'C:\Users\wnsgu\Desktop\upstage\cookbook\file\사진\documents.json', 'r', encoding='utf-8') as f1, \
     open(r'C:\Users\wnsgu\Desktop\upstage\cookbook\file\pdf\documents.json', 'r', encoding='utf-8') as f2:
    docs1 = json.load(f1)
    docs2 = json.load(f2)

# Combine JSON documents
combined_docs = docs1 + docs2

# Convert combined docs to Document objects, checking if 'content' exists and renaming it to 'page_content'
documents = []
for doc in combined_docs:
    if 'content' in doc:
        documents.append(Document(page_content=doc['content'], metadata=doc.get('metadata', {})))
    else:
        print(f"문서에 'content'가 없습니다: {doc}")

# json 파일, csv 파일, 정책 파일 병합


# HTML 태그를 제거하는 함수
def clean_html(content):
    soup = BeautifulSoup(content, 'html.parser')
    return soup.get_text()

# 텍스트 분할 함수
def chunking(docs):
    # 텍스트 분할기 설정 (chunk 크기를 1000자로 설정하고, 100자의 오버랩을 설정)
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        chunk_size=1000, chunk_overlap=100, language=Language.HTML
    )

    # 문서를 분할
    split_docs = []
    for doc in docs:
        # HTML 태그 제거
        cleaned_content = clean_html(doc.page_content)

        # 텍스트를 분할
        chunks = text_splitter.split_text(cleaned_content)
        split_docs.extend([Document(page_content=chunk, metadata=doc.metadata) for chunk in chunks])

    return split_docs

# Load youth_policies data and df_sorted
youth_policies_df = pd.read_csv(r'C:\Users\wnsgu\Desktop\upstage\youth_policies_new.csv')
df_sorted = pd.read_csv(r'C:\Users\wnsgu\Desktop\upstage\cookbook\Solar-Fullstack-LLM-101\df_sorted.csv')

# Update document content with youth_policies information
for doc in documents:
    title = doc.metadata.get('title')
    if title in youth_policies_df['정책 ID'].values:
        matching_row = youth_policies_df[youth_policies_df['정책 ID'] == title].iloc[0]
    else:
        # If no match, use the first row or another row from youth_policies_df
        matching_row = youth_policies_df.iloc[0]

    # Combine metadata (except title) into page_content
    additional_content = {key: value for key, value in matching_row.to_dict().items() if key != '정책명'}
    updated_content = f"{doc.page_content}\n\nAdditional Information:\n{json.dumps(additional_content, ensure_ascii=False, indent=2)}"
    doc.page_content = updated_content

    # Update metadata to only include 'title' as '정책명'
    doc.metadata = {'title': matching_row['정책명']}

# Convert youth_policies to Document objects
for index, row in youth_policies_df.iterrows():
    documents.append(Document(
        page_content="",  # Do not add CSV content to page_content
        metadata={'title': row['정책명'], **{key: value for key, value in row.to_dict().items() if key != '정책명'}}
    ))

# Convert df_sorted to Document objects
df_sorted_docs = []
for index, row in df_sorted.iterrows():
    df_sorted_docs.append(Document(
        page_content=row['text'],
        metadata={'title': row['title']}
    ))

# Split documents using the chunking function
split_docs = chunking(documents)

# Split df_sorted documents using the chunking function
split_df_sorted_docs = chunking(df_sorted_docs)

# Save combined JSON for documents and youth_policies
with open(r'C:\Users\wnsgu\Desktop\upstage\cookbook\combined_documents.json', 'w', encoding='utf-8') as f:
    json.dump([doc.dict() for doc in split_docs], f, ensure_ascii=False, indent=4)

# Save split df_sorted documents as a separate JSON file
with open(r'C:\Users\wnsgu\Desktop\upstage\cookbook\split_df_sorted.json', 'w', encoding='utf-8') as f:
    json.dump([doc.dict() for doc in split_df_sorted_docs], f, ensure_ascii=False, indent=4)
