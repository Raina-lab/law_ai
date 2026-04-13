import html
import base64
from pathlib import Path
from datetime import datetime, timedelta

import requests
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


def load_avatar_base64(image_path: str = "assistant_avatar.jpg") -> str:
    path = Path(image_path)
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode("utf-8")
    return ""


def read_uploaded_files(files) -> str:
    if not files:
        return ""

    parts = []
    for file in files:
        try:
            suffix = Path(file.name).suffix.lower()
            if suffix in [".txt", ".md", ".csv", ".json", ".py"]:
                text = file.read().decode("utf-8", errors="ignore").strip()
                if text:
                    preview = text[:4000]
                    parts.append(f"文件名：{file.name}\n文件内容：\n{preview}")
                else:
                    parts.append(f"文件名：{file.name}\n文件内容为空。")
            else:
                parts.append(f"已上传文件：{file.name}（当前版本暂不自动解析该格式内容，可结合文件名和用户描述进行处理）")
        except Exception:
            parts.append(f"已上传文件：{file.name}（读取失败，请结合用户描述处理）")

    return "\n\n".join(parts)


ASSISTANT_AVATAR_BASE64 = load_avatar_base64()
def load_image_base64(path: str) -> str:
    p = Path(path)
    return base64.b64encode(p.read_bytes()).decode("utf-8") if p.exists() else ""

PAGE_BG_BASE64 = load_image_base64("background1.jpg")
NEWS_BG_BASE64 = load_image_base64("background2.jpg")

APP_KEY = st.secrets["APP_kEY"]
APP_ID = st.secrets["APP_ID"]
YUANQI_URL = "https://yuanqi.tencent.com/openapi/v1/agent/chat/completions"

NEWS_CONTENT = [
    {
        "section": "新业态劳动关系认定（穿透“伪装”）",
        "items": [
            {
                "title": "外卖骑手注册“个体户”仍被认定劳动关系（最高法指导案例）",
                "body": "江苏某公司要求外卖骑手注册为个体工商户，并以合作名义规避用工责任。法院穿透形式审查实质，认定公司通过派单、考勤、罚款实施劳动管理，双方存在劳动关系，公司需承担工伤保险责任。",
            },
            {
                "title": "济南网约取件员劳动关系确认案",
                "body": "公司以“合作”名义拖欠工资，但因对劳动者存在监督、提成扣减等管理，法院认定其属于企业业务组成部分，双方存在劳动关系。",
            },
            {
                "title": "网络主播案（成都案例）",
                "body": "尽管双方签署《直播合作协议》，但主播实际上接受公司对直播内容、直播时段的严格管理，并按月领取固定底薪，最终被认定存在劳动关系。",
            },
            {
                "title": "北京怀柔：算法管理 = 用工主体责任",
                "body": "平台通过算法实施强制派单、收入控制等管理行为，法院认定平台与外包公司承担连带责任。",
            },
            {
                "title": "上海一中院：严惩“恶意封号”",
                "body": "根据晨会、罚款、群管理等事实认定劳动关系，公司以“拒单一次”为由封号解约，被认定违法解除。",
            },
        ],
    },
    {
        "section": "恶意欠薪与刑事追责",
        "items": [
            {
                "title": "临沂兰山“拒不支付劳动报酬罪”系列案",
                "body": "多家企业在收到支付通知后仍逃匿失联、恶意拖欠工资，相关责任人被刑拘并上网追逃。",
            },
            {
                "title": "77名船员近千万工资“一站式”调解",
                "body": "通过“水上解纷”协同机制，项目方与船东最终结清全部欠薪，成为典型案例。",
            },
        ],
    },
    {
        "section": "企业规章制度的合法性边界",
        "items": [
            {
                "title": "江苏南京：普通厨师“无密可保”案",
                "body": "普通厨师未接触商业秘密，竞业限制协议被认定无效，明确“无密可保”不应限制劳动者择业。",
            },
            {
                "title": "推拿师李某案（最高法典型案例）",
                "body": "客户资料、基础报价属于一般经营信息，不属于法定保密义务对象，竞业限制不生效。",
            },
            {
                "title": "高管配偶代持股案",
                "body": "通过亲属设立竞争公司规避竞业限制，仍被认定为违约，需承担违约责任。",
            },
            {
                "title": "济南汽车公司“期票扣款”案",
                "body": "员工因个人原因离职即扣除“期票账户”余额，法院认定属于变相克扣劳动报酬，条款无效。",
            },
            {
                "title": "章丘法院“负激励”无效案",
                "body": "公司以“负激励”为名对交通事故责任人扣款，法院认定实质为罚款，缺乏法律依据。",
            },
        ],
    },
    {
        "section": "高管维权与用工“把戏”揭露",
        "items": [
            {
                "title": "人事高管索要二倍工资被驳回",
                "body": "负责人事工作的高管未与自己签订劳动合同，法院认为其自身对合同签署负有管理职责，不支持双倍工资请求。",
            },
            {
                "title": "“1元卖公司”恶意逃债被撤销",
                "body": "股东以1元价格将股权转让给“职业背债人”企图逃避欠薪责任，法院认定恶意串通并撤销变更。",
            },
        ],
    },
    {
        "section": "社保与特殊保护：刚性底线不可破",
        "items": [
            {
                "title": "孕期调岗降薪违法",
                "body": "用人单位不得以“照顾”为名，对孕期女职工变相降薪；调整岗位导致待遇下降的，属于违法行为。",
            },
            {
                "title": "“自愿放弃社保”无效",
                "body": "即使企业以“社保补助”形式发钱并约定不参保，该约定仍属无效，用人单位仍需承担相应责任。",
            },
            {
                "title": "天津：新业态职业伤害保障试点",
                "body": "即使不认定传统劳动关系，平台仍需按试点规则承担职业伤害保障待遇。",
            },
        ],
    },
]

st.markdown(
    """
    <style>
        :root
             html {
                color-scheme: light !important;
            }

            body, .stApp {
                color-scheme: light !important;
            }

            [data-testid="stAppViewContainer"] {
                color: #0f172a !important;
            }

            .panel-title,
            .news-heading-inline,
            .news-section-inline,
            .news-item-title-inline,
            .input-title,
            .brand-title,
            .brand-kicker,
            .markdown-bubble h1,
            .markdown-bubble h2,
            .markdown-bubble h3,
            .markdown-bubble h4,
            .markdown-bubble h5,
            .markdown-bubble h6,
            .markdown-bubble p,
            .markdown-bubble li,
            .markdown-bubble strong {
                color: #0f172a !important;
            }

            .brand-subtitle,
            .news-body-inline,
            .input-tip,
            .upload-title,
            .msg-time,
            .assistant .msg-time {
                color: #475569 !important;
            }

            .msg-bubble.assistant,
            .news-item-inline,
            .input-shell,
            .brand-card {
                background: rgba(255,255,255,0.88) !important;
                color: #0f172a !important;
                border-color: rgba(203, 213, 225, 0.75) !important;
            }
            {
            --bg-1: #f5f8fc;
            --bg-2: #edf3fa;
            --line: rgba(148, 163, 184, 0.11);
            --card: rgba(255,255,255,0.84);
            --card-border: rgba(203, 213, 225, 0.72);
            --text-main: #0f172a;
            --text-sub: #64748b;
            --text-soft: #475569;
            --accent: #2563eb;
            --accent-soft: rgba(37, 99, 235, 0.10);
            --shadow-lg: 0 18px 40px rgba(15, 23, 42, 0.08);
            --shadow-md: 0 10px 24px rgba(15, 23, 42, 0.06);
        }

        html, body, .stApp {
            background: transparent !important;
        }

        [data-testid="stAppViewContainer"] {
            background:
                linear-gradient(rgba(255,255,255,0.65), rgba(255,255,255,0.75)),
                url("data:image/jpeg;base64,__PAGE_BG__") center/cover fixed;
        }

        .main {
            background: transparent !important;
            min-height: 100vh;
        }

        .news-wrap {
            max-width: 100%;
            background: rgba(255,255,255,0.65);
            border-radius: 22px;
            padding: 16px 14px 20px 14px;
            min-height: 100%;
            backdrop-filter: blur(10px);
        }   

        header[data-testid="stHeader"] {
            background: rgba(255,255,255,0.35);
        }

        div[data-testid="stDecoration"] {
            display: none;
        }

        .main .block-container {
            background: transparent !important;
            max-width: 1380px;
            padding-top: 0.5rem;
            padding-bottom: 0.9rem;
        }

        .brand-card {
            position: relative;
            overflow: hidden;
            background:
                linear-gradient(135deg, rgba(255,255,255,0.97) 0%, rgba(244,248,255,0.94) 52%, rgba(232,242,255,0.92) 100%);
            border: 1px solid rgba(203, 213, 225, 0.66);
            border-radius: 34px;
            padding: 34px 30px 30px 30px;
            box-shadow:
                0 24px 56px rgba(15, 23, 42, 0.08),
                inset 0 1px 0 rgba(255,255,255,0.8);
            backdrop-filter: blur(18px);
        }

        .brand-card::before {
            content: "";
            position: absolute;
            width: 220px;
            height: 220px;
            right: -70px;
            top: -90px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(37, 99, 235, 0.14) 0%, rgba(37, 99, 235, 0.03) 58%, transparent 74%);
        }

        .brand-card::after {
            content: "";
            position: absolute;
            left: -40px;
            bottom: -55px;
            width: 180px;
            height: 180px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(96, 165, 250, 0.10) 0%, rgba(96, 165, 250, 0.02) 60%, transparent 76%);
        }

        .brand-kicker {
            position: relative;
            z-index: 1;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            margin-bottom: 14px;
            border-radius: 999px;
            background: rgba(37, 99, 235, 0.08);
            border: 1px solid rgba(37, 99, 235, 0.12);
            color: #2563eb;
            font-size: 0.84rem;
            font-weight: 700;
            letter-spacing: 0.2px;
        }

        .brand-title {
            position: relative;
            z-index: 1;
            font-size: 2.5rem;
            line-height: 1.08;
            font-weight: 900;
            color: #0f172a;
            margin-bottom: 0.9rem;
            letter-spacing: -1px;
        }

        .brand-subtitle {
            position: relative;
            z-index: 1;
            font-size: 1.02rem;
            line-height: 1.95;
            color: #64748b;
            max-width: 92%;
        }

        .brand-highlight {
            color: #2563eb;
            font-weight: 800;
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
            font-size: 1.42rem;
            font-weight: 850;
            color: var(--text-main);
            letter-spacing: -0.4px;
        }

        .mode-badge {
            display: inline-flex;
            align-items: center;
            padding: 8px 14px;
            border-radius: 999px;
            background: linear-gradient(180deg, rgba(255,255,255,0.85) 0%, rgba(37, 99, 235, 0.08) 100%);
            color: var(--accent);
            border: 1px solid rgba(37, 99, 235, 0.16);
            font-size: 0.92rem;
            font-weight: 700;
            white-space: nowrap;
            box-shadow: 0 6px 14px rgba(37, 99, 235, 0.08);
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 26px !important;
            border: 1px solid rgba(203, 213, 225, 0.78) !important;
            background: linear-gradient(180deg, rgba(255,255,255,0.84) 0%, rgba(255,255,255,0.76) 100%) !important;
            box-shadow: var(--shadow-md) !important;
            backdrop-filter: blur(12px) !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            padding: 14px 16px !important;
        }

        div[data-testid="stChatMessage"] {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            margin: 0 0 14px 0 !important;
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

        .assistant-wrap {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            width: 100%;
        }

        .assistant-avatar {
            width: 44px;
            height: 44px;
            min-width: 44px;
            border-radius: 50%;
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            box-shadow: 0 6px 16px rgba(15, 23, 42, 0.15);
            border: 2px solid rgba(255,255,255,0.92);
            margin-top: 2px;
        }

        .assistant-avatar.fallback {
            background: linear-gradient(135deg, #64748b 0%, #94a3b8 100%);
        }

        .msg-bubble {
            max-width: 88%;
            border-radius: 20px;
            padding: 14px 16px;
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.05);
            line-height: 1.78;
            font-size: 0.97rem;
            word-break: break-word;
            white-space: normal;
        }

        .msg-bubble.user {
            background: linear-gradient(135deg, #2563eb 0%, #60a5fa 100%);
            color: #ffffff;
            border-bottom-right-radius: 8px;
        }

        .msg-bubble.assistant {
            background: linear-gradient(180deg, rgba(255,255,255,0.98) 0%, rgba(248,250,252,0.96) 100%);
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
            font-weight: 800;
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
            color: rgba(255,255,255,0.92);
            opacity: 0.95;
        }

        .markdown-bubble h1,
        .markdown-bubble h2,
        .markdown-bubble h3,
        .markdown-bubble h4,
        .markdown-bubble h5,
        .markdown-bubble h6 {
            color: #0f172a;
            margin-top: 0.35rem;
            margin-bottom: 0.55rem;
            line-height: 1.45;
        }

        .markdown-bubble p {
            margin-bottom: 0.6rem;
            color: #0f172a;
        }

        .markdown-bubble ul,
        .markdown-bubble ol {
            padding-left: 1.2rem;
            margin-bottom: 0.6rem;
        }

        .markdown-bubble li {
            margin-bottom: 0.25rem;
            color: #0f172a;
        }

        .markdown-bubble strong {
            font-weight: 800;
            color: #0f172a;
        }

        .markdown-bubble code {
            background: rgba(148, 163, 184, 0.12);
            padding: 2px 6px;
            border-radius: 6px;
            font-size: 0.9em;
        }

        .markdown-bubble pre {
            background: #f8fafc;
            border: 1px solid rgba(203, 213, 225, 0.8);
            border-radius: 12px;
            padding: 12px;
            overflow-x: auto;
        }

        .markdown-bubble blockquote {
            border-left: 3px solid rgba(37, 99, 235, 0.35);
            padding-left: 10px;
            color: #475569;
            margin: 0.6rem 0;
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
            border-radius: 18px;
            border: 1px solid rgba(37, 99, 235, 0.10);
            background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(238,246,255,0.95) 100%);
            color: var(--text-main);
            font-weight: 800;
            padding-top: 0.76rem;
            padding-bottom: 0.76rem;
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.05);
            transition: all 0.18s ease;
        }

        div[data-testid="stButton"] button:hover {
            transform: translateY(-1px);
            border-color: rgba(37, 99, 235, 0.22);
            background: linear-gradient(180deg, #ffffff 0%, #eaf3ff 100%);
            color: var(--accent);
        }

        .input-shell {
            max-width: 860px;
            background: linear-gradient(180deg, rgba(255,255,255,0.92) 0%, rgba(241,247,255,0.92) 100%);
            border: 1px solid rgba(203, 213, 225, 0.72);
            border-radius: 28px;
            padding: 16px;
            box-shadow: 0 12px 28px rgba(15, 23, 42, 0.06);
            backdrop-filter: blur(10px);
        }

        .input-title {
            font-size: 1.08rem;
            font-weight: 850;
            color: var(--text-main);
            margin-bottom: 8px;
            text-align: center;
        }

        .input-tip {
            font-size: 0.88rem;
            color: var(--text-sub);
            margin-bottom: 10px;
            text-align: center;
            line-height: 1.7;
        }

        .upload-title {
            font-size: 0.88rem;
            font-weight: 700;
            color: var(--text-sub);
            margin: 10px 0 8px 2px;
        }

        .input-shell div[data-testid="stTextArea"] textarea {
            background: rgba(255,255,255,0.98) !important;
            border: 1px solid rgba(203, 213, 225, 0.65) !important;
            border-radius: 18px !important;
            min-height: 98px !important;
            color: var(--text-main) !important;
            padding-top: 14px !important;
            font-size: 0.98rem !important;
            box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.02) !important;
        }

        .input-shell div[data-testid="stTextArea"] textarea:focus {
            border-color: rgba(37, 99, 235, 0.35) !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.08) !important;
        }

        .input-shell div[data-testid="stTextArea"] label {
            display: none !important;
        }

        .input-shell div[data-testid="stFileUploader"] {
            background: rgba(255,255,255,0.72);
            border-radius: 18px;
            padding: 8px 10px;
            border: 1px dashed rgba(148, 163, 184, 0.35);
        }

        .send-row div[data-testid="stButton"] button {
            background: linear-gradient(135deg, #2563eb 0%, #60a5fa 100%);
            color: white;
            border: none;
            border-radius: 18px;
            box-shadow: 0 14px 26px rgba(37, 99, 235, 0.24);
        }

        .send-row div[data-testid="stButton"] button:hover {
            color: white;
            background: linear-gradient(135deg, #1d4ed8 0%, #4f9cf5 100%);
        }

        .news-wrap {
            max-width: 100%;
            border-radius: 22px;
        }

        .news-heading-inline {
            font-size: 1.18rem;
            font-weight: 850;
            color: var(--text-main);
            margin-bottom: 10px;
            letter-spacing: -0.2px;
        }

        .news-section-inline {
            font-size: 0.98rem;
            font-weight: 850;
            color: #17305c;
            margin: 16px 0 10px 0;
            padding-left: 10px;
            border-left: 3px solid rgba(37, 99, 235, 0.28);
        }

        .news-item-inline {
            padding: 12px 12px 12px 14px;
            margin-bottom: 12px;
            border: 1px solid rgba(255,255,255,0.35);
            border-radius: 18px;
            background: rgba(255,255,255,0.65);
            backdrop-filter: blur(8px);
            box-shadow: 0 6px 14px rgba(15, 23, 42, 0.08);
        }

        .news-item-title-inline {
            font-weight: 780;
            color: #0f172a;
            margin-bottom: 6px;
            line-height: 1.6;
        }

        .news-body-inline {
            color: #475569;
            line-height: 1.78;
            font-size: 0.93rem;
        }

        .news-wrap::before {
            display: none !important;
        }


        @media (max-width: 1100px) {
            .panel-head {
                flex-direction: column;
                align-items: flex-start;
            }

            .func-wrap,
            .input-shell,
            .panel-head {
                max-width: 100%;
            }

            .brand-subtitle {
                max-width: 100%;
            }
        }

        footer {
            display: none !important;
        }
    </style>
    """.replace("__PAGE_BG__", PAGE_BG_BASE64).replace("__NEWS_BG__", NEWS_BG_BASE64),
    unsafe_allow_html=True,
)

MODE_CONFIG = {
    "法律咨询": {"mode_desc": "普通法律咨询"},
    "文书生成": {"mode_desc": "文书生成"},
    "文书审查": {"mode_desc": "文书审查"},
    "合同生成": {"mode_desc": "合同生成"},
}

if "active_mode" not in st.session_state:
    st.session_state.active_mode = "法律咨询"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "label": "法智护航",
            "content": """您好，欢迎使用法智护航。未选择下方专项功能时，系统将默认按照普通法律咨询流程处理；选择专项功能后，再进入对应服务流程。

示例问题：
1. 工作3年2个月，月薪1万5，被裁该赔多少？
2. N还是2N？具体怎么算？
3. 公司拖欠工资 / 不缴社保？""",
            "time": now_text(),
        }
    ]

if "is_typing" not in st.session_state:
    st.session_state.is_typing = False


def trim_messages() -> None:
    if len(st.session_state.messages) > 12:
        st.session_state.messages = [st.session_state.messages[0]] + st.session_state.messages[-11:]


def call_yuanqi_api(mode: str, prompt: str) -> str:
    final_prompt = f"""当前服务模式：{mode}

请严格按照当前模式处理用户请求。
如果当前模式是法律咨询，请进行法律分析和维权建议；
如果当前模式是文书生成，请生成对应法律文书；
如果当前模式是文书审查，请进行审查并提出修改意见；
如果当前模式是合同生成，请输出合同文本草案。

请使用清晰、自然、适合网页展示的 Markdown 格式输出，避免输出多余代码符号说明。

用户输入：
{prompt}
"""

    try:
        res = requests.post(
            YUANQI_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {APP_KEY}",
            },
            json={
                "assistant_id": APP_ID,
                "user_id": "law_ai_user",
                "stream": False,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": final_prompt,
                            }
                        ],
                    }
                ],
            },
            timeout=60,
        )

        data = res.json()

        if res.status_code != 200:
            return f"请求出错：{res.status_code} - {data}"

        return data.get("choices", [{}])[0].get("message", {}).get("content", "未获取到回复")

    except requests.exceptions.RequestException as e:
        return f"请求出错：{str(e)}"
    except Exception as e:
        return f"结果解析失败：{str(e)}"


def switch_mode(mode: str) -> None:
    st.session_state.active_mode = mode
    st.session_state.messages.append(
        {
            "role": "assistant",
            "label": "法智护航",
            "content": f"已切换到{MODE_CONFIG[mode]['mode_desc']}模式，请继续输入您的需求。",
            "time": now_text(),
        }
    )
    trim_messages()


def send_message() -> None:
    content = st.session_state.get("user_input", "").strip()
    files = st.session_state.get("uploaded_files", [])

    if not content and not files:
        return

    file_text = read_uploaded_files(files)
    user_display = content if content else "已上传文件，请结合附件内容处理。"

    if file_text:
        if content:
            api_input = f"{content}\n\n【用户上传文件】\n{file_text}"
        else:
            api_input = f"请结合以下上传文件内容进行处理：\n\n{file_text}"
    else:
        api_input = content

    st.session_state.messages.append(
        {
            "role": "user",
            "label": "用户",
            "content": user_display,
            "time": now_text(),
        }
    )

    if files:
        uploaded_names = "\n".join([f"- {f.name}" for f in files])
        st.session_state.messages.append(
            {
                "role": "assistant",
                "label": "系统附件",
                "content": f"已接收以下文件：\n{uploaded_names}",
                "time": now_text(),
            }
        )

    st.session_state.is_typing = True
    reply = call_yuanqi_api(st.session_state.active_mode, api_input)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "label": "法智护航",
            "content": reply,
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
            <div class="brand-kicker">劳动法智能服务平台</div>
            <div class="brand-title">法智护航</div>
            <div class="brand-subtitle">
                聚焦<span class="brand-highlight">劳动关系认定</span>、
                <span class="brand-highlight">欠薪追责</span>、
                <span class="brand-highlight">竞业限制</span>与
                <span class="brand-highlight">社保保障</span>等劳动法热点，
                左侧栏目实时汇集典型案例、裁判规则与维权指引。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(height=600, border=True):

        st.markdown(
            '<div class="news-wrap"><div class="news-heading-inline">新闻速递</div>',
            unsafe_allow_html=True,
        )

        for section in NEWS_CONTENT:
            st.markdown(
                f'<div class="news-section-inline">{html.escape(section["section"])}</div>',
                unsafe_allow_html=True,
            )

            for item in section["items"]:
                body_html = html.escape(item["body"]).replace("\n", "<br>")

                st.markdown(
                    f"""
                    <div class="news-item-inline">
                        <div class="news-item-title-inline">{html.escape(item["title"])}</div>
                        <div class="news-body-inline">{body_html}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    with st.container(height=1800, border=False):
        st.markdown(
            f"""
            <div class="panel-head">
                <div class="panel-title">开封府劳动仲裁官</div>
                <div class="mode-badge">当前模式：{st.session_state.active_mode}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(height=400, border=True):
            for msg in st.session_state.messages:
                role = "user" if msg["role"] == "user" else "assistant"
                safe_label = html.escape(msg.get("label", "消息"))
                safe_time = html.escape(msg.get("time", "刚刚"))

                if role == "user":
                    safe_content = html.escape(msg["content"]).replace("\n", "<br>")
                    with st.chat_message(role):
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
                else:
                    avatar_class = "assistant-avatar"
                    avatar_style = ""
                    if ASSISTANT_AVATAR_BASE64:
                        avatar_style = f"background-image:url('data:image/jpeg;base64,{ASSISTANT_AVATAR_BASE64}');"
                    else:
                        avatar_class += " fallback"

                    st.markdown(
                        f"""
                        <div class="msg-row assistant">
                            <div class="assistant-wrap">
                                <div class="{avatar_class}" style="{avatar_style}"></div>
                                <div class="msg-bubble assistant markdown-bubble">
                                    <div class="msg-meta">
                                        <span class="msg-name">{safe_label}</span>
                                        <span class="msg-time">{safe_time}</span>
                                    </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown(msg["content"])

                    st.markdown(
                        """
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            if st.session_state.is_typing:
                avatar_class = "assistant-avatar"
                avatar_style = ""
                if ASSISTANT_AVATAR_BASE64:
                    avatar_style = f"background-image:url('data:image/jpeg;base64,{ASSISTANT_AVATAR_BASE64}');"
                else:
                    avatar_class += " fallback"

                st.markdown(
                    f"""
                    <div class="msg-row assistant">
                        <div class="assistant-wrap">
                            <div class="{avatar_class}" style="{avatar_style}"></div>
                            <div class="msg-bubble assistant markdown-bubble">
                                <div class="msg-meta">
                                    <span class="msg-name">法智护航</span>
                                    <span class="msg-time">输入中</span>
                                </div>
                                <div class="typing-dots"><span></span><span></span><span></span></div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown('<div class="func-wrap">', unsafe_allow_html=True)
        btn0, btn1, btn2, btn3 = st.columns(4)

        with btn0:
            if st.button("法律咨询", use_container_width=True):
                switch_mode("法律咨询")
                st.rerun()

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

        #st.markdown('<div class="input-shell">', unsafe_allow_html=True)
        #st.markdown(
         #   '<div class="input-tip">请输入案件事实、争议焦点、文书内容或合同需求，系统将根据当前模式通过同一智能体工作流进行处理。</div>',
          #  unsafe_allow_html=True,
        #)

        st.text_area(
            " ",
            key="user_input",
            label_visibility="collapsed",
            placeholder="请输入案件事实、争议焦点、文书内容或合同需求，系统将根据当前模式通过智能体工作流进行处理。",
            height=110,
        )

        st.markdown('<div class="upload-title">上传附件</div>', unsafe_allow_html=True)
        st.file_uploader(
            "上传附件",
            key="uploaded_files",
            label_visibility="collapsed",
            accept_multiple_files=True,
            type=["txt", "md", "csv", "json", "pdf", "doc", "docx", "png", "jpg", "jpeg"],
        )

        st.markdown('<div class="send-row">', unsafe_allow_html=True)
        st.button("发送", use_container_width=True, on_click=send_message)
        #st.markdown('</div></div>', unsafe_allow_html=True)
