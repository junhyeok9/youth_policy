# 청년 정책 추천 챗봇

## 프로젝트 개요
청년 정채글 




## Project Structure

```
youth_policy
├─ .gitignore
├─ chatbot.py
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
