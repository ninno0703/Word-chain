import streamlit as st
import requests

# 初始化 Session State (用於在網頁重新整理時保留資料)
if 'used_words' not in st.session_state:
    st.session_state.used_words = []
if 'current_word' not in st.session_state:
    st.session_state.current_word = ""

def is_valid_word(word):
    """透過 Dictionary API 檢查單字是否存在"""
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(api_url, timeout=5)
        return response.status_code == 200
    except:
        return False

# 網頁介面設置
st.title("🔤 英文單字接龍遊戲")
st.write("輸入一個英文單字來開始或繼續接龍！")

# 顯示目前的遊戲狀態
if st.session_state.current_word:
    st.info(f"上一個單字是：**{st.session_state.current_word}**")
    st.write(f"請輸入以 **{st.session_state.current_word[-1].upper()}** 開頭的單字")
else:
    st.success("遊戲開始！請輸入任意單字。")

# 使用者輸入
user_input = st.text_input("請在此輸入單字：", key="input_text").strip().lower()
submit_button = st.button("送出")

if submit_button and user_input:
    # 邏輯判斷
    if not user_input.isalpha():
        st.error("請僅輸入英文字母。")
    elif user_input in st.session_state.used_words:
        st.error(f"單字 '{user_input}' 已經被用過了！")
    elif st.session_state.current_word and user_input[0] != st.session_state.current_word[-1]:
        st.error(f"接龍規則錯誤！必須以 '{st.session_state.current_word[-1]}' 開頭。")
    else:
        with st.spinner('正在字典中驗證單字...'):
            if is_valid_word(user_input):
                st.session_state.used_words.append(user_input)
                st.session_state.current_word = user_input
                st.balloons() # 噴彩帶特效
                st.rerun() # 重新整理頁面顯示最新狀態
            else:
                st.error(f"無效單字：'{user_input}' 在網路字典中找不到。")

# 側邊欄顯示歷史記錄
st.sidebar.header("已使用的單字")
st.sidebar.write(st.session_state.used_words)

if st.sidebar.button("重新開始遊戲"):
    st.session_state.used_words = []
    st.session_state.current_word = ""
    st.rerun()