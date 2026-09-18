"""Streamlit application for the 16-type work-style diagnosis."""

import html

import streamlit as st

from questions import AXES, QUESTIONS
from scoring import (
    build_type_code,
    calculate_scores,
    display_percentages,
    find_tied_axes,
    tendency_label,
)
from types_data import TYPES


QUESTIONS_PER_PAGE = 8
TOTAL_PAGES = len(QUESTIONS) // QUESTIONS_PER_PAGE


st.set_page_config(
    page_title="仕事スタイル16タイプ診断",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    :root {--ink:#25314d; --muted:#6b7280; --blue:#5a72d8; --pink:#d86f92; --surface:#ffffff;}
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background: linear-gradient(180deg, #f7f8ff 0%, #ffffff 32%); color: var(--ink);}
    .block-container {max-width: 780px; padding-top: 2.2rem; padding-bottom: 4rem;}
    h1, h2, h3 {color: var(--ink); letter-spacing: -.02em;}
    .eyebrow {color: var(--blue); font-size:.82rem; font-weight:800; letter-spacing:.11em; text-transform:uppercase;}
    .hero {padding: 2.2rem 2rem; border:1px solid #e4e7f4; border-radius:24px; background:rgba(255,255,255,.9); box-shadow:0 18px 50px rgba(58,71,121,.08); margin-bottom:1.2rem;}
    .hero h1 {font-size:2.35rem; margin:.4rem 0 .8rem; line-height:1.25;}
    .hero p {color:#566078; font-size:1.05rem; line-height:1.8; margin:0;}
    .meta-row {display:grid; grid-template-columns:repeat(3,1fr); gap:.7rem; margin:1.2rem 0;}
    .meta-card {padding:.9rem .7rem; text-align:center; border-radius:14px; background:#f2f4ff;}
    .meta-card strong {display:block; font-size:1.1rem; color:#4053b4;}
    .meta-card span {font-size:.8rem; color:#6c748b;}
    .axis-grid {display:grid; grid-template-columns:repeat(2,1fr); gap:.75rem; margin:1rem 0 1.4rem;}
    .axis-card {padding:1rem; border:1px solid #e8e9f2; border-radius:14px; background:#fff;}
    .axis-card strong {display:block; margin-bottom:.25rem;}
    .axis-card span {font-size:.85rem; color:#72798c;}
    .question-card {padding:1rem 1.1rem; margin:1rem 0 .35rem; border:1px solid #e5e7f1; border-radius:14px; background:#fff; box-shadow:0 5px 18px rgba(57,67,105,.035);}
    .scale-labels {display:flex; justify-content:space-between; max-width:440px; margin:.15rem auto -.25rem; color:#737b91; font-size:.78rem; font-weight:650;}
    div[role="radiogroup"][aria-orientation="horizontal"] {justify-content:space-between; max-width:440px; margin:0 auto .3rem;}
    .axis-title {font-size:.84rem; color:var(--muted); margin-bottom:.2rem; font-weight:650;}
    .bar-labels {display:flex; justify-content:space-between; gap:1rem; font-weight:750; margin-top:1.15rem; font-size:.94rem;}
    .bar {display:flex; width:100%; height:18px; overflow:hidden; border-radius:999px; background:#ececf2; box-shadow:inset 0 0 0 1px rgba(50,56,80,.05);}
    .bar-first {background:linear-gradient(90deg,#7187e6,#5369ca);}
    .bar-second {background:linear-gradient(90deg,#d96f92,#e58eaa);}
    .type-hero {padding:1.7rem; border:1px solid #e3e6f4; border-radius:20px; background:linear-gradient(135deg,#f3f5ff,#fff5f8); margin:.5rem 0 1.5rem;}
    .type-code {display:inline-block; padding:.28rem .72rem; background:#e6eaff; color:#4052ba; border-radius:999px; font-weight:850; letter-spacing:.14em;}
    .type-hero h1 {font-size:2rem; margin:.65rem 0 .65rem;}
    .type-hero p {line-height:1.85; color:#4d5871; margin:0;}
    .section-card {padding:1.1rem 1.2rem; border:1px solid #e7e8f0; border-radius:15px; background:#fff; height:100%;}
    div.stButton > button, div.stFormSubmitButton > button {border-radius:999px; min-height:3rem; font-weight:750;}
    @media (max-width:640px) {
      .block-container {padding:1.1rem 1rem 3rem;}
      .hero {padding:1.5rem 1.15rem; border-radius:18px;}
      .hero h1 {font-size:1.85rem;}
      .axis-grid {grid-template-columns:1fr;}
      .meta-row {gap:.4rem;}
      .meta-card {padding:.7rem .3rem;}
      .bar-labels {font-size:.82rem;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialize_state():
    defaults = {"phase": "intro", "page": 0, "answers": {}, "tie_answers": {}}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def restart():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def render_intro():
    st.markdown(
        """
        <div class="hero">
          <div class="eyebrow">WORK STYLE DIAGNOSIS</div>
          <h1>あなたらしい仕事の進め方を、<br>4つの軸から見つけよう。</h1>
          <p>判断の起点、仕事の進め方、周囲との関わり方、価値の生み出し方。32の質問から、あなたの仕事スタイルを16タイプで整理します。</p>
        </div>
        <div class="meta-row">
          <div class="meta-card"><strong>32問</strong><span>質問数</span></div>
          <div class="meta-card"><strong>約4分</strong><span>所要時間</span></div>
          <div class="meta-card"><strong>16タイプ</strong><span>診断結果</span></div>
        </div>
        <div class="axis-grid">
          <div class="axis-card"><strong>現実重視 R ↔ 理想重視 V</strong><span>判断するとき、何を起点にするか</span></div>
          <div class="axis-card"><strong>計画型 P ↔ 柔軟型 F</strong><span>仕事をどのように進めるか</span></div>
          <div class="axis-card"><strong>個人型 I ↔ 協働型 C</strong><span>周囲とどのように関わるか</span></div>
          <div class="axis-card"><strong>既存改善型 E ↔ 新規開拓型 N</strong><span>どのように価値を生み出すか</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("正解や優劣はありません。理想の自分ではなく、普段の行動に近いものを選んでください。")
    if st.button("診断を始める", type="primary", use_container_width=True):
        st.session_state.phase = "questions"
        st.rerun()


def render_questionnaire():
    page = st.session_state.page
    start = page * QUESTIONS_PER_PAGE
    page_questions = QUESTIONS[start : start + QUESTIONS_PER_PAGE]

    st.title("仕事スタイル16タイプ診断")
    st.write("普段の自分に最も近いものを、直感的に選んでください。")
    st.progress((page + 1) / TOTAL_PAGES, text=f"{page + 1} / {TOTAL_PAGES}ページ")
    st.caption("中央の丸は「どちらともいえない」です。")

    with st.form(f"questions_page_{page}"):
        for question in page_questions:
            st.markdown(
                f'<div class="question-card"><strong>Q{question["id"]}. {html.escape(question["text"])}</strong></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="scale-labels"><span>そう思わない</span><span>そう思う</span></div>',
                unsafe_allow_html=True,
            )
            previous = st.session_state.answers.get(question["id"])
            index = previous - 1 if previous else None
            st.radio(
                question["text"],
                options=[1, 2, 3, 4, 5],
                index=index,
                horizontal=True,
                key=f"answer_{question['id']}",
                label_visibility="collapsed",
                format_func=lambda value: " ",
            )

        back_col, next_col = st.columns(2)
        back = back_col.form_submit_button("前のページ", use_container_width=True, disabled=page == 0)
        next_label = "回答を確定する" if page == TOTAL_PAGES - 1 else "次のページ"
        next_clicked = next_col.form_submit_button(next_label, type="primary", use_container_width=True)

    if back:
        save_visible_answers(page_questions, require_all=False)
        st.session_state.page -= 1
        st.rerun()

    if next_clicked:
        missing = save_visible_answers(page_questions, require_all=True)
        if missing:
            st.error("このページに未回答の質問があります。すべて回答してから進んでください。")
        elif page < TOTAL_PAGES - 1:
            st.session_state.page += 1
            st.rerun()
        else:
            scores = calculate_scores(QUESTIONS, st.session_state.answers, AXES)
            st.session_state.scores = scores
            st.session_state.phase = "ties" if find_tied_axes(scores) else "result"
            st.rerun()


def save_visible_answers(page_questions, require_all):
    missing = []
    for question in page_questions:
        value = st.session_state.get(f"answer_{question['id']}")
        if value is None:
            if require_all:
                missing.append(question["id"])
        else:
            st.session_state.answers[question["id"]] = value
    return missing


def render_tie_breakers():
    tied_axes = find_tied_axes(st.session_state.scores)
    st.title("最後に、もう少しだけ教えてください")
    st.write("回答がちょうど均衡した項目について、より近いほうを選んでください。グラフは50％対50％のまま表示します。")

    with st.form("tie_breakers"):
        for axis_id in tied_axes:
            axis = AXES[axis_id]
            st.subheader(axis["title"])
            st.radio(
                axis["tie_question"],
                options=[axis["first_code"], axis["second_code"]],
                format_func=lambda code, a=axis: a["tie_first"] if code == a["first_code"] else a["tie_second"],
                index=None,
                key=f"tie_{axis_id}",
            )
        submitted = st.form_submit_button("診断結果を見る", type="primary", use_container_width=True)

    if submitted:
        missing = [axis_id for axis_id in tied_axes if st.session_state.get(f"tie_{axis_id}") is None]
        if missing:
            st.error("すべての項目を選択してください。")
        else:
            st.session_state.tie_answers = {
                axis_id: st.session_state[f"tie_{axis_id}"] for axis_id in tied_axes
            }
            st.session_state.phase = "result"
            st.rerun()


def render_axis_bar(axis_id, score):
    axis = AXES[axis_id]
    first, second = display_percentages(score)
    st.markdown(
        f"""
        <div class="axis-title">{html.escape(axis['title'])}・{html.escape(tendency_label(score))}</div>
        <div class="bar-labels">
          <span>{html.escape(axis['first_label'])} {first}%</span>
          <span>{second}% {html.escape(axis['second_label'])}</span>
        </div>
        <div class="bar">
          <div class="bar-first" style="width:{first}%"></div>
          <div class="bar-second" style="width:{second}%"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result():
    scores = st.session_state.scores
    code = build_type_code(scores, AXES, st.session_state.tie_answers)
    result = TYPES[code]

    st.markdown('<div class="eyebrow">YOUR WORK STYLE</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="type-hero">
          <span class="type-code">{html.escape(code)}</span>
          <h1>{html.escape(result['name'])}</h1>
          <p>{html.escape(result['summary'])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("4つの傾向スコア")
    for axis_id in AXES:
        render_axis_bar(axis_id, scores[axis_id])
    st.caption("傾向スコアは回答に基づく相対的な強さを示すもので、能力の優劣を表すものではありません。")

    left, right = st.columns(2)
    with left:
        st.subheader("強み")
        for item in result["strengths"]:
            st.markdown(f"- {item}")
    with right:
        st.subheader("注意したいこと")
        for item in result["cautions"]:
            st.markdown(f"- {item}")

    st.subheader("チームで担いやすい役割")
    st.write(result["role"])
    st.subheader("力を発揮しやすい環境")
    st.write(result["environment"])

    st.info("この診断は自己理解を支援するオリジナルコンテンツであり、医学的・心理学的な診断ではありません。")
    st.button("もう一度診断する", on_click=restart, use_container_width=True)


initialize_state()

if st.session_state.phase == "intro":
    render_intro()
elif st.session_state.phase == "questions":
    render_questionnaire()
elif st.session_state.phase == "ties":
    render_tie_breakers()
else:
    render_result()
