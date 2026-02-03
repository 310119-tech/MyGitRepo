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
    # 嚴格型別檢查，排除 bool
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

# === 遊戲：剪刀石頭布 (Rock-Paper-Scissors) ===
st.subheader("✂️🪨📄 剪刀石頭布（Rock-Paper-Scissors）")
# 初始化統計
if 'rps_stats' not in st.session_state:
    st.session_state.rps_stats = {"wins": 0, "losses": 0, "ties": 0, "rounds": 0, "history": []}

rps_choice = st.radio("選擇你的出拳：", ("剪刀", "石頭", "布"))
col1, col2 = st.columns([1, 2])
with col1:
    if st.button("出拳！"):
        comp = random.choice(["剪刀", "石頭", "布"])
        player = rps_choice
        if player == comp:
            result = "平手"
            st.session_state.rps_stats["ties"] += 1
        else:
            # 何者勝何者（key 贏 value）
            wins_map = {"剪刀": "布", "石頭": "剪刀", "布": "石頭"}
            if wins_map[player] == comp:
                result = "你贏了"
                st.session_state.rps_stats["wins"] += 1
            else:
                result = "你輸了"
                st.session_state.rps_stats["losses"] += 1
        st.session_state.rps_stats["rounds"] += 1
        st.session_state.rps_stats["history"].append({"player": player, "comp": comp, "result": result})
        st.write(f"你：{player}；電腦：{comp} → **{result}**")

with col2:
    st.write(f"勝：{st.session_state.rps_stats['wins']}，敗：{st.session_state.rps_stats['losses']}，平：{st.session_state.rps_stats['ties']}，回合：{st.session_state.rps_stats['rounds']}")
    if st.session_state.rps_stats["history"]:
        st.write("最近回合：")
        for h in st.session_state.rps_stats["history"][-5:]:
            st.write(f"你：{h['player']}，電腦：{h['comp']} → {h['result']}")
    if st.button("重設戰績"):
        st.session_state.rps_stats = {"wins": 0, "losses": 0, "ties": 0, "rounds": 0, "history": []}
        st.success("戰績已重設。")


# === 遊戲：猜質數挑戰 (Prime Quiz) ===
st.subheader("🧠 猜質數挑戰（Is it prime?）")
# 初始化狀態
if 'prime' not in st.session_state:
    st.session_state.prime = {"score": 0, "total": 0, "current": random.randint(2, 100), "history": [], "attempted": False}

col1, col2 = st.columns(2)
with col1:
    if st.button("下一題"):
        st.session_state.prime["current"] = random.randint(2, 200)
        st.session_state.prime["attempted"] = False

number = st.session_state.prime["current"]
st.write(f"請判斷： **{number}** 是不是質數？")

# 答案按鈕
if st.button("是 (Prime)"):
    if not st.session_state.prime.get("attempted", False):
        correct = is_prime(number)
        st.session_state.prime["total"] += 1
        if correct:
            st.session_state.prime["score"] += 1
            st.success("答對了！這是質數。")
        else:
            st.error(f"答錯了，{number} 不是質數。")
        st.session_state.prime["history"].append({"num": number, "your": "是", "correct": correct})
        st.session_state.prime["attempted"] = True

if st.button("否 (Not Prime)"):
    if not st.session_state.prime.get("attempted", False):
        correct = not is_prime(number)
        st.session_state.prime["total"] += 1
        if correct:
            st.session_state.prime["score"] += 1
            st.success("答對了！這個數不是質數。")
        else:
            st.error(f"答錯了，{number} 其實是質數。")
        st.session_state.prime["history"].append({"num": number, "your": "否", "correct": correct})
        st.session_state.prime["attempted"] = True

# 顯示分數與歷史
st.write(f"得分：{st.session_state.prime['score']} / {st.session_state.prime['total']}")
if st.session_state.prime["history"]:
    st.write("最近題目：")
    for h in st.session_state.prime["history"][-6:]:
        st.write(f"{h['num']} → 你：{h['your']}，正確：{h['correct']}")

if st.button("重置質數挑戰統計"):
    st.session_state.prime = {"score": 0, "total": 0, "current": random.randint(2, 100), "history": [], "attempted": False}
    st.success("質數挑戰已重置。")
