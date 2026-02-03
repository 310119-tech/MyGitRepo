import streamlit as st
import pandas as pd
import math
import random

def is_prime(n: int) -> bool:
    """回傳 True 表示 n 是質數；False 表示不是。

    要求：
    - 輸入必須為正整數（>0）。
    - 若輸入不是正整數，則會拋出 ValueError。
    """
    # 嚴格檢查型別，排除 bool（bool 是 int 的子類別）
    if type(n) is not int or n <= 0:
        raise ValueError("輸入必須為正整數")
    if n == 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = int(math.isqrt(n))
    for i in range(3, limit + 1, 2):
        if n % i == 0:
            return False
    return True

# 1. 設定網頁標題
st.title("Hello! 👋 Streamlit 小工具與遊戲")

# 2. 顯示基本文字
st.write("這是梁育維的第一個 Streamlit 網頁應用程式。")

# 3. 增加一些互動元件 (按鈕)
if st.button('點擊我打招呼'):
    st.success('你好！歡迎來到 Streamlit 的世界！')

# 4. 簡單的輸入框互動
name = st.text_input("請輸入你的名字：")
if name:
    st.write(f"我是梁育維 很高興認識你，{name}！")

# 5. 顯示數據表格 (Streamlit 最強大的功能之一)
st.subheader("📊 數據展示範例（示範）")
df = pd.DataFrame({
    '欄位 A': [1, 2, 3, 4],
    '欄位 B': [10, 20, 30, 40]
})
st.dataframe(df) # 互動式表格
st.line_chart(df) # 快速畫圖

# === 小遊戲：猜數字 ===
st.subheader("🎮 猜數字小遊戲：挑戰你的直覺")
col1, col2 = st.columns(2)
with col1:
    min_val = st.number_input("最小值", value=1, step=1)
    max_val = st.number_input("最大值", value=100, step=1)
    if min_val >= max_val:
        st.error("最小值必須小於最大值。請調整範圍。")

with col2:
    if st.button("開始新遊戲") or 'secret' not in st.session_state:
        if min_val < max_val:
            st.session_state.secret = random.randint(min_val, max_val)
            st.session_state.attempts = 0
            st.session_state.history = []
            st.session_state.won = False
            st.session_state.min_val = min_val
            st.session_state.max_val = max_val
            st.success("新的遊戲已開始！請開始猜數字。")

# 若遊戲尚未初始化，顯示提示
if 'secret' not in st.session_state:
    st.info("請按『開始新遊戲』以初始化遊戲。")
else:
    if st.session_state.get('min_val') != min_val or st.session_state.get('max_val') != max_val:
        st.info("您已更改範圍，請按『開始新遊戲』以重新生成答案。")

    if 'secret' in st.session_state and min_val < max_val:
        guess = st.number_input("輸入你的猜測：", min_value=int(min_val), max_value=int(max_val), step=1, value=int(min_val))
        if st.button("猜一猜"):
            if st.session_state.get('won'):
                st.warning("遊戲已結束，請開始新遊戲或重新開始。")
            else:
                st.session_state.attempts += 1
                st.session_state.history.append(int(guess))
                secret = st.session_state.secret
                if int(guess) == secret:
                    st.success(f"恭喜！答對了，數字是 {secret}。你猜了 {st.session_state.attempts} 次。")
                    st.balloons()
                    st.session_state.won = True
                elif int(guess) < secret:
                    st.info("太小了！")
                else:
                    st.info("太大了！")

        # 顯示遊戲狀態
        st.write(f"嘗試次數：{st.session_state.get('attempts', 0)}")
        st.write(f"猜過的數字：{st.session_state.get('history', [])}")

        if st.button("重新開始遊戲"):
            st.session_state.secret = random.randint(min_val, max_val)
            st.session_state.attempts = 0
            st.session_state.history = []
            st.session_state.won = False
            st.success("已重新開始遊戲！")