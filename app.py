import streamlit as st
from dotenv import load_dotenv
from langchain.schema import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI  # langchain-community に分離されたのでこちらを使用

# 環境変数を読み込む
load_dotenv()

# LLMにプロンプトを渡して回答を得る関数を定義
def get_advice(input_text, expert_type):
    # 専門家の種類に応じてシステムメッセージを切り替え
    if expert_type == "インテリアの専門家":
        system_message = "あなたはインテリアの専門家です。"
    elif expert_type == "料理の専門家":
        system_message = "あなたは料理の専門家です。"
    else:
        return ["無効な専門家の種類です。"]  # エラーでもリストで返すことでUIが壊れないように

    # ChatOpenAI インスタンスを作成
    # 🔧 修正ポイント: max_tokens=200 → 応答全体での最大トークン数
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, max_tokens=200)

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=input_text[:100]),  # インプットは最大100文字に制限
    ]

    # 🔧 修正ポイント③: invoke() → generate() に変更（複数回答に対応）
    # generate() は 2次元リストでメッセージを渡す必要がある
    results = llm.generate([[msg for msg in messages]])

    # 🔧 修正ポイント④: 複数回答を .generations[0] から取り出して .text を取得
    advices = [gen.text for gen in results.generations[0]]

    return advices

# Streamlitアプリの設定
st.title("専門家アドバイスシステム")
st.write("このアプリでは、インテリアまたは料理の専門家からアドバイスを受けることができます。")

# 専門家の種類を選択するラジオボタン
expert_type = st.radio("専門家の種類を選択してください:", ("インテリアの専門家", "料理の専門家"))

# 入力フォームの設定
input_text = st.text_area("質問を入力してください:")

# ボタンが押されたときの処理
if st.button("アドバイスを取得"):
    if input_text:
        advices = get_advice(input_text, expert_type)
        st.write("専門家からのアドバイス:")
        # アドバイスを1件ずつ表示（ラベル付き）
        for i, advice in enumerate(advices, 1):
            st.markdown(f"**アドバイス {i}:** {advice}")
    else:
        st.write("質問を入力してください。")


