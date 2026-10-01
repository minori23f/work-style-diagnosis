"""Streamlit application for the 16-type work-style diagnosis."""

import base64
import html
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from questions import AXES, QUESTIONS
from scoring import (
    build_type_code,
    calculate_scores,
    display_percentages,
    infer_tie_answers,
    tendency_label,
)
from types_data import TYPES


QUESTIONS_PER_PAGE = 8
TOTAL_PAGES = (len(QUESTIONS) + QUESTIONS_PER_PAGE - 1) // QUESTIONS_PER_PAGE
CHARACTER_DIR = Path(__file__).parent / "assets" / "characters"


st.set_page_config(
    page_title="仕事スタイル16タイプ診断",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    :root {--ink:#27243d; --muted:#716f80; --purple:#6c63ff; --pink:#ec6f9e; --mint:#3dc7b0; --yellow:#f2b84b; --surface:#ffffff;}
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {
      background:
        radial-gradient(circle at 8% 5%, rgba(108,99,255,.13), transparent 23rem),
        radial-gradient(circle at 92% 12%, rgba(236,111,158,.12), transparent 21rem),
        linear-gradient(180deg, #fbfaff 0%, #ffffff 38%);
      color:var(--ink);
    }
    .block-container {max-width: 780px; padding-top: 2.2rem; padding-bottom: 4rem;}
    h1, h2, h3 {color: var(--ink); letter-spacing: -.02em;}
    .eyebrow {color:var(--purple); font-size:.78rem; font-weight:900; letter-spacing:.13em; text-transform:uppercase;}
    .hero {position:relative; overflow:hidden; padding:2.35rem 2.1rem; border:1px solid rgba(108,99,255,.14); border-radius:28px; background:rgba(255,255,255,.92); box-shadow:0 22px 60px rgba(69,55,134,.11); margin-bottom:1.2rem;}
    .hero::after {content:""; position:absolute; width:150px; height:150px; border-radius:42% 58% 63% 37%; right:-45px; top:-52px; background:linear-gradient(135deg,rgba(108,99,255,.2),rgba(236,111,158,.22)); transform:rotate(18deg);}
    .hero h1 {font-size:2.45rem; margin:.45rem 0 .9rem; line-height:1.28; position:relative; z-index:1;}
    .hero p {color:#5d5970; font-size:1.04rem; line-height:1.85; margin:0; max-width:610px; position:relative; z-index:1;}
    .gradient-word {background:linear-gradient(90deg,var(--purple),var(--pink)); -webkit-background-clip:text; background-clip:text; color:transparent;}
    .meta-row {display:grid; grid-template-columns:repeat(3,1fr); gap:.7rem; margin:1.2rem 0;}
    .meta-card {padding:.95rem .7rem; text-align:center; border-radius:16px; border:1px solid rgba(108,99,255,.08);}
    .meta-card:nth-child(1) {background:#f0efff;}
    .meta-card:nth-child(2) {background:#fff0f5;}
    .meta-card:nth-child(3) {background:#eafaf7;}
    .meta-card strong {display:block; font-size:1.15rem; color:#4e45c7;}
    .meta-card span {font-size:.8rem; color:#6c748b;}
    .axis-grid {display:grid; grid-template-columns:repeat(2,1fr); gap:.75rem; margin:1rem 0 1.4rem;}
    .axis-card {padding:1.05rem; border:1px solid #ece9f5; border-radius:18px; background:rgba(255,255,255,.92); box-shadow:0 7px 24px rgba(55,45,105,.045);}
    .axis-head {display:flex; align-items:center; gap:.45rem; margin-bottom:.55rem; font-weight:800;}
    .axis-icon {font-size:1.15rem;}
    .axis-poles {display:flex; align-items:center; gap:.38rem; flex-wrap:wrap; font-size:.87rem; color:#514e60;}
    .axis-poles .arrow {color:#a8a4b8; font-weight:800;}
    .code-badge {display:inline-flex; align-items:center; justify-content:center; width:1.9rem; height:1.9rem; border-radius:10px; color:white; font-size:.94rem; font-weight:950; box-shadow:0 5px 12px rgba(56,43,112,.16);}
    .code-purple {background:linear-gradient(135deg,#766eff,#5b52d9);}
    .code-pink {background:linear-gradient(135deg,#f07ca7,#d95786);}
    .code-mint {background:linear-gradient(135deg,#55d8c0,#27aa94);}
    .code-yellow {background:linear-gradient(135deg,#f5c565,#e49b24);}
    .question-card {display:flex; align-items:flex-start; gap:.8rem; padding:1.05rem 1.15rem; margin:1.1rem 0 .35rem; border:1px solid #e8e5f1; border-radius:17px; background:rgba(255,255,255,.95); box-shadow:0 7px 24px rgba(57,44,105,.05);}
    .q-number {flex:0 0 auto; display:inline-flex; align-items:center; justify-content:center; min-width:2.35rem; height:2rem; padding:0 .45rem; border-radius:10px; background:linear-gradient(135deg,#766eff,#ec6f9e); color:#fff; font-size:.78rem; font-weight:900;}
    .q-text {line-height:1.75; padding-top:.05rem;}
    div[role="radiogroup"][aria-orientation="horizontal"] {
      display:grid !important;
      grid-template-columns:minmax(82px,auto) repeat(5,minmax(38px,1fr)) minmax(58px,auto);
      align-items:center;
      column-gap:.35rem;
      width:100% !important;
      max-width:620px;
      margin:.15rem auto .45rem;
    }
    div[role="radiogroup"][aria-orientation="horizontal"]::before {content:"そう思わない"; justify-self:end; color:#777386; font-size:.76rem; font-weight:700; white-space:nowrap;}
    div[role="radiogroup"][aria-orientation="horizontal"]::after {content:"そう思う"; justify-self:start; color:#777386; font-size:.76rem; font-weight:700; white-space:nowrap;}
    div[role="radiogroup"][aria-orientation="horizontal"] label[data-baseweb="radio"] {justify-self:center; margin:0 !important; padding:.35rem !important; border-radius:999px; transition:transform .15s ease, background .15s ease;}
    div[role="radiogroup"][aria-orientation="horizontal"] label[data-baseweb="radio"]:hover {transform:scale(1.12); background:#f1efff;}
    div[role="radiogroup"][aria-orientation="horizontal"] label[data-baseweb="radio"] > div:last-child {display:none !important;}
    .result-heading {margin:2.3rem 0 1rem;}
    .result-heading .eyebrow {margin-bottom:.3rem;}
    .result-heading h2 {font-size:1.48rem; margin:0;}
    .axis-result-card {padding:1.25rem 1.35rem 1.35rem; margin:0 0 1rem; border:1px solid #e8e5f2; border-radius:20px; background:rgba(255,255,255,.96); box-shadow:0 9px 28px rgba(58,45,109,.055);}
    .axis-result-top {display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; margin-bottom:.9rem;}
    .axis-category {color:var(--muted); font-size:.8rem; font-weight:800; margin-bottom:.2rem;}
    .axis-dominant {font-size:1.16rem; line-height:1.45; color:var(--ink); font-weight:900;}
    .tendency-chip {flex:0 0 auto; padding:.35rem .65rem; border-radius:999px; background:#f0efff; color:#5d54d7; font-size:.76rem; font-weight:850;}
    .bar-labels {display:flex; justify-content:space-between; gap:1rem; font-weight:780; margin:0 0 .6rem; font-size:.96rem;}
    .bar {display:flex; width:100%; height:16px; overflow:hidden; border-radius:999px; background:#ececf2; box-shadow:inset 0 0 0 1px rgba(50,56,80,.05);}
    .bar-first {background:linear-gradient(90deg,#766eff,#5b52d9);}
    .bar-second {background:linear-gradient(90deg,#ec6f9e,#f19ab8);}
    .result-pole {display:inline-flex; align-items:center; gap:.35rem;}
    .mini-code {display:inline-flex; align-items:center; justify-content:center; width:1.55rem; height:1.55rem; border-radius:8px; color:#fff; background:#746bed; font-size:.72rem; font-weight:950;}
    .result-pole:last-child .mini-code {background:#df678f;}
    .type-hero {display:grid; grid-template-columns:minmax(190px,.8fr) minmax(0,1.35fr); align-items:center; gap:1.4rem; padding:1.3rem 1.6rem 1.5rem; border:1px solid rgba(108,99,255,.16); border-radius:28px; background:linear-gradient(135deg,#f1f0ff,#fff1f6 68%,#effbf8); box-shadow:0 20px 55px rgba(67,52,124,.11); margin:.5rem 0 1.6rem; overflow:hidden;}
    .type-visual {display:flex; align-items:flex-end; justify-content:center; min-height:285px;}
    .type-visual img {width:100%; max-height:315px; object-fit:contain; filter:drop-shadow(0 15px 18px rgba(61,45,113,.16));}
    .type-code {display:inline-block; padding:.38rem .85rem; background:#fff; color:#574dcc; border:1px solid rgba(108,99,255,.18); border-radius:999px; font-size:.84rem; font-weight:950; letter-spacing:.18em; box-shadow:0 5px 15px rgba(66,52,122,.08);}
    .type-kicker {font-size:.82rem; color:#77708a; font-weight:750; margin-top:1rem;}
    .type-hero h1 {font-size:2.65rem; line-height:1.25; margin:.18rem 0 .8rem; background:linear-gradient(90deg,#4d43c4,#d85484); -webkit-background-clip:text; background-clip:text; color:transparent;}
    .type-hero p {font-size:1.02rem; line-height:1.9; color:#4d5368; margin:0;}
    .info-card {padding:1.25rem 1.3rem; border:1px solid #e7e8f0; border-radius:19px; background:#fff; height:100%; box-shadow:0 8px 24px rgba(58,45,109,.045);}
    .info-card-head {display:flex; align-items:center; gap:.5rem; margin-bottom:.75rem; color:#403b58; font-size:.98rem; font-weight:900;}
    .info-card-icon {display:inline-flex; align-items:center; justify-content:center; width:2rem; height:2rem; border-radius:10px; background:#f0efff;}
    .info-card ul {padding-left:1.3rem; margin:0;}
    .info-card li {font-size:1rem; line-height:1.75; color:#4c4a5c; margin:.45rem 0; padding-left:.15rem;}
    .info-card.strength .info-card-icon {background:#eafaf7;}
    .info-card.caution .info-card-icon {background:#fff3e3;}
    .info-card.role .info-card-icon {background:#f0efff;}
    .info-card.environment .info-card-icon {background:#fff0f5;}
    div.stButton > button, div.stFormSubmitButton > button {border-radius:999px; min-height:3rem; font-weight:800;}
    button[kind="primary"] {background:linear-gradient(90deg,var(--purple),var(--pink)) !important; border:none !important; box-shadow:0 10px 24px rgba(108,99,255,.22);}
    button[kind="primary"]:hover {transform:translateY(-1px); box-shadow:0 13px 28px rgba(108,99,255,.28);}
    @media (max-width:640px) {
      .block-container {padding:1.1rem 1rem 3rem;}
      .hero {padding:1.5rem 1.15rem; border-radius:18px;}
      .hero h1 {font-size:1.9rem;}
      .axis-grid {grid-template-columns:1fr;}
      .meta-row {gap:.4rem;}
      .meta-card {padding:.7rem .3rem;}
      .bar-labels {font-size:.82rem;}
      .type-hero {grid-template-columns:1fr; gap:.25rem; padding:1rem 1.1rem 1.4rem; text-align:center;}
      .type-visual {min-height:220px;}
      .type-visual img {max-height:245px;}
      .type-hero h1 {font-size:2.15rem;}
      .axis-result-top {align-items:center;}
      .axis-dominant {font-size:1.04rem;}
      div[role="radiogroup"][aria-orientation="horizontal"] {grid-template-columns:70px repeat(5,minmax(30px,1fr)) 48px; column-gap:.08rem;}
      div[role="radiogroup"][aria-orientation="horizontal"]::before,
      div[role="radiogroup"][aria-orientation="horizontal"]::after {font-size:.66rem;}
      div[role="radiogroup"][aria-orientation="horizontal"] label[data-baseweb="radio"] {padding:.22rem !important;}
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


def request_scroll_to_top():
    st.session_state["scroll_to_top"] = True


def scroll_to_top_if_requested():
    if st.session_state.pop("scroll_to_top", False):
        components.html(
            """
            <script>
            const scrollToTop = () => {
              const parentWindow = window.parent;
              const parentDocument = parentWindow.document;
              const anchor = parentDocument.getElementById('page-top-anchor');

              if (anchor) {
                anchor.scrollIntoView({block: 'start', inline: 'nearest'});
              }

              parentWindow.scrollTo(0, 0);
              parentDocument.documentElement.scrollTop = 0;
              parentDocument.body.scrollTop = 0;

              [
                '[data-testid="stMain"]',
                '[data-testid="stAppViewContainer"]',
                'section.main',
                '.main'
              ].forEach((selector) => {
                const element = parentDocument.querySelector(selector);
                if (element) {
                  element.scrollTop = 0;
                  if (typeof element.scrollTo === 'function') {
                    element.scrollTo(0, 0);
                  }
                }
              });
            };

            scrollToTop();
            window.requestAnimationFrame(scrollToTop);
            window.setTimeout(scrollToTop, 100);
            window.setTimeout(scrollToTop, 300);
            </script>
            """,
            height=0,
        )


def character_data_uri(code):
    image_path = CHARACTER_DIR / f"{code}.png"
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def bullet_items_html(items):
    return "".join(f"<li>{html.escape(item)}</li>" for item in items)


def render_info_card(title, icon, items, style_name):
    st.markdown(
        f"""
        <div class="info-card {style_name}">
          <div class="info-card-head"><span class="info-card-icon">{icon}</span>{html.escape(title)}</div>
          <ul>{bullet_items_html(items)}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def restart():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    request_scroll_to_top()
    st.rerun()


def render_intro():
    question_count = len(QUESTIONS)
    estimated_minutes = max(1, round(question_count / 8))
    st.markdown(
        f"""
        <div class="hero">
          <div class="eyebrow">WORK STYLE DIAGNOSIS</div>
          <h1>あなたの仕事スタイル、<br><span class="gradient-word">4文字</span>で見つけよう。</h1>
          <p>いつもの判断や進め方には、あなたらしいパターンがあります。{question_count}の質問から強みや心地よい働き方を、16タイプで楽しく整理します。</p>
        </div>
        <div class="meta-row">
          <div class="meta-card"><strong>{question_count}問</strong><span>質問数</span></div>
          <div class="meta-card"><strong>約{estimated_minutes}分</strong><span>所要時間</span></div>
          <div class="meta-card"><strong>16タイプ</strong><span>診断結果</span></div>
        </div>
        <div class="axis-grid">
          <div class="axis-card"><div class="axis-head"><span class="axis-icon">🔎</span>判断の起点</div><div class="axis-poles"><b class="code-badge code-purple">R</b><span>現実重視</span><span class="arrow">↔</span><b class="code-badge code-pink">V</b><span>理想重視</span></div></div>
          <div class="axis-card"><div class="axis-head"><span class="axis-icon">🗺️</span>仕事の進め方</div><div class="axis-poles"><b class="code-badge code-mint">P</b><span>計画型</span><span class="arrow">↔</span><b class="code-badge code-yellow">F</b><span>柔軟型</span></div></div>
          <div class="axis-card"><div class="axis-head"><span class="axis-icon">🤝</span>周囲との関わり方</div><div class="axis-poles"><b class="code-badge code-purple">I</b><span>個人型</span><span class="arrow">↔</span><b class="code-badge code-pink">C</b><span>協働型</span></div></div>
          <div class="axis-card"><div class="axis-head"><span class="axis-icon">✨</span>価値の生み出し方</div><div class="axis-poles"><b class="code-badge code-mint">E</b><span>既存改善型</span><span class="arrow">↔</span><b class="code-badge code-yellow">N</b><span>新規開拓型</span></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("正解や優劣はありません。理想の自分ではなく、普段の行動に近いものを選んでください。")
    if st.button("診断を始める", type="primary", use_container_width=True):
        st.session_state.phase = "questions"
        request_scroll_to_top()
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
                f'<div class="question-card"><span class="q-number">Q{question["id"]}</span><span class="q-text">{html.escape(question["text"])}</span></div>',
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
                format_func=lambda value: str(value),
            )

        back_col, next_col = st.columns(2)
        back = back_col.form_submit_button("前のページ", use_container_width=True, disabled=page == 0)
        next_label = "回答を確定する" if page == TOTAL_PAGES - 1 else "次のページ"
        next_clicked = next_col.form_submit_button(next_label, type="primary", use_container_width=True)

    if back:
        save_visible_answers(page_questions, require_all=False)
        st.session_state.page -= 1
        request_scroll_to_top()
        st.rerun()

    if next_clicked:
        missing = save_visible_answers(page_questions, require_all=True)
        if missing:
            st.error("このページに未回答の質問があります。すべて回答してから進んでください。")
        elif page < TOTAL_PAGES - 1:
            st.session_state.page += 1
            request_scroll_to_top()
            st.rerun()
        else:
            scores = calculate_scores(QUESTIONS, st.session_state.answers, AXES)
            st.session_state.scores = scores
            st.session_state.tie_answers = infer_tie_answers(
                QUESTIONS,
                st.session_state.answers,
                AXES,
                scores,
            )
            st.session_state.phase = "result"
            request_scroll_to_top()
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


def render_axis_bar(axis_id, score):
    axis = AXES[axis_id]
    first, second = display_percentages(score)
    if score == 50.0:
        dominant_text = "2つの傾向が同じくらい"
    elif score > 50.0:
        dominant_text = f"{axis['first_label']}が優勢"
    else:
        dominant_text = f"{axis['second_label']}が優勢"
    st.markdown(
        f"""
        <div class="axis-result-card">
          <div class="axis-result-top">
            <div>
              <div class="axis-category">{html.escape(axis['title'])}</div>
              <div class="axis-dominant">{html.escape(dominant_text)}</div>
            </div>
            <span class="tendency-chip">{html.escape(tendency_label(score))}</span>
          </div>
          <div class="bar-labels">
            <span class="result-pole"><b class="mini-code">{html.escape(axis['first_code'])}</b>{html.escape(axis['first_label'])} {first}%</span>
            <span class="result-pole">{second}% {html.escape(axis['second_label'])}<b class="mini-code">{html.escape(axis['second_code'])}</b></span>
          </div>
          <div class="bar">
            <div class="bar-first" style="width:{first}%"></div>
            <div class="bar-second" style="width:{second}%"></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result():
    scores = st.session_state.scores
    code = build_type_code(scores, AXES, st.session_state.tie_answers)
    result = TYPES[code]
    image_uri = character_data_uri(code)

    st.markdown(
        f"""
        <div class="type-hero">
          <div class="type-visual"><img src="{image_uri}" alt="{html.escape(result['name'])}のキャラクター"></div>
          <div class="type-copy">
            <span class="type-code">YOUR TYPE&nbsp;&nbsp;{html.escape(code)}</span>
            <div class="type-kicker">あなたの仕事スタイルは</div>
            <h1>{html.escape(result['name'])}</h1>
            <p>{html.escape(result['summary'])}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="result-heading"><div class="eyebrow">YOUR BALANCE</div><h2>4つの仕事スタイル傾向</h2></div>',
        unsafe_allow_html=True,
    )
    for axis_id in AXES:
        render_axis_bar(axis_id, scores[axis_id])
    st.caption("傾向スコアは回答に基づく相対的な強さを示すもので、能力の優劣を表すものではありません。")

    st.markdown(
        '<div class="result-heading"><div class="eyebrow">WORKING WITH YOU</div><h2>仕事で表れやすい特徴</h2></div>',
        unsafe_allow_html=True,
    )
    left, right = st.columns(2)
    with left:
        render_info_card("強み", "✨", result["strengths"], "strength")
    with right:
        render_info_card("注意したいこと", "💡", result["cautions"], "caution")

    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
    role_col, environment_col = st.columns(2)
    with role_col:
        render_info_card("チームで担いやすい役割", "🧩", result["role"], "role")
    with environment_col:
        render_info_card("力を発揮しやすい環境", "🌱", result["environment"], "environment")

    st.info("この診断は自己理解を支援するオリジナルコンテンツであり、医学的・心理学的な診断ではありません。")
    st.button("もう一度診断する", on_click=restart, use_container_width=True)


initialize_state()
st.markdown('<div id="page-top-anchor"></div>', unsafe_allow_html=True)
scroll_to_top_if_requested()

if st.session_state.phase == "intro":
    render_intro()
elif st.session_state.phase == "questions":
    render_questionnaire()
else:
    render_result()
