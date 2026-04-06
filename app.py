import html
from datetime import datetime, timedelta

import streamlit as st

st.set_page_config(
    page_title="法智护航",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def now_text() -> str:
    beijing_time = datetime.utcnow() + timedelta(hours=8)
    return beijing_time.strftime("%H:%M")


st.markdown(
    """
    <style>
        :root {
            --bg-1: #f4f8fc;
            --bg-2: #eaf1f8;
            --line: rgba(148, 163, 184, 0.12);
            --card: rgba(255,255,255,0.82);
            --card-border: rgba(203, 213, 225, 0.72);
            --text-main: #0f172a;
            --text-sub: #5b6b82;
            --accent: #2f6df6;
            --accent-soft: rgba(47, 109, 246, 0.10);
            --shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
        }

        .stApp {
            background:
                radial-gradient(circle at 18px 18px, var(--line) 1.4px, transparent 1.7px),
                linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 100%);
            background-size: 36px 36px, cover;
        }

        header[data-testid="stHeader"] {
            background: rgba(255,255,255,0.38);
        }

        div[data-testid="stDecoration"] {
            display: none;
        }

        .main .block-container {
            max-width: 1380px;
            padding-top: 0.55rem;
            padding-bottom: 0.8rem;
        }

        .brand-card {
            background: var(--card);
            border: 1px solid var(--card-border);
            border-radius: 28px;
            padding: 26px 24px;
            box-shadow: var(--shadow);
            backdrop-filter: blur(12px);
        }

        .brand-title {
            font-size: 2.15rem;
            font-weight: 800;
            color: var(--text-main);
            margin-bottom: 0.45rem;
            letter-spacing: -0.5px;
        }

        .brand-subtitle {
            font-size: 1rem;
            line-height: 1.9;
            color: var(--text-sub);
        }

        .news-panel {
            margin-top: 16px;
            min-height: 70vh;
            background: linear-gradient(160deg, #d9e8ff 0%, #c8ddff 52%, #b6d2ff 100%);
            border: 1px solid rgba(133, 164, 214, 0.24);
            border-radius: 32px;
            padding: 28px 24px;
            box-shadow: var(--shadow);
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .news-panel:before,
        .news-panel:after {
            content: "";
            position: absolute;
            border-radius: 999px;
            background: rgba(255,255,255,0.22);
            filter: blur(4px);
        }

        .news-panel:before {
            width: 220px;
            height: 220px;
            top: -60px;
            right: -30px;
        }

        .news-panel:after {
            width: 180px;
            height: 180px;
            bottom: -50px;
            left: -40px;
        }

        .news-text {
            position: relative;
            z-index: 1;
            font-size: 3.2rem;
            line-height: 1.18;
            font-weight: 800;
            color: #17305c;
            letter-spacing: 0.5px;
        }

        .panel-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 12px;
            max-width: 860px;
        }

        .panel-title {
            font-size: 1.38rem;
            font-weight: 800;
            color: var(--text-main);
            letter-spacing: -0.3px;
        }

        .mode-badge {
            display: inline-flex;
            align-items: center;
            padding: 8px 14px;
            border-radius: 999px;
            background: var(--accent-soft);
            color: var(--accent);
            border: 1px solid rgba(47, 109, 246, 0.16);
            font-size: 0.92rem;
            font-weight: 700;
            white-space: nowrap;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 24px !important;
            border: 1px solid rgba(203, 213, 225, 0.78) !important;
            background: rgba(255,255,255,0.72) !important;
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.05) !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            padding: 12px 14px !important;
        }

        div[data-testid="stChatMessage"] {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            margin: 0 0 12px 0 !important;
        }

        div[data-testid="stChatMessageAvatar"] {
            display: none !important;
        }

        div[data-testid="stChatMessageContent"] {
            width: 100%;
            max-width: 100%;
            padding: 0 !important;
        }

        .msg-row {
            display: flex;
            width: 100%;
        }

        .msg-row.user {
            justify-content: flex-end;
        }

        .msg-row.assistant {
            justify-content: flex-start;
        }

        .msg-bubble {
            max-width: 88%;
            border-radius: 20px;
            padding: 14px 16px;
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.05);
            line-height: 1.76;
            font-size: 0.97rem;
            word-break: break-word;
            white-space: normal;
        }

        .msg-bubble.user {
            background: linear-gradient(135deg, #2f6df6 0%, #58a6ff 100%);
            color: #ffffff;
            border-bottom-right-radius: 8px;
        }

        .msg-bubble.assistant {
            background: rgba(255,255,255,0.96);
            border: 1px solid rgba(203, 213, 225, 0.72);
            color: var(--text-main);
            border-bottom-left-radius: 8px;
        }

        .msg-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            margin-bottom: 7px;
            font-size: 0.8rem;
        }

        .msg-name {
            font-weight: 700;
        }

        .msg-time {
            font-size: 0.76rem;
            white-space: nowrap;
        }

        .assistant .msg-time {
            color: var(--text-sub);
            opacity: 0.78;
        }

        .user .msg-time {
            color: rgba(255,255,255,0.9);
            opacity: 0.95;
        }

        .typing-dots {
            display: inline-flex;
            gap: 6px;
            align-items: center;
            padding: 4px 0 2px 0;
        }

        .typing-dots span {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #94a3b8;
            display: inline-block;
            animation: blink 1.2s infinite ease-in-out;
        }

        .typing-dots span:nth-child(2) {
            animation-delay: 0.2s;
        }

        .typing-dots span:nth-child(3) {
            animation-delay: 0.4s;
        }

        @keyframes blink {
            0%, 80%, 100% {
                opacity: 0.28;
                transform: translateY(0);
            }
            40% {
                opacity: 1;
                transform: translateY(-2px);
            }
        }

        .func-wrap {
            max-width: 860px;
            margin-bottom: 14px;
        }

        div[data-testid="stButton"] button {
            width: 100%;
            border-radius: 16px;
            border: 1px solid rgba(47, 109, 246, 0.10);
            background: linear-gradient(135deg, #ffffff 0%, #edf4ff 100%);
            color: var(--text-main);
            font-weight: 700;
            padding-top: 0.72rem;
            padding-bottom: 0.72rem;
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.05);
            transition: all 0.18s ease;
        }

        div[data-testid="stButton"] button:hover {
            transform: translateY(-1px);
            border-color: rgba(47, 109, 246, 0.24);
            background: linear-gradient(135deg, #f8fbff 0%, #e4efff 100%);
            color: var(--accent);
        }

        .input-shell {
            max-width: 860px;
            background: linear-gradient(145deg, #f6faff 0%, #eef5ff 100%);
            border: 1px solid rgba(203, 213, 225, 0.72);
            border-radius: 26px;
            padding: 16px;
            box-shadow: 0 12px 28px rgba(15, 23, 42, 0.06);
        }

        .input-title {
            font-size: 1.08rem;
            font-weight: 800;
            color: var(--text-main);
            margin-bottom: 8px;
            text-align: center;
        }

        .input-tip {
            font-size: 0.88rem;
            color: var(--text-sub);
            margin-bottom: 8px;
            text-align: center;
            line-height: 1.7;
        }

        .input-shell div[data-testid="stTextArea"] textarea {
            background: rgba(255,255,255,0.98) !important;
            border: 1px solid rgba(203, 213, 225, 0.65) !important;
            border-radius: 18px !important;
            min-height: 98px !important;
            color: var(--text-main) !important;
            padding-top: 14px !important;
            font-size: 0.98rem !important;
        }

        .input-shell div[data-testid="stTextArea"] textarea:focus {
            border-color: rgba(47, 109, 246, 0.35) !important;
            box-shadow: 0 0 0 3px rgba(47, 109, 246, 0.08) !important;
        }

        .input-shell div[data-testid="stTextArea"] label {
            display: none !important;
        }

        .send-row div[data-testid="stButton"] button {
            background: linear-gradient(135deg, #2f6df6 0%, #58a6ff 100%);
            color: white;
            border: none;
            border-radius: 16px;
            box-shadow: 0 12px 22px rgba(47, 109, 246, 0.22);
        }

        .send-row div[data-testid="stButton"] button:hover {
            color: white;
            background: linear-gradient(135deg, #2a63de 0%, #4b98ee 100%);
        }

        @media (max-width: 1100px) {
            .news-text {
                font-size: 2.45rem;
            }

            .panel-head {
                flex-direction: column;
                align-items: flex-start;
            }

            .func-wrap,
            .input-shell,
            .panel-head {
                max-width: 100%;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

MODE_CONFIG = {
    "法律咨询": {
        "reply": "已收到您的法律咨询问题。当前将按普通法律咨询流程处理，后续这里可直接接入法律咨询类 API，为您提供劳动纠纷、证据准备、维权路径、仲裁流程等智能咨询服务。",
    },
    "文书生成": {
        "reply": "已收到您的文书生成需求。后续这里将接入文书生成相关 API，根据案件信息生成对应法律文书。",
    },
    "文书审查": {
        "reply": "已收到您的文书审查需求。后续这里将接入文书审查相关 API，对文本进行风险检查并输出修改建议。",
    },
    "合同生成": {
        "reply": "已收到您的合同生成需求。后续这里将接入合同生成相关 API，结合具体用工场景生成合同文本。",
    },
}

if "active_mode" not in st.session_state:
    st.session_state.active_mode = "法律咨询"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "label": "法智护航",
            "content": "您好，欢迎使用法智护航。未选择下方专项功能时，系统将默认按照普通法律咨询流程处理；选择专项功能后，再进入对应服务流程。",
            "time": now_text(),
        }
    ]

if "is_typing" not in st.session_state:
    st.session_state.is_typing = False


def trim_messages() -> None:
    if len(st.session_state.messages) > 12:
        st.session_state.messages = [st.session_state.messages[0]] + st.session_state.messages[-11:]


def switch_mode(mode: str) -> None:
    st.session_state.active_mode = mode
    mode_hint = {
        "文书生成": "已切换到文书生成模式。",
        "文书审查": "已切换到文书审查模式。",
        "合同生成": "已切换到合同生成模式。",
    }[mode]
    st.session_state.messages.append(
        {
            "role": "assistant",
            "label": "法智护航",
            "content": mode_hint + MODE_CONFIG[mode]["reply"],
            "time": now_text(),
        }
    )
    trim_messages()


def send_message() -> None:
    content = st.session_state.get("user_input", "").strip()
    if not content:
        return

    st.session_state.messages.append(
        {
            "role": "user",
            "label": "用户",
            "content": content,
            "time": now_text(),
        }
    )

    st.session_state.is_typing = True
    st.session_state.messages.append(
        {
            "role": "assistant",
            "label": "法智护航",
            "content": MODE_CONFIG[st.session_state.active_mode]["reply"],
            "time": now_text(),
        }
    )
    trim_messages()
    st.session_state.user_input = ""
    st.session_state.is_typing = False


left_col, right_col = st.columns([0.92, 1.45], gap="large")

with left_col:
    st.markdown(
        """
        <div class="brand-card">
            <div class="brand-title">法智护航</div>
            <div class="brand-subtitle">
                面向劳动法的多功能多智能体法律咨询平台。左侧区域预留给后续新闻资讯、热点案例、政策更新和内容丰富页面展示。
            </div>
        </div>
        <div class="news-panel">
            <div class="news-text">相关资讯<br>与内容丰<br>富页面</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_col:
    st.markdown(
        f"""
        <div class="panel-head">
            <div class="panel-title">智能法律服务台</div>
            <div class="mode-badge">当前模式：{st.session_state.active_mode}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(height=420, border=True):
        for msg in st.session_state.messages:
            role = "user" if msg["role"] == "user" else "assistant"
            with st.chat_message(role):
                safe_label = html.escape(msg.get("label", "消息"))
                safe_time = html.escape(msg.get("time", "刚刚"))
                safe_content = html.escape(msg["content"]).replace("\n", "<br>")
                st.markdown(
                    f"""
                    <div class="msg-row {role}">
                        <div class="msg-bubble {role}">
                            <div class="msg-meta">
                                <span class="msg-name">{safe_label}</span>
                                <span class="msg-time">{safe_time}</span>
                            </div>
                            <div>{safe_content}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        if st.session_state.is_typing:
            with st.chat_message("assistant"):
                st.markdown(
                    """
                    <div class="msg-row assistant">
                        <div class="msg-bubble assistant">
                            <div class="msg-meta">
                                <span class="msg-name">法智护航</span>
                                <span class="msg-time">输入中</span>
                            </div>
                            <div class="typing-dots"><span></span><span></span><span></span></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown('<div class="func-wrap">', unsafe_allow_html=True)
    btn1, btn2, btn3 = st.columns(3)

    with btn1:
        if st.button("文书生成", use_container_width=True):
            switch_mode("文书生成")
            st.rerun()

    with btn2:
        if st.button("文书审查", use_container_width=True):
            switch_mode("文书审查")
            st.rerun()

    with btn3:
        if st.button("合同生成", use_container_width=True):
            switch_mode("合同生成")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-shell">', unsafe_allow_html=True)
    st.markdown('<div class="input-title">文字输入</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="input-tip">未选择专项功能时，将直接按普通法律咨询流程处理；选择按钮后则进入对应专项服务。</div>',
        unsafe_allow_html=True,
    )
    st.text_area(
        "文字输入",
        key="user_input",
        label_visibility="collapsed",
        placeholder="请输入您的法律咨询问题、案件描述、文书内容或合同需求...",
        height=110,
    )
    st.markdown('<div class="send-row">', unsafe_allow_html=True)
    st.button("发送", use_container_width=True, on_click=send_message)
    st.markdown('</div></div>', unsafe_allow_html=True)
