import streamlit as st
import requests
import pandas as pd

# 設置網頁標題
st.set_page_config(page_title="英文單字接龍 - 雲端對戰版", layout="centered")

# --- 初始化 Session State ---
if 'used_words' not in st.session_state:
    st.session_state.used_words = []
if 'current_word' not in st.session_state:
    st.session_state.current_word = ""

# --- 功能函式 ---
def is_valid_word(word):
    """聯網驗證單字"""
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(api_url, timeout=5)
        return response.status_code == 200
    except:
        return False

def handle_submit():
    """處理送出邏輯 (包含清空輸入框)"""
    user_input = st.session_state.widget.strip().lower()
    
    if not user_input:
        return

    # 驗證邏輯
    if not user_input.isalpha():
        st.toast("❌ 請僅輸入英文字母", icon="⚠️")
    elif user_input in st.session_state.used_words:
        st.toast(f"❌ '{user_input}' 已被用過", icon="🚫")
    elif st.session_state.current_word and user_input[0] != st.session_state.current_word[-1]:
        st.toast(f"❌ 必須以 '{st.session_state.current_word[-1]}' 開頭", icon="❗")
    else:
        if is_valid_word(user_input):
            st.session_state.used_words.append(user_input)
            st.session_state.current_word = user_input
            st.toast(f"✅ 成功接龍: {user_input}", icon="🎉")
        else:
            st.toast(f"❌ 字典找不到 '{user_input}'", icon="🔍")
    
    # 清空輸入框內容
    st.session_state.widget = ""

# --- 側邊欄：存檔與讀取 ---
st.sidebar.title("💾 遊戲存檔管理")

# 1. 下載進度 (Download)
if st.session_state.used_words:
    df = pd.DataFrame(st.session_state.used_words, columns=["Word History"])
    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="📥 下載目前遊戲進度",
        data=csv,
        file_name="word_chain_save.csv",
        mime="text/csv",
    )

# 2. 上傳進度 (Upload)
uploaded_file = st.sidebar.file_uploader("📤 上傳之前的存檔 (CSV)", type="csv")
if uploaded_file is not None:
    try:
        load_df = pd.read_csv(uploaded_file)
        loaded_list = load_df["Word History"].tolist()
        if st.sidebar.button("確認載入存檔"):
            st.session_state.used_words = loaded_list
            st.session_state.current_word = loaded_list[-1] if loaded_list else ""
            st.sidebar.success("載入成功！")
            st.rerun()
    except Exception as e:
        st.sidebar.error("存檔格式不正確")

if st.sidebar.button("♻️ 重新開始新遊戲"):
    st.session_state.used_words = []
    st.session_state.current_word = ""
    st.rerun()

# --- 主畫面 UI ---
st.title("🔤 英文單字接龍")

# 狀態顯示
if st.session_state.current_word:
    st.subheader(f"當前目標字母: :red[{st.session_state.current_word[-1].upper()}]")
    st.info(f"上一個單字: **{st.session_state.current_word}**")
else:
    st.subheader("請輸入任意單字開始遊戲")

# 輸入框 (綁定 on_change 實現 Enter 發送並自動清空)
st.text_input(
    "輸入單字後按 Enter 發送：",
    key="widget",
    on_change=handle_submit
)

# 歷史紀錄展示
st.divider()
st.write("📜 **接龍歷史紀錄:**")
st.write(" → ".join(st.session_state.used_words) if st.session_state.used_words else "暫無紀錄")