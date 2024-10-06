# 청년정책 추천 챗봇

## 프로젝트 개요

청년정책 추천 챗봇은 청년들이 거주지, 나이, 취업 상태 등과 같은 개인 정보를 입력하면 맞춤형 청년정책을 추천해주는 AI 챗봇입니다. 이 프로젝트는 사용자들이 복잡한 청년정책 정보를 쉽게 이해하고, 자신에게 맞는 청년정책을 간편하게 찾을 수 있도록 돕는 것을 목표로 합니다.

이 챗봇은 대한민국 공식 전자정부 웹사이트인 [온통청년](https://www.youthcenter.go.kr/main.do)의 청년정책 데이터를 기반으로 하여, 지역별, 연령별, 상황에 맞는 정책을 빠르게 제공하며, 정책의 상세한 내용도 함께 안내합니다. Gradio 인터페이스를 사용해 웹 브라우저에서 손쉽게 챗봇을 사용할 수 있으며, 직관적인 대화 형식으로 누구나 쉽게 접근할 수 있습니다.

### 주요 기능
- 지역, 나이, 취업 상태 등 개인 정보 입력을 통한 맞춤형 청년정책 추천
- 신청 기간, 자격 요건, 필수 지원 서류 등 청년정책의 세부적인 정보에 관한 질의응답
- 어려운 용어 의미 질의응답
- 간단한 자연어 입력만으로도 대화 가능
- 외부 웹사이트 검색을 통한 풍부하고 다양한 정보 제공
- 웹 브라우저를 통한 사용 편의성 제공 (Gradio 인터페이스 활용)


## Project Structure

```
youth_policy
├─ .gitignore
├─ chatbot.py
├─ data
│  ├─ chromadb.py
│  ├─ crawling_words.ipynb
│  ├─ layout_analyzer.py
│  └─ policy_crawling_and_attached_file_save.py
├─ download_db.py
├─ README.md
└─ requirements.txt
```

## Installation

1. **Clone the repository**:

    Clone the repository to your local machine using the following command:

    ```bash
    git clone https://github.com/junhyeok9/youth_policy.git
    ```


2. **Navigate to the project directory**:

    Move into the directory of the cloned repository:

    ```bash
    cd youth_policy
    ```

3. **Install the required packages**:

    Install all the dependencies listed in the ```requirements.txt``` file:

    ```bash
    pip install -r requirements.txt
    ```


## Usage

1. **Download the Chroma DB from Google Drive**:

    Run the ```download_db.py``` script to download the necessary database files.

    ```bash
    python download_db.py
    ```   

2. **Set up API keys in environment variables**:

    Rename the ```.env.example``` file to ```.env```, and add your API keys inside the file.

3. **Run the chatbot**:

    Start the chatbot by running the ```chatbot.py``` script.

    ```bash
    python chatbot.py
    ```

4. **Open the Gradio interface**:

    After running the chatbot, open the Gradio interface in your web browser by navigating to:

    ```
    http://127.0.0.1:7860
    ```

## Example

![example](https://github.com/user-attachments/assets/06e4137f-2012-471d-a3df-2bf065eb4019)

## Authors

This project was created by the following contributors:

- **강민정** - 입력 필요
- **원준혁** - 입력 필요
- **이세은** - 입력 필요

