import streamlit as st
st.title("梁育維是Gay!!!")

import streamlit as st
import pandas as pd

# 1. 設定網頁標題
st.title("Hello World! 👋")

# 2. 顯示基本文字
st.write("這是我的第一個 Streamlit 網頁應用程式。")

# 3. 增加一些互動元件 (按鈕)
if st.button('點擊我打招呼'):
    st.success('你好！歡迎來到 Streamlit 的世界！')

# 4. 簡單的輸入框互動
name = st.text_input("請輸入你的名字：")
if name:
    st.write(f"很高興認識你，{name}！")

# 5. 顯示數據表格 (Streamlit 最強大的功能之一)
st.subheader("數據展示範例")
df = pd.DataFrame({
    '欄位 A': [1, 2, 3, 4],
    '欄位 B': [10, 20, 30, 40]
})
st.dataframe(df) # 互動式表格
st.line_chart(df) # 快速畫圖