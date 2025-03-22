import streamlit as st
from dotenv import load_dotenv
from langchain.schema import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI  # langchain-community に分離されたのでこちらを使用

# 環境変数を読み込む
load_dotenv()

MAX_CHARS = 100  # 入力の最大文字数

# LLMにプロンプトを渡して回答を得る関数を定義
def get_advice(input_text, expert_type):
    # 専門家の種類に応じてシステムメッセージを切り替え
    if expert_type == "インテリアの専門家":
        system_message = "あなたはインテリアの専門家です。回答は重複させず異なる視点で提案し、短く簡潔に要約してください。"
    elif expert_type == "料理の専門家":
        system_message = "あなたは料理の専門家です。回答は重複させず回答は重複させず異なる視点で提案し、短く簡潔に要約してください。"
    else:
        return ["無効な専門家の種類です。"]

    # ChatOpenAI インスタンスを作成
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, max_tokens=200, n=1)

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=input_text[:MAX_CHARS]),  # インプットは最大100文字に制限
    ]

    # 複数応答を取得
    results = llm.generate([[msg for msg in messages]])
    advices = [gen.text for gen in results.generations[0]]
    return advices

# Streamlitアプリの設定
st.title("専門家アドバイスシステム")
st.write("このアプリでは、インテリアまたは料理の専門家からアドバイスを受けることができます。")

# 専門家の種類を選択するラジオボタン
expert_type = st.radio("専門家の種類を選択してください:", ("インテリアの専門家", "料理の専門家"))

# ユーザーの入力用フォーム
st.subheader("質問を入力してください（最大100文字）")

# 入力用のテキストエリア（最大文字数指定）
input_text = st.text_area(
    "例：リビングの照明を変えたいのですが、どんなものが良いでしょうか？",
    max_chars=MAX_CHARS,
    height=100,
    help="Command + Enter で送信、Enterだけで改行できます。",
)


# Command+Enterで送信（デフォルト動作）
if st.button("アドバイスを取得") or (input_text and st.session_state.get("submit_on_enter", False)):
    if input_text.strip():
        advices = get_advice(input_text, expert_type)
        st.write("専門家からのアドバイス:")
        for i, advice in enumerate(advices, 1):
            st.markdown(f"**アドバイス {i}:** {advice}")
    else:
        st.warning("質問を入力してください。")


