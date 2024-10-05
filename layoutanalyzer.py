{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# LayoutAnalyzer\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## install & Setting"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "! pip3 install -qU  markdownify  langchain-upstage rank_bm25 python-dotenv"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "pip install langchain-community"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "pip install chromadb"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "import chromadb\n",
    "import os\n",
    "import zipfile\n",
    "import requests\n",
    "from dotenv import load_dotenv\n",
    "from typing import List\n",
    "import getpass\n",
    "from pprint import pprint\n",
    "import warnings\n",
    "import json\n",
    "warnings.filterwarnings(\"ignore\")\n",
    "from IPython import get_ipython\n",
    "from langchain_community.vectorstores.chroma import Chroma\n",
    "from langchain_upstage import UpstageEmbeddings\n",
    "from langchain.docstore.document import Document\n",
    "from langchain_text_splitters import (\n",
    "    Language,\n",
    "    RecursiveCharacterTextSplitter,\n",
    ")\n",
    "from langchain_upstage import UpstageLayoutAnalysisLoader\n",
    "import pandas as pd\n",
    "from langchain_core.documents import Document\n",
    "from langchain_core.vectorstores import VectorStore\n",
    "\n",
    "\n",
    "upstage_api_key_env_name = \"UPSTAGE_API_KEY\"\n",
    "tavily_api_key_env_name = \"TAVILY_API_KEY\"\n",
    "\n",
    "def load_env():\n",
    "    # Running in Google Colab\n",
    "    if \"google.colab\" in str(get_ipython()):\n",
    "        from google.colab import userdata\n",
    "        upstage_api_key = userdata.get(upstage_api_key_env_name)\n",
    "        tavily_api_key = userdata.get(tavily_api_key_env_name)\n",
    "        return (os.environ.setdefault(\"UPSTAGE_API_KEY\", upstage_api_key),\n",
    "        # os.environ.setdefault(\"LANGCHAIN_API_KEY\", langchain_api_key),\n",
    "        os.environ.setdefault(\"TAVILY_API_KEY\", tavily_api_key))\n",
    "    else:\n",
    "        # Running in local Jupyter Notebook\n",
    "        from dotenv import load_dotenv\n",
    "        load_dotenv()\n",
    "        return (os.environ.get(upstage_api_key_env_name),\n",
    "        os.environ.get(tavily_api_key_env_name))\n",
    "\n",
    "UPSTAGE_API_KEY, TAVILY_API_KEY = load_env()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[Document(metadata={}, page_content='Korea is a beautiful country to visit in the spring.'), Document(metadata={}, page_content='The best time to visit Korea is in the fall.'), Document(metadata={}, page_content='Best way to find bug is using unit test.'), Document(metadata={}, page_content='Python is a great programming language for beginners.'), Document(metadata={}, page_content='Sung Kim is a great teacher.')]\n"
     ]
    }
   ],
   "source": [
    "# sample\n",
    "sample_text = [\n",
    "    \"Korea is a beautiful country to visit in the spring.\",\n",
    "    \"The best time to visit Korea is in the fall.\",\n",
    "    \"Best way to find bug is using unit test.\",\n",
    "    \"Python is a great programming language for beginners.\",\n",
    "    \"Sung Kim is a great teacher.\",\n",
    "]\n",
    "\n",
    "splits = RecursiveCharacterTextSplitter().create_documents(sample_text)\n",
    "\n",
    "print(splits)\n",
    "\n",
    "vectorstore = Chroma.from_documents(\n",
    "    documents=splits,\n",
    "    ids=[doc.page_content for doc in splits],\n",
    "    embedding=UpstageEmbeddings(model=\"solar-embedding-1-large\"),\n",
    ")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## pdf 변환"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [],
   "source": [
    "# pdf 파일 및 사진 파일 폴더 생성 및 옮기기\n",
    "\n",
    "# Path to the folder containing the files\n",
    "folder_path = r\"C:\\Users\\wnsgu\\Desktop\\upstage\\cookbook\\file\"\n",
    "\n",
    "# Define subfolder paths for categorized files\n",
    "pdf_folder = os.path.join(folder_path, \"pdf\")\n",
    "photo_folder = os.path.join(folder_path, \"사진\")\n",
    "\n",
    "# Create subfolders if they do not exist\n",
    "os.makedirs(pdf_folder, exist_ok=True)\n",
    "os.makedirs(photo_folder, exist_ok=True)\n",
    "\n",
    "# Function to extract files from ZIP to a new subfolder\n",
    "def extract_zip(file_path: str, extract_to: str):\n",
    "    subfolder = os.path.join(extract_to, os.path.splitext(os.path.basename(file_path))[0])\n",
    "    os.makedirs(subfolder, exist_ok=True)\n",
    "    with zipfile.ZipFile(file_path, 'r') as zip_ref:\n",
    "        zip_ref.extractall(subfolder)\n",
    "    return subfolder\n",
    "\n",
    "# Function to convert hwp, hwpx files to PDF (assuming you have an appropriate tool installed)\n",
    "def convert_to_pdf(file_path: str, output_folder: str) -> str:\n",
    "    pdf_path = os.path.join(output_folder, os.path.basename(file_path) + \".pdf\")\n",
    "    # Placeholder for conversion logic, you should replace this with actual conversion code.\n",
    "    # For example, using pyhwp, unoconv, or calling an external script to do the conversion.\n",
    "    # convert(file_path, pdf_path)\n",
    "    return pdf_path\n",
    "\n",
    "# Gather all files from the folder (including extracted ZIP files)\n",
    "all_files = []\n",
    "\n",
    "for root, _, files in os.walk(folder_path):\n",
    "    for file in files:\n",
    "        file_path = os.path.join(root, file)\n",
    "\n",
    "        # Extract ZIP files to a new subfolder\n",
    "        if file.lower().endswith(\".zip\"):\n",
    "            try:\n",
    "                extract_zip(file_path, photo_folder)  # Extract ZIP files to '사진' folder\n",
    "            except Exception as e:\n",
    "                print(f\"Failed to extract ZIP: {file_path}, reason: {e}\")\n",
    "\n",
    "        # Convert hwp, hwpx files to PDF and save in 'pdf' folder\n",
    "        elif file.lower().endswith((\".hwp\", \".hwpx\")):\n",
    "            try:\n",
    "                pdf_file = convert_to_pdf(file_path, pdf_folder)\n",
    "                all_files.append(pdf_file)\n",
    "            except Exception as e:\n",
    "                print(f\"Failed to convert to PDF: {file_path}, reason: {e}\")\n",
    "\n",
    "        # Move PDF files to 'pdf' folder\n",
    "        elif file.lower().endswith(\".pdf\"):\n",
    "            pdf_dest = os.path.join(pdf_folder, os.path.basename(file_path))\n",
    "            os.rename(file_path, pdf_dest)\n",
    "            all_files.append(pdf_dest)\n",
    "\n",
    "        # Move images or Excel files to '사진' folder\n",
    "        elif file.lower().endswith((\".jpg\", \".jpeg\", \".png\", \".xls\", \".xlsx\")):\n",
    "            photo_dest = os.path.join(photo_folder, os.path.basename(file_path))\n",
    "            os.rename(file_path, photo_dest)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Number of successfully processed documents: 226\n",
      "Number of failed files: 10\n",
      "                                                file  \\\n",
      "0  C:\\Users\\wnsgu\\Desktop\\upstage\\cookbook\\file\\p...   \n",
      "1  C:\\Users\\wnsgu\\Desktop\\upstage\\cookbook\\file\\p...   \n",
      "2  C:\\Users\\wnsgu\\Desktop\\upstage\\cookbook\\file\\p...   \n",
      "3  C:\\Users\\wnsgu\\Desktop\\upstage\\cookbook\\file\\p...   \n",
      "4  C:\\Users\\wnsgu\\Desktop\\upstage\\cookbook\\file\\p...   \n",
      "5  C:\\Users\\wnsgu\\Desktop\\upstage\\cookbook\\file\\p...   \n",
      "6  C:\\Users\\wnsgu\\Desktop\\upstage\\cookbook\\file\\p...   \n",
      "7  C:\\Users\\wnsgu\\Desktop\\upstage\\cookbook\\file\\p...   \n",
      "8  C:\\Users\\wnsgu\\Desktop\\upstage\\cookbook\\file\\p...   \n",
      "9  C:\\Users\\wnsgu\\Desktop\\upstage\\cookbook\\file\\p...   \n",
      "\n",
      "                                              reason  \n",
      "0                     Failed to analyze layout: '/S'  \n",
      "1                     Failed to analyze layout: '/S'  \n",
      "2                     Failed to analyze layout: '/S'  \n",
      "3                     Failed to analyze layout: '/D'  \n",
      "4                     Failed to analyze layout: '/S'  \n",
      "5  Failed to analyze layout: unhashable type: 'In...  \n",
      "6                     Failed to analyze layout: '/S'  \n",
      "7                     Failed to analyze layout: '/S'  \n",
      "8                     Failed to analyze layout: '/D'  \n",
      "9                     Failed to analyze layout: '/S'  \n"
     ]
    }
   ],
   "source": [
    "# pdf파일 layoutanalyzer 이용해서 변환\n",
    "\n",
    "# Function to analyze PDF files using UpstageLayoutAnalysisLoader\n",
    "def layout_analysis(filenames: List[str]) -> List[Document]:\n",
    "    layout_analysis_loader = UpstageLayoutAnalysisLoader(filenames, output_type=\"html\")\n",
    "    return layout_analysis_loader.load()\n",
    "\n",
    "# Function to extract files from ZIP to a new subfolder\n",
    "def extract_zip(file_path: str, extract_to: str):\n",
    "    subfolder = os.path.join(extract_to, os.path.splitext(os.path.basename(file_path))[0])\n",
    "    os.makedirs(subfolder, exist_ok=True)\n",
    "    with zipfile.ZipFile(file_path, 'r') as zip_ref:\n",
    "        zip_ref.extractall(subfolder)\n",
    "    return subfolder\n",
    "\n",
    "# Function to convert hwp, hwpx files to PDF (assuming you have an appropriate tool installed)\n",
    "def convert_to_pdf(file_path: str) -> str:\n",
    "    pdf_path = file_path + \".pdf\"\n",
    "    # Placeholder for conversion logic, you should replace this with actual conversion code.\n",
    "    # For example, using pyhwp, unoconv, or calling an external script to do the conversion.\n",
    "    # convert(file_path, pdf_path)\n",
    "    return pdf_path\n",
    "\n",
    "# Path to the folder containing the files\n",
    "folder_path = r\"C:\\Users\\wnsgu\\Desktop\\upstage\\cookbook\\file\\pdf\"\n",
    "\n",
    "# Gather all files from the folder (including extracted ZIP files)\n",
    "all_files = []\n",
    "failed_files = []\n",
    "\n",
    "for root, _, files in os.walk(folder_path):\n",
    "    for file in files:\n",
    "        file_path = os.path.join(root, file)\n",
    "\n",
    "        # Extract ZIP files to a new subfolder\n",
    "        if file.lower().endswith(\".zip\"):\n",
    "            try:\n",
    "                new_subfolder = extract_zip(file_path, root)\n",
    "                # Add extracted files to all_files list\n",
    "                for sub_root, _, sub_files in os.walk(new_subfolder):\n",
    "                    all_files.extend([os.path.join(sub_root, sub_file) for sub_file in sub_files])\n",
    "            except Exception as e:\n",
    "                failed_files.append({\"file\": file_path, \"reason\": f\"Failed to extract ZIP: {e}\"})\n",
    "        else:\n",
    "            all_files.append(file_path)\n",
    "\n",
    "# Process all files (convert to PDF if necessary)\n",
    "pdf_files = []\n",
    "for file_path in all_files:\n",
    "    if file_path.lower().endswith((\".hwp\", \".hwpx\")):\n",
    "        try:\n",
    "            pdf_file = convert_to_pdf(file_path)\n",
    "            pdf_files.append(pdf_file)\n",
    "        except Exception as e:\n",
    "            failed_files.append({\"file\": file_path, \"reason\": f\"Failed to convert to PDF: {e}\"})\n",
    "    elif file_path.lower().endswith(\".pdf\"):\n",
    "        pdf_files.append(file_path)\n",
    "\n",
    "# Analyze PDFs and keep track of failures\n",
    "documents = []\n",
    "for pdf_file in pdf_files:\n",
    "    try:\n",
    "        docs = layout_analysis([pdf_file])\n",
    "        \n",
    "        # 파일명 추출\n",
    "        file_name = os.path.splitext(os.path.basename(pdf_file))[0]  # 확장자를 제거한 파일명 (예: 'Rfffff')\n",
    "        \n",
    "        # 각 Document 객체에 파일명을 title로 추가\n",
    "        for doc in docs:\n",
    "            doc.metadata['title'] = file_name\n",
    "        \n",
    "        documents.extend(docs)\n",
    "    except Exception as e:\n",
    "        failed_files.append({\"file\": pdf_file, \"reason\": f\"Failed to analyze layout: {e}\"})\n",
    "\n",
    "# Convert failed files list to DataFrame\n",
    "failed_files_df = pd.DataFrame(failed_files)\n",
    "\n",
    "# Save the failed files DataFrame to a CSV\n",
    "failed_files_csv_path = os.path.join(folder_path, \"failed_files.csv\")\n",
    "failed_files_df.to_csv(failed_files_csv_path, index=False)\n",
    "\n",
    "# Output the results\n",
    "print(f\"Number of successfully processed documents: {len(documents)}\")\n",
    "if not failed_files_df.empty:\n",
    "    print(f\"Number of failed files: {len(failed_files_df)}\")\n",
    "    print(failed_files_df)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Documents saved to: C:\\Users\\wnsgu\\Desktop\\upstage\\cookbook\\file\\pdf\\documents.json\n"
     ]
    }
   ],
   "source": [
    "# json으로 변환\n",
    "\n",
    "# documents 리스트를 JSON 형식으로 변환하기\n",
    "documents_data = []\n",
    "for doc in documents:\n",
    "    documents_data.append({\n",
    "        'content': doc.page_content,  # 문서 내용\n",
    "        'metadata': doc.metadata      # 메타데이터 (예: title 등)\n",
    "    })\n",
    "\n",
    "# 저장 경로 설정\n",
    "documents_json_path = os.path.join(folder_path, \"documents.json\")\n",
    "\n",
    "# JSON 파일로 저장하기\n",
    "with open(documents_json_path, 'w', encoding='utf-8') as f:\n",
    "    json.dump(documents_data, f, ensure_ascii=False, indent=4)\n",
    "\n",
    "# 결과 출력\n",
    "print(f\"Documents saved to: {documents_json_path}\")\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 정책 파일 병합"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "file_path1='C:/Users/wnsgu/Desktop/upstage/cookbook/poly_words/poly_words/법무부_(생활법률지식)1.법률용어_20191231.csv'\n",
    "file_path2='C:/Users/wnsgu/Desktop/upstage/cookbook/poly_words/poly_words/생활법령_근로.csv'\n",
    "file_path3='C:/Users/wnsgu/Desktop/upstage/cookbook/poly_words/poly_words/생활법령_복지.csv'\n",
    "file_path4='C:/Users/wnsgu/Desktop/upstage/cookbook/poly_words/poly_words/생활법령_주거.csv'\n",
    "file_path5='C:/Users/wnsgu/Desktop/upstage/cookbook/poly_words/poly_words/주택청약 용어.csv'\n",
    "file_path6='C:/Users/wnsgu/Desktop/upstage/cookbook/poly_words/poly_words/청년정보 용어사전.csv'\n",
    "\n",
    "\n",
    "a=pd.read_csv(file_path1, encoding='cp949')\n",
    "b=pd.read_csv(file_path2)\n",
    "c=pd.read_csv(file_path3)\n",
    "d=pd.read_csv(file_path4)\n",
    "e=pd.read_csv(file_path5)\n",
    "f=pd.read_csv(file_path6)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [],
   "source": [
    "a.drop(columns=['용어번호'], inplace=True)\n",
    "a.rename(columns={'용어명': 'title', '설명': 'text'}, inplace=True)\n",
    "e.rename(columns={'용어': 'title', '설명': 'text'}, inplace=True)\n",
    "f.rename(columns={'용어': 'title', '뜻': 'text'}, inplace=True)\n",
    "result = pd.concat([a, b, c, d, e, f], axis=0, ignore_index=True)\n",
    "df_sorted = result.sort_values(by='title')\n",
    "df_sorted.to_csv(\"df_sorted.csv\", index=False)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## OCR"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "c:\\Users\\wnsgu\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\langchain_upstage\\layout_analysis.py:135: UserWarning: UpstageLayoutAnalysisLoader is deprecated.Please use langchain_upstage.document_parse.UpstageDocumentParseLoader instead.\n",
      "  warnings.warn(\n",
      "c:\\Users\\wnsgu\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\langchain_upstage\\layout_analysis_parsers.py:160: UserWarning: UpstageLayoutAnalysisParser is deprecated.Please use langchain_upstage.document_parse_parsers.UpstageDocumentParseParser instead.\n",
      "  warnings.warn(\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Number of successfully processed documents: 26\n",
      "Documents saved to: C:\\Users\\wnsgu\\Desktop\\upstage\\cookbook\\file\\사진\\documents.json\n"
     ]
    }
   ],
   "source": [
    "# document ocr을 이용한 파일 정보 가지고오기\n",
    "\n",
    "# Load API key from .env file\n",
    "load_dotenv()\n",
    "api_key = os.getenv(\"API_KEY\")\n",
    "\n",
    "# Path to the folder containing the image files\n",
    "folder_path = r\"C:\\Users\\wnsgu\\Desktop\\upstage\\cookbook\\file\\사진\"\n",
    "\n",
    "# Gather all image files from the folder\n",
    "image_extensions = (\".jpg\", \".jpeg\", \".png\", \".bmp\", \".tiff\")\n",
    "image_files = [os.path.join(root, file) for root, _, files in os.walk(folder_path) for file in files if file.lower().endswith(image_extensions)]\n",
    "\n",
    "# Process each image file with UpstageLayoutAnalysisLoader\n",
    "documents = []\n",
    "failed_files = []\n",
    "\n",
    "for image_file in image_files:\n",
    "    try:\n",
    "        # Load the image file with OCR\n",
    "        layzer = UpstageLayoutAnalysisLoader([image_file], output_type=\"html\", use_ocr=True)\n",
    "        \n",
    "        # Use lazy_load method for better memory efficiency\n",
    "        docs = layzer.load()  # You can use layzer.lazy_load() if needed\n",
    "\n",
    "        # Extract filename without extension\n",
    "        file_name = os.path.splitext(os.path.basename(image_file))[0]\n",
    "\n",
    "        # Append the result to documents\n",
    "        for doc in docs:\n",
    "            doc.metadata['title'] = file_name\n",
    "            documents.append({\n",
    "                'content': doc.page_content,  # 문서 내용\n",
    "                'metadata': doc.metadata      # 메타데이터 (예: title 등)\n",
    "            })\n",
    "\n",
    "    except Exception as e:\n",
    "        # Record the failure for this file\n",
    "        failed_files.append({\"file\": image_file, \"reason\": str(e)})\n",
    "\n",
    "# Save the results as JSON\n",
    "documents_json_path = os.path.join(folder_path, \"documents.json\")\n",
    "with open(documents_json_path, 'w', encoding='utf-8') as f:\n",
    "    json.dump(documents, f, ensure_ascii=False, indent=4)\n",
    "\n",
    "# Save failed files to a CSV\n",
    "if failed_files:\n",
    "    failed_files_df = pd.DataFrame(failed_files)\n",
    "    failed_files_csv_path = os.path.join(folder_path, \"failed_files.csv\")\n",
    "    failed_files_df.to_csv(failed_files_csv_path, index=False)\n",
    "\n",
    "# Output the results\n",
    "print(f\"Number of successfully processed documents: {len(documents)}\")\n",
    "if failed_files:\n",
    "    print(f\"Number of failed files: {len(failed_files)}\")\n",
    "    print(failed_files_df)\n",
    "    print(f\"Failed files saved to: {failed_files_csv_path}\")\n",
    "\n",
    "print(f\"Documents saved to: {documents_json_path}\")\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
