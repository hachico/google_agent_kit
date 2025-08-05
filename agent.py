from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType, Tool
from tools import search_website, get_web_content
import os

# 環境変数からGemini APIキーを読み込み
os.environ['GOOGLE_API_KEY'] = 'AIzaSyD90mQbSJiOvJKZklUpe4Sjr-xR9ztzlTE'

# Geminiモデルの初期化
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")

# ツールリストの定義
tools = [
    Tool(
        name="Search Website",
        func=search_website,
        description="""会社のウェブサイトURLを検索するためのツール。
        入力は会社名。例: 'グーグル'
        """
    ),
    Tool(
        name="Get Web Content",
        func=get_web_content,
        description="""指定されたURLのウェブコンテンツを全て取得するためのツール。
        入力はURL。例: 'https://www.google.com/'
        """
    )
]

# エージェントの初期化
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True # エージェントの思考プロセスを表示
)

# エージェントの実行関数
def run_agent(company_name: str):
    """エージェントを実行して会社情報を取得します。"""
    prompt = f"""
    以下の会社名について、公式ウェブサイトから以下の情報を取得してください。
    - 会社名
    - 住所
    - 電話番号
    - 設立年
    もし情報が見つからない場合は、「情報が見つかりませんでした」と返答してください。
    会社名: {company_name}
    """
    return agent.run(prompt)

if __name__ == "__main__":
    result = run_agent("グーグル")
    print("\n--- 最終結果 ---")
    print(result)