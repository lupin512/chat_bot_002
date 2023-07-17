import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": st.secrets.AppSettings.chatbot_setting}
        ]

if "messages_len" not in st.session_state:
    st.session_state["messages_len"] = 0

if "total_tokens" not in st.session_state:
    st.session_state["total_tokens"] = 0

if "all_tokens" not in st.session_state:
    st.session_state["all_tokens"] = 0

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["messages_len"] = len(messages)
    st.session_state["total_tokens"] = response["usage"]["total_tokens"]
    st.session_state["all_tokens"] += response["usage"]["total_tokens"]
    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

st.write("現在のmesseage数は" + str(st.session_state["messages_len"]) + "です")
st.write("今回消費したtokenは" + str(st.session_state["total_tokens"]) + "です")
st.write("累計での消費tokenは" + str(st.session_state["all_tokens"]) + "です")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
