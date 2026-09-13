"""
Modern Trade Reconciliation AI — v2.3
Hybrid Promo Input + Password Login + Cloud Ready
"""

import streamlit as st
import pandas as pd
import io
import json
from datetime import datetime

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Modern Trade Reconciliation AI",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# 🔐 PASSWORD LOGIN
# ══════════════════════════════════════════════════════════════════════════════
def check_password() -> bool:
    try:
        correct_pw = st.secrets["app"]["password"]
        app_title  = st.secrets["app"].get("title", "Modern Trade Reconciliation AI")
        team_name  = st.secrets["app"].get("team",  "ทีมบัญชี")
    except Exception:
        correct_pw = "MT029030445*"
        app_title  = "Modern Trade Reconciliation AI"
        team_name  = "ทีมบัญชี"

    if st.session_state.get("_logged_in"):
        return True

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700;800&display=swap');
    html,body,[class*="css"]{ font-family:'Sarabun',sans-serif !important; }
    .stApp { background:linear-gradient(135deg,#EEF5FF 0%,#D0F7EE 100%) !important; }
    [data-testid="stSidebar"]{ display:none !important; }
    .stButton>button {
        background:linear-gradient(135deg,#3A8EDE,#1B6CA8) !important;
        color:#fff !important; border:none !important; border-radius:10px !important;
        font-size:16px !important; font-weight:700 !important; padding:12px !important;
        box-shadow:0 4px 14px rgba(58,142,222,.38) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown(f"""
        <div style="background:#fff;border-radius:20px;padding:42px 36px 32px;
                    box-shadow:0 8px 40px rgba(58,142,222,.18);
                    border:2px solid #C5DEFF;text-align:center;margin-top:60px;">
            <div style="font-size:66px;line-height:1;margin-bottom:10px;">🧾</div>
            <h2 style="color:#1A3A5C;font-size:21px;font-weight:800;margin:0 0 4px 0;">{app_title}</h2>
            <p style="color:#5A7BA8;font-size:13px;margin:0 0 26px 0;">{team_name} · ระบบใช้งานภายใน</p>
        """, unsafe_allow_html=True)

        pw = st.text_input("รหัสผ่าน", type="password",
                           placeholder="ใส่รหัสผ่านเพื่อเข้าใช้งาน",
                           label_visibility="collapsed")
        btn = st.button("🔓  เข้าสู่ระบบ", use_container_width=True, type="primary")

        st.markdown("""
        <p style="color:#A0B4CC;font-size:12px;margin-top:16px;">
            🔒 ใช้งานเฉพาะภายในทีมเท่านั้น<br>ข้อมูลที่อัปโหลดไม่ถูกบันทึก
        </p></div>
        """, unsafe_allow_html=True)

        if btn:
            if pw == correct_pw:
                st.session_state["_logged_in"] = True
                st.rerun()
            else:
                st.error("❌ รหัสผ่านไม่ถูกต้อง กรุณาลองใหม่ครับ")
    return False

if not check_password():
    st.stop()

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family:'Sarabun',sans-serif !important; }
.stApp { background:#EEF5FF !important; }

/* ─── Sidebar ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(170deg,#1B6CA8 0%,#124D80 55%,#0C3358 100%) !important;
}
[data-testid="stSidebar"] * { color:#fff !important; }
[data-testid="stSidebar"] .stSelectbox>div>div {
    background:rgba(255,255,255,.14) !important;
    border:1.5px solid rgba(255,255,255,.30) !important;
    border-radius:10px !important; font-size:14px !important;
}
[data-testid="stSidebar"] .stTextInput>div>div>input {
    background:rgba(255,255,255,.14) !important;
    border:1.5px solid rgba(255,255,255,.30) !important;
    border-radius:10px !important; font-size:14px !important; color:#fff !important;
}
[data-testid="stSidebar"] .stTextInput>div>div>input::placeholder {
    color:rgba(255,255,255,.50) !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background:rgba(255,255,255,.10) !important;
    border:2px dashed rgba(255,255,255,.40) !important;
    border-radius:10px !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] label,
[data-testid="stSidebar"] [data-testid="stFileUploader"] span {
    color:#fff !important; font-size:13px !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] small {
    color:rgba(255,255,255,.65) !important; font-size:11px !important;
}

/* ─── Hero ─── */
.hero {
    background: linear-gradient(125deg,#3A8EDE 0%,#30BFA0 100%);
    border-radius:16px; padding:28px 34px; margin-bottom:22px;
    display:flex; align-items:center; gap:20px;
    box-shadow:0 4px 24px rgba(58,142,222,.22);
}
.hero h1 {
    color:#fff !important; font-size:27px !important; font-weight:800 !important;
    margin:0 0 5px 0 !important; line-height:1.25;
    text-shadow:0 1px 4px rgba(0,0,0,.18);
}
.hero p  { color:rgba(255,255,255,.90) !important; font-size:15px !important; margin:0 !important; }
.hero-icon { font-size:58px; line-height:1; flex-shrink:0; }
.hero-badge {
    display:inline-block; background:rgba(255,255,255,.22);
    border:1px solid rgba(255,255,255,.40); border-radius:24px;
    padding:4px 14px; font-size:12px; font-weight:700; color:#fff; margin-top:8px;
}

/* ─── Section labels ─── */
.sec-label {
    font-size:11px; letter-spacing:1.3px; font-weight:700;
    opacity:.72; text-transform:uppercase; margin-bottom:6px; color:#fff;
}
.card-title {
    font-size:17px; font-weight:800; color:#2C7BE5;
    margin-bottom:14px; display:flex; align-items:center; gap:8px;
    border-bottom:2.5px solid #D6EAFF; padding-bottom:10px;
}

/* ─── Upload zones (main) ─── */
[data-testid="stFileUploader"] {
    background:#EAF4FF !important;
    border:2.5px dashed #4A90D9 !important;
    border-radius:12px !important; padding:14px !important;
    transition:all .2s;
}
[data-testid="stFileUploader"]:hover {
    background:#D6EAFF !important; border-color:#1B6CA8 !important;
}
[data-testid="stFileUploader"] label {
    font-size:15px !important; font-weight:700 !important; color:#2C7BE5 !important;
}

/* ─── Promo sidebar upload override ─── */
.sidebar-upload [data-testid="stFileUploader"] {
    background:rgba(255,255,255,.10) !important;
    border:2px dashed rgba(255,255,255,.45) !important;
}

/* ─── Buttons ─── */
.stButton>button {
    background:linear-gradient(135deg,#3A8EDE 0%,#1B6CA8 100%) !important;
    color:#fff !important; border:none !important; border-radius:10px !important;
    font-size:16px !important; font-weight:700 !important; padding:12px 32px !important;
    box-shadow:0 4px 14px rgba(58,142,222,.38) !important; transition:all .2s !important;
}
.stButton>button:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 7px 20px rgba(58,142,222,.45) !important;
}
[data-testid="stDownloadButton"]>button {
    background:linear-gradient(135deg,#30BFA0 0%,#1A8A72 100%) !important;
    color:#fff !important; border:none !important; border-radius:10px !important;
    font-size:15px !important; font-weight:700 !important; padding:10px 22px !important;
    box-shadow:0 4px 14px rgba(48,191,160,.35) !important;
}

/* ─── Metrics ─── */
[data-testid="metric-container"] {
    background:#fff !important; border:2px solid #C5DEFF !important;
    border-radius:12px !important; padding:16px !important;
    box-shadow:0 2px 10px rgba(58,142,222,.08) !important;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size:13px !important; font-weight:700 !important; color:#5A7BA8 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size:24px !important; font-weight:800 !important; color:#2C7BE5 !important;
}

/* ─── Info boxes ─── */
.box-info  { background:#EAF4FF; border-left:5px solid #3A8EDE; border-radius:0 10px 10px 0; padding:12px 16px; font-size:14px; color:#1A3A5C; margin:10px 0; }
.box-tip   { background:#E0F7F1; border-left:5px solid #30BFA0; border-radius:0 10px 10px 0; padding:12px 16px; font-size:14px; color:#0D4A3A; margin:10px 0; }
.box-error { background:#FDECEA; border-left:5px solid #D32F2F; border-radius:0 10px 10px 0; padding:14px 18px; font-size:15px; font-weight:700; color:#B71C1C; margin:10px 0; }
.box-warn  { background:#FFF8E1; border-left:5px solid #F9A825; border-radius:0 10px 10px 0; padding:13px 16px; font-size:14px; font-weight:600; color:#7A4F00; margin:10px 0; }
.box-promo { background:#F3E5F5; border-left:5px solid #8E24AA; border-radius:0 10px 10px 0; padding:12px 16px; font-size:14px; color:#4A148C; margin:10px 0; }

/* ─── Source badges ─── */
.src-badge {
    display:inline-block; border-radius:20px;
    padding:3px 12px; font-size:12px; font-weight:700; margin:2px 4px;
}
.src-gdrive { background:#E8F0FE; color:#1967D2; border:1.5px solid #7BAAF7; }
.src-manual { background:#F3E5F5; color:#6A1B9A; border:1.5px solid #CE93D8; }

/* ─── Promo summary card ─── */
.promo-card {
    background:linear-gradient(135deg,#F3E5F5 0%,#EDE7F6 100%);
    border:2px solid #CE93D8; border-radius:12px;
    padding:16px 20px; margin:12px 0;
    box-shadow:0 2px 8px rgba(142,36,170,.12);
}
.promo-card-title {
    font-size:15px; font-weight:800; color:#6A1B9A; margin-bottom:10px;
    display:flex; align-items:center; gap:8px;
}

/* ─── Calc button special ─── */
.calc-btn .stButton>button {
    background:linear-gradient(135deg,#E53935 0%,#B71C1C 100%) !important;
    font-size:17px !important; padding:14px 36px !important;
    box-shadow:0 5px 18px rgba(229,57,53,.40) !important;
}

/* ─── Table ─── */
thead th {
    background:#3A8EDE !important; color:#fff !important;
    font-size:15px !important; font-weight:800 !important;
    padding:12px 10px !important; text-align:center !important;
}
tbody td { font-size:15px !important; padding:10px 10px !important; }

/* ─── Steps ─── */
.step-row { display:flex; align-items:center; gap:12px; padding:10px 14px; background:#fff; border-radius:10px; border:2px solid #C5DEFF; margin-bottom:8px; }
.step-num { width:32px; height:32px; background:#3A8EDE; color:#fff; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:15px; flex-shrink:0; }
.step-text{ font-size:15px; font-weight:600; color:#1A3A5C; }

/* ─── Demo ribbon ─── */
.demo-ribbon {
    background:linear-gradient(90deg,#FF6F00,#FFA000); color:#fff;
    text-align:center; padding:9px; font-size:15px; font-weight:800;
    border-radius:10px; margin-bottom:18px;
    box-shadow:0 3px 12px rgba(255,111,0,.30);
}
/* ─── CPAXT badge ─── */
.cpaxt-badge {
    display:inline-block; background:#1B6CA8; color:#fff;
    border-radius:6px; padding:2px 8px; font-size:11px; font-weight:700;
    margin-left:6px; vertical-align:middle;
}

@keyframes pulse {
    0%  { box-shadow:0 0 0 0 rgba(211,47,47,.40); }
    70% { box-shadow:0 0 0 8px rgba(211,47,47,0); }
    100%{ box-shadow:0 0 0 0 rgba(211,47,47,0); }
}
::-webkit-scrollbar { width:7px; }
::-webkit-scrollbar-thumb { background:#C5DEFF; border-radius:4px; }
::-webkit-scrollbar-thumb:hover { background:#3A8EDE; }
hr { border:none !important; border-top:2.5px solid #C5DEFF !important; margin:20px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# CONSTANTS
# ════════════════════════════════════════════════════════
STORES = [
    "7-Eleven",
    "Big C (รวม Pure และ Big C mini)",
    "Jiffy (ปตท. บริหารธุรกิจค้าปลีก / PTTRM)",
    "Tops (รวม Tops Daily และ Tops Care)",
    "CPAXT (Makro หน้าร้าน)",
    "CPAXT (Makro Online / Makro PRO)",
    "CPAXT (Lotus's Wholesale)",
    "Go Wholesale",
    "Ucare",
    "Ek-Chai Distribution (Lotus's / Lotus's Super)",
    "Watsons",
    "Golden Place (สุวรรณชาด)",
    "Tsuruha",
    "PT Max",
    "P&F",
    "AEON Thailand (MaxValu)",
    "TFG / Thaifoods Group",
    "CJ Express",
    "Foodland",
    "Harbor Land",
    "Boots",
    "Gourmet Market",
    "Fascino / Profascino (ฟาร์มาฮอฟ)",
    "Lawson 108",
    "วิลล่า มาร์เก็ท เจพี (Villa Market)",
    "Baimiang",
]

CPAXT_STORES = {
    "CPAXT (Makro หน้าร้าน)",
    "CPAXT (Makro Online / Makro PRO)",
    "CPAXT (Lotus's Wholesale)",
}

# ════════════════════════════════════════════════════════
# MOCKUP DATA
# ════════════════════════════════════════════════════════
MOCKUP_DB: dict[str, dict] = {
    "7-Eleven":                                    {"doc":"REM-7EL-2567-0891","date":"05/09/2567","period":"ส.ค. 67","billing_co":"ซีพี ออลล์ จำกัด (มหาชน)",                          "total":4_820_500,"promo":312_400,"dc":89_600, "mkt":145_000,"ship":28_500, "other":12_300,"net":4_232_700,"sp":"ok",  "sd":"over","sm":"ok",  "ss":"ok","so":"ok"},
    "Big C (รวม Pure และ Big C mini)":             {"doc":"REM-BGC-2567-1123","date":"03/09/2567","period":"ส.ค. 67","billing_co":"บิ๊กซี ซูเปอร์เซ็นเตอร์ จำกัด (มหาชน)",           "total":8_380_000,"promo":678_000,"dc":242_000,"mkt":375_000,"ship":57_000, "other":30_000,"net":6_998_000,"sp":"ok",  "sd":"ok",  "sm":"over","ss":"ok","so":"ok"},
    "Jiffy (ปตท. บริหารธุรกิจค้าปลีก / PTTRM)":  {"doc":"REM-JIF-2567-0234","date":"06/09/2567","period":"ส.ค. 67","billing_co":"ปตท. บริหารธุรกิจค้าปลีก จำกัด (PTTRM)",          "total":890_000,  "promo":72_000, "dc":18_000, "mkt":38_000, "ship":9_500,  "other":3_200, "net":749_300, "sp":"ok",  "sd":"over","sm":"ok",  "ss":"ok","so":"ok"},
    "Tops (รวม Tops Daily และ Tops Care)":         {"doc":"REM-TOP-2567-0987","date":"02/09/2567","period":"ส.ค. 67","billing_co":"เซ็นทรัล ฟู้ด รีเทล จำกัด",                       "total":7_880_000,"promo":629_000,"dc":201_000,"mkt":395_000,"ship":65_500, "other":32_000,"net":6_557_500,"sp":"over","sd":"ok",  "sm":"ok",  "ss":"ok","so":"ok"},
    "CPAXT (Makro หน้าร้าน)":                     {"doc":"REM-MKR-2567-1456","date":"01/09/2567","period":"ส.ค. 67","billing_co":"สยามแม็คโคร จำกัด (มหาชน) — CPAXT",              "total":12_800_000,"promo":980_000,"dc":420_000,"mkt":650_000,"ship":85_000,"other":42_000,"net":10_623_000,"sp":"ok", "sd":"over","sm":"over","ss":"ok","so":"ok"},
    "CPAXT (Makro Online / Makro PRO)":            {"doc":"REM-MKRO-2567-0312","date":"01/09/2567","period":"ส.ค. 67","billing_co":"สยามแม็คโคร จำกัด (มหาชน) — CPAXT Online",       "total":3_450_000,"promo":278_000,"dc":92_000, "mkt":158_000,"ship":36_000, "other":17_500,"net":2_868_500,"sp":"ok",  "sd":"ok",  "sm":"ok",  "ss":"ok","so":"ok"},
    "CPAXT (Lotus's Wholesale)":                   {"doc":"REM-LTWS-2567-0789","date":"01/09/2567","period":"ส.ค. 67","billing_co":"เอก-ชัย ดิสทริบิวชั่น ซิสเทม จำกัด — Wholesale","total":5_620_000,"promo":448_000,"dc":185_000,"mkt":289_000,"ship":50_000, "other":25_000,"net":4_623_000,"sp":"ok",  "sd":"ok",  "sm":"over","ss":"ok","so":"ok"},
    "Go Wholesale":                                {"doc":"REM-GWS-2567-0567","date":"05/09/2567","period":"ส.ค. 67","billing_co":"โก โฮลเซล จำกัด",                                 "total":3_200_000,"promo":258_000,"dc":85_000, "mkt":145_000,"ship":32_000, "other":15_000,"net":2_665_000,"sp":"ok",  "sd":"ok",  "sm":"ok",  "ss":"ok","so":"ok"},
    "Ucare":                                       {"doc":"REM-UCR-2567-0123","date":"08/09/2567","period":"ส.ค. 67","billing_co":"ยูแคร์ จำกัด",                                     "total":450_000,  "promo":38_000, "dc":9_500,  "mkt":21_000, "ship":5_000,  "other":2_100, "net":374_400, "sp":"ok",  "sd":"ok",  "sm":"ok",  "ss":"ok","so":"ok"},
    "Ek-Chai Distribution (Lotus's / Lotus's Super)":{"doc":"REM-LTS-2567-2341","date":"01/09/2567","period":"ส.ค. 67","billing_co":"เอก-ชัย ดิสทริบิวชั่น ซิสเทม จำกัด",         "total":16_100_000,"promo":1_275_000,"dc":530_000,"mkt":830_000,"ship":127_000,"other":62_500,"net":13_275_500,"sp":"ok","sd":"ok","sm":"over","ss":"ok","so":"ok"},
    "Watsons":                                     {"doc":"REM-WAT-2567-0789","date":"04/09/2567","period":"ส.ค. 67","billing_co":"วัตสัน (ประเทศไทย) จำกัด",                         "total":2_150_000,"promo":172_000,"dc":56_000, "mkt":98_000, "ship":22_000, "other":9_800, "net":1_792_200,"sp":"over","sd":"ok","sm":"ok","ss":"ok","so":"ok"},
    "Golden Place (สุวรรณชาด)":                   {"doc":"REM-GLP-2567-0345","date":"06/09/2567","period":"ส.ค. 67","billing_co":"บริษัท สุวรรณชาด จำกัด (Golden Place)",             "total":680_000,  "promo":55_000, "dc":14_500, "mkt":32_000, "ship":7_500,  "other":3_000, "net":568_000, "sp":"ok",  "sd":"ok",  "sm":"ok",  "ss":"ok","so":"ok"},
    "Tsuruha":                                     {"doc":"REM-TSR-2567-0234","date":"03/09/2567","period":"ส.ค. 67","billing_co":"สยาม ทสุรุฮะ จำกัด",                               "total":1_890_000,"promo":150_000,"dc":49_000, "mkt":85_000, "ship":19_500, "other":8_500, "net":1_578_000,"sp":"ok",  "sd":"over","sm":"ok","ss":"ok","so":"ok"},
    "PT Max":                                      {"doc":"REM-PTM-2567-0678","date":"05/09/2567","period":"ส.ค. 67","billing_co":"พีที มัลติ คอนเวนเนียนซ์ สโตร์ จำกัด",             "total":760_000,  "promo":62_000, "dc":16_000, "mkt":35_000, "ship":8_000,  "other":3_200, "net":635_800, "sp":"ok",  "sd":"ok",  "sm":"ok",  "ss":"ok","so":"ok"},
    "P&F":                                         {"doc":"REM-PNF-2567-0156","date":"08/09/2567","period":"ส.ค. 67","billing_co":"พี แอนด์ เอฟ จำกัด",                               "total":520_000,  "promo":42_000, "dc":11_000, "mkt":24_000, "ship":5_800,  "other":2_400, "net":434_800, "sp":"ok",  "sd":"ok",  "sm":"over","ss":"ok","so":"ok"},
    "AEON Thailand (MaxValu)":                     {"doc":"REM-AEN-2567-0891","date":"02/09/2567","period":"ส.ค. 67","billing_co":"อิออน (ไทยแลนด์) จำกัด",                           "total":3_450_000,"promo":275_000,"dc":90_000, "mkt":155_000,"ship":34_000, "other":16_000,"net":2_880_000,"sp":"ok",  "sd":"ok",  "sm":"ok",  "ss":"ok","so":"ok"},
    "TFG / Thaifoods Group":                       {"doc":"REM-TFG-2567-0432","date":"06/09/2567","period":"ส.ค. 67","billing_co":"ไทยฟู้ดส์ กรุ๊ป จำกัด (มหาชน)",                   "total":1_120_000,"promo":89_000, "dc":23_500, "mkt":52_000, "ship":12_000, "other":5_200, "net":938_300, "sp":"ok",  "sd":"ok",  "sm":"ok",  "ss":"ok","so":"ok"},
    "CJ Express":                                  {"doc":"REM-CJE-2567-0567","date":"04/09/2567","period":"ส.ค. 67","billing_co":"ซีเจ เอ็กซ์เพรส กรุ๊ป จำกัด",                     "total":870_000,  "promo":69_500, "dc":18_000, "mkt":40_000, "ship":9_000,  "other":3_800, "net":729_700, "sp":"over","sd":"ok","sm":"ok","ss":"ok","so":"ok"},
    "Foodland":                                    {"doc":"REM-FLD-2567-0321","date":"07/09/2567","period":"ส.ค. 67","billing_co":"ฟู้ดแลนด์ ซูเปอร์มาร์เก็ต จำกัด",                  "total":2_340_000,"promo":186_000,"dc":61_000, "mkt":108_000,"ship":24_000, "other":10_500,"net":1_950_500,"sp":"ok",  "sd":"ok",  "sm":"over","ss":"ok","so":"ok"},
    "Harbor Land":                                 {"doc":"REM-HBL-2567-0145","date":"08/09/2567","period":"ส.ค. 67","billing_co":"ฮาร์เบอร์แลนด์ จำกัด",                              "total":590_000,  "promo":47_000, "dc":12_500, "mkt":27_500, "ship":6_500,  "other":2_800, "net":493_700, "sp":"ok",  "sd":"ok",  "sm":"ok",  "ss":"ok","so":"ok"},
    "Boots":                                       {"doc":"REM-BOT-2567-1234","date":"03/09/2567","period":"ส.ค. 67","billing_co":"บูทส์ รีเทล (ประเทศไทย) จำกัด",                    "total":4_120_000,"promo":328_000,"dc":107_000,"mkt":190_000,"ship":42_000, "other":19_500,"net":3_433_500,"sp":"ok",  "sd":"over","sm":"ok","ss":"ok","so":"ok"},
    "Gourmet Market":                              {"doc":"REM-GRM-2567-0678","date":"05/09/2567","period":"ส.ค. 67","billing_co":"เดอะ มอลล์ กรุ๊ป จำกัด (Gourmet Market)",           "total":1_680_000,"promo":134_000,"dc":44_000, "mkt":78_000, "ship":17_500, "other":7_800, "net":1_398_700,"sp":"ok",  "sd":"ok",  "sm":"ok",  "ss":"ok","so":"ok"},
    "Fascino / Profascino (ฟาร์มาฮอฟ)":           {"doc":"REM-FSC-2567-0234","date":"06/09/2567","period":"ส.ค. 67","billing_co":"โปรฟาสซิโน จำกัด (ฟาร์มาฮอฟ)",                    "total":920_000,  "promo":73_500, "dc":19_000, "mkt":43_000, "ship":9_800,  "other":4_100, "net":770_600, "sp":"ok",  "sd":"ok",  "sm":"over","ss":"ok","so":"ok"},
    "Lawson 108":                                  {"doc":"REM-LW1-2567-0789","date":"07/09/2567","period":"ส.ค. 67","billing_co":"สโตร์ วัน จำกัด (Lawson 108)",                      "total":1_050_000,"promo":83_500, "dc":21_500, "mkt":49_000, "ship":11_000, "other":4_700, "net":880_300, "sp":"ok",  "sd":"ok",  "sm":"ok",  "ss":"ok","so":"ok"},
    "วิลล่า มาร์เก็ท เจพี (Villa Market)":        {"doc":"REM-VLM-2567-0456","date":"02/09/2567","period":"ส.ค. 67","billing_co":"วิลล่า มาร์เก็ท เจพี จำกัด",                       "total":2_780_000,"promo":221_000,"dc":72_500, "mkt":128_000,"ship":28_500, "other":12_800,"net":2_317_200,"sp":"ok",  "sd":"ok",  "sm":"ok",  "ss":"ok","so":"ok"},
    "Baimiang":                                    {"doc":"REM-BMG-2567-0123","date":"08/09/2567","period":"ส.ค. 67","billing_co":"ใบเมี่ยง จำกัด",                                    "total":380_000,  "promo":30_500, "dc":8_000,  "mkt":18_000, "ship":4_200,  "other":1_800, "net":317_500, "sp":"ok",  "sd":"ok",  "sm":"ok",  "ss":"ok","so":"ok"},
}

# ════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════
def fmt(v) -> str:
    try:    return f"฿{float(v):>14,.2f}"
    except: return "฿0.00"

def get_status(s: str) -> str:
    if s == "over":  return "❌ ห้างหักเกิน"
    if s == "short": return "⚠️ ยอดขาด"
    return "✅ ตรงกัน"

def make_invoices(store: str) -> list[dict]:
    d = MOCKUP_DB.get(store, {})
    if not d: return []
    key = d["doc"][-4:]
    rows = []
    for num, (label, base, sk) in enumerate([
        ("ส่วนลดโปรโมชั่น", d["promo"], "sp"),
        ("ค่า DC",           d["dc"],    "sd"),
        ("ค่าการตลาด",       d["mkt"],   "sm"),
        ("ค่าขนส่ง",         d["ship"],  "ss"),
        ("อื่นๆ",             d["other"], "so"),
    ], start=1):
        ratio = 0.87 if d.get(sk) == "over" else 1.0
        sub   = round(base * ratio, 2)
        vat   = round(sub  * 0.07,  2)
        rows.append({"invoice_no": f"INV-{key}-{num:03d}", "date": d["date"],
                     "type": label, "subtotal": sub, "vat": vat, "total": round(sub+vat,2)})
    return rows

def build_recon_df(store: str) -> pd.DataFrame:
    d   = MOCKUP_DB.get(store, MOCKUP_DB[STORES[0]])
    inv = make_invoices(store)
    defs = [
        ("ส่วนลดโปรโมชั่น", d["promo"], "ส่วนลดโปรโมชั่น", d["sp"]),
        ("ค่า DC",           d["dc"],    "ค่า DC",           d["sd"]),
        ("ค่าการตลาด",       d["mkt"],   "ค่าการตลาด",       d["sm"]),
        ("ค่าขนส่ง",         d["ship"],  "ค่าขนส่ง",         d["ss"]),
        ("อื่นๆ",             d["other"], "อื่นๆ",            d["so"]),
    ]
    rows = []
    for label, store_amt, inv_type, sk in defs:
        calc = sum(i["total"] for i in inv if i["type"] == inv_type)
        rows.append({"รายการ": label, "ยอดห้าง (บาท)": store_amt,
                     "ยอดคำนวณ (บาท)": calc, "ผลต่าง (บาท)": store_amt - calc,
                     "สถานะ": get_status(sk)})
    total_ded = d["promo"]+d["dc"]+d["mkt"]+d["ship"]+d["other"]
    calc_net  = d["total"] - total_ded
    rows.append({"รายการ": "💰 ยอดสุทธิ", "ยอดห้าง (บาท)": d["net"],
                 "ยอดคำนวณ (บาท)": calc_net, "ผลต่าง (บาท)": d["net"]-calc_net,
                 "สถานะ": "✅ ตรงกัน"})
    return pd.DataFrame(rows)

def style_df(df: pd.DataFrame):
    def col_status(val):
        if "❌" in str(val): return "color:#B71C1C;font-weight:900;font-size:15px"
        if "⚠️" in str(val): return "color:#E65100;font-weight:800;font-size:15px"
        if "✅" in str(val): return "color:#1B5E20;font-weight:800;font-size:15px"
        return ""
    def col_diff(val):
        try:
            v = float(str(val).replace("฿","").replace(",",""))
            if v > 1:  return "color:#B71C1C;font-weight:800"
            if v < -1: return "color:#E65100;font-weight:800"
            return "color:#1B5E20;font-weight:700"
        except: return ""
    disp = df.copy()
    disp["ยอดห้าง (บาท)"]   = df["ยอดห้าง (บาท)"].apply(fmt)
    disp["ยอดคำนวณ (บาท)"] = df["ยอดคำนวณ (บาท)"].apply(fmt)
    disp["ผลต่าง (บาท)"]    = df["ผลต่าง (บาท)"].apply(fmt)
    return (disp.style
        .applymap(col_status, subset=["สถานะ"])
        .applymap(col_diff,   subset=["ผลต่าง (บาท)"])
        .set_properties(**{"font-size":"15px","font-family":"Sarabun,sans-serif","text-align":"center"})
        .set_properties(subset=["รายการ"], **{"text-align":"left","font-weight":"700","font-size":"15px"})
        .set_table_styles([
            {"selector":"thead th","props":[("background","#3A8EDE"),("color","white"),
             ("font-size","15px"),("font-weight","800"),("text-align","center"),("padding","12px 10px")]},
            {"selector":"tbody tr:nth-child(even)","props":[("background","#EAF4FF")]},
            {"selector":"tbody tr:hover","props":[("background","#D0F7EE")]},
        ]))

def to_excel(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df.to_excel(w, index=False, sheet_name="Report")
        ws = w.sheets["Report"]
        for col in ws.columns:
            mx = max((len(str(c.value or "")) for c in col), default=10)
            ws.column_dimensions[col[0].column_letter].width = min(mx+4, 42)
    return buf.getvalue()

# ════════════════════════════════════════════════════════
# SESSION STATE
# ════════════════════════════════════════════════════════
defaults = {"store": STORES[0], "show_result": False, "gdrive": "", "calc_clicked": False}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════
with st.sidebar:

    # ── Logo ─────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;padding:10px 0 20px 0;
                border-bottom:1px solid rgba(255,255,255,.20);margin-bottom:18px;">
        <div style="font-size:52px;line-height:1">🧾</div>
        <div style="font-size:17px;font-weight:800;margin:8px 0 2px 0;">MT Recon AI</div>
        <div style="font-size:12px;opacity:.70;">Mockup Demo v2.2</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Store selector ────────────────────────────────
    st.markdown('<p class="sec-label">🏪 เลือกห้าง / นิติบุคคล</p>', unsafe_allow_html=True)
    selected_store = st.selectbox("ห้าง", STORES,
                                  index=STORES.index(st.session_state["store"]),
                                  label_visibility="collapsed",
                                  help="ชื่อตามนามนิติบุคคลบนหัวบิลจริง")
    st.session_state["store"] = selected_store

    if selected_store in CPAXT_STORES:
        st.markdown("""
        <div style="background:rgba(255,165,0,.18);border:1px solid rgba(255,165,0,.45);
                    border-radius:8px;padding:9px 12px;font-size:12px;margin-top:4px;">
            🏢 <strong>กลุ่ม CPAXT</strong> — ออกบิลแยกตามช่องทาง<br>
            หน้าร้าน · Online/PRO · Wholesale
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ════════════════════════════════════════════════
    # ฝั่งขาย — HYBRID PROMO INPUT
    # ════════════════════════════════════════════════
    st.markdown("""
    <div style="background:rgba(255,255,255,.10);border-radius:10px;padding:14px 14px 6px 14px;margin-bottom:4px;">
        <div style="font-size:13px;font-weight:800;letter-spacing:.3px;margin-bottom:10px;">
            📦 ข้อมูลโปรโมชั่นฝั่งขาย
        </div>
    """, unsafe_allow_html=True)

    # ① Google Drive Link
    st.markdown('<p class="sec-label" style="margin-top:4px;">🔗 Google Drive Link</p>', unsafe_allow_html=True)
    gdrive = st.text_input(
        "GDrive", value=st.session_state["gdrive"],
        placeholder="https://drive.google.com/drive/folders/...",
        label_visibility="collapsed",
        help="ลิงก์ Google Drive ของโปรโมชั่นฝั่งขายสำหรับห้างนี้"
    )
    st.session_state["gdrive"] = gdrive

    if gdrive:
        st.markdown('<p style="font-size:11px;color:rgba(255,255,255,.75);margin:2px 0 8px 2px;">✅ รับลิงก์แล้ว</p>', unsafe_allow_html=True)

    # Divider + OR
    st.markdown("""
    <div style="display:flex;align-items:center;gap:8px;margin:10px 0;">
        <div style="flex:1;height:1px;background:rgba(255,255,255,.25);"></div>
        <div style="font-size:11px;font-weight:700;opacity:.65;">หรือ</div>
        <div style="flex:1;height:1px;background:rgba(255,255,255,.25);"></div>
    </div>
    """, unsafe_allow_html=True)

    # ② Manual Promo Upload
    st.markdown('<p class="sec-label">📎 อัปโหลดใบโปรโมชั่น (Manual)</p>', unsafe_allow_html=True)
    promo_files = st.file_uploader(
        "Promo Upload",
        type=["pdf", "xlsx", "xls", "jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="promo_up",
        label_visibility="collapsed",
        help="ลากวางได้หลายไฟล์ — PDF, Excel, รูปเงื่อนไขโปรโมชั่น"
    )

    if promo_files:
        st.markdown(
            f'<p style="font-size:11px;color:rgba(255,255,255,.80);margin:4px 0 0 2px;">'
            f'✅ รับไฟล์โปรโมชั่น <strong>{len(promo_files)}</strong> ไฟล์</p>',
            unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Source summary ─────────────────────────────
    has_gdrive = bool(gdrive and gdrive.strip().startswith("http"))
    has_manual = bool(promo_files)
    has_promo  = has_gdrive or has_manual

    if has_promo:
        src_html = ""
        if has_gdrive: src_html += '<span class="src-badge src-gdrive">☁️ Google Drive</span>'
        if has_manual: src_html += f'<span class="src-badge src-manual">📎 Manual ({len(promo_files)} ไฟล์)</span>'
        st.markdown(f'<div style="margin:8px 0 0 0;">{src_html}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Sidebar stats ──────────────────────────────
    if st.session_state["show_result"]:
        d = MOCKUP_DB.get(selected_store, {})
        st.markdown('<p class="sec-label">📊 สรุปรอบนี้</p>', unsafe_allow_html=True)
        n_over = sum(1 for k in ["sp","sd","sm","ss","so"] if d.get(k) == "over")
        n_ok   = 5 - n_over
        c1, c2 = st.columns(2)
        with c1:
            st.metric("✅ ตรงกัน", n_ok)
            st.metric("❌ หักเกิน", n_over)
        with c2:
            st.metric("💰 ยอดโอน", f'฿{d.get("total",0)/1e6:.2f}M')
            st.metric("📋 รายการ", "5")
        st.markdown("---")

    st.markdown('<p style="font-size:11px;opacity:.50;text-align:center;">v2.2 · © 2025 MT Recon AI</p>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# MAIN PAGE
# ════════════════════════════════════════════════════════

# Demo ribbon
st.markdown('<div class="demo-ribbon">🎯 โหมดจำลองข้อมูล (Mockup Demo) — เลือกห้าง อัปโหลดเอกสาร แล้วกด "เริ่มคำนวณยันยอด"</div>', unsafe_allow_html=True)

# Hero
cpaxt_badge = ' <span class="cpaxt-badge">CPAXT Group</span>' if selected_store in CPAXT_STORES else ""
billing_co  = MOCKUP_DB.get(selected_store, {}).get("billing_co", selected_store)
st.markdown(f"""
<div class="hero">
    <div class="hero-icon">🤖</div>
    <div>
        <h1>Modern Trade Reconciliation AI</h1>
        <p>
            ห้างที่เลือก: <strong>{selected_store}</strong>{cpaxt_badge}<br>
            <span style="font-size:13px;opacity:.85;">นิติบุคคล: {billing_co}</span>
        </p>
        <span class="hero-badge">🎯 Mockup Demo v2.2 · Hybrid Promo Input · Streamlit</span>
    </div>
</div>
""", unsafe_allow_html=True)

# How-to steps
with st.expander("📋 วิธีใช้งานระบบ (คลิกดู)", expanded=False):
    steps = [
        ("1","🏪","เลือกชื่อนิติบุคคลจาก Dropdown ด้านซ้าย (26 ห้าง)"),
        ("2","☁️","ใส่ลิงก์ Google Drive โปรโมชั่นฝั่งขาย (ถ้ามี)"),
        ("3","📎","หรืออัปโหลดไฟล์ใบโปรฯ ด้วยตัวเอง (Manual Upload)"),
        ("4","📄","อัปโหลดใบโอนเงิน (ฝั่งซ้าย) — PDF / JPG / PNG"),
        ("5","🧾","อัปโหลดใบแจ้งหนี้/บิล (ฝั่งขวา) — ลากวางหลายไฟล์"),
        ("6","🔴","กดปุ่ม \"เริ่มคำนวณยันยอด\" เพื่อดูผลทันที"),
    ]
    for n, icon, txt in steps:
        st.markdown(f'<div class="step-row"><div class="step-num">{n}</div><div class="step-text">{icon} {txt}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Promo source summary (main area) ─────────────────
if has_promo:
    src_parts = []
    if has_gdrive: src_parts.append(f"☁️ Google Drive")
    if has_manual: src_parts.append(f"📎 Manual Upload ({len(promo_files)} ไฟล์: {', '.join(f.name for f in promo_files[:3])}{'...' if len(promo_files)>3 else ''})")
    st.markdown(
        f'<div class="box-promo">📦 <strong>โหลดข้อมูลโปรโมชั่นจาก {len(src_parts)} แหล่ง:</strong> '
        + " &nbsp;+&nbsp; ".join(src_parts)
        + " — ระบบจะรวมข้อมูลทั้งสองแหล่งโดยอัตโนมัติ</div>",
        unsafe_allow_html=True)
else:
    st.markdown('<div class="box-warn">⚠️ ยังไม่มีข้อมูลโปรโมชั่นฝั่งขาย — ใส่ลิงก์ Google Drive หรืออัปโหลดไฟล์ใน Sidebar ด้านซ้าย</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# UPLOAD: 2 COLUMNS (บัญชี)
# ════════════════════════════════════════════════════════
col_l, col_r = st.columns(2, gap="large")

with col_l:
    st.markdown('<div class="card-title">📄 ใบโอนเงิน (Remittance Advice)</div>', unsafe_allow_html=True)
    st.markdown('<div class="box-info">📌 อัปโหลดใบโอนเงินจากห้างฯ — PDF หรือรูปภาพ JPG/PNG</div>', unsafe_allow_html=True)
    rem_file = st.file_uploader(
        "ใบโอนเงิน", type=["pdf","jpg","jpeg","png"],
        key="rem_up", label_visibility="collapsed")
    if rem_file:
        st.markdown(f'<div class="box-tip">✅ <strong>{rem_file.name}</strong> ({rem_file.size/1024:.1f} KB)</div>', unsafe_allow_html=True)
        if rem_file.type.startswith("image/"):
            st.image(rem_file, caption="Preview ใบโอนเงิน", use_container_width=True)

with col_r:
    st.markdown('<div class="card-title">🧾 ใบแจ้งหนี้ / บิลไปรษณีย์</div>', unsafe_allow_html=True)
    st.markdown('<div class="box-info">📌 ลากวางหลายไฟล์ได้พร้อมกัน — PDF จากเมล หรือรูปถ่ายบิล</div>', unsafe_allow_html=True)
    inv_files = st.file_uploader(
        "ใบแจ้งหนี้", type=["pdf","jpg","jpeg","png"],
        accept_multiple_files=True,
        key="inv_up", label_visibility="collapsed")
    if inv_files:
        st.markdown(
            f'<div class="box-tip">✅ รับแล้ว <strong>{len(inv_files)}</strong> ไฟล์:<br>'
            + "<br>".join(f"• {f.name} ({f.size/1024:.1f} KB)" for f in inv_files)
            + "</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# CALCULATE BUTTON
# ════════════════════════════════════════════════════════
bc, _, sc = st.columns([3, 1, 3])
with bc:
    # Red calculate button
    st.markdown('<div class="calc-btn">', unsafe_allow_html=True)
    calc_clicked = st.button("🔴  เริ่มคำนวณยันยอด", use_container_width=True, type="primary")
    st.markdown("</div>", unsafe_allow_html=True)

with sc:
    all_ready = has_promo and rem_file
    if all_ready:
        st.markdown('<div class="box-tip">✅ ข้อมูลครบ — กดเริ่มคำนวณได้เลย</div>', unsafe_allow_html=True)
    elif not has_promo and not rem_file:
        st.markdown('<div class="box-info">📂 กดคำนวณเพื่อดูข้อมูลจำลองก็ได้ครับ</div>', unsafe_allow_html=True)
    elif not has_promo:
        st.markdown('<div class="box-warn">⚠️ ยังไม่มีข้อมูลโปรโมชั่นฝั่งขาย</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="box-warn">⚠️ ยังไม่ได้อัปโหลดใบโอนเงิน</div>', unsafe_allow_html=True)

if calc_clicked:
    st.session_state["show_result"] = True
    st.session_state["calc_clicked"] = True


# ════════════════════════════════════════════════════════
# RESULTS
# ════════════════════════════════════════════════════════
if st.session_state["show_result"]:
    d    = MOCKUP_DB.get(selected_store, MOCKUP_DB[STORES[0]])
    invs = make_invoices(selected_store)
    df   = build_recon_df(selected_store)

    st.markdown("---")
    st.markdown(
        f"<h2 style='color:#1A3A5C;font-size:23px;font-weight:800;'>"
        f"📊 ผลการคำนวณยันยอด — {selected_store}</h2>",
        unsafe_allow_html=True)

    # Promo sources used
    src_labels = []
    if has_gdrive: src_labels.append("☁️ Google Drive")
    if has_manual: src_labels.append(f"📎 Manual ({len(promo_files)} ไฟล์)")
    if not src_labels: src_labels.append("🔵 ข้อมูลจำลอง (Demo)")
    st.markdown(
        f'<div class="box-promo">📦 <strong>รวมข้อมูลโปรโมชั่นจาก:</strong> '
        + " + ".join(src_labels) + "</div>",
        unsafe_allow_html=True)

    # Metrics
    n_over = sum(1 for k in ["sp","sd","sm","ss","so"] if d.get(k) == "over")
    m1,m2,m3,m4,m5 = st.columns(5)
    m1.metric("📄 เลขที่เอกสาร",  d["doc"])
    m2.metric("📅 วันที่โอน",      d["date"])
    m3.metric("🗓️ รอบบิล",         d["period"])
    m4.metric("💰 ยอดโอนรวม",     f'฿{d["total"]:,.0f}')
    m5.metric("❌ หักเกิน",         f"{n_over} รายการ")

    st.markdown("<br>", unsafe_allow_html=True)

    # Remittance detail
    with st.expander("🏢 ข้อมูลนิติบุคคลและใบโอนเงิน", expanded=True):
        r1,r2,r3,r4 = st.columns(4)
        r1.metric("บริษัทที่ออกบิล",  d["billing_co"])
        r2.metric("ยอดโอนรวม",        f'฿{d["total"]:,.2f}')
        r3.metric("รวมหักทั้งหมด",    f'฿{d["promo"]+d["dc"]+d["mkt"]+d["ship"]+d["other"]:,.2f}')
        r4.metric("ยอดสุทธิ",          f'฿{d["net"]:,.2f}')
        if selected_store in CPAXT_STORES:
            st.markdown('<div class="box-warn">🏢 <strong>กลุ่ม CPAXT</strong> — ตรวจสอบให้ครบทั้ง 3 ช่องทาง: หน้าร้าน · Online/PRO · Wholesale</div>', unsafe_allow_html=True)

    # ── Reconciliation table ─────────────────────────
    st.markdown(
        "<h3 style='color:#3A8EDE;font-size:19px;font-weight:800;margin-top:18px;'>"
        "📑 ตารางเปรียบเทียบ — ยอดห้าง VS ยอดคำนวณจริง (แยก 4 หมวด)</h3>",
        unsafe_allow_html=True)
    st.dataframe(style_df(df), use_container_width=True, height=310)

    # ── Alert banner ─────────────────────────────────
    over_items = [
        label for label, sk in [
            ("ส่วนลดโปรโมชั่น","sp"),("ค่า DC","sd"),
            ("ค่าการตลาด","sm"),("ค่าขนส่ง","ss"),("อื่นๆ","so")
        ] if d.get(sk) == "over"
    ]
    if over_items:
        st.markdown(
            f'<div class="box-error">'
            f'❌ <strong>ห้างหักเงินเกิน {len(over_items)} รายการ:</strong> '
            + " &nbsp;·&nbsp; ".join(f"<u>{x}</u>" for x in over_items)
            + "<br>กรุณาตรวจสอบเอกสารและติดต่อห้างฯ เพื่อขอเครดิตคืน"
            + "</div>", unsafe_allow_html=True)
    else:
        st.markdown('<div class="box-tip">✅ ยอดตรงกันทุกรายการ — ไม่พบความคลาดเคลื่อน</div>', unsafe_allow_html=True)

    # ── Invoice detail ────────────────────────────────
    with st.expander(f"🧾 รายละเอียดใบแจ้งหนี้ ({len(invs)} รายการ)", expanded=False):
        inv_df = pd.DataFrame([{
            "เลขที่ Invoice": i["invoice_no"], "วันที่": i["date"],
            "ประเภท": i["type"], "ยอดก่อน VAT": fmt(i["subtotal"]),
            "VAT (7%)": fmt(i["vat"]), "ยอดรวม": fmt(i["total"]),
        } for i in invs])
        st.dataframe(
            inv_df.style
            .set_properties(**{"font-size":"15px","text-align":"center"})
            .set_properties(subset=["ประเภท"], **{"text-align":"left","font-weight":"700"}),
            use_container_width=True)

    # ── Promo files detail ────────────────────────────
    if has_manual:
        with st.expander(f"📎 ไฟล์โปรโมชั่น Manual Upload ({len(promo_files)} ไฟล์)", expanded=False):
            for f in promo_files:
                ext  = f.name.rsplit(".",1)[-1].upper()
                icon = "📊" if ext in ("XLSX","XLS") else ("📄" if ext=="PDF" else "🖼️")
                st.markdown(
                    f'<div class="step-row">'
                    f'<div style="font-size:20px">{icon}</div>'
                    f'<div class="step-text"><strong>{f.name}</strong> &nbsp;'
                    f'<span style="color:#5A7BA8;font-size:13px;">({f.size/1024:.1f} KB · {ext})</span></div>'
                    f'</div>',
                    unsafe_allow_html=True)

    # ── Bar chart ─────────────────────────────────────
    st.markdown(
        "<h3 style='color:#3A8EDE;font-size:18px;font-weight:800;margin-top:20px;'>"
        "📈 เปรียบเทียบค่าใช้จ่ายรายหมวด</h3>",
        unsafe_allow_html=True)
    chart_df = pd.DataFrame({
        "หมวด": ["ส่วนลดโปรโมชั่น","ค่า DC","ค่าการตลาด","ค่าขนส่ง","อื่นๆ"],
        "ยอดห้าง":   [d["promo"], d["dc"], d["mkt"], d["ship"], d["other"]],
        "ยอดคำนวณ": [
            sum(i["total"] for i in invs if i["type"]=="ส่วนลดโปรโมชั่น"),
            sum(i["total"] for i in invs if i["type"]=="ค่า DC"),
            sum(i["total"] for i in invs if i["type"]=="ค่าการตลาด"),
            sum(i["total"] for i in invs if i["type"]=="ค่าขนส่ง"),
            d["other"],
        ],
    }).set_index("หมวด")
    st.bar_chart(chart_df, height=260, use_container_width=True)

    # ── Export ────────────────────────────────────────
    st.markdown("---")
    st.markdown("<h3 style='color:#3A8EDE;font-size:18px;font-weight:800;'>📥 Export รายงาน</h3>", unsafe_allow_html=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    sn = selected_store[:20].replace("/","-").replace(" ","_").replace("(","").replace(")","")

    e1, e2, e3 = st.columns(3)
    with e1:
        st.download_button("📊 Reconciliation (.xlsx)",
                           data=to_excel(df),
                           file_name=f"recon_{sn}_{ts}.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)
    with e2:
        inv_export = pd.DataFrame([{
            "Invoice No": i["invoice_no"],"วันที่": i["date"],"ประเภท": i["type"],
            "ยอดก่อน VAT": i["subtotal"],"VAT": i["vat"],"ยอดรวม": i["total"]
        } for i in invs])
        st.download_button("🧾 Invoice Detail (.xlsx)",
                           data=to_excel(inv_export),
                           file_name=f"invoices_{sn}_{ts}.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)
    with e3:
        full = json.dumps({
            "store": selected_store, "billing_company": d["billing_co"],
            "timestamp": datetime.now().isoformat(),
            "promo_sources": {
                "gdrive": gdrive if has_gdrive else None,
                "manual_files": [f.name for f in promo_files] if has_manual else [],
            },
            "remittance": d, "invoices": invs,
        }, ensure_ascii=False, indent=2)
        st.download_button("📋 Full Data (.json)",
                           data=full.encode("utf-8"),
                           file_name=f"full_{sn}_{ts}.json",
                           mime="application/json",
                           use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 เริ่มใหม่ / Clear All"):
        st.session_state["show_result"]  = False
        st.session_state["calc_clicked"] = False
        st.rerun()

# ── Footer ─────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:16px;border-top:2.5px solid #C5DEFF;margin-top:16px;">
    <p style="color:#5A7BA8;font-size:13px;margin:0;">
        🤖 <strong>Modern Trade Reconciliation AI</strong> · Mockup Demo v2.2 · Hybrid Promo Input · Streamlit<br>
        <span style="font-size:11px;opacity:.65;">© 2025 · ข้อมูลในหน้านี้เป็นข้อมูลจำลองเพื่อสาธิตเท่านั้น</span>
    </p>
</div>
""", unsafe_allow_html=True)
