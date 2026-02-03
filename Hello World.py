import streamlit as st
import pandas as pd
import random
import os
import json
import time

# 主標題
st.title("Hello! 👋 梁育維的歡樂小天地")
st.subheader("✨ 今日特輯：簡單、好玩、充滿驚喜！")
st.write("歡迎來到一個專門放小遊戲與小工具的角落，放輕鬆、來玩一局吧！")

# 歡迎區
st.header("📣 歡迎區 — 打招呼有儀式感")
st.write("輸入你的名字或按個按鈕，說聲哈囉吧。")
if st.button("點我打招呼"):
    st.success("哈囉！希望你今天心情很好 😊")

# 數據小天地
st.subheader("📊 數據小天地 — 看圖說故事")
df = pd.DataFrame({"A": [1, 2, 3], "B": [3, 2, 1]})
st.write("簡單示範：")
st.dataframe(df)

# 小遊戲角落
st.subheader("🎮 小遊戲角落 — 玩一下放鬆一下")
st.write("這裡會放入猜數字、單字挑戰……快來挑戰吧！")

# 單字挑戰介紹
st.subheader("🔤 單字挑戰 — 詞彙大考驗")
st.write("三種難度，答錯即結束；答對就繼續！試試看能拿幾分吧。")

# 側欄
st.sidebar.title("🧭 快速選單")
st.sidebar.write("點選或捲動找到你想玩的遊戲，祝遊戲愉快！")

# === 單字四選一問答（Multiple-choice Word Quiz） ===
st.subheader("🔤 四選一單字挑戰 — 答錯即結束，看看你能拿多少分！")
# 檔案以儲存最高分
HIGHSCORE_FILE = os.path.join("data", "word_quiz_highscore.json")


def load_highscore() -> int:
    try:
        with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return int(data.get("highscore", 0))
    except Exception:
        return 0


def save_highscore(score: int):
    os.makedirs(os.path.dirname(HIGHSCORE_FILE), exist_ok=True)
    with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
        json.dump({"highscore": int(score)}, f)


# 讀取外部字庫（若無則使用內建）
def load_word_bank():
    default = []
    try:
        with open(os.path.join("data", "word_bank.json"), "r", encoding="utf-8") as f:
            default = json.load(f)
    except Exception:
        # 建立簡單備援
        default = [
            {"word": w, "definition": w, "difficulty": "簡單"} for w in ["apple", "book", "chair", "dog", "cat"]
        ]
    pools = {"簡單": [], "中等": [], "困難": []}
    for entry in default:
        diff = entry.get("difficulty", "簡單")
        if diff not in pools:
            diff = "簡單"
        pools[diff].append(entry)
    return pools

POOLS = load_word_bank()

POINTS = {"簡單": 1, "中等": 2, "困難": 3}

# 初始化最高分
if "word_quiz_highscore" not in st.session_state:
    st.session_state.word_quiz_highscore = load_highscore()

# 初始化遊戲狀態
if "word_quiz_game" not in st.session_state:
    st.session_state.word_quiz_game = {
        "active": False,
        "difficulty": "簡單",
        "score": 0,
        "used": set(),  # 已使用過的題目(word)
        "current": None,  # dict: {definition, options, answer, start_time}
        "history": [],
        "time_limit": 0,  # 秒, 0 表示無限時間
        "question_idx": 0,  # 用來作為 radio widget 的唯一 key
    }

# 側欄顯示記分板與最高分
st.sidebar.header("📝 單字挑戰 記分板")
st.sidebar.write(f"目前分數：{st.session_state.word_quiz_game['score']} 分")
st.sidebar.write(f"目前最高紀錄：{st.session_state.word_quiz_highscore} 分")

# 計時器設定（側欄）
st.sidebar.subheader("⏱ 時間設定")
st.sidebar.write("將在每題開始時啟動計時；若超過時間則視為答錯。輸入 0 表示不計時。")
st.session_state.word_quiz_game['time_limit'] = st.sidebar.number_input("每題限定秒數：", min_value=0, max_value=300, value=int(st.session_state.word_quiz_game.get('time_limit', 0)), step=5)
if st.sidebar.button("重置最高紀錄"):
    save_highscore(0)
    st.session_state.word_quiz_highscore = 0
    st.sidebar.success("最高紀錄已重置。")

# 選擇難度
diff = st.selectbox("選擇難度：", ("簡單", "中等", "困難"), index=(0 if st.session_state.word_quiz_game['difficulty'] == '簡單' else (1 if st.session_state.word_quiz_game['difficulty'] == '中等' else 2)))
if diff != st.session_state.word_quiz_game['difficulty']:
    st.session_state.word_quiz_game['difficulty'] = diff
    st.info("已更改難度，請按『開始新遊戲』以應用新難度。")

# 使用分頁整理 UI
tab1, tab2 = st.tabs(["🔤 單字挑戰", "🎮 其他遊戲（Placeholder）"])
with tab1:
    # 開始新遊戲 / 重新開始
    if st.button("開始新遊戲"):
        st.session_state.word_quiz_game.update({
            "active": True,
            "score": 0,
            "used": set(),
            "current": None,
            "history": [],
            "difficulty": diff,
            "question_idx": 0,
        })
        st.success("遊戲已開始，祝你幸運！")

    # 結束並儲存分數
    if st.button("結束並儲存分數"):
        final = st.session_state.word_quiz_game['score']
        if final > st.session_state.word_quiz_highscore:
            save_highscore(final)
            st.session_state.word_quiz_highscore = final
            st.success(f"已儲存並更新最高分：{final} 分！")
            st.balloons()
        else:
            st.info(f"遊戲結束，你的分數：{final} 分 （未超越最高紀錄 {st.session_state.word_quiz_highscore} 分）")
        st.session_state.word_quiz_game['active'] = False

    # 產生題目函式：回傳 (definition, options, answer)
    def _make_question_from_pool(pool_entries):
        choices = [e for e in pool_entries if e['word'] not in st.session_state.word_quiz_game['used']]
        if not choices:
            return None, [], None
        entry = random.choice(choices)
        word = entry['word']
        # 選其他三個錯誤選項
        others = [e['word'] for e in pool_entries if e['word'] != word]
        # 若其他選項不足，補入其他難度詞庫
        if len(others) < 3:
            all_words = [e['word'] for k in POOLS for e in POOLS[k] if e['word'] != word]
            others = list(set(others + all_words))
        wrongs = random.sample(others, k=3) if len(others) >= 3 else random.sample(others, k=len(others))
        options = wrongs + [word]
        random.shuffle(options)
        return entry.get('definition', ''), options, word

    # 幫助函式：產生下一題並設定狀態
    def _advance_question(pool_entries):
        definition, options, answer = _make_question_from_pool(pool_entries)
        if definition is None:
            st.success("恭喜！已回答完此難度的所有題目。遊戲結束。")
            st.session_state.word_quiz_game['active'] = False
            st.session_state.word_quiz_game['current'] = None
        else:
            st.session_state.word_quiz_game['current'] = {
                'definition': definition,
                'options': options,
                'answer': answer,
                'start_time': time.time()
            }
            # 增加題目索引以重置 widget keys
            st.session_state.word_quiz_game['question_idx'] += 1

    # 主遊戲邏輯
    if st.session_state.word_quiz_game['active']:
        difficulty = st.session_state.word_quiz_game.get('difficulty', '簡單')
        pool_entries = POOLS.get(difficulty, [])

        if not st.session_state.word_quiz_game['current']:
            _advance_question(pool_entries)

        if st.session_state.word_quiz_game['current']:
            cur = st.session_state.word_quiz_game['current']
            st.write(f"題目（定義）： **{cur['definition']}**")

            # 顯示剩餘時間（若有設定）
            tlimit = int(st.session_state.word_quiz_game.get('time_limit', 0))
            if tlimit > 0:
                elapsed = int(time.time() - cur.get('start_time', time.time()))
                remaining = max(0, tlimit - elapsed)
                st.write(f"剩餘時間： {remaining} 秒")

            # 顯示 2x2 按鈕（按鈕標籤即為答案文字）
            rows = [st.columns(2) for _ in range(2)]
            btn_clicked = None
            for i, opt in enumerate(cur['options']):
                row = rows[i // 2]
                col = row[i % 2]
                with col:
                    # 直接用按鈕顯示答案文字（更直觀）
                    if st.button(opt, key=f"word_quiz_btn_{st.session_state.word_quiz_game['question_idx']}_{i}"):
                        btn_clicked = opt

            # 自動檢查是否時間到（若到會自動判為答錯並結束遊戲）
            if tlimit > 0:
                elapsed = int(time.time() - cur.get('start_time', time.time()))
                remaining = max(0, tlimit - elapsed)
                if remaining <= 0 and st.session_state.word_quiz_game['active']:
                    st.error("時間到！答錯了。遊戲結束。")
                    final = st.session_state.word_quiz_game['score']
                    if final > st.session_state.word_quiz_highscore:
                        save_highscore(final)
                        st.session_state.word_quiz_highscore = final
                        st.balloons()
                        st.success(f"新的最高紀錄：{final} 分！恭喜！")
                    else:
                        st.info(f"目前最高紀錄仍為：{st.session_state.word_quiz_highscore} 分。")
                    st.session_state.word_quiz_game['active'] = False
                    st.session_state.word_quiz_game['current'] = None

            if btn_clicked:
                # 時間檢查（防禦性檢查）
                if tlimit > 0 and (time.time() - cur.get('start_time', time.time())) > tlimit:
                    st.error("時間到！答錯了。遊戲結束。")
                    final = st.session_state.word_quiz_game['score']
                    if final > st.session_state.word_quiz_highscore:
                        save_highscore(final)
                        st.session_state.word_quiz_highscore = final
                        st.balloons()
                        st.success(f"新的最高紀錄：{final} 分！恭喜！")
                    else:
                        st.info(f"目前最高紀錄仍為：{st.session_state.word_quiz_highscore} 分。")
                    st.session_state.word_quiz_game['active'] = False
                    st.session_state.word_quiz_game['current'] = None
                else:
                    if btn_clicked == cur['answer']:
                        pts = POINTS.get(difficulty, 1)
                        st.session_state.word_quiz_game['score'] += pts
                        st.session_state.word_quiz_game['history'].append({'word': cur['answer'], 'points': pts})
                        st.session_state.word_quiz_game['used'].add(cur['answer'])
                        # 準備下一題（立即生出新題）
                        _advance_question(pool_entries)
                        # 嘗試強制重新執行（大多數環境支援）以立即呈現下一題
                        try:
                            if hasattr(st, 'experimental_set_query_params'):
                                st.experimental_set_query_params(_next=int(time.time()))
                        except Exception:
                            # 如果無法使用 experimental_set_query_params，保留目前狀態（下一次 rerun 將呈現新題）
                            pass
                        # 顯示簡短成功提示（不阻礙流程）
                        st.success(f"答對！獲得 {pts} 分，目前分數：{st.session_state.word_quiz_game['score']} 分。下一題！")
                    else:
                        final = st.session_state.word_quiz_game['score']
                        st.error(f"答錯了！正確答案是：{cur['answer']}。遊戲結束，你的最終分數：{final} 分。")
                        # 更新最高分
                        if final > st.session_state.word_quiz_highscore:
                            save_highscore(final)
                            st.session_state.word_quiz_highscore = final
                            st.balloons()
                            st.success(f"新的最高紀錄：{final} 分！恭喜！")
                        else:
                            st.info(f"目前最高紀錄仍為：{st.session_state.word_quiz_highscore} 分。")
                        st.session_state.word_quiz_game['active'] = False
                        st.session_state.word_quiz_game['current'] = None

    with tab2:
        st.write("其他遊戲放在這裡（可擴充）")

    # 側欄顯示歷史與分數
    st.sidebar.write("---")
    st.sidebar.write(f"遊戲狀態：{'進行中' if st.session_state.word_quiz_game['active'] else '未進行'}")
    st.sidebar.write(f"目前分數：{st.session_state.word_quiz_game['score']} 分")
    if st.session_state.word_quiz_game['history']:
        st.sidebar.write("最近答對：")
        for h in st.session_state.word_quiz_game['history'][-10:]:
            st.sidebar.write(f"{h['word']} (+{h['points']} 分)")

# 載入 time 模組（用於計時）
import time

