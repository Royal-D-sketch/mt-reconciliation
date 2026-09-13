"""
Modern Trade Reconciliation AI — Production v3.2
เพิ่มระบบสร้างรายงานอินโฟกราฟิกผู้บริหาร (Executive Infographic Report) + คำบรรยายเชิงกลยุทธ์ + Export รูปภาพ PNG และ Excel
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
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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

        user_in = st.text_input("ชื่อผู้ใช้ (Username)", placeholder="ระบุชื่อผู้ใช้งาน")
        pw_in   = st.text_input("รหัสผ่าน (Password)", type="password", placeholder="ระบุรหัสผ่าน")
        
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
# 🎨 CUSTOM STYLING
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
    border-radius:16px; padding:24px 30px; margin-bottom:20px;
    display:flex; align-items:center; gap:20px;
    box-shadow:0 4px 24px rgba(58,142,222,.22);
}
.hero h1 {
    color:#fff !important; font-size:26px !important; font-weight:800 !important;
    margin:0 0 4px 0 !important; line-height:1.25;
    text-shadow:0 1px 4px rgba(0,0,0,.18);
}
.hero p  { color:rgba(255,255,255,.92) !important; font-size:15px !important; margin:0 !important; }
.hero-icon { font-size:54px; line-height:1; flex-shrink:0; }
.hero-badge {
    display:inline-block; background:rgba(255,255,255,.24);
    border:1px solid rgba(255,255,255,.45); border-radius:24px;
    padding:4px 14px; font-size:12px; font-weight:700; color:#fff; margin-top:8px;
}

/* ─── Cards & Headers ─── */
.sec-label {
    font-size:11px; letter-spacing:1.3px; font-weight:700;
    opacity:.75; text-transform:uppercase; margin-bottom:6px; color:#fff;
}
.card-title {
    font-size:17px; font-weight:800; color:#2C7BE5;
    margin-bottom:12px; display:flex; align-items:center; gap:8px;
    border-bottom:2.5px solid #D6EAFF; padding-bottom:9px;
}

/* ─── Upload Zones ─── */
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
    font-size:23px !important; font-weight:800 !important; color:#2C7BE5 !important;
}

/* ─── Info Boxes ─── */
.box-info  { background:#EAF4FF; border-left:5px solid #3A8EDE; border-radius:0 10px 10px 0; padding:12px 16px; font-size:14px; color:#1A3A5C; margin:10px 0; }
.box-tip   { background:#E0F7F1; border-left:5px solid #30BFA0; border-radius:0 10px 10px 0; padding:12px 16px; font-size:14px; color:#0D4A3A; margin:10px 0; }
.box-error { background:#FDECEA; border-left:5px solid #D32F2F; border-radius:0 10px 10px 0; padding:14px 18px; font-size:15px; font-weight:700; color:#B71C1C; margin:10px 0; }
.box-warn  { background:#FFF8E1; border-left:5px solid #F9A825; border-radius:0 10px 10px 0; padding:13px 16px; font-size:14px; font-weight:600; color:#7A4F00; margin:10px 0; }
.box-exec  { background:#F0F4FF; border-left:5px solid #1B6CA8; border-radius:0 12px 12px 0; padding:18px 22px; font-size:15px; line-height:1.7; color:#1A3A5C; margin:14px 0; }

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

.calc-btn .stButton>button {
    background:linear-gradient(135deg,#E53935 0%,#B71C1C 100%) !important;
    font-size:16px !important; padding:13px 32px !important;
    box-shadow:0 5px 18px rgba(229,57,53,.40) !important;
}

.save-btn .stButton>button {
    background:linear-gradient(135deg,#2E7D32 0%,#1B5E20 100%) !important;
    font-size:15px !important; padding:12px 28px !important;
    box-shadow:0 4px 14px rgba(46,125,50,.35) !important;
}

/* ─── Table ─── */
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
    font-size:15px !important; font-weight:700 !important; color:#5A7BA8 !important;
    border-radius:8px 8px 0 0 !important; padding:10px 20px !important;
}
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {
    background:#3A8EDE !important; color:#fff !important;
}
[data-testid="stTabs"] [data-baseweb="tab-panel"] {
    background:#fff !important; border:2px solid #C5DEFF !important;
    border-top:none !important; border-radius:0 0 12px 12px !important;
    padding:22px !important; margin-bottom:20px;
}

::-webkit-scrollbar { width:7px; }
::-webkit-scrollbar-thumb { background:#C5DEFF; border-radius:4px; }
::-webkit-scrollbar-thumb:hover { background:#3A8EDE; }
hr { border:none !important; border-top:2.5px solid #C5DEFF !important; margin:20px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS & DATABASE
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

DB_FILE = "annual_recon_database.csv"

def load_annual_db() -> pd.DataFrame:
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
    df = load_annual_db()
    new_row = pd.DataFrame([row_data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DB_FILE, index=False, encoding="utf-8-sig")
    return True

# ══════════════════════════════════════════════════════════════════════════════
# MOCKUP DATA (5 Categories)
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

def fmt(v) -> str:
    try:    return f"฿{float(v):>14,.2f}"
    except: return "฿0.00"

def get_status_label(s: str) -> str:
    if s == "over":  return "❌ ห้างหักเกิน"
    if s == "short": return "⚠️ ยอดขาด"
    return "✅ ตรงกัน"

def build_reconciliation_table(store: str) -> pd.DataFrame:
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

def generate_recon_pdf(df: pd.DataFrame, store_name: str, billing_co: str, doc_no: str, period: str, date_str: str, total_amt: float, prepared_by: str) -> bytes:
    """สร้างเอกสารรายงาน Reconciliation ในรูปแบบ PDF มาตรฐาน A4"""
    fig = plt.figure(figsize=(8.27, 11.69), dpi=200, facecolor="#FFFFFF")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")

    # Top Header banner
    rect_top = patches.FancyBboxPatch((0.05, 0.90), 0.90, 0.07, boxstyle="round,pad=0.015,rounding_size=0.02", facecolor="#3A8EDE", edgecolor="#1B6CA8", linewidth=1.5)
    ax.add_patch(rect_top)
    ax.text(0.50, 0.945, "MODERN TRADE RECONCILIATION REPORT", color="white", fontsize=15, fontweight="bold", ha="center", va="center")
    ax.text(0.50, 0.915, f"STORE: {store_name.upper()}", color="#D0F5EC", fontsize=11, fontweight="bold", ha="center", va="center")

    # Document Meta Information Box
    rect_info = patches.FancyBboxPatch((0.05, 0.79), 0.90, 0.09, boxstyle="round,pad=0.01,rounding_size=0.015", facecolor="#F4F8FF", edgecolor="#C5DEFF", linewidth=1)
    ax.add_patch(rect_info)
    
    ax.text(0.08, 0.855, f"Legal Entity: {billing_co}", fontsize=9, fontweight="bold", color="#1A3A5C")
    ax.text(0.08, 0.830, f"Document No: {doc_no}", fontsize=9, color="#1A3A5C")
    ax.text(0.08, 0.805, f"Billing Period: {period}", fontsize=9, color="#1A3A5C")

    ax.text(0.55, 0.855, f"Transfer Date: {date_str}", fontsize=9, color="#1A3A5C")
    ax.text(0.55, 0.830, f"Total Transferred: THB {total_amt:,.2f}", fontsize=9, fontweight="bold", color="#1B6CA8")
    ax.text(0.55, 0.805, f"Prepared By: {prepared_by} | Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}", fontsize=8.5, color="#5A7BA8")

    # Table Header row
    y_start = 0.74
    rect_th = patches.Rectangle((0.05, y_start), 0.90, 0.03, facecolor="#4A90D9", edgecolor="none")
    ax.add_patch(rect_th)
    ax.text(0.07, y_start + 0.009, "Expense Category", color="white", fontsize=9, fontweight="bold")
    ax.text(0.48, y_start + 0.009, "Store Billed", color="white", fontsize=9, fontweight="bold", ha="right")
    ax.text(0.66, y_start + 0.009, "Promo Calc", color="white", fontsize=9, fontweight="bold", ha="right")
    ax.text(0.81, y_start + 0.009, "Difference", color="white", fontsize=9, fontweight="bold", ha="right")
    ax.text(0.92, y_start + 0.009, "Status", color="white", fontsize=9, fontweight="bold", ha="center")

    curr_y = y_start - 0.028
    for idx, row in df.iterrows():
        bg_col = "#EAF4FF" if idx % 2 == 1 else "#FFFFFF"
        if "ยอดโอนสุทธิ" in str(row.get("หมวดหมู่ค่าใช้จ่าย", "")) or "Net Amount" in str(row.get("หมวดหมู่ค่าใช้จ่าย", "")):
            bg_col = "#D6EAFF"
        
        rect_row = patches.Rectangle((0.05, curr_y), 0.90, 0.027, facecolor=bg_col, edgecolor="#E0EBF7", linewidth=0.5)
        ax.add_patch(rect_row)

        cat_title = str(row.get("หมวดหมู่ค่าใช้จ่าย", ""))
        store_val = row.get("ยอดในบิลห้าง (บาท)", 0)
        calc_val = row.get("ยอดคำนวณตามโปรฯ (บาท)", 0)
        diff_val = row.get("ผลต่าง (บาท)", 0)
        st_val = str(row.get("สถานะการตรวจสอบ", ""))

        ax.text(0.07, curr_y + 0.008, cat_title[:38], color="#1A3A5C", fontsize=8, fontweight="bold" if "ยอดโอนสุทธิ" in cat_title else "normal")
        ax.text(0.48, curr_y + 0.008, f"THB {store_val:,.2f}" if isinstance(store_val, (int, float)) else str(store_val), color="#1A3A5C", fontsize=8, ha="right")
        ax.text(0.66, curr_y + 0.008, f"THB {calc_val:,.2f}" if isinstance(calc_val, (int, float)) else str(calc_val), color="#1A3A5C", fontsize=8, ha="right")
        
        diff_color = "#B71C1C" if isinstance(diff_val, (int, float)) and diff_val > 1 else ("#1B5E20" if isinstance(diff_val, (int, float)) and abs(diff_val) <= 1 else "#1A3A5C")
        ax.text(0.81, curr_y + 0.008, f"THB {diff_val:,.2f}" if isinstance(diff_val, (int, float)) else str(diff_val), color=diff_color, fontsize=8, fontweight="bold", ha="right")
        
        st_color = "#B71C1C" if "❌" in st_val else ("#1B5E20" if "✅" in st_val else "#E67E22")
        ax.text(0.92, curr_y + 0.008, "OVERCHARGE" if "❌" in st_val else ("MATCH" if "✅" in st_val else "DIFF"), color=st_color, fontsize=7.5, fontweight="bold", ha="center")
        
        curr_y -= 0.027

    # Audit / Signature Block
    rect_sig = patches.FancyBboxPatch((0.05, 0.06), 0.90, 0.14, boxstyle="round,pad=0.01,rounding_size=0.015", facecolor="#F8FAFD", edgecolor="#C5DEFF", linewidth=1)
    ax.add_patch(rect_sig)

    ax.text(0.08, 0.170, "AUDIT APPROVAL & SIGN-OFF:", fontsize=9, fontweight="bold", color="#1B6CA8")
    ax.text(0.18, 0.100, "__________________________\nPrepared by (Accounting)", fontsize=8, color="#5A7BA8", ha="center")
    ax.text(0.50, 0.100, "__________________________\nReviewed by (Finance Head)", fontsize=8, color="#5A7BA8", ha="center")
    ax.text(0.82, 0.100, "__________________________\nApproved by (Management)", fontsize=8, color="#5A7BA8", ha="center")

    ax.text(0.50, 0.030, "Confidential - For Internal Accounting & Audit Reconciliation Purposes Only", fontsize=8, color="#A0B4CC", ha="center")

    buf = io.BytesIO()
    plt.savefig(buf, format="pdf", bbox_inches="tight", facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    return buf.getvalue()

# ══════════════════════════════════════════════════════════════════════════════
# 🖼️ INFOGRAPHIC IMAGE GENERATOR (Matplotlib & Pillow)
# ══════════════════════════════════════════════════════════════════════════════
def generate_infographic_image(tot_sales: float, tot_promo: float, promo_breakdown: dict, overcharge_items: list, store_name: str, prepared_by: str) -> bytes:
    """สร้างไฟล์รูปภาพอินโฟกราฟิกความละเอียดสูงสำหรับรายงานผู้บริหาร"""
    fig = plt.figure(figsize=(12, 14), dpi=200, facecolor="#F4F8FF")
    
    # ── Background styling ──
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor("#F4F8FF")
    ax.axis("off")

    # Header Card
    rect_header = patches.FancyBboxPatch((0.04, 0.88), 0.92, 0.09, boxstyle="round,pad=0.02,rounding_size=0.03", facecolor="#3A8EDE", edgecolor="#2176AE", linewidth=2)
    ax.add_patch(rect_header)
    ax.text(0.50, 0.935, "MODERN TRADE RECONCILIATION AI", color="white", fontsize=18, fontweight="bold", ha="center", va="center")
    ax.text(0.50, 0.900, f"EXECUTIVE SUMMARY REPORT - {store_name.upper()}", color="#D0F5EC", fontsize=13, fontweight="bold", ha="center", va="center")

    # KPI 1: Total Sales
    rect_kpi1 = patches.FancyBboxPatch((0.04, 0.74), 0.28, 0.11, boxstyle="round,pad=0.015,rounding_size=0.02", facecolor="white", edgecolor="#C5DEFF", linewidth=1.5)
    ax.add_patch(rect_kpi1)
    ax.text(0.18, 0.815, "TOTAL SALES / TRANSFER", color="#5A7BA8", fontsize=10, fontweight="bold", ha="center")
    ax.text(0.18, 0.765, f"THB {tot_sales:,.0f}", color="#1B6CA8", fontsize=16, fontweight="bold", ha="center")

    # KPI 2: Total Promo
    rect_kpi2 = patches.FancyBboxPatch((0.36, 0.74), 0.28, 0.11, boxstyle="round,pad=0.015,rounding_size=0.02", facecolor="white", edgecolor="#C5DEFF", linewidth=1.5)
    ax.add_patch(rect_kpi2)
    ax.text(0.50, 0.815, "PROMOTION EXPENSES (5 CATS)", color="#5A7BA8", fontsize=10, fontweight="bold", ha="center")
    ax.text(0.50, 0.765, f"THB {tot_promo:,.0f}", color="#30BFA0", fontsize=16, fontweight="bold", ha="center")

    # KPI 3: Promo Ratio %
    ratio = (tot_promo / tot_sales * 100) if tot_sales > 0 else 0
    rect_kpi3 = patches.FancyBboxPatch((0.68, 0.74), 0.28, 0.11, boxstyle="round,pad=0.015,rounding_size=0.02", facecolor="white", edgecolor="#C5DEFF", linewidth=1.5)
    ax.add_patch(rect_kpi3)
    ax.text(0.82, 0.815, "PROMO / SALES RATIO", color="#5A7BA8", fontsize=10, fontweight="bold", ha="center")
    ax.text(0.82, 0.765, f"{ratio:.1f}%", color="#E67E22", fontsize=16, fontweight="bold", ha="center")

    # ── Donut Chart for Promo Categories ──
    ax_pie = fig.add_axes([0.08, 0.45, 0.40, 0.25])
    labels = ["1. Promo Support", "2. Media & Brochure", "3. Display Fees", "4. Rebate Bonus", "5. Co-op Fund"]
    values = [
        promo_breakdown.get("c1", 0),
        promo_breakdown.get("c2", 0),
        promo_breakdown.get("c3", 0),
        promo_breakdown.get("c4", 0),
        promo_breakdown.get("c5", 0)
    ]
    colors = ["#4A90D9", "#3DBFA0", "#F39C12", "#E74C3C", "#9B59B6"]
    
    if sum(values) > 0:
        wedges, texts, autotexts = ax_pie.pie(
            values, autopct="%1.1f%%", startangle=140, colors=colors,
            pctdistance=0.75, wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2)
        )
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontsize(9)
            autotext.set_weight("bold")
    ax_pie.set_title("5 PROMOTION EXPENSE BREAKDOWN", fontsize=11, fontweight="bold", color="#1A3A5C", pad=12)

    # ── Bar Chart for Category Values ──
    ax_bar = fig.add_axes([0.56, 0.45, 0.38, 0.25])
    bars = ax_bar.barh(labels[::-1], [v/1000 for v in values[::-1]], color=colors[::-1], height=0.55, edgecolor="none")
    ax_bar.set_facecolor("white")
    ax_bar.set_title("SPENDING BY CATEGORY (THB in Thousands)", fontsize=10, fontweight="bold", color="#1A3A5C")
    ax_bar.tick_params(axis="both", labelsize=8, colors="#5A7BA8")
    for spine in ax_bar.spines.values():
        spine.set_color("#C5DEFF")
    for bar in bars:
        w = bar.get_width()
        ax_bar.text(w + (max(values)/1000 * 0.03), bar.get_y() + bar.get_height()/2, f"THB {w:,.0f}k", ha="left", va="center", fontsize=8, fontweight="bold", color="#1A3A5C")

    # ── Executive Commentary Card (Bottom) ──
    rect_comm = patches.FancyBboxPatch((0.04, 0.08), 0.92, 0.32, boxstyle="round,pad=0.02,rounding_size=0.03", facecolor="white", edgecolor="#3A8EDE", linewidth=2)
    ax.add_patch(rect_comm)
    
    ax.text(0.08, 0.370, "EXECUTIVE MANAGEMENT COMMENTARY & ACTION ITEMS", color="#1B6CA8", fontsize=12, fontweight="bold")
    
    commentary_text = (
        f"1. OVERVIEW: Total sales volume reached THB {tot_sales:,.2f} with promotion expenditure of THB {tot_promo:,.2f} ({ratio:.1f}% ratio).\n\n"
        f"2. KEY FINDINGS: Promotion Support & Rebate Bonuses represent the largest investment categories.\n"
    )
    if overcharge_items:
        commentary_text += f"3. AUDIT ALERTS (ACTION REQUIRED):\n   [!] Detected discrepancies / overcharges in {len(overcharge_items)} categories:\n   " + ", ".join(overcharge_items) + "\n   -> Recommendation: Issue formal Debit Dispute & claim credits back immediately.\n\n"
    else:
        commentary_text += "3. AUDIT ALERTS: All deductions match agreed promotion contract terms. Zero unauthorized overcharge detected.\n\n"
    
    commentary_text += (
        f"4. STRATEGIC RECOMMENDATION: Optimize display space rental and review rebate targets for the upcoming quarter.\n"
        f"   Report Generated: {datetime.now().strftime('%d/%m/%Y %H:%M')} | Prepared By: {prepared_by}"
    )
    
    ax.text(0.08, 0.220, commentary_text, color="#1A3A5C", fontsize=9.5, va="center", linespacing=1.4)

    # Footer
    ax.text(0.50, 0.035, "Generated automatically by Modern Trade Reconciliation AI Platform", color="#8EA4C0", fontsize=9, ha="center")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    return buf.getvalue()

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INIT
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
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:8px 0 16px 0;border-bottom:1px solid rgba(255,255,255,.20);margin-bottom:14px;">
        <div style="font-size:48px;line-height:1">🧾</div>
        <div style="font-size:17px;font-weight:800;margin:6px 0 2px 0;">MT Recon AI</div>
        <div style="font-size:11px;opacity:.75;">Claude 3.5 Sonnet Vision · v3.2</div>
    </div>
    """, unsafe_allow_html=True)

    cur_user = st.session_state.get("_user", {})
    st.markdown(f"""
    <div style="background:rgba(255,255,255,.12);border-radius:10px;padding:11px 13px;margin-bottom:14px;border:1px solid rgba(255,255,255,.25);">
        <div style="font-size:11px;opacity:.8;color:#fff;">👤 ผู้ใช้งานปัจจุบัน:</div>
        <div style="font-size:15px;font-weight:800;color:#fff;margin:2px 0;">{cur_user.get('name', 'ผู้ใช้งาน')}</div>
        <div style="font-size:12px;color:#D0F5EC;font-weight:700;">{cur_user.get('badge', '')}</div>
    </div>
    """, unsafe_allow_html=True)

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

    st.markdown('<p class="sec-label" style="margin-top:10px;">🔑 Anthropic API Key (Claude AI)</p>', unsafe_allow_html=True)
    key_val = st.text_input(
        "API Key",
        value=st.session_state["api_key"],
        type="password",
        placeholder="sk-ant-api03-... (Auto AI พร้อมใช้)",
        label_visibility="collapsed"
    )
    st.session_state["api_key"] = key_val

    st.markdown("---")

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

    if st.button("🚪 ออกจากระบบ (Logout)", use_container_width=True):
        st.session_state["_logged_in"] = False
        st.session_state["_user"] = None
        st.rerun()

    st.markdown('<p style="font-size:11px;opacity:.50;text-align:center;margin-top:12px;">v3.2 Production · Claude 3.5 Sonnet · © 2025</p>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN PAGE (Hero + 3 Tabs)
# ══════════════════════════════════════════════════════════════════════════════
cpaxt_badge = ' <span class="cpaxt-badge">CPAXT Group</span>' if selected_store in CPAXT_STORES else ""
billing_co  = MOCKUP_DB.get(selected_store, {}).get("billing_co", selected_store)

st.markdown(f"""
<div class="hero">
    <div class="hero-icon">🤖</div>
    <div>
        <div style="font-size:14px;font-weight:700;color:rgba(255,255,255,.88);margin-bottom:2px;">
            ผู้ใช้งาน: {cur_user.get('name', '')} ({cur_user.get('badge', '')})
        </div>
        <h1>Modern Trade Reconciliation AI</h1>
        <p>
            ห้างที่กำลังตรวจสอบ: <strong>{selected_store}</strong>{cpaxt_badge} &nbsp;|&nbsp; 
            <span style="font-size:13px;opacity:.90;">นิติบุคคล: {billing_co}</span>
        </p>
        <span class="hero-badge">Claude 3.5 Sonnet Vision · 5 หมวดโปรโมชั่น · รายงานอินโฟกราฟิกผู้บริหาร</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── TOP 3 TABS ────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📑 1. ตรวจสอบและยันยอดรอบโอน (Reconciliation)",
    "📊 2. สรุปภาพรวมค่าใช้จ่ายรายปี (Annual Dashboard)",
    "📈 3. รายงานอินโฟกราฟิกผู้บริหาร (Executive Infographics & Report)"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: ตรวจสอบและยันยอดรอบโอน
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
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

    btn_col, _, info_col = st.columns([3, 1, 3])
    with btn_col:
        st.markdown('<div class="calc-btn">', unsafe_allow_html=True)
        calc_clicked = st.button("🔴  เริ่มคำนวณยันยอด (AI Calculate)", use_container_width=True, type="primary")
        st.markdown("</div>", unsafe_allow_html=True)

    with info_col:
        if has_promo and rem_file:
            st.markdown('<div class="box-tip">✅ ข้อมูลครบถ้วน — กดคำนวณยันยอดได้ทันที</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="box-info">💡 กดเริ่มคำนวณเพื่อประมวลผลข้อมูลเอกสาร</div>', unsafe_allow_html=True)

    if calc_clicked:
        st.session_state["show_result"] = True
        st.session_state["saved_msg"] = False

    if st.session_state["show_result"]:
        d  = MOCKUP_DB.get(selected_store, MOCKUP_DB[STORES[0]])
        df = build_reconciliation_table(selected_store)

        st.markdown("---")
        st.markdown(f"<h2 style='color:#1A3A5C;font-size:22px;font-weight:800;'>📊 ผลการตรวจสอบและคัดแยก 5 หมวดหมู่ — {selected_store}</h2>", unsafe_allow_html=True)

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("📄 เลขที่เอกสาร", d["doc"])
        m2.metric("📅 วันที่โอน", d["date"])
        m3.metric("🗓️ รอบบิล", d["period"])
        m4.metric("💰 ยอดโอนรวม", f'฿{d["total"]:,.0f}')
        
        over_count = len(df[df["สถานะการตรวจสอบ"].str.contains("❌")])
        m5.metric("❌ รายการหักเกิน", f"{over_count} หมวด")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<h3 style='color:#3A8EDE;font-size:18px;font-weight:800;'>📑 ตารางเปรียบเทียบ ยอดในบิลห้าง VS ยอดคำนวณตามเงื่อนไขโปรฯ</h3>", unsafe_allow_html=True)
        st.dataframe(style_df(df), use_container_width=True, height=360)

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

        # ── Action Buttons: Save & Reset ──
        act_col1, act_col2, _ = st.columns([2.5, 1.5, 2])

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
            if st.button("🔄 ล้างข้อมูลรอบนี้ (Reset)", use_container_width=True):
                st.session_state["show_result"] = False
                st.session_state["saved_msg"] = False
                st.rerun()

        if st.session_state.get("saved_msg"):
            st.success("✅ บันทึกยอดรอบโอนนี้ลงฐานข้อมูลสะสมรายปีสำเร็จเรียบร้อย! คลิกดูที่แท็บ 2 และแท็บ 3 ได้เลยครับ")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Export Section: Excel, CSV, PDF ──
        st.markdown("<h3 style='color:#3A8EDE;font-size:18px;font-weight:800;'>📥 Export รายงานผลการตรวจสอบรอบนี้ (3 รูปแบบ)</h3>", unsafe_allow_html=True)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        sn = selected_store[:15].replace("/","-").replace(" ","_")

        exp_col1, exp_col2, exp_col3 = st.columns(3)

        with exp_col1:
            st.download_button(
                "📊 Export เป็น Excel (.xlsx)",
                data=to_excel_report(df, sheet_name="Recon_Report"),
                file_name=f"recon_{sn}_{ts}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        with exp_col2:
            # CSV with UTF-8-SIG for proper Thai characters in Excel
            csv_bytes = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
            st.download_button(
                "📄 Export เป็น CSV (.csv)",
                data=csv_bytes,
                file_name=f"recon_{sn}_{ts}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with exp_col3:
            # A4 PDF Document
            pdf_bytes = generate_recon_pdf(
                df=df,
                store_name=selected_store,
                billing_co=d["billing_co"],
                doc_no=d["doc"],
                period=d["period"],
                date_str=d["date"],
                total_amt=d["total"],
                prepared_by=cur_user.get("name", "ฝ่ายบัญชี Modern Trade")
            )
            st.download_button(
                "📑 Export เป็น PDF (.pdf)",
                data=pdf_bytes,
                file_name=f"recon_{sn}_{ts}.pdf",
                mime="application/pdf",
                use_container_width=True
            )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: สรุปภาพรวมค่าใช้จ่ายรายปี (Annual Dashboard)
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<h2 style='color:#1A3A5C;font-size:22px;font-weight:800;'>📊 สรุปภาพรวมค่าใช้จ่ายโปรโมชั่นสะสมรายปี</h2>", unsafe_allow_html=True)
    annual_df = load_annual_db()

    if len(annual_df) == 0:
        sample_records = [
            {"บันทึกเมื่อ": "01/08/2567 10:00:00", "ห้าง": "7-Eleven", "นิติบุคคล": "ซีพี ออลล์ จำกัด (มหาชน)", "เลขที่เอกสาร": "REM-7EL-2567-0701", "รอบบิล": "ก.ค. 67", "วันที่โอน": "05/08/2567", "ยอดโอนรวม": 4500000, "1_ส่วนลดแชร์โปรโมชั่น": 160000, "2_ค่าลงสื่อโฆษณา": 60000, "3_ค่าเช่าพื้นที่พิเศษ": 45000, "4_ส่วนลดเป้าหมาย": 130000, "5_ค่ากองทุนร่วมกิจกรรม": 20000, "ค่าDC": 85000, "ค่าขนส่ง": 25000, "อื่นๆ": 10000, "รวมหักจริง": 535000, "ยอดสุทธิ": 3965000, "สถานะ": "✅ ปกติ", "ผู้บันทึก": "คุณอาร์ต"},
            {"บันทึกเมื่อ": "05/08/2567 11:30:00", "ห้าง": "Big C (รวม Pure และ Big C mini)", "นิติบุคคล": "บิ๊กซี ซูเปอร์เซ็นเตอร์ จำกัด (มหาชน)", "เลขที่เอกสาร": "REM-BGC-2567-0702", "รอบบิล": "ก.ค. 67", "วันที่โอน": "03/08/2567", "ยอดโอนรวม": 7800000, "1_ส่วนลดแชร์โปรโมชั่น": 350000, "2_ค่าลงสื่อโฆษณา": 120000, "3_ค่าเช่าพื้นที่พิเศษ": 90000, "4_ส่วนลดเป้าหมาย": 200000, "5_ค่ากองทุนร่วมกิจกรรม": 55000, "ค่าDC": 230000, "ค่าขนส่ง": 50000, "อื่นๆ": 25000, "รวมหักจริง": 1120000, "ยอดสุทธิ": 6680000, "สถานะ": "❌ มีรายการหักเกิน", "ผู้บันทึก": "คุณญาณี"},
            {"บันทึกเมื่อ": "10/08/2567 14:00:00", "ห้าง": "CPAXT (Makro หน้าร้าน)", "นิติบุคคล": "สยามแม็คโคร จำกัด (มหาชน) — CPAXT", "เลขที่เอกสาร": "REM-MKR-2567-0703", "รอบบิล": "ก.ค. 67", "วันที่โอน": "01/08/2567", "ยอดโอนรวม": 11500000, "1_ส่วนลดแชร์โปรโมชั่น": 480000, "2_ค่าลงสื่อโฆษณา": 190000, "3_ค่าเช่าพื้นที่พิเศษ": 130000, "4_ส่วนลดเป้าหมาย": 340000, "5_ค่ากองทุนร่วมกิจกรรม": 75000, "ค่าDC": 390000, "ค่าขนส่ง": 75000, "อื่นๆ": 38000, "รวมหักจริง": 1718000, "ยอดสุทธิ": 9782000, "สถานะ": "❌ มีรายการหักเกิน", "ผู้บันทึก": "คุณนก"},
            {"บันทึกเมื่อ": "05/09/2567 15:00:00", "ห้าง": "7-Eleven", "นิติบุคคล": "ซีพี ออลล์ จำกัด (มหาชน)", "เลขที่เอกสาร": "REM-7EL-2567-0891", "รอบบิล": "ส.ค. 67", "วันที่โอน": "05/09/2567", "ยอดโอนรวม": 4820500, "1_ส่วนลดแชร์โปรโมชั่น": 180000, "2_ค่าลงสื่อโฆษณา": 65000, "3_ค่าเช่าพื้นที่พิเศษ": 48000, "4_ส่วนลดเป้าหมาย": 145000, "5_ค่ากองทุนร่วมกิจกรรม": 25000, "ค่าDC": 89600, "ค่าขนส่ง": 28500, "อื่นๆ": 12300, "รวมหักจริง": 593400, "ยอดสุทธิ": 4227100, "สถานะ": "❌ มีรายการหักเกิน", "ผู้บันทึก": "คุณอาร์ต"},
        ]
        annual_df = pd.DataFrame(sample_records)
        annual_df.to_csv(DB_FILE, index=False, encoding="utf-8-sig")

    f_col1, f_col2, _ = st.columns([2, 2, 2])
    with f_col1:
        store_filter = st.selectbox("🔍 กรองดูเฉพาะห้าง:", ["ทั้งหมด (All Stores)"] + STORES)
    with f_col2:
        status_filter = st.selectbox("🔍 กรองตามสถานะ:", ["ทั้งหมด", "เฉพาะที่มีรายการหักเกิน ❌", "เฉพาะที่ถูกต้อง ✅"])

    filtered_df = annual_df.copy()
    if store_filter != "ทั้งหมด (All Stores)":
        filtered_df = filtered_df[filtered_df["ห้าง"] == store_filter]
    if status_filter == "เฉพาะที่มีรายการหักเกิน ❌":
        filtered_df = filtered_df[filtered_df["สถานะ"].str.contains("❌")]
    elif status_filter == "เฉพาะที่ถูกต้อง ✅":
        filtered_df = filtered_df[filtered_df["สถานะ"].str.contains("✅")]

    st.markdown("<br>", unsafe_allow_html=True)

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
    st.markdown("<h3 style='color:#3A8EDE;font-size:18px;font-weight:800;'>📑 ตารางประวัติบันทึกสะสมรายรอบ</h3>", unsafe_allow_html=True)
    st.dataframe(filtered_df, use_container_width=True, height=320)

    st.markdown("---")
    st.markdown("<h3 style='color:#3A8EDE;font-size:18px;font-weight:800;'>📥 Export ข้อมูลสะสมรายปี</h3>", unsafe_allow_html=True)
    exp_c1, exp_c2, _ = st.columns([2, 2, 2])
    with exp_c1:
        annual_excel = to_excel_report(filtered_df, sheet_name="Annual_Summary")
        st.download_button(
            "📊 Export เป็น Excel (.xlsx)",
            data=annual_excel,
            file_name=f"annual_summary_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    with exp_c2:
        annual_csv = filtered_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
        st.download_button(
            "📄 Export เป็น CSV (.csv)",
            data=annual_csv,
            file_name=f"annual_summary_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: รายงานอินโฟกราฟิกผู้บริหาร (Executive Infographics & Report)
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<h2 style='color:#1A3A5C;font-size:22px;font-weight:800;'>📈 รายงานสรุปอินโฟกราฟิกสำหรับผู้บริหาร (Executive Infographic Brief)</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#5A7BA8;font-size:14px;'>สรุปสาระสำคัญ ประเด็นที่ต้องจับตา ข้อเสนอแนะเชิงกลยุทธ์ และกราฟิกวิเคราะห์พร้อมดาวน์โหลดเป็นรูปภาพหรือไฟล์ Excel</p>", unsafe_allow_html=True)

    d_info = MOCKUP_DB.get(selected_store, MOCKUP_DB["7-Eleven"])
    df_info = build_reconciliation_table(selected_store)

    tot_s = d_info["total"]
    c1 = d_info["c1_promo_support"]
    c2 = d_info["c2_media_brochure"]
    c3 = d_info["c3_display_fee"]
    c4 = d_info["c4_rebate_bonus"]
    c5 = d_info["c5_coop_fund"]
    tot_p = c1 + c2 + c3 + c4 + c5
    ratio_p = (tot_p / tot_s * 100) if tot_s > 0 else 0

    over_items_info = [
        label for label, sk in [
            ("(1) ส่วนลดแชร์โปรโมชั่น", "s_c1"), ("(2) ค่าลงสื่อโฆษณา", "s_c2"),
            ("(3) ค่าเช่าพื้นที่พิเศษ", "s_c3"), ("(4) ส่วนลดเป้าหมาย Rebate", "s_c4"),
            ("(5) ค่ากองทุนร่วมกิจกรรม", "s_c5"), ("ค่ากระจายสินค้า DC", "s_dc")
        ] if d_info.get(sk) == "over"
    ]

    # Executive Commentary in Thai
    st.markdown(f"""
    <div class="box-exec">
        <h3 style="color:#1B6CA8;font-size:18px;font-weight:800;margin-top:0;">📋 บทวิเคราะห์สรุปสำหรับผู้บริหาร (Executive Commentary)</h3>
        <p><strong>1. ภาพรวมการดำเนินงาน (Performance Overview):</strong><br>
        ในรอบบิลนี้ ห้าง <strong>{selected_store}</strong> ({d_info['billing_co']}) มียอดขาย/ยอดโอนรวมทั้งสิ้น <strong>{fmt(tot_s)}</strong> โดยมีค่าใช้จ่ายโปรโมชั่นรวมทั้ง 5 หมวดอยู่ที่ <strong>{fmt(tot_p)}</strong> คิดเป็นสัดส่วน <strong>{ratio_p:.1f}%</strong> ของยอดขายรวม ซึ่งอยู่ในระดับ {'⚠️ ค่อนข้างสูงกว่าเกณฑ์เฉลี่ย' if ratio_p > 10 else '✅ อยู่ในเกณฑ์มาตรฐาน'}</p>
        
        <p><strong>2. หมวดหมู่ค่าใช้จ่ายหลัก (Top Expense Driver):</strong><br>
        หมวดหมู่ที่มีการใช้งบประมาณสูงสุดคือ <strong>(1) ค่าส่วนลดแชร์โปรโมชั่น ({fmt(c1)})</strong> และ <strong>(4) ส่วนลดเป้าหมาย/Rebate ({fmt(c4)})</strong> สะท้อนถึงการเน้นการผลักดันยอดขายผ่านแคมเปญลดราคาและเป้าเติบโต</p>
        
        <p><strong>3. ประเด็นเร่งด่วนที่ต้องดำเนินการ (Audit Action Required):</strong><br>
        {'❌ <strong>พบความคลาดเคลื่อน / ห้างหักเงินเกินข้อตกลงจำนวน ' + str(len(over_items_info)) + ' รายการ:</strong> ' + ' · '.join(over_items_info) + '<br>👉 <em>ข้อเสนอแนะ: มอบหมายฝ่ายบัญชีออกหนังสือทักท้วง (Dispute Note) พร้อมแนบหลักฐานใบโปรโมชั่นเพื่อขอปรับปรุงยอดคืนในรอบถัดไป</em>' if over_items_info else '✅ <em>ไม่พบรายการหักเงินเกินข้อตกลง ยอดเงินในบิลห้างตรงกับเงื่อนไขสัญญาโปรโมชั่น 100%</em>'}</p>
        
        <p><strong>4. ข้อเสนอแนะเชิงกลยุทธ์สำหรับการเจรจาต่อรอง (Strategic Recommendation):</strong><br>
        แนะนำให้ทบทวนสัญญาร่วมกิจกรรม (Co-op Fund) และค่าเช่าพื้นที่พิเศษ (Display) เพื่อนำตัวเลขจริงไปใช้ต่อรองขอปรับลดเปอร์เซ็นต์ค่าธรรมเนียมในการเซ็นสัญญาการค้าปีถัดไป</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Render Matplotlib Infographic Image ──
    st.markdown("<h3 style='color:#3A8EDE;font-size:18px;font-weight:800;'>🖼️ ตัวอย่างการแสดงผลกราฟิกอินโฟกราฟิก (Executive Infographic Preview)</h3>", unsafe_allow_html=True)

    promo_dict = {"c1": c1, "c2": c2, "c3": c3, "c4": c4, "c5": c5}
    png_bytes = generate_infographic_image(
        tot_sales=tot_s,
        tot_promo=tot_p,
        promo_breakdown=promo_dict,
        overcharge_items=over_items_info,
        store_name=selected_store,
        prepared_by=cur_user.get("name", "ฝ่ายบัญชี Modern Trade")
    )

    st.image(png_bytes, caption=f"Infographic Report — {selected_store} (สัดส่วนโปรโมชั่น {ratio_p:.1f}%)", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Export Buttons for Executives (PNG Image & Formatted Excel) ──
    st.markdown("<h3 style='color:#3A8EDE;font-size:18px;font-weight:800;'>📥 ดาวน์โหลดรายงานสำหรับผู้บริหาร</h3>", unsafe_allow_html=True)
    
    dn_col1, dn_col2, _ = st.columns([2, 2, 2])

    with dn_col1:
        ts_img = datetime.now().strftime("%Y%m%d_%H%M%S")
        sn_img = selected_store[:15].replace("/","-").replace(" ","_")
        st.download_button(
            "🖼️ ดาวน์โหลดเป็นไฟล์รูปภาพ (PNG Infographic)",
            data=png_bytes,
            file_name=f"executive_infographic_{sn_img}_{ts_img}.png",
            mime="image/png",
            use_container_width=True
        )

    with dn_col2:
        # Create Multi-tab Excel for Executive
        buf_exec_excel = io.BytesIO()
        with pd.ExcelWriter(buf_exec_excel, engine="openpyxl") as writer:
            # Sheet 1: Executive Summary
            exec_summary_df = pd.DataFrame([
                {"หัวข้อ": "ห้าง / ลูกค้า", "รายละเอียด": selected_store},
                {"หัวข้อ": "บริษัทนิติบุคคล", "รายละเอียด": d_info["billing_co"]},
                {"หัวข้อ": "เลขที่เอกสาร", "รายละเอียด": d_info["doc"]},
                {"หัวข้อ": "รอบบิล / วันที่", "รายละเอียด": f"{d_info['period']} (โอนวันที่ {d_info['date']})"},
                {"หัวข้อ": "ยอดขาย/ยอดโอนรวม (บาท)", "รายละเอียด": tot_s},
                {"หัวข้อ": "ค่าใช้จ่ายโปรโมชั่น 5 หมวด (บาท)", "รายละเอียด": tot_p},
                {"หัวข้อ": "สัดส่วนโปรโมชั่นต่องานขาย (%)", "รายละเอียด": f"{ratio_p:.2f}%"},
                {"หัวข้อ": "สถานะการตรวจสอบ", "รายละเอียด": f"พบหักเกิน {len(over_items_info)} หมวด" if over_items_info else "ถูกต้องตามสัญญา"},
                {"หัวข้อ": "ผู้จัดทำรายงาน", "รายละเอียด": cur_user.get("name", "ฝ่ายบัญชี")}
            ])
            exec_summary_df.to_excel(writer, index=False, sheet_name="Executive_Summary")
            
            # Sheet 2: 5 Categories Detail
            df_info.to_excel(writer, index=False, sheet_name="Promotion_5_Categories")

        st.download_button(
            "📊 ดาวน์โหลดรายงานผู้บริหารเป็น Excel (.xlsx)",
            data=buf_exec_excel.getvalue(),
            file_name=f"executive_report_{sn_img}_{ts_img}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:16px;border-top:2.5px solid #C5DEFF;margin-top:16px;">
    <p style="color:#5A7BA8;font-size:13px;margin:0;">
        🤖 <strong>Modern Trade Reconciliation AI</strong> · ขับเคลื่อนด้วย Claude 3.5 Sonnet Vision · Built with Streamlit<br>
        <span style="font-size:11px;opacity:.70;">ระบบคัดแยก 5 หมวดหมู่โปรโมชั่น · รายงานอินโฟกราฟิกผู้บริหาร · Export PNG & Excel</span>
    </p>
</div>
""", unsafe_allow_html=True)
