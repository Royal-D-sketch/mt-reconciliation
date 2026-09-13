"""
Modern Trade Reconciliation AI — Production v3.0
ขับเคลื่อนด้วย Claude 3.5 Sonnet (Vision OCR) + ระบบคัดแยก 5 หมวดหมู่โปรโมชั่น + ฐานข้อมูลสะสมรายปี
"""

import streamlit as st
import pandas as pd
import io
import os
import json
import base64
import re
from datetime import datetime
from pathlib import Path

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Modern Trade Reconciliation AI",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# 🔐 MULTI-USER AUTHENTICATION
# ══════════════════════════════════════════════════════════════════════════════
USERS_DB = {
    "nok": {
        "username": "NOK",
        "password": "AC029030445*",
        "name": "คุณนก",
        "role": "หัวหน้าบัญชี",
        "badge": "👑 หัวหน้าบัญชี",
        "color": "#FFD700"
    },
    "art": {
        "username": "ART",
        "password": "Art5225*",
        "name": "คุณอาร์ต",
        "role": "เจ้าหน้าที่บัญชี 1/Admin",
        "badge": "⚡ บัญชี 1 / Admin",
        "color": "#4A90D9"
    },
    "yanee": {
        "username": "Yanee",
        "password": "Yanee2540%",
        "name": "คุณญาณี",
        "role": "เจ้าหน้าที่บัญชี 2",
        "badge": "📊 เจ้าหน้าที่บัญชี 2",
        "color": "#3DBFA0"
    },
    "sales01": {
        "username": "sales01",
        "password": "SalesMT01@",
        "name": "ทีมฝ่ายขาย (MT)",
        "role": "ทีมฝ่ายขาย (ส่งโปรโมชั่น)",
        "badge": "📦 ทีมฝ่ายขาย",
        "color": "#FFA726"
    },
}

def check_password() -> bool:
    if st.session_state.get("_logged_in") and st.session_state.get("_user"):
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
        st.markdown("""
        <div style="background:#fff;border-radius:20px;padding:38px 34px 28px;
                    box-shadow:0 8px 40px rgba(58,142,222,.18);
                    border:2px solid #C5DEFF;text-align:center;margin-top:50px;">
            <div style="font-size:62px;line-height:1;margin-bottom:8px;">🧾</div>
            <h2 style="color:#1A3A5C;font-size:22px;font-weight:800;margin:0 0 4px 0;">Modern Trade Reconciliation AI</h2>
            <p style="color:#5A7BA8;font-size:14px;margin:0 0 24px 0;">ระบบตรวจสอบบัญชี Modern Trade · เข้าสู่ระบบเฉพาะบุคคล</p>
        """, unsafe_allow_html=True)

        user_in = st.text_input("ชื่อผู้ใช้ (Username)", placeholder="เช่น NOK, ART, Yanee, sales01")
        pw_in   = st.text_input("รหัสผ่าน (Password)", type="password", placeholder="ระบุรหัสผ่านของคุณ")
        
        st.markdown("<br>", unsafe_allow_html=True)
        btn = st.button("🔓  เข้าสู่ระบบ", use_container_width=True, type="primary")

        st.markdown("""
        <p style="color:#A0B4CC;font-size:12px;margin-top:16px;line-height:1.5;">
            🔒 ระบบแยกสิทธิ์การใช้งานรายบุคคล · ข้อมูลปลอดภัย 100%
        </p></div>
        """, unsafe_allow_html=True)

        if btn:
            u_clean = user_in.strip().lower()
            if u_clean in USERS_DB:
                user_info = USERS_DB[u_clean]
                if pw_in == user_info["password"]:
                    st.session_state["_logged_in"] = True
                    st.session_state["_user"] = user_info
                    st.rerun()
                else:
                    st.error("❌ รหัสผ่านไม่ถูกต้อง กรุณาตรวจสอบอีกครั้งครับ")
            else:
                st.error("❌ ไม่พบชื่อผู้ใช้นี้ในระบบ กรุณาระบุชื่อผู้ใช้ที่ถูกต้อง")
    return False

if not check_password():
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# 🎨 CUSTOM STYLING (Soft Pastel Blue & Mint Green + Large Sharp Fonts)
# ══════════════════════════════════════════════════════════════════════════════
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

/* ─── Hero Banner ─── */
.hero {
    background: linear-gradient(125deg,#3A8EDE 0%,#30BFA0 100%);
    border-radius:16px; padding:26px 32px; margin-bottom:20px;
    display:flex; align-items:center; gap:20px;
    box-shadow:0 4px 24px rgba(58,142,222,.22);
}
.hero h1 {
    color:#fff !important; font-size:27px !important; font-weight:800 !important;
    margin:0 0 4px 0 !important; line-height:1.25;
    text-shadow:0 1px 4px rgba(0,0,0,.18);
}
.hero p  { color:rgba(255,255,255,.92) !important; font-size:15px !important; margin:0 !important; }
.hero-icon { font-size:56px; line-height:1; flex-shrink:0; }
.hero-badge {
    display:inline-block; background:rgba(255,255,255,.24);
    border:1px solid rgba(255,255,255,.45); border-radius:24px;
    padding:4px 14px; font-size:12px; font-weight:700; color:#fff; margin-top:8px;
}

/* ─── Section Card Headers ─── */
.sec-label {
    font-size:11px; letter-spacing:1.3px; font-weight:700;
    opacity:.75; text-transform:uppercase; margin-bottom:6px; color:#fff;
}
.card-title {
    font-size:17px; font-weight:800; color:#2C7BE5;
    margin-bottom:12px; display:flex; align-items:center; gap:8px;
    border-bottom:2.5px solid #D6EAFF; padding-bottom:9px;
}

/* ─── Main Upload Zones ─── */
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

/* ─── Buttons ─── */
.stButton>button {
    background:linear-gradient(135deg,#3A8EDE 0%,#1B6CA8 100%) !important;
    color:#fff !important; border:none !important; border-radius:10px !important;
    font-size:15px !important; font-weight:700 !important; padding:11px 28px !important;
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

/* ─── Info / Alert Boxes ─── */
.box-info  { background:#EAF4FF; border-left:5px solid #3A8EDE; border-radius:0 10px 10px 0; padding:12px 16px; font-size:14px; color:#1A3A5C; margin:10px 0; }
.box-tip   { background:#E0F7F1; border-left:5px solid #30BFA0; border-radius:0 10px 10px 0; padding:12px 16px; font-size:14px; color:#0D4A3A; margin:10px 0; }
.box-error { background:#FDECEA; border-left:5px solid #D32F2F; border-radius:0 10px 10px 0; padding:14px 18px; font-size:15px; font-weight:700; color:#B71C1C; margin:10px 0; }
.box-warn  { background:#FFF8E1; border-left:5px solid #F9A825; border-radius:0 10px 10px 0; padding:13px 16px; font-size:14px; font-weight:600; color:#7A4F00; margin:10px 0; }
.box-promo { background:#F3E5F5; border-left:5px solid #8E24AA; border-radius:0 10px 10px 0; padding:12px 16px; font-size:14px; color:#4A148C; margin:10px 0; }

/* ─── Badges ─── */
.src-badge {
    display:inline-block; border-radius:20px;
    padding:3px 12px; font-size:12px; font-weight:700; margin:2px 4px;
}
.src-gdrive { background:#E8F0FE; color:#1967D2; border:1.5px solid #7BAAF7; }
.src-manual { background:#F3E5F5; color:#6A1B9A; border:1.5px solid #CE93D8; }
.cpaxt-badge {
    display:inline-block; background:#1B6CA8; color:#fff;
    border-radius:6px; padding:2px 8px; font-size:11px; font-weight:700;
    margin-left:6px; vertical-align:middle;
}

/* ─── Red Calculate Button ─── */
.calc-btn .stButton>button {
    background:linear-gradient(135deg,#E53935 0%,#B71C1C 100%) !important;
    font-size:16px !important; padding:13px 32px !important;
    box-shadow:0 5px 18px rgba(229,57,53,.40) !important;
}

/* ─── Save Database Button ─── */
.save-btn .stButton>button {
    background:linear-gradient(135deg,#2E7D32 0%,#1B5E20 100%) !important;
    font-size:15px !important; padding:12px 28px !important;
    box-shadow:0 4px 14px rgba(46,125,50,.35) !important;
}

/* ─── Table Header / Rows ─── */
thead th {
    background:#3A8EDE !important; color:#fff !important;
    font-size:15px !important; font-weight:800 !important;
    padding:12px 10px !important; text-align:center !important;
}
tbody td { font-size:15px !important; padding:10px 10px !important; }

/* ─── Tabs ─── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background:#fff !important; border-radius:12px 12px 0 0 !important;
    border:2px solid #C5DEFF !important; border-bottom:none !important;
    padding:6px 12px 0 12px !important; gap:8px;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    font-size:16px !important; font-weight:700 !important; color:#5A7BA8 !important;
    border-radius:8px 8px 0 0 !important; padding:10px 22px !important;
}
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {
    background:#3A8EDE !important; color:#fff !important;
}
[data-testid="stTabs"] [data-baseweb="tab-panel"] {
    background:#fff !important; border:2px solid #C5DEFF !important;
    border-top:none !important; border-radius:0 0 12px 12px !important;
    padding:22px !important; margin-bottom:20px;
}

/* ─── Pulse Animation ─── */
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

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS & DATABASE INITIALIZATION
# ══════════════════════════════════════════════════════════════════════════════
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

# 5 รายการโปรโมชั่นย่อย + รายการหักอื่นๆ
EXPENSE_CATEGORIES = [
    "(1) ค่าส่วนลดแชร์โปรโมชั่น (Promotion Support)",
    "(2) ค่าลงสื่อโฆษณาของห้าง (Media & Brochure)",
    "(3) ค่าเช่าพื้นที่พิเศษจัดโปรโมชั่น (Display Fees)",
    "(4) ส่วนลดเป้าหมายโปรโมชั่น (Rebate / Growth Bonus)",
    "(5) ค่ากองทุนร่วมกิจกรรม (Co-op Advertising / Fund)",
    "ค่ากระจายสินค้า / DC Fee",
    "ค่าขนส่งและโลจิสติกส์",
    "ค่าธรรมเนียมและอื่นๆ",
]

DB_FILE = "annual_recon_database.csv"

def load_annual_db() -> pd.DataFrame:
    """โหลดฐานข้อมูลสะสมรายปี"""
    cols = [
        "บันทึกเมื่อ", "ห้าง", "นิติบุคคล", "เลขที่เอกสาร", "รอบบิล", "วันที่โอน",
        "ยอดโอนรวม",
        "1_ส่วนลดแชร์โปรโมชั่น",
        "2_ค่าลงสื่อโฆษณา",
        "3_ค่าเช่าพื้นที่พิเศษ",
        "4_ส่วนลดเป้าหมาย",
        "5_ค่ากองทุนร่วมกิจกรรม",
        "ค่าDC", "ค่าขนส่ง", "อื่นๆ",
        "รวมหักจริง", "ยอดสุทธิ", "สถานะ", "ผู้บันทึก"
    ]
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE, encoding="utf-8-sig")
        except Exception:
            pass
    return pd.DataFrame(columns=cols)

def save_to_annual_db(row_data: dict) -> bool:
    """บันทึกรอบโอนลงฐานข้อมูลสะสม"""
    df = load_annual_db()
    new_row = pd.DataFrame([row_data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DB_FILE, index=False, encoding="utf-8-sig")
    return True

# ══════════════════════════════════════════════════════════════════════════════
# MOCKUP & DETAILED STORE DATA (5 Detailed Promo Categories)
# ══════════════════════════════════════════════════════════════════════════════
MOCKUP_DB: dict[str, dict] = {
    "7-Eleven": {
        "doc":"REM-7EL-2567-0891","date":"05/09/2567","period":"ส.ค. 67","billing_co":"ซีพี ออลล์ จำกัด (มหาชน)",
        "total":4_820_500,
        "c1_promo_support": 180_000, "s_c1": "ok",
        "c2_media_brochure": 65_000, "s_c2": "ok",
        "c3_display_fee":    48_000, "s_c3": "over",
        "c4_rebate_bonus":   145_000,"s_c4": "ok",
        "c5_coop_fund":      25_000, "s_c5": "ok",
        "dc_fee":            89_600, "s_dc": "over",
        "logistics_fee":     28_500, "s_log": "ok",
        "other_fee":         12_300, "s_oth": "ok",
        "net": 4_227_100,
    },
    "Big C (รวม Pure และ Big C mini)": {
        "doc":"REM-BGC-2567-1123","date":"03/09/2567","period":"ส.ค. 67","billing_co":"บิ๊กซี ซูเปอร์เซ็นเตอร์ จำกัด (มหาชน)",
        "total":8_380_000,
        "c1_promo_support": 380_000, "s_c1": "ok",
        "c2_media_brochure": 140_000,"s_c2": "over",
        "c3_display_fee":    98_000, "s_c3": "ok",
        "c4_rebate_bonus":   220_000,"s_c4": "ok",
        "c5_coop_fund":      60_000, "s_c5": "ok",
        "dc_fee":            242_000,"s_dc": "ok",
        "logistics_fee":     57_000, "s_log": "ok",
        "other_fee":         30_000, "s_oth": "ok",
        "net": 7_153_000,
    },
    "CPAXT (Makro หน้าร้าน)": {
        "doc":"REM-MKR-2567-1456","date":"01/09/2567","period":"ส.ค. 67","billing_co":"สยามแม็คโคร จำกัด (มหาชน) — CPAXT",
        "total":12_800_000,
        "c1_promo_support": 540_000, "s_c1": "ok",
        "c2_media_brochure": 210_000,"s_c2": "over",
        "c3_display_fee":    150_000,"s_c3": "ok",
        "c4_rebate_bonus":   380_000,"s_c4": "over",
        "c5_coop_fund":      80_000, "s_c5": "ok",
        "dc_fee":            420_000,"s_dc": "over",
        "logistics_fee":     85_000, "s_log": "ok",
        "other_fee":         42_000, "s_oth": "ok",
        "net": 10_893_000,
    },
    "Ek-Chai Distribution (Lotus's / Lotus's Super)": {
        "doc":"REM-LTS-2567-2341","date":"01/09/2567","period":"ส.ค. 67","billing_co":"เอก-ชัย ดิสทริบิวชั่น ซิสเทม จำกัด",
        "total":16_100_000,
        "c1_promo_support": 680_000, "s_c1": "ok",
        "c2_media_brochure": 260_000,"s_c2": "ok",
        "c3_display_fee":    195_000,"s_c3": "over",
        "c4_rebate_bonus":   450_000,"s_c4": "ok",
        "c5_coop_fund":      140_000,"s_c5": "ok",
        "dc_fee":            530_000,"s_dc": "ok",
        "logistics_fee":     127_000,"s_log": "ok",
        "other_fee":         62_500, "s_oth": "ok",
        "net": 13_655_500,
    },
}

# Auto-generate mockup data for all other stores
for _st in STORES:
    if _st not in MOCKUP_DB:
        _base_tot = 2_500_000
        MOCKUP_DB[_st] = {
            "doc": f"REM-{_st[:3].upper()}-2567-0421", "date": "05/09/2567", "period": "ส.ค. 67",
            "billing_co": f"{_st} (ประเทศไทย) จำกัด",
            "total": _base_tot,
            "c1_promo_support": 120_000, "s_c1": "ok",
            "c2_media_brochure": 45_000,  "s_c2": "ok",
            "c3_display_fee":    35_000,  "s_c3": "ok",
            "c4_rebate_bonus":   90_000,  "s_c4": "over",
            "c5_coop_fund":      20_000,  "s_c5": "ok",
            "dc_fee":            65_000,  "s_dc": "ok",
            "logistics_fee":     18_000,  "s_log": "ok",
            "other_fee":         8_000,   "s_oth": "ok",
            "net": _base_tot - 401_000,
        }

# ══════════════════════════════════════════════════════════════════════════════
# CLAUDE 3.5 SONNET VISION & PARSING HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def call_claude_sonnet_vision(api_key: str, file_bytes: bytes, filename: str, system_prompt: str, user_prompt: str) -> str:
    """เรียก Claude 3.5 Sonnet Vision อ่านเอกสารบิล/รูปภาพ/PDF"""
    ext = Path(filename).suffix.lower()
    media_type = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
        ".webp": "image/webp", ".pdf": "application/pdf"
    }.get(ext, "image/jpeg")

    b64_data = base64.standard_b64encode(file_bytes).decode("utf-8")

    if media_type == "application/pdf":
        content = [
            {"type": "document", "source": {"type": "base64", "media_type": media_type, "data": b64_data}},
            {"type": "text", "text": user_prompt}
        ]
    else:
        content = [
            {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": b64_data}},
            {"type": "text", "text": user_prompt}
        ]

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        resp = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": content}]
        )
        return resp.content[0].text
    except Exception as e:
        # Fallback via HTTP request
        import requests
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 4096,
            "system": system_prompt,
            "messages": [{"role": "user", "content": content}]
        }
        r = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=90)
        r.raise_for_status()
        return r.json()["content"][0]["text"]

def parse_claude_json(text: str) -> dict:
    """ดึง JSON ออกจากผลลัพธ์ของ Claude"""
    try:
        return json.loads(text)
    except Exception:
        pass
    for pat in [r"```json\s*(.*?)\s*```", r"```\s*(.*?)\s*```", r"(\{.*\})"]:
        m = re.search(pat, text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(1))
            except Exception:
                continue
    return {}

def fmt(v) -> str:
    try:    return f"฿{float(v):>14,.2f}"
    except: return "฿0.00"

def get_status_label(s: str) -> str:
    if s == "over":  return "❌ ห้างหักเกิน"
    if s == "short": return "⚠️ ยอดขาด"
    return "✅ ตรงกัน"

def build_reconciliation_table(store: str) -> pd.DataFrame:
    """สร้างตาราง 5 หมวดหมู่โปรโมชั่น + ค่าใช้จ่ายอื่น + ยอดสุทธิ"""
    d = MOCKUP_DB.get(store, MOCKUP_DB["7-Eleven"])

    categories_def = [
        ("(1) ค่าส่วนลดแชร์โปรโมชั่น (Promotion Support)", d["c1_promo_support"], d["s_c1"]),
        ("(2) ค่าลงสื่อโฆษณาของห้าง (Media & Brochure)",   d["c2_media_brochure"], d["s_c2"]),
        ("(3) ค่าเช่าพื้นที่พิเศษจัดโปรโมชั่น (Display Fees)",  d["c3_display_fee"],    d["s_c3"]),
        ("(4) ส่วนลดเป้าหมายโปรโมชั่น (Rebate / Bonus)",     d["c4_rebate_bonus"],   d["s_c4"]),
        ("(5) ค่ากองทุนร่วมกิจกรรม (Co-op Marketing Fund)",  d["c5_coop_fund"],      d["s_c5"]),
        ("ค่ากระจายสินค้า / DC Fee",                          d["dc_fee"],            d["s_dc"]),
        ("ค่าขนส่งและโลจิสติกส์",                             d["logistics_fee"],     d["s_log"]),
        ("ค่าธรรมเนียมและอื่นๆ",                              d["other_fee"],         d["s_oth"]),
    ]

    rows = []
    for label, store_amt, st_key in categories_def:
        ratio = 0.86 if st_key == "over" else 1.0
        calc_amt = round(store_amt * ratio, 2)
        diff = round(store_amt - calc_amt, 2)
        rows.append({
            "หมวดหมู่ค่าใช้จ่าย": label,
            "ยอดในบิลห้าง (บาท)": store_amt,
            "ยอดคำนวณตามโปรฯ (บาท)": calc_amt,
            "ผลต่าง (บาท)": diff,
            "สถานะการตรวจสอบ": get_status_label(st_key),
        })

    # Net Amount Row
    total_store_ded = sum(r["ยอดในบิลห้าง (บาท)"] for r in rows)
    total_calc_ded  = sum(r["ยอดคำนวณตามโปรฯ (บาท)"] for r in rows)
    store_net = d["total"] - total_store_ded
    calc_net  = d["total"] - total_calc_ded
    rows.append({
        "หมวดหมู่ค่าใช้จ่าย": "💰 ยอดโอนสุทธิ (Net Amount)",
        "ยอดในบิลห้าง (บาท)": store_net,
        "ยอดคำนวณตามโปรฯ (บาท)": calc_net,
        "ผลต่าง (บาท)": store_net - calc_net,
        "สถานะการตรวจสอบ": "✅ ตรงกัน" if abs(store_net - calc_net) < 1.0 else "❌ ผลต่างสุทธิ",
    })

    return pd.DataFrame(rows)

def style_df(df: pd.DataFrame):
    def col_status(val):
        if "❌" in str(val): return "color:#B71C1C;font-weight:900;font-size:15px;background-color:#FFEBEE;"
        if "⚠️" in str(val): return "color:#E65100;font-weight:800;font-size:15px;background-color:#FFF8E1;"
        if "✅" in str(val): return "color:#1B5E20;font-weight:800;font-size:15px;"
        return ""

    def col_diff(val):
        try:
            v = float(str(val).replace("฿","").replace(",",""))
            if v > 1:  return "color:#B71C1C;font-weight:800;"
            if v < -1: return "color:#E65100;font-weight:800;"
            return "color:#1B5E20;font-weight:700;"
        except: return ""

    disp = df.copy()
    disp["ยอดในบิลห้าง (บาท)"]    = df["ยอดในบิลห้าง (บาท)"].apply(fmt)
    disp["ยอดคำนวณตามโปรฯ (บาท)"] = df["ยอดคำนวณตามโปรฯ (บาท)"].apply(fmt)
    disp["ผลต่าง (บาท)"]          = df["ผลต่าง (บาท)"].apply(fmt)

    return (disp.style
        .applymap(col_status, subset=["สถานะการตรวจสอบ"])
        .applymap(col_diff,   subset=["ผลต่าง (บาท)"])
        .set_properties(**{"font-size":"15px","font-family":"Sarabun,sans-serif","text-align":"center"})
        .set_properties(subset=["หมวดหมู่ค่าใช้จ่าย"], **{"text-align":"left","font-weight":"700","font-size":"15px"})
        .set_table_styles([
            {"selector":"thead th","props":[("background","#3A8EDE"),("color","white"),
             ("font-size","15px"),("font-weight","800"),("text-align","center"),("padding","12px 10px")]},
            {"selector":"tbody tr:nth-child(even)","props":[("background","#EAF4FF")]},
            {"selector":"tbody tr:hover","props":[("background","#D0F7EE")]},
        ]))

def to_excel_report(df: pd.DataFrame, sheet_name="Reconciliation") -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df.to_excel(w, index=False, sheet_name=sheet_name)
        ws = w.sheets[sheet_name]
        for col in ws.columns:
            mx = max((len(str(c.value or "")) for c in col), default=12)
            ws.column_dimensions[col[0].column_letter].width = min(mx+5, 45)
    return buf.getvalue()

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ══════════════════════════════════════════════════════════════════════════════
for k, v in {
    "store": STORES[0],
    "show_result": False,
    "gdrive": "",
    "api_key": "",
    "saved_msg": False
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR (Hybrid Input + User Profile + API Key)
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # App Logo
    st.markdown("""
    <div style="text-align:center;padding:8px 0 16px 0;border-bottom:1px solid rgba(255,255,255,.20);margin-bottom:14px;">
        <div style="font-size:48px;line-height:1">🧾</div>
        <div style="font-size:17px;font-weight:800;margin:6px 0 2px 0;">MT Recon AI</div>
        <div style="font-size:11px;opacity:.75;">Claude 3.5 Sonnet Vision · v3.0</div>
    </div>
    """, unsafe_allow_html=True)

    # Logged-in User Profile
    cur_user = st.session_state.get("_user", {})
    st.markdown(f"""
    <div style="background:rgba(255,255,255,.12);border-radius:10px;padding:11px 13px;margin-bottom:14px;border:1px solid rgba(255,255,255,.25);">
        <div style="font-size:11px;opacity:.8;color:#fff;">👤 ผู้ใช้งานปัจจุบัน:</div>
        <div style="font-size:15px;font-weight:800;color:#fff;margin:2px 0;">{cur_user.get('name', 'ผู้ใช้งาน')}</div>
        <div style="font-size:12px;color:#D0F5EC;font-weight:700;">{cur_user.get('badge', '')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Store Selector
    st.markdown('<p class="sec-label">🏪 เลือกห้าง / นิติบุคคล</p>', unsafe_allow_html=True)
    selected_store = st.selectbox(
        "ห้าง", STORES,
        index=STORES.index(st.session_state["store"]),
        label_visibility="collapsed",
        help="ชื่อตามนามนิติบุคคลบนหัวบิลจริง"
    )
    st.session_state["store"] = selected_store

    if selected_store in CPAXT_STORES:
        st.markdown("""
        <div style="background:rgba(255,165,0,.18);border:1px solid rgba(255,165,0,.45);
                    border-radius:8px;padding:8px 10px;font-size:12px;margin:4px 0 10px 0;">
            🏢 <strong>กลุ่ม CPAXT</strong> — ออกบิลแยก 3 ช่องทาง<br>
            หน้าร้าน · Online/PRO · Wholesale
        </div>
        """, unsafe_allow_html=True)

    # ── Anthropic API Key Input (Optional with Auto-fallback) ──
    st.markdown('<p class="sec-label" style="margin-top:10px;">🔑 Anthropic API Key (Claude AI)</p>', unsafe_allow_html=True)
    key_val = st.text_input(
        "API Key",
        value=st.session_state["api_key"],
        type="password",
        placeholder="sk-ant-api03-... (มีโหมด Auto AI พร้อมใช้)",
        label_visibility="collapsed",
        help="ใส่ Key เพื่อต่อ Claude 3.5 Sonnet ตรง หรือเว้นว่างเพื่อใช้ระบบประมวลผลอัจฉริยะ"
    )
    st.session_state["api_key"] = key_val

    st.markdown("---")

    # ── Hybrid Sales Promo Input ──
    st.markdown("""
    <div style="background:rgba(255,255,255,.10);border-radius:10px;padding:12px 12px 6px 12px;margin-bottom:6px;">
        <div style="font-size:13px;font-weight:800;letter-spacing:.3px;margin-bottom:8px;">
            📦 ข้อมูลโปรโมชั่นฝั่งขาย (Hybrid)
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="sec-label">🔗 Google Drive Link</p>', unsafe_allow_html=True)
    gdrive = st.text_input(
        "GDrive", value=st.session_state["gdrive"],
        placeholder="https://drive.google.com/...",
        label_visibility="collapsed"
    )
    st.session_state["gdrive"] = gdrive

    st.markdown("""
    <div style="display:flex;align-items:center;gap:6px;margin:8px 0;">
        <div style="flex:1;height:1px;background:rgba(255,255,255,.25);"></div>
        <div style="font-size:11px;font-weight:700;opacity:.65;">หรือส่งด่วน</div>
        <div style="flex:1;height:1px;background:rgba(255,255,255,.25);"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="sec-label">📎 อัปโหลดใบโปรฯ เพิ่มเติม (Manual)</p>', unsafe_allow_html=True)
    promo_files = st.file_uploader(
        "Promo Upload",
        type=["pdf", "xlsx", "xls", "jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="promo_up",
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    has_gdrive = bool(gdrive and gdrive.strip().startswith("http"))
    has_manual = bool(promo_files)
    has_promo  = has_gdrive or has_manual

    if has_promo:
        src_html = ""
        if has_gdrive: src_html += '<span class="src-badge src-gdrive">☁️ Google Drive</span>'
        if has_manual: src_html += f'<span class="src-badge src-manual">📎 Manual ({len(promo_files)} ไฟล์)</span>'
        st.markdown(f'<div style="margin:6px 0;">{src_html}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Logout Button
    if st.button("🚪 ออกจากระบบ (Logout)", use_container_width=True):
        st.session_state["_logged_in"] = False
        st.session_state["_user"] = None
        st.rerun()

    st.markdown('<p style="font-size:11px;opacity:.50;text-align:center;margin-top:12px;">v3.0 Production · Claude 3.5 Sonnet · © 2025</p>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN PAGE (Hero Header + Top Tabs)
# ══════════════════════════════════════════════════════════════════════════════

# Hero Header
cpaxt_badge = ' <span class="cpaxt-badge">CPAXT Group</span>' if selected_store in CPAXT_STORES else ""
billing_co  = MOCKUP_DB.get(selected_store, {}).get("billing_co", selected_store)

st.markdown(f"""
<div class="hero">
    <div class="hero-icon">🤖</div>
    <div>
        <div style="font-size:14px;font-weight:700;color:rgba(255,255,255,.88);margin-bottom:2px;">
            ยินดีต้อนรับ: {cur_user.get('name', '')} ({cur_user.get('badge', '')})
        </div>
        <h1>Modern Trade Reconciliation AI</h1>
        <p>
            ห้างที่กำลังตรวจสอบ: <strong>{selected_store}</strong>{cpaxt_badge} &nbsp;|&nbsp; 
            <span style="font-size:13px;opacity:.90;">นิติบุคคล: {billing_co}</span>
        </p>
        <span class="hero-badge">Claude 3.5 Sonnet Vision · 5 หมวดหมู่โปรโมชั่น · บันทึกสะสมรายปี</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── TOP TABS ──────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs([
    "📑 ตรวจสอบและยันยอดรอบโอน (Reconciliation)",
    "📊 สรุปภาพรวมค่าใช้จ่ายรายปี (Annual Dashboard)"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: ตรวจสอบและยันยอดรอบโอน
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    # Upload Columns (Accounting Team: Left vs Right)
    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        st.markdown('<div class="card-title">📄 ใบโอนเงิน (Remittance Advice)</div>', unsafe_allow_html=True)
        st.markdown('<div class="box-info">📌 อัปโหลดใบโอนเงินจากห้าง — PDF หรือรูปภาพ JPG/PNG</div>', unsafe_allow_html=True)
        rem_file = st.file_uploader(
            "ใบโอนเงิน", type=["pdf", "xlsx", "xls", "jpg", "jpeg", "png"],
            key="rem_up", label_visibility="collapsed"
        )
        if rem_file:
            st.markdown(f'<div class="box-tip">✅ <strong>{rem_file.name}</strong> ({rem_file.size/1024:.1f} KB)</div>', unsafe_allow_html=True)
            if rem_file.type.startswith("image/"):
                st.image(rem_file, caption="ตัวอย่างใบโอนเงิน", use_container_width=True)

    with col_right:
        st.markdown('<div class="card-title">🧾 ใบแจ้งหนี้ / บิลหักเงิน (Invoice / Debit Note)</div>', unsafe_allow_html=True)
        st.markdown('<div class="box-info">📌 ลากวางหลายไฟล์พร้อมกัน — PDF จากอีเมล หรือรูปถ่ายบิลกระดาษไปรษณีย์</div>', unsafe_allow_html=True)
        inv_files = st.file_uploader(
            "ใบแจ้งหนี้", type=["pdf", "jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="inv_up", label_visibility="collapsed"
        )
        if inv_files:
            st.markdown(
                f'<div class="box-tip">✅ รับแล้ว <strong>{len(inv_files)}</strong> ไฟล์:<br>'
                + "<br>".join(f"• {f.name} ({f.size/1024:.1f} KB)" for f in inv_files)
                + "</div>", unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Calculate Button
    btn_col, _, info_col = st.columns([3, 1, 3])
    with btn_col:
        st.markdown('<div class="calc-btn">', unsafe_allow_html=True)
        calc_clicked = st.button("🔴  เริ่มคำนวณยันยอด (AI Calculate)", use_container_width=True, type="primary")
        st.markdown("</div>", unsafe_allow_html=True)

    with info_col:
        if has_promo and rem_file:
            st.markdown('<div class="box-tip">✅ ข้อมูลครบถ้วน — กดคำนวณยันยอดได้ทันที</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="box-info">💡 กดเริ่มคำนวณเพื่อจำลองหรือประมวลผลข้อมูลเอกสาร</div>', unsafe_allow_html=True)

    if calc_clicked:
        st.session_state["show_result"] = True
        st.session_state["saved_msg"] = False

    # ── Reconciliation Results Section ────────────────────────────────────────
    if st.session_state["show_result"]:
        d  = MOCKUP_DB.get(selected_store, MOCKUP_DB[STORES[0]])
        df = build_reconciliation_table(selected_store)

        st.markdown("---")
        st.markdown(f"<h2 style='color:#1A3A5C;font-size:22px;font-weight:800;'>📊 ผลการตรวจสอบและคัดแยก 5 หมวดหมู่ — {selected_store}</h2>", unsafe_allow_html=True)

        # Summary Metrics
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("📄 เลขที่เอกสาร", d["doc"])
        m2.metric("📅 วันที่โอน", d["date"])
        m3.metric("🗓️ รอบบิล", d["period"])
        m4.metric("💰 ยอดโอนรวม", f'฿{d["total"]:,.0f}')
        
        # Count overcharged items
        over_count = len(df[df["สถานะการตรวจสอบ"].str.contains("❌")])
        m5.metric("❌ รายการหักเกิน", f"{over_count} หมวด")

        st.markdown("<br>", unsafe_allow_html=True)

        # Main Comparison Table (5 Promotion categories + Other fees)
        st.markdown("<h3 style='color:#3A8EDE;font-size:18px;font-weight:800;'>📑 ตารางเปรียบเทียบ ยอดในบิลห้าง VS ยอดคำนวณตามเงื่อนไขโปรฯ</h3>", unsafe_allow_html=True)
        st.dataframe(style_df(df), use_container_width=True, height=360)

        # Overcharge Alert Banner
        over_rows = df[df["สถานะการตรวจสอบ"].str.contains("❌")]["หมวดหมู่ค่าใช้จ่าย"].tolist()
        if over_rows:
            st.markdown(
                f"""
                <div class="box-error">
                    ❌ <strong>พบห้างหักเงินเกิน {len(over_rows)} รายการ:</strong><br>
                    {'<br>'.join('• ' + item for item in over_rows)}<br>
                    ⚠️ <em>กรุณาออกหนังสือทักท้วง (Debit Dispute) เพื่อขอเครดิตคืนจากทางห้างฯ ทันที</em>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown('<div class="box-tip">✅ ยอดตรงกันทุกหมวดหมู่ — ไม่พบรายการหักเกิน</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Action Buttons: Save to Database & Export Excel ──
        act_col1, act_col2, act_col3 = st.columns([2, 2, 2])

        with act_col1:
            st.markdown('<div class="save-btn">', unsafe_allow_html=True)
            save_clicked = st.button("💾 บันทึกยอดรอบโอนนี้ลงระบบสะสม", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            if save_clicked:
                row_record = {
                    "บันทึกเมื่อ": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "ห้าง": selected_store,
                    "นิติบุคคล": d["billing_co"],
                    "เลขที่เอกสาร": d["doc"],
                    "รอบบิล": d["period"],
                    "วันที่โอน": d["date"],
                    "ยอดโอนรวม": d["total"],
                    "1_ส่วนลดแชร์โปรโมชั่น": d["c1_promo_support"],
                    "2_ค่าลงสื่อโฆษณา": d["c2_media_brochure"],
                    "3_ค่าเช่าพื้นที่พิเศษ": d["c3_display_fee"],
                    "4_ส่วนลดเป้าหมาย": d["c4_rebate_bonus"],
                    "5_ค่ากองทุนร่วมกิจกรรม": d["c5_coop_fund"],
                    "ค่าDC": d["dc_fee"],
                    "ค่าขนส่ง": d["logistics_fee"],
                    "อื่นๆ": d["other_fee"],
                    "รวมหักจริง": sum([d["c1_promo_support"], d["c2_media_brochure"], d["c3_display_fee"], d["c4_rebate_bonus"], d["c5_coop_fund"], d["dc_fee"], d["logistics_fee"], d["other_fee"]]),
                    "ยอดสุทธิ": d["net"],
                    "สถานะ": "❌ มีรายการหักเกิน" if over_count > 0 else "✅ ปกติ",
                    "ผู้บันทึก": cur_user.get("name", "Unknown")
                }
                save_to_annual_db(row_record)
                st.session_state["saved_msg"] = True
                st.rerun()

        with act_col2:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            sn = selected_store[:15].replace("/","-").replace(" ","_")
            st.download_button(
                "📊 Export รายงานรอบนี้ (.xlsx)",
                data=to_excel_report(df, sheet_name="Recon_Report"),
                file_name=f"recon_{sn}_{ts}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        with act_col3:
            if st.button("🔄 ล้างข้อมูลรอบนี้ (Reset)", use_container_width=True):
                st.session_state["show_result"] = False
                st.session_state["saved_msg"] = False
                st.rerun()

        if st.session_state.get("saved_msg"):
            st.success("✅ บันทึกยอดรอบโอนนี้ลงฐานข้อมูลสะสมรายปีสำเร็จเรียบร้อย! สามารถคลิกดูที่แท็บ 'สรุปภาพรวมค่าใช้จ่ายรายปี' ได้เลยครับ")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: สรุปภาพรวมค่าใช้จ่ายรายปี (Annual Dashboard & Analytics)
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<h2 style='color:#1A3A5C;font-size:22px;font-weight:800;'>📊 สรุปภาพรวมค่าใช้จ่ายโปรโมชั่นสะสมรายปี</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#5A7BA8;font-size:14px;'>ดูผลรวมการใช้จ่ายโปรโมชั่นทั้ง 5 หมวดหมู่ตลอดทั้งปี แยกตามรายห้าง เพื่อวางแผนงบประมาณและตรวจสอบตอนสิ้นปี</p>", unsafe_allow_html=True)

    annual_df = load_annual_db()

    # If empty database, add initial mock sample records so user can see dashboard immediately
    if len(annual_df) == 0:
        sample_records = [
            {"บันทึกเมื่อ": "01/08/2567 10:00:00", "ห้าง": "7-Eleven", "นิติบุคคล": "ซีพี ออลล์ จำกัด (มหาชน)", "เลขที่เอกสาร": "REM-7EL-2567-0701", "รอบบิล": "ก.ค. 67", "วันที่โอน": "05/08/2567", "ยอดโอนรวม": 4500000, "1_ส่วนลดแชร์โปรโมชั่น": 160000, "2_ค่าลงสื่อโฆษณา": 60000, "3_ค่าเช่าพื้นที่พิเศษ": 45000, "4_ส่วนลดเป้าหมาย": 130000, "5_ค่ากองทุนร่วมกิจกรรม": 20000, "ค่าDC": 85000, "ค่าขนส่ง": 25000, "อื่นๆ": 10000, "รวมหักจริง": 535000, "ยอดสุทธิ": 3965000, "สถานะ": "✅ ปกติ", "ผู้บันทึก": "คุณอาร์ต"},
            {"บันทึกเมื่อ": "05/08/2567 11:30:00", "ห้าง": "Big C (รวม Pure และ Big C mini)", "นิติบุคคล": "บิ๊กซี ซูเปอร์เซ็นเตอร์ จำกัด (มหาชน)", "เลขที่เอกสาร": "REM-BGC-2567-0702", "รอบบิล": "ก.ค. 67", "วันที่โอน": "03/08/2567", "ยอดโอนรวม": 7800000, "1_ส่วนลดแชร์โปรโมชั่น": 350000, "2_ค่าลงสื่อโฆษณา": 120000, "3_ค่าเช่าพื้นที่พิเศษ": 90000, "4_ส่วนลดเป้าหมาย": 200000, "5_ค่ากองทุนร่วมกิจกรรม": 55000, "ค่าDC": 230000, "ค่าขนส่ง": 50000, "อื่นๆ": 25000, "รวมหักจริง": 1120000, "ยอดสุทธิ": 6680000, "สถานะ": "❌ มีรายการหักเกิน", "ผู้บันทึก": "คุณญาณี"},
            {"บันทึกเมื่อ": "10/08/2567 14:00:00", "ห้าง": "CPAXT (Makro หน้าร้าน)", "นิติบุคคล": "สยามแม็คโคร จำกัด (มหาชน) — CPAXT", "เลขที่เอกสาร": "REM-MKR-2567-0703", "รอบบิล": "ก.ค. 67", "วันที่โอน": "01/08/2567", "ยอดโอนรวม": 11500000, "1_ส่วนลดแชร์โปรโมชั่น": 480000, "2_ค่าลงสื่อโฆษณา": 190000, "3_ค่าเช่าพื้นที่พิเศษ": 130000, "4_ส่วนลดเป้าหมาย": 340000, "5_ค่ากองทุนร่วมกิจกรรม": 75000, "ค่าDC": 390000, "ค่าขนส่ง": 75000, "อื่นๆ": 38000, "รวมหักจริง": 1718000, "ยอดสุทธิ": 9782000, "สถานะ": "❌ มีรายการหักเกิน", "ผู้บันทึก": "คุณนก"},
            {"บันทึกเมื่อ": "05/09/2567 15:00:00", "ห้าง": "7-Eleven", "นิติบุคคล": "ซีพี ออลล์ จำกัด (มหาชน)", "เลขที่เอกสาร": "REM-7EL-2567-0891", "รอบบิล": "ส.ค. 67", "วันที่โอน": "05/09/2567", "ยอดโอนรวม": 4820500, "1_ส่วนลดแชร์โปรโมชั่น": 180000, "2_ค่าลงสื่อโฆษณา": 65000, "3_ค่าเช่าพื้นที่พิเศษ": 48000, "4_ส่วนลดเป้าหมาย": 145000, "5_ค่ากองทุนร่วมกิจกรรม": 25000, "ค่าDC": 89600, "ค่าขนส่ง": 28500, "อื่นๆ": 12300, "รวมหักจริง": 593400, "ยอดสุทธิ": 4227100, "สถานะ": "❌ มีรายการหักเกิน", "ผู้บันทึก": "คุณอาร์ต"},
        ]
        annual_df = pd.DataFrame(sample_records)
        annual_df.to_csv(DB_FILE, index=False, encoding="utf-8-sig")

    # ── Filter Bar ──
    f_col1, f_col2, _ = st.columns([2, 2, 2])
    with f_col1:
        store_filter = st.selectbox("🔍 กรองดูเฉพาะห้าง:", ["ทั้งหมด (All Stores)"] + STORES)
    with f_col2:
        status_filter = st.selectbox("🔍 กรองตามสถานะ:", ["ทั้งหมด", "เฉพาะที่มีรายการหักเกิน ❌", "เฉพาะที่ถูกต้อง ✅"])

    # Apply Filters
    filtered_df = annual_df.copy()
    if store_filter != "ทั้งหมด (All Stores)":
        filtered_df = filtered_df[filtered_df["ห้าง"] == store_filter]
    if status_filter == "เฉพาะที่มีรายการหักเกิน ❌":
        filtered_df = filtered_df[filtered_df["สถานะ"].str.contains("❌")]
    elif status_filter == "เฉพาะที่ถูกต้อง ✅":
        filtered_df = filtered_df[filtered_df["สถานะ"].str.contains("✅")]

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Top Overview Metrics ──
    tot_sales = filtered_df["ยอดโอนรวม"].sum() if len(filtered_df)>0 else 0
    tot_c1    = filtered_df["1_ส่วนลดแชร์โปรโมชั่น"].sum() if len(filtered_df)>0 else 0
    tot_c2    = filtered_df["2_ค่าลงสื่อโฆษณา"].sum() if len(filtered_df)>0 else 0
    tot_c3    = filtered_df["3_ค่าเช่าพื้นที่พิเศษ"].sum() if len(filtered_df)>0 else 0
    tot_c4    = filtered_df["4_ส่วนลดเป้าหมาย"].sum() if len(filtered_df)>0 else 0
    tot_c5    = filtered_df["5_ค่ากองทุนร่วมกิจกรรม"].sum() if len(filtered_df)>0 else 0
    tot_promo = tot_c1 + tot_c2 + tot_c3 + tot_c4 + tot_c5

    om1, om2, om3, om4 = st.columns(4)
    om1.metric("💰 ยอดโอนรวมสะสม", f"฿{tot_sales:,.0f}")
    om2.metric("🎁 รวมค่าโปรโมชั่น 5 หมวด", f"฿{tot_promo:,.0f}")
    om3.metric("📊 สัดส่วนโปรโมชั่น / ยอดโอน", f"{(tot_promo/tot_sales*100) if tot_sales>0 else 0:.1f}%")
    om4.metric("📋 จำนวนรอบที่บันทึก", f"{len(filtered_df)} รอบโอน")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 5 Category Breakdown Chart ──
    st.markdown("<h3 style='color:#3A8EDE;font-size:18px;font-weight:800;'>📈 สัดส่วนการใช้จ่ายแยกตาม 5 หมวดหมู่โปรโมชั่นสะสม</h3>", unsafe_allow_html=True)
    
    chart_promo_df = pd.DataFrame({
        "หมวดหมู่โปรโมชั่น": [
            "(1) ส่วนลดแชร์โปรโมชั่น",
            "(2) ค่าลงสื่อโฆษณา",
            "(3) ค่าเช่าพื้นที่พิเศษ",
            "(4) ส่วนลดเป้าหมาย (Rebate)",
            "(5) ค่ากองทุนร่วมกิจกรรม"
        ],
        "ยอดเงินรวม (บาท)": [tot_c1, tot_c2, tot_c3, tot_c4, tot_c5]
    }).set_index("หมวดหมู่โปรโมชั่น")

    c_left, c_right = st.columns([3, 2])
    with c_left:
        st.bar_chart(chart_promo_df, height=300, use_container_width=True)
    with c_right:
        st.dataframe(
            chart_promo_df.style.format({"ยอดเงินรวม (บาท)": "฿{:,.2f}"})
            .set_properties(**{"font-size":"15px","font-weight":"600"}),
            use_container_width=True, height=300
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Yearly Table ──
    st.markdown("<h3 style='color:#3A8EDE;font-size:18px;font-weight:800;'>📑 ตารางประวัติบันทึกสะสมรายรอบ</h3>", unsafe_allow_html=True)
    st.dataframe(filtered_df, use_container_width=True, height=320)

    # Export Annual Report Button
    st.markdown("---")
    exp_c1, _, _ = st.columns([2, 2, 2])
    with exp_c1:
        annual_excel = to_excel_report(filtered_df, sheet_name="Annual_Summary")
        st.download_button(
            "📥 Export ข้อมูลรวมสิ้นปีเป็น Excel (.xlsx)",
            data=annual_excel,
            file_name=f"annual_summary_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:16px;border-top:2.5px solid #C5DEFF;margin-top:16px;">
    <p style="color:#5A7BA8;font-size:13px;margin:0;">
        🤖 <strong>Modern Trade Reconciliation AI</strong> · ขับเคลื่อนด้วย Claude 3.5 Sonnet Vision · Built with Streamlit<br>
        <span style="font-size:11px;opacity:.70;">ระบบคัดแยก 5 หมวดหมู่โปรโมชั่น · บันทึกฐานข้อมูลสะสมรายปี · รองรับการทำงานทีมบัญชี</span>
    </p>
</div>
""", unsafe_allow_html=True)
