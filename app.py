
import streamlit as st
from datetime import datetime
from pathlib import Path
import csv
from PIL import Image

from utils.session_manager import initialize_session

# ==========================================
# PNEUMO-AI | MAIN APPLICATION
# ==========================================

st.set_page_config(
    page_title="PNEUMO-AI | Intelligent X-Ray Analysis",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# SESSION MANAGEMENT
# ==========================================

initialize_session()

# ==========================================
# CUSTOM DESIGN SYSTEM
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #12263A;
    --muted: #718398;
    --navy: #0B1B2B;
    --navy-2: #122B40;
    --teal: #0D9488;
    --teal-bright: #35D0BE;
    --cyan: #70D9E8;
    --line: #E3EAF1;
    --surface: #FFFFFF;
    --canvas: #F3F7FA;
}

html, body, [class*="css"], [data-testid="stMarkdownContainer"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background:
        radial-gradient(ellipse at 85% 0%, rgba(13,148,136,.055), transparent 30%),
        var(--canvas);
    color: var(--ink);
}
[data-testid="stHeader"] {
    background: rgba(243,247,250,.88);
    backdrop-filter: blur(12px);
}
[data-testid="stToolbar"] { right: 1.5rem; }
.block-container {
    max-width: 1600px;
    padding-top: 2.1rem;
    padding-bottom: 3rem;
}
h1, h2, h3, h4, [data-testid="stMetricValue"] {
    font-family: 'Manrope', sans-serif !important;
    letter-spacing: -0.035em;
}
h1, h2, h3 { color: var(--ink); }
p, li { line-height: 1.72; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1B2B 0%, #10283B 100%);
    border-right: 1px solid rgba(255,255,255,.07);
}
[data-testid="stSidebar"] > div:first-child { padding-top: 1.2rem; }
[data-testid="stSidebar"] * { color: #E8F0F7; }
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,.10);
    margin: 1.25rem 0;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: .48rem .65rem;
    border-radius: 10px;
    transition: background .2s ease, transform .2s ease;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255,255,255,.075);
    transform: translateX(2px);
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    font-size: .91rem;
    font-weight: 600;
}
.brand { padding: 12px 8px 25px; }
.brand-icon {
    display: inline-flex; width: 46px; height: 46px;
    background: linear-gradient(145deg, #35D0BE, #087E83);
    border: 1px solid rgba(255,255,255,.22);
    border-radius: 15px; align-items: center; justify-content: center;
    font-size: 23px; margin-right: 10px; vertical-align: middle;
    box-shadow: 0 8px 22px rgba(13,148,136,.22);
}
.brand-name {
    display: inline-block; font-family: 'Manrope',sans-serif;
    font-size: 21px; font-weight: 800; color: white; vertical-align: middle;
    letter-spacing: -.04em;
}
.brand-sub {
    color: #8EA5B9; font-size: 9px; letter-spacing: 2.1px;
    margin-left: 57px; margin-top: -4px;
}
.main-title {
    color: var(--ink); font-family: 'Manrope',sans-serif;
    font-size: clamp(1.8rem, 2.4vw, 2.25rem); font-weight: 800;
    letter-spacing: -.055em; margin-bottom: 4px;
}
.sub-title { color: var(--muted); font-size: 13px; }

/* Hero and content surfaces */
.hero {
    position: relative; overflow: hidden;
    background: linear-gradient(112deg, #10263B 0%, #17465A 57%, #087F83 100%);
    padding: 34px 38px; border-radius: 22px; color: white;
    margin: 20px 0 28px;
    border: 1px solid rgba(255,255,255,.13);
    box-shadow: 0 18px 42px rgba(13,43,62,.15);
}
.hero:after {
    content: ""; position: absolute; width: 330px; height: 330px;
    right: -90px; top: -170px; border-radius: 50%;
    border: 1px solid rgba(255,255,255,.13);
    box-shadow: 0 0 0 32px rgba(255,255,255,.025), 0 0 0 68px rgba(255,255,255,.02);
    pointer-events: none;
}
.hero-label {
    color: #7FE0D3; font-size: 10px; font-weight: 800;
    letter-spacing: 2.2px; text-transform: uppercase;
}
.hero-title {
    font-family: 'Manrope',sans-serif; font-size: clamp(1.55rem,2.3vw,2rem);
    line-height: 1.25; font-weight: 800; letter-spacing: -.04em;
    margin: 12px 0;
}
.hero-description {
    color: #D0E1E9; font-size: 13px; max-width: 720px; line-height: 1.8;
}
.section-title {
    font-family: 'Manrope',sans-serif; font-size: 16px;
    font-weight: 800; color: #183149; letter-spacing: -.025em;
    margin: 27px 0 13px;
}
.metric-card, .info-card, .feature-card, .step-card {
    background: rgba(255,255,255,.96);
    border: 1px solid var(--line); border-radius: 17px;
    padding: 21px; box-shadow: 0 7px 24px rgba(20,45,70,.045);
    transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease;
}
.metric-card:hover, .info-card:hover, .feature-card:hover, .step-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 32px rgba(20,45,70,.085);
    border-color: #C9DCE5;
}
.metric-card { min-height: 128px; }
.metric-label {
    color: #78899B; font-size: 10px; font-weight: 800; letter-spacing: .09em;
}
.metric-value {
    color: #172D42; font-family: 'Manrope',sans-serif;
    font-size: 27px; font-weight: 800; margin-top: 12px; letter-spacing: -.04em;
}
.metric-note { color: var(--teal); font-size: 10px; margin-top: 4px; font-weight: 700; }
.info-card { min-height: 145px; }
.info-title { color: #1C354B; font-size: 14px; font-weight: 800; margin-bottom: 9px; }
.info-description { color: #718398; font-size: 12px; line-height: 1.8; }
.feature-card { min-height: 164px; padding: 20px; }
.feature-icon {
    display: inline-flex; align-items: center; justify-content: center;
    width: 42px; height: 42px; border-radius: 13px;
    background: linear-gradient(145deg,#E3F8F5,#EAF4FA);
    color: #087F83; font-size: 20px; margin-bottom: 15px;
}
.feature-title { color: #173149; font-weight: 800; font-size: 13px; margin-bottom: 6px; }
.feature-copy { color: #718398; font-size: 11px; line-height: 1.65; }
.step-card { min-height: 205px; padding: 19px; }
.step-number {
    color: #0D9488; font-family: 'Manrope',sans-serif;
    font-size: 11px; font-weight: 800; letter-spacing: .1em;
}
.step-icon {
    display: flex; align-items: center; justify-content: center;
    width: 44px; height: 44px; border-radius: 14px;
    background: #EAF7F6; color: #087F83; font-size: 21px; margin: 13px 0;
}
.step-title { color: #173149; font-weight: 800; font-size: 13px; margin-bottom: 7px; }
.step-copy { color: #718398; font-size: 11px; line-height: 1.7; }
.footer {
    color: #91A0AE; font-size: 10px; text-align: center;
    padding: 34px 0 8px; line-height: 1.8;
}
.footer .creator-credit {
    display: block; margin-top: 5px; color: #A0AEBB;
    font-size: 9px; letter-spacing: .025em;
}

/* Native Streamlit components */
div[data-testid="stMetric"] {
    background: white; border: 1px solid var(--line);
    padding: 17px 19px; border-radius: 16px;
    box-shadow: 0 5px 18px rgba(20,45,70,.035);
}
[data-testid="stMetricLabel"] { color: #718398 !important; font-weight: 700; }
[data-testid="stMetricValue"] { color: #173149 !important; font-weight: 800; }
.stButton > button, .stDownloadButton > button {
    border-radius: 11px; min-height: 43px; font-weight: 700;
    border: 1px solid #D8E3EB; transition: all .2s ease;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(105deg,#0D9488,#087F83);
    border: 0; color: white; box-shadow: 0 7px 18px rgba(13,148,136,.18);
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-1px); border-color: #0D9488;
    box-shadow: 0 7px 18px rgba(20,45,70,.09);
}
[data-testid="stFileUploader"] section {
    background: #FFFFFF; border: 1.5px dashed #B9CDD8;
    border-radius: 16px; padding: 16px;
}
[data-testid="stFileUploader"] section:hover { border-color: #0D9488; }
[data-testid="stAlert"] { border-radius: 13px; border-width: 1px; }
[data-testid="stExpander"] {
    background: white; border: 1px solid var(--line); border-radius: 13px;
}
[data-testid="stDataFrame"] {
    border: 1px solid var(--line); border-radius: 13px; overflow: hidden;
}
.stProgress > div > div > div > div { background: linear-gradient(90deg,#0D9488,#55C9BC); }
.stSelectbox > div > div, .stTextInput > div > div, .stTextArea textarea {
    border-radius: 10px;
}
hr { border-color: #E3EAF1; }
.footer { border-top: 1px solid #E7EDF3; }

/* Dynamic research dashboard */
.analytics-panel {
    background: linear-gradient(145deg,#FFFFFF 0%,#F9FCFD 100%);
    border: 1px solid #E1EAF0; border-radius: 20px;
    padding: 22px; box-shadow: 0 10px 28px rgba(20,45,70,.055);
    height: 100%;
}
.analytics-heading {
    color: #173149; font-family: 'Manrope',sans-serif;
    font-size: 14px; font-weight: 800; margin-bottom: 4px;
}
.analytics-sub { color:#8393A4; font-size:11px; margin-bottom:16px; }
.donut-wrap { display:flex; align-items:center; justify-content:center; gap:24px; flex-wrap:wrap; padding:8px 0 4px; }
.donut-chart { width:190px; height:190px; flex:0 0 190px; filter: drop-shadow(0 8px 14px rgba(15,45,65,.10)); }
.donut-center { font-family:'Manrope',sans-serif; font-size:27px; font-weight:800; fill:#173149; }
.donut-caption { font-family:'DM Sans',sans-serif; font-size:9px; fill:#8494A5; letter-spacing:1.2px; }
.legend-stack { min-width:155px; flex:1; }
.legend-row { display:flex; align-items:center; justify-content:space-between; gap:12px; padding:11px 0; border-bottom:1px solid #EDF1F5; }
.legend-label { display:flex; align-items:center; gap:9px; color:#64778A; font-size:12px; font-weight:700; }
.legend-dot { width:9px; height:9px; border-radius:50%; display:inline-block; }
.legend-value { color:#173149; font-family:'Manrope',sans-serif; font-size:15px; font-weight:800; }
.insight-strip {
    margin-top:16px; padding:12px 14px; border-radius:12px;
    background:linear-gradient(100deg,#EAF8F6,#F0F7FB);
    color:#547184; font-size:11px; line-height:1.65;
}
.activity-item { display:flex; gap:12px; padding:12px 0; border-bottom:1px solid #EDF1F5; }
.activity-mark { width:34px;height:34px;border-radius:11px;background:#EAF7F6;color:#0D9488;display:flex;align-items:center;justify-content:center;font-weight:800;flex:0 0 34px; }
.activity-title { color:#173149;font-size:12px;font-weight:800; }
.activity-meta { color:#8796A5;font-size:10px;margin-top:3px; }
.result-prob-card { background:#fff;border:1px solid #E3EAF1;border-radius:15px;padding:16px 18px; }
.result-prob-top { display:flex;justify-content:space-between;gap:10px;color:#64778A;font-size:11px;font-weight:700; }
.result-prob-value { color:#173149;font-family:'Manrope',sans-serif;font-size:20px;font-weight:800;margin:6px 0 10px; }
.result-prob-track {height:8px;background:#EDF2F5;border-radius:99px;overflow:hidden;}
.result-prob-fill {height:100%;border-radius:99px;background:linear-gradient(90deg,#0D9488,#55C9BC);}
@keyframes chartReveal { from { stroke-dashoffset:283; opacity:.35; } to { opacity:1; } }
.donut-segment { animation: chartReveal 1.15s cubic-bezier(.2,.8,.2,1) both; }

.creator-signature {
    margin: 22px 3px 5px;
    padding: 0;
    border: 0;
    border-radius: 0;
    background: transparent;
    line-height: 1.45;
}
.creator-name {
    color: #A9BAC7; font-family: 'DM Sans',sans-serif;
    font-size: 10px; font-weight: 500; letter-spacing: 0;
}
.creator-email {
    display: inline-block; color: #8297A7 !important;
    font-size: 9px; font-weight: 400; text-decoration: none; margin-top: 1px;
}
.creator-email:hover { color: #A9BAC7 !important; }

@media (max-width: 900px) {
    .block-container { padding: 1.2rem 1rem 2rem; }
    .hero { padding: 25px 22px; }
    .metric-card, .info-card, .feature-card, .step-card { padding: 17px; }
}
@media (prefers-reduced-motion: reduce) {
    *, *:before, *:after { transition: none !important; animation: none !important; }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("""
    <div class="brand">
        <span class="brand-icon">🫁</span>
        <span class="brand-name">PNEUMO-AI</span>
        <div class="brand-sub">INTELLIGENT HEALTHCARE AI</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.caption("MAIN MENU")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "X-Ray Analysis",
            "Grad-CAM Explainability",
            "Prediction History",
            "Model Information",
            "Dataset Gallery",
            "About & Disclaimer"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("""
    <div style="
        background:#1B3448;
        padding:15px;
        border-radius:12px;
        margin-top:15px;
    ">
        <div style="font-size:10px;color:#7FE0D3;font-weight:700;">
            AI MODEL STATUS
        </div>
        <div style="font-size:13px;color:white;font-weight:700;margin-top:8px;">
            ● System Initialized
        </div>
        <div style="font-size:10px;color:#A6BACB;margin-top:5px;">
            MobileNetV2 · S2_011
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="creator-signature">
            <div class="creator-name">tarigan</div>
            <a class="creator-email" href="mailto:arianto.tarigan97@gmail.com">
                arianto.tarigan97@gmail.com
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":

    history = st.session_state.get("prediction_history", [])
    active_case = st.session_state.get("active_case")

    total_analyses = len(history)
    normal_count = sum(
        1 for item in history if item.get("predicted_class") == "NORMAL"
    )
    pneumonia_count = sum(
        1 for item in history if item.get("predicted_class") == "PNEUMONIA"
    )
    average_confidence = (
        sum(float(item.get("confidence", 0)) for item in history) / total_analyses
        if total_analyses else 0
    )

    st.markdown(
        '<div class="main-title">Dashboard</div>'
        '<div class="sub-title">Intelligent Chest X-Ray Classification System</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="hero">
        <div class="hero-label">ARTIFICIAL INTELLIGENCE · MEDICAL IMAGING</div>
        <div class="hero-title">
            Advanced Chest X-Ray<br>Analysis with Explainable AI
        </div>
        <div class="hero-description">
            A research-based artificial intelligence system designed
            to classify chest X-ray images into NORMAL and PNEUMONIA
            categories, supported by visual explanation using Grad-CAM.
            This application is intended for research and educational purposes.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Live Session Overview</div>',
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TOTAL ANALYSES", total_analyses, help="Jumlah prediksi pada sesi Streamlit aktif.")
    m2.metric("NORMAL", normal_count)
    m3.metric("PNEUMONIA", pneumonia_count)
    m4.metric(
        "AVERAGE CONFIDENCE",
        f"{average_confidence * 100:.2f}%" if total_analyses else "—"
    )

    st.caption("Statistik ini dihitung dari riwayat sesi aktif, bukan metrik evaluasi dataset penelitian.")

    left, right = st.columns([1.08, 1])

    with left:
        st.markdown('<div class="section-title">Session Classification Summary</div>', unsafe_allow_html=True)
        normal_pct = (normal_count / total_analyses * 100) if total_analyses else 0
        pneumonia_pct = (pneumonia_count / total_analyses * 100) if total_analyses else 0
        circumference = 283
        normal_dash = circumference * normal_count / total_analyses if total_analyses else 0
        pneumonia_dash = circumference * pneumonia_count / total_analyses if total_analyses else 0
        normal_offset = 0
        pneumonia_offset = -normal_dash
        donut_svg = f"""
        <svg class="donut-chart" viewBox="0 0 200 200" role="img" aria-label="Distribusi prediksi sesi">
          <circle cx="100" cy="100" r="45" fill="none" stroke="#EDF2F5" stroke-width="18"/>
          <circle cx="100" cy="100" r="45" fill="none" stroke="#0D9488" stroke-width="18"
            stroke-linecap="round" stroke-dasharray="{normal_dash:.2f} {circumference-normal_dash:.2f}"
            stroke-dashoffset="0" transform="rotate(-90 100 100)" class="donut-segment"/>
          <circle cx="100" cy="100" r="45" fill="none" stroke="#E7A64B" stroke-width="18"
            stroke-linecap="round" stroke-dasharray="{pneumonia_dash:.2f} {circumference-pneumonia_dash:.2f}"
            stroke-dashoffset="{-normal_dash:.2f}" transform="rotate(-90 100 100)" class="donut-segment"/>
          <text x="100" y="96" text-anchor="middle" class="donut-center">{total_analyses}</text>
          <text x="100" y="115" text-anchor="middle" class="donut-caption">ANALYSES</text>
        </svg>
        """
        st.markdown(
            f'<div class="analytics-panel"><div class="analytics-heading">Prediction distribution</div>'
            f'<div class="analytics-sub">Komposisi hasil klasifikasi pada sesi Streamlit aktif</div>'
            f'<div class="donut-wrap">{donut_svg}<div class="legend-stack">'
            f'<div class="legend-row"><div class="legend-label"><span class="legend-dot" style="background:#0D9488"></span>NORMAL</div>'
            f'<div><span class="legend-value">{normal_count}</span><span style="color:#8A9AAA;font-size:10px;"> · {normal_pct:.1f}%</span></div></div>'
            f'<div class="legend-row"><div class="legend-label"><span class="legend-dot" style="background:#E7A64B"></span>PNEUMONIA</div>'
            f'<div><span class="legend-value">{pneumonia_count}</span><span style="color:#8A9AAA;font-size:10px;"> · {pneumonia_pct:.1f}%</span></div></div>'
            f'<div class="legend-row"><div class="legend-label">Average confidence</div>'
            f'<div class="legend-value">{average_confidence*100:.1f}%</div></div></div></div>'
            f'<div class="insight-strip">{"Belum ada prediksi pada sesi ini. Mulai analisis untuk mengisi visualisasi." if not total_analyses else f"Distribusi saat ini: {normal_count} citra NORMAL dan {pneumonia_count} citra PNEUMONIA. Angka ini merupakan ringkasan penggunaan aplikasi, bukan metrik evaluasi dataset."}</div></div>',
            unsafe_allow_html=True
        )

    with right:
        st.markdown('<div class="section-title">Current Workspace</div>', unsafe_allow_html=True)
        if active_case is not None:
            st.markdown(
                f'<div class="analytics-panel"><div class="analytics-heading">Active Chest X-Ray Case</div>'
                f'<div class="analytics-sub">Workspace aktif untuk klasifikasi dan interpretasi Grad-CAM</div>'
                f'<div class="activity-item"><div class="activity-mark">XR</div><div>'
                f'<div class="activity-title">{active_case.get("filename", "-")}</div>'
                f'<div class="activity-meta">Case ID · {active_case.get("case_id", "-")}</div></div></div>'
                f'<div class="activity-item"><div class="activity-mark">AI</div><div>'
                f'<div class="activity-title">{"Prediction completed" if active_case.get("prediction") is not None else "Awaiting prediction"}</div>'
                f'<div class="activity-meta">{"Hasil klasifikasi tersedia untuk Grad-CAM." if active_case.get("prediction") is not None else "Jalankan analisis pada halaman X-Ray Analysis."}</div></div></div>'
                f'<div class="activity-item"><div class="activity-mark">✳</div><div>'
                f'<div class="activity-title">{len(active_case.get("gradcam_results", {}))} Grad-CAM result(s) cached</div>'
                f'<div class="activity-meta">Visualisasi tersimpan selama sesi aktif.</div></div></div></div>',
                unsafe_allow_html=True
            )
            if active_case.get("prediction") is None:
                st.warning("Citra aktif belum dianalisis.")
            else:
                st.success("Citra aktif siap digunakan pada halaman Grad-CAM.")
        else:
            st.markdown(
                '<div class="analytics-panel"><div class="analytics-heading">Your research workspace</div>'
                '<div class="analytics-sub">Status sesi aplikasi</div>'
                '<div style="padding:25px 8px;text-align:center;">'
                '<div style="font-size:38px;margin-bottom:10px;">⌁</div>'
                '<div style="color:#173149;font-weight:800;font-size:14px;">No active case</div>'
                '<div style="color:#8796A5;font-size:11px;margin-top:6px;">Unggah citra melalui X-Ray Analysis untuk memulai workspace.</div>'
                '</div></div>',
                unsafe_allow_html=True
            )

    st.markdown('<div class="section-title">Research Model Profile</div>', unsafe_allow_html=True)
    p1, p2, p3, p4 = st.columns(4)
    p1.markdown('<div class="metric-card"><div class="metric-label">AI ARCHITECTURE</div><div class="metric-value" style="font-size:22px;">MobileNetV2</div><div class="metric-note">Transfer Learning</div></div>', unsafe_allow_html=True)
    p2.markdown('<div class="metric-card"><div class="metric-label">SELECTED MODEL</div><div class="metric-value" style="font-size:22px;">S2_011</div><div class="metric-note">Selected experiment</div></div>', unsafe_allow_html=True)
    p3.markdown('<div class="metric-card"><div class="metric-label">INPUT RESOLUTION</div><div class="metric-value" style="font-size:22px;">224 × 224</div><div class="metric-note">RGB image</div></div>', unsafe_allow_html=True)
    p4.markdown('<div class="metric-card"><div class="metric-label">CLASSIFICATION</div><div class="metric-value" style="font-size:22px;">2 Classes</div><div class="metric-note">NORMAL / PNEUMONIA</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Research Configuration</div>', unsafe_allow_html=True)
    config_left, config_right = st.columns([1.2, 1])

    with config_left:
        st.markdown("""
        <div class="info-card">
            <div class="info-title">Selected Experiment: S2_011</div>
            <div class="info-description">
                Architecture: MobileNetV2<br>
                Transfer Learning: Enabled<br>
                Fine-tuning: Enabled<br>
                Optimizer: Adam<br>
                Learning Rate: 0.001<br>
                Batch Size: 32<br>
                Dropout: 0.3<br>
                Input Preprocessing: MobileNetV2 [-1, 1]
            </div>
        </div>
        """, unsafe_allow_html=True)

    with config_right:
        st.markdown("""
        <div class="info-card">
            <div class="info-title">Research Use & Limitation</div>
            <div class="info-description">
                PNEUMO-AI merupakan prototipe penelitian untuk klasifikasi
                citra X-Ray dada dan eksplorasi visualisasi Grad-CAM.
                Hasil prediksi dan heatmap bukan diagnosis medis dan tidak
                menggantikan pemeriksaan tenaga medis profesional.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        PNEUMO-AI · INTELLIGENT CHEST X-RAY ANALYSIS<br>
        Research Prototype · Not a substitute for professional medical diagnosis
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# OTHER PAGES - PNEUMO-AI MODULES
# ==========================================

elif page == "X-Ray Analysis":

    from io import BytesIO
    from PIL import Image
    from utils.predictor import predict_image
    from utils.session_manager import set_active_case, get_active_case, save_prediction, get_prediction

    st.markdown(
        '<div class="main-title">X-Ray Analysis</div>'
        '<div class="sub-title">AI-assisted Chest X-Ray Classification</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="info-card">
        <div class="info-title">Chest X-Ray Classification</div>
        <div class="info-description">
            Upload citra X-Ray dada untuk mendapatkan hasil klasifikasi
            menggunakan model MobileNetV2 S2_011.
            Sistem menghasilkan prediksi NORMAL atau PNEUMONIA
            beserta probabilitas masing-masing kelas. Citra yang sama
            akan digunakan kembali pada halaman Grad-CAM tanpa upload ulang.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Upload X-Ray Image</div>',
                unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Pilih citra X-Ray dada",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=False,
        key="xray_uploader"
    )

    if uploaded_file is not None:
        try:
            image_bytes = uploaded_file.getvalue()
            original_image = Image.open(BytesIO(image_bytes)).convert("RGB")
            active_case = set_active_case(
                uploaded_file.name, image_bytes, original_image
            )
            # Central case library: single and batch cases share the same Grad-CAM selector.
            if "gradcam_case_library" not in st.session_state:
                st.session_state["gradcam_case_library"] = {}
            st.session_state["gradcam_case_library"][active_case["case_id"]] = active_case

            left, right = st.columns([1, 1])
            with left:
                st.markdown("**Original Chest X-Ray**")
                st.image(original_image, use_container_width=True)
                st.caption(f"Nama file: {uploaded_file.name}")

            with right:
                st.markdown("**Image Information**")
                st.write(f"Format: {uploaded_file.type}")
                st.write(
                    f"Resolusi asli: {original_image.width} × {original_image.height}"
                )
                st.write("Model: MobileNetV2 S2_011")
                st.write("Input model: 224 × 224 RGB")
                st.caption(f"Case ID: {active_case['case_id']}")

            st.markdown("---")

            if st.button(
                "ANALYZE X-RAY",
                type="primary",
                use_container_width=True
            ):
                with st.spinner("Model sedang menganalisis citra..."):
                    try:
                        result = predict_image(active_case["original_image"])
                        save_prediction(result)
                        st.success("Analisis berhasil disimpan pada sesi ini.")
                    except Exception as e:
                        st.error(f"Analisis gagal: {e}")

            prediction = get_prediction()
            latest = st.session_state.get("latest_analysis")

            if prediction is not None and latest is not None:
                st.markdown("---")
                st.markdown(
                    '<div class="section-title">Classification Result</div>',
                    unsafe_allow_html=True
                )

                predicted_class = prediction["predicted_class"]
                confidence = prediction["confidence"]
                probabilities = prediction["probabilities"]

                if predicted_class == "NORMAL":
                    st.success("HASIL KLASIFIKASI: NORMAL")
                else:
                    st.warning("HASIL KLASIFIKASI: PNEUMONIA")

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Predicted Class", predicted_class)
                with c2:
                    st.metric("Confidence", f"{confidence * 100:.2f}%")
                with c3:
                    st.metric("Model", "S2_011")

                st.markdown('<div class="section-title">Class Probability Profile</div>', unsafe_allow_html=True)
                p1, p2 = st.columns(2)
                for col, class_name, color in [
                    (p1, "NORMAL", "#0D9488"),
                    (p2, "PNEUMONIA", "#E7A64B")
                ]:
                    value = max(0.0, min(1.0, float(probabilities[class_name])))
                    with col:
                        st.markdown(
                            f'<div class="result-prob-card"><div class="result-prob-top"><span>{class_name}</span><span>MODEL OUTPUT</span></div>'
                            f'<div class="result-prob-value">{value*100:.2f}%</div>'
                            f'<div class="result-prob-track"><div class="result-prob-fill" style="width:{value*100:.2f}%;background:linear-gradient(90deg,{color},{color}AA);"></div></div></div>',
                            unsafe_allow_html=True
                        )

                st.caption(f"Waktu analisis: {latest['timestamp']}")
                st.info(
                    "Hasil ini merupakan keluaran model penelitian dan bukan diagnosis medis. "
                    "Interpretasi klinis harus dilakukan oleh tenaga medis profesional. "
                    "Buka menu Grad-CAM Explainability untuk melihat visualisasi citra yang sama."
                )

        except Exception as e:
            st.error(f"Gagal membaca atau memproses citra: {e}")
    else:
        active_case = get_active_case()
        if active_case is not None:
            st.info(
                f"Kasus aktif tersimpan dalam sesi: {active_case['filename']} "
                "(pilih kembali citra melalui uploader untuk menampilkannya)."
            )
        else:
            st.info("Silakan unggah citra X-Ray untuk memulai analisis.")


    # ==========================================
    # BATCH X-RAY ANALYSIS
    # ==========================================
    st.markdown("---")
    st.markdown('<div class="section-title">Batch X-Ray Analysis</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
        <div class="info-title">Collective Image Classification</div>
        <div class="info-description">
            Unggah beberapa citra sekaligus untuk menjalankan klasifikasi berurutan
            menggunakan model MobileNetV2 S2_011. Hasil batch disimpan dalam riwayat
            sesi dan dapat diunduh sebagai CSV. Grad-CAM tetap dijalankan secara
            individual melalui Active Case.
        </div>
    </div>
    """, unsafe_allow_html=True)

    batch_files = st.file_uploader(
        "Pilih beberapa citra X-Ray (JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="batch_xray_uploader",
        help="Untuk menjaga stabilitas, unggah maksimal 50 citra per batch dan ukuran maksimal 15 MB per file."
    )

    MAX_BATCH_FILES = 50
    MAX_FILE_BYTES = 15 * 1024 * 1024

    if batch_files:
        batch_count = len(batch_files)
        batch_total_bytes = sum(len(item.getvalue()) for item in batch_files)
        batch_size_mb = batch_total_bytes / (1024 * 1024)
        import hashlib
        current_batch_hash = hashlib.sha256()
        for item in batch_files:
            raw = item.getvalue()
            current_batch_hash.update(item.name.encode("utf-8", errors="ignore"))
            current_batch_hash.update(hashlib.sha256(raw).digest())
        current_batch_id = current_batch_hash.hexdigest()[:16]
        b1, b2, b3 = st.columns(3)
        b1.metric("Selected images", batch_count)
        b2.metric("Total upload size", f"{batch_size_mb:.1f} MB")
        b3.metric("Batch limit", f"{MAX_BATCH_FILES} images")

        if batch_count > MAX_BATCH_FILES:
            st.error(f"Jumlah citra melebihi batas {MAX_BATCH_FILES} file. Kurangi jumlah file sebelum memulai.")
        elif batch_total_bytes > 200 * 1024 * 1024:
            st.error("Total ukuran batch melebihi batas 200 MB. Kurangi jumlah atau ukuran file untuk menjaga stabilitas aplikasi.")
        else:
            with st.expander("Review uploaded files", expanded=False):
                st.dataframe(
                    [{"No.": idx + 1, "Filename": item.name,
                      "Size (MB)": round(len(item.getvalue()) / (1024 * 1024), 2)}
                     for idx, item in enumerate(batch_files)],
                    use_container_width=True,
                    hide_index=True
                )

            run_batch = st.button(
                "RUN BATCH ANALYSIS",
                type="primary",
                use_container_width=True,
                key="run_batch_analysis"
            )

            if run_batch:
                from io import BytesIO
                from PIL import Image

                batch_id = current_batch_id
                if st.session_state.get("last_batch_id") == batch_id:
                    st.info("Batch yang sama sudah pernah diproses pada sesi ini. Hasil sebelumnya ditampilkan kembali.")
                else:
                    batch_output = []
                    batch_errors = []
                    progress = st.progress(0, text="Menyiapkan batch analysis...")
                    status = st.empty()
                    total = len(batch_files)

                    for index, item in enumerate(batch_files, start=1):
                        status.caption(f"Memproses {index}/{total}: {item.name}")
                        try:
                            raw = item.getvalue()
                            if len(raw) > MAX_FILE_BYTES:
                                raise ValueError("Ukuran file melebihi batas 15 MB.")

                            image = Image.open(BytesIO(raw)).convert("RGB")
                            result = predict_image(image)

                            record = {
                                "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                                "filename": item.name,
                                "predicted_class": result["predicted_class"],
                                "confidence": float(result["confidence"]),
                                "probabilities": {
                                    "NORMAL": float(result["probabilities"]["NORMAL"]),
                                    "PNEUMONIA": float(result["probabilities"]["PNEUMONIA"]),
                                },
                                "case_id": "BATCH-" + hashlib.sha256(raw).hexdigest()[:12],
                                "batch_id": batch_id,
                            }
                            batch_output.append(record)

                            if "gradcam_case_library" not in st.session_state:
                                st.session_state["gradcam_case_library"] = {}
                            st.session_state["gradcam_case_library"][record["case_id"]] = {
                                "case_id": record["case_id"],
                                "image_hash": hashlib.sha256(raw).hexdigest(),
                                "filename": item.name,
                                "image_bytes": raw,
                                # Keep compressed bytes in memory; decode only when selected for Grad-CAM.
                                "original_image": None,
                                "created_at": record["timestamp"],
                                "prediction": {
                                    "predicted_class": result["predicted_class"],
                                    "confidence": float(result["confidence"]),
                                    "probabilities": {
                                        "NORMAL": float(result["probabilities"]["NORMAL"]),
                                        "PNEUMONIA": float(result["probabilities"]["PNEUMONIA"]),
                                    },
                                },
                                "gradcam_results": {},
                                "batch_id": batch_id,
                            }
                        except Exception as exc:
                            batch_errors.append({
                                "filename": item.name,
                                "error": f"{type(exc).__name__}: {exc}"
                            })

                        progress.progress(index / total, text=f"Processed {index} of {total}")

                    # Append successful records once, so dashboard and history reflect batch activity.
                    if batch_output:
                        history = st.session_state.get("prediction_history", [])
                        existing_case_ids = {row.get("case_id") for row in history}
                        for record in reversed(batch_output):
                            if record["case_id"] not in existing_case_ids:
                                history.insert(0, record)
                        st.session_state.prediction_history = history

                    st.session_state["batch_analysis_results"] = batch_output
                    st.session_state["batch_analysis_errors"] = batch_errors
                    st.session_state["last_batch_id"] = batch_id
                    st.session_state["last_batch_timestamp"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    progress.progress(1.0, text="Batch processing completed.")
                    status.empty()

                    if batch_output:
                        st.success(f"Batch selesai: {len(batch_output)} citra berhasil dianalisis.")
                    if batch_errors:
                        st.warning(f"{len(batch_errors)} file tidak berhasil diproses. Periksa daftar error di bawah.")

            results = st.session_state.get("batch_analysis_results", [])
            errors = st.session_state.get("batch_analysis_errors", [])
            if st.session_state.get("last_batch_id") != current_batch_id:
                results = []
                errors = []

            if results:
                st.markdown('<div class="section-title">Batch Results</div>', unsafe_allow_html=True)
                normal_total = sum(row["predicted_class"] == "NORMAL" for row in results)
                pneumonia_total = sum(row["predicted_class"] == "PNEUMONIA" for row in results)
                average_batch_conf = sum(row["confidence"] for row in results) / len(results)

                r1, r2, r3, r4 = st.columns(4)
                r1.metric("Successful", len(results))
                r2.metric("NORMAL", normal_total)
                r3.metric("PNEUMONIA", pneumonia_total)
                r4.metric("Average confidence", f"{average_batch_conf * 100:.2f}%")

                st.markdown('<div class="section-title">Classification Results Table</div>', unsafe_allow_html=True)
                display_rows = [{
                    "Filename": row["filename"],
                    "Prediction": row["predicted_class"],
                    "Confidence": f'{row["confidence"] * 100:.2f}%',
                    "NORMAL": f'{row["probabilities"]["NORMAL"] * 100:.2f}%',
                    "PNEUMONIA": f'{row["probabilities"]["PNEUMONIA"] * 100:.2f}%',
                    "Case ID": row["case_id"],
                } for row in results]
                st.dataframe(display_rows, use_container_width=True, hide_index=True)

                import csv
                from io import StringIO
                csv_buffer = StringIO()
                writer = csv.DictWriter(
                    csv_buffer,
                    fieldnames=[
                        "timestamp", "filename", "predicted_class", "confidence",
                        "probability_normal", "probability_pneumonia", "case_id", "batch_id"
                    ]
                )
                writer.writeheader()
                for row in results:
                    writer.writerow({
                        "timestamp": row["timestamp"],
                        "filename": row["filename"],
                        "predicted_class": row["predicted_class"],
                        "confidence": row["confidence"],
                        "probability_normal": row["probabilities"]["NORMAL"],
                        "probability_pneumonia": row["probabilities"]["PNEUMONIA"],
                        "case_id": row["case_id"],
                        "batch_id": row["batch_id"],
                    })
                st.download_button(
                    "DOWNLOAD BATCH RESULTS (CSV)",
                    data=csv_buffer.getvalue().encode("utf-8-sig"),
                    file_name=f"PNEUMO_AI_BATCH_{st.session_state.get('last_batch_id', 'RESULTS')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

                st.caption(
                    "Catatan: confidence dan probabilitas merupakan keluaran model, bukan kepastian diagnosis. "
                    "Hasil batch adalah ringkasan analisis aplikasi dan bukan evaluasi performa pada dataset uji."
                )

            if errors:
                with st.expander(f"Files not processed ({len(errors)})", expanded=True):
                    st.dataframe(errors, use_container_width=True, hide_index=True)
    else:
        st.caption("Belum ada file batch yang dipilih. Fitur analisis satuan di atas tetap dapat digunakan seperti biasa.")


elif page == "Grad-CAM Explainability":

    from utils.gradcam import generate_gradcam
    from utils.session_manager import get_active_case, get_prediction, get_gradcam, save_gradcam

    st.markdown(
        '<div class="main-title">Grad-CAM Explainability</div>'
        '<div class="sub-title">'
        'Visual explanation of MobileNetV2 S2_011 predictions'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="info-card">
        <div class="info-title">Explainable Artificial Intelligence</div>
        <div class="info-description">
            Grad-CAM menghasilkan visualisasi area citra yang
            berkontribusi terhadap prediksi model. Visualisasi ini
            digunakan sebagai pendukung interpretasi hasil klasifikasi,
            bukan sebagai bukti diagnosis medis. Halaman ini menggunakan
            citra aktif dari X-Ray Analysis, sehingga tidak perlu upload ulang.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # All successfully analyzed single and batch images are selectable here.
    case_library = st.session_state.get("gradcam_case_library", {})
    if not case_library:
        st.info("Belum ada citra yang tersimpan untuk Grad-CAM. Unggah dan analisis citra melalui X-Ray Analysis, baik satuan maupun batch.")
        active_case = None
        prediction = None
    else:
        case_ids = list(case_library.keys())
        case_labels = {
            case_id: (
                f'{case_library[case_id].get("filename", "Unnamed image")} '
                f'· {case_library[case_id].get("prediction", {}).get("predicted_class", "UNCLASSIFIED")} '
                f'· {case_id}'
            )
            for case_id in case_ids
        }
        current_active = get_active_case()
        default_case_id = (
            current_active.get("case_id")
            if current_active and current_active.get("case_id") in case_library
            else case_ids[-1]
        )
        if st.session_state.get("gradcam_case_selector") not in case_library:
            st.session_state["gradcam_case_selector"] = default_case_id

        selected_case_id = st.selectbox(
            "Pilih citra untuk Grad-CAM",
            options=case_ids,
            index=case_ids.index(default_case_id),
            format_func=lambda value: case_labels[value],
            key="gradcam_case_selector",
            help="Daftar ini memuat citra yang berhasil dianalisis melalui upload satuan maupun batch selama sesi aplikasi aktif."
        )
        active_case = case_library[selected_case_id]
        if active_case.get("original_image") is None:
            from io import BytesIO
            from PIL import Image
            active_case["original_image"] = Image.open(
                BytesIO(active_case["image_bytes"])
            ).convert("RGB")
        # Grad-CAM utilities use the active-case interface; point it to the selected library entry.
        st.session_state["active_case"] = active_case
        prediction = active_case.get("prediction")

        st.caption(
            f'{len(case_library)} citra tersedia · '
            "Pilih salah satu citra untuk membuat visualisasi Grad-CAM."
        )

    if active_case is None:
        st.warning("Belum ada citra yang tersedia. Silakan analisis citra melalui X-Ray Analysis.")
    elif prediction is None:
        st.warning("Citra sudah tersedia, tetapi belum dianalisis. Jalankan ANALYZE X-RAY pada halaman X-Ray Analysis terlebih dahulu.")
        st.image(active_case["original_image"], caption=active_case["filename"], use_container_width=True)
    else:
        original_image = active_case["original_image"]
        st.markdown('<div class="section-title">Active Chest X-Ray Case</div>', unsafe_allow_html=True)
        st.image(
            original_image,
            caption=f"{active_case['filename']} · Case ID: {active_case['case_id']}",
            use_container_width=True
        )
        st.caption(
            f"Prediksi model: {prediction['predicted_class']} | "
            f"Confidence: {prediction['confidence'] * 100:.2f}%"
        )
        st.markdown("---")

        target_option = st.selectbox(
            "Kelas yang akan dijelaskan",
            ["Predicted Class (Automatic)", "NORMAL", "PNEUMONIA"],
            index=0
        )
        actual_target = (
            prediction["predicted_class"]
            if target_option == "Predicted Class (Automatic)"
            else target_option
        )

        cached_result = get_gradcam(actual_target)

        if st.button(
            "GENERATE GRAD-CAM",
            type="primary",
            use_container_width=True
        ):
            with st.spinner("Menghitung Grad-CAM menggunakan model S2_011..."):
                try:
                    result = generate_gradcam(
                        original_image,
                        target_class=None if target_option == "Predicted Class (Automatic)" else actual_target
                    )
                    save_gradcam(actual_target, result)
                    cached_result = result
                    st.success("Grad-CAM berhasil dibuat dan disimpan pada cache kasus aktif.")
                except Exception as e:
                    st.error(f"Grad-CAM gagal dijalankan: {e}")
                    cached_result = None

        if cached_result is not None:
            result = cached_result
            st.markdown("---")
            st.markdown(
                '<div class="section-title">Grad-CAM Visualization Results</div>',
                unsafe_allow_html=True
            )

            predicted_class = result["predicted_class"]
            explained_class = result["target_class"]
            probability = result["probability"]

            if predicted_class == "NORMAL":
                st.success(f"MODEL PREDICTION: {predicted_class}")
            else:
                st.warning(f"MODEL PREDICTION: {predicted_class}")

            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Predicted Class", predicted_class)
            with c2:
                st.metric("Explained Class", explained_class)
            with c3:
                st.metric("Class Probability", f"{probability * 100:.2f}%")

            st.markdown(f"**Target explanation:** {explained_class}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image(result["original_image"], caption="Original X-Ray", use_container_width=True)
            with col2:
                st.image(result["heatmap"], caption="Grad-CAM Heatmap", use_container_width=True)
            with col3:
                st.image(result["overlay"], caption="Grad-CAM Overlay", use_container_width=True)

            st.info(
                "Area berwarna pada heatmap menunjukkan kontribusi relatif terhadap kelas yang dipilih. "
                "Visualisasi ini merupakan penjelasan model dan tidak menunjukkan lokasi penyakit secara pasti."
            )
        else:
            st.info("Pilih kelas penjelasan, lalu tekan GENERATE GRAD-CAM. Hasil yang sudah dibuat akan tersimpan dalam sesi untuk kasus ini.")


elif page == "Prediction History":

    import pandas as pd

    history = st.session_state.get("prediction_history", [])
    active_case = st.session_state.get("active_case")

    st.markdown('<div class="main-title">Prediction History</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">Riwayat klasifikasi dan detail kasus selama sesi aplikasi berlangsung</div>',
        unsafe_allow_html=True
    )

    if history:
        total_count = len(history)
        normal_count = sum(1 for item in history if item.get("predicted_class") == "NORMAL")
        pneumonia_count = sum(1 for item in history if item.get("predicted_class") == "PNEUMONIA")

        k1, k2, k3 = st.columns(3)
        with k1:
            st.metric("Total Analyses", total_count)
        with k2:
            st.metric("NORMAL", normal_count)
        with k3:
            st.metric("PNEUMONIA", pneumonia_count)

        st.markdown('<div class="section-title">Session Analytics</div>', unsafe_allow_html=True)
        hist_left, hist_right = st.columns(2)
        with hist_left:
            st.markdown('<div class="analytics-panel"><div class="analytics-heading">Class distribution</div><div class="analytics-sub">Jumlah prediksi per kelas</div></div>', unsafe_allow_html=True)
            st.bar_chart({"Jumlah kasus": {"NORMAL": normal_count, "PNEUMONIA": pneumonia_count}}, color="#0D9488", height=210)
        with hist_right:
            st.markdown('<div class="analytics-panel"><div class="analytics-heading">Confidence overview</div><div class="analytics-sub">Rata-rata confidence dari seluruh riwayat sesi</div></div>', unsafe_allow_html=True)
            confidence_values = [float(item.get("confidence", 0)) * 100 for item in history]
            mean_conf = sum(confidence_values) / len(confidence_values) if confidence_values else 0
            st.metric("Average confidence", f"{mean_conf:.2f}%")
            st.progress(max(0.0, min(1.0, mean_conf / 100)))
            st.caption("Confidence merupakan tingkat keyakinan keluaran model pada prediksi, bukan probabilitas model benar.")

        st.markdown('<div class="section-title">Riwayat Analisis</div>', unsafe_allow_html=True)

        filter_col, search_col = st.columns([1, 2])
        with filter_col:
            class_filter = st.selectbox(
                "Filter prediksi",
                ["Semua", "NORMAL", "PNEUMONIA"],
                key="history_class_filter"
            )
        with search_col:
            search_term = st.text_input(
                "Cari nama file atau Case ID",
                placeholder="Masukkan nama file atau Case ID...",
                key="history_search"
            ).strip().lower()

        filtered_history = []
        for item in history:
            predicted_class = item.get("predicted_class", "-")
            filename = item.get("filename", "-")
            case_id = item.get("case_id", "-")

            if class_filter != "Semua" and predicted_class != class_filter:
                continue
            if search_term and search_term not in filename.lower() and search_term not in case_id.lower():
                continue
            filtered_history.append(item)

        st.caption(f"Menampilkan {len(filtered_history)} dari {total_count} catatan sesi.")

        if filtered_history:
            table_rows = []
            for item in filtered_history:
                probabilities = item.get("probabilities", {}) or {}
                table_rows.append({
                    "Waktu": item.get("timestamp", "-"),
                    "Nama File": item.get("filename", "-"),
                    "Prediksi": item.get("predicted_class", "-"),
                    "Confidence": f"{float(item.get('confidence', 0)) * 100:.2f}%",
                    "NORMAL": f"{float(probabilities.get('NORMAL', 0)) * 100:.2f}%",
                    "PNEUMONIA": f"{float(probabilities.get('PNEUMONIA', 0)) * 100:.2f}%",
                    "Case ID": item.get("case_id", "-")
                })

            st.dataframe(
                table_rows,
                use_container_width=True,
                hide_index=True
            )

            st.markdown('<div class="section-title">Detail Kasus</div>', unsafe_allow_html=True)
            for index, item in enumerate(filtered_history):
                case_id = item.get("case_id", "-")
                filename = item.get("filename", "-")
                predicted_class = item.get("predicted_class", "-")
                confidence = float(item.get("confidence", 0))
                probabilities = item.get("probabilities", {}) or {}
                is_active_case = (
                    active_case is not None
                    and active_case.get("case_id") == case_id
                )

                with st.expander(
                    f"{predicted_class} · {filename} · {item.get('timestamp', '-')}",
                    expanded=False
                ):
                    d1, d2, d3 = st.columns(3)
                    with d1:
                        st.metric("Predicted Class", predicted_class)
                    with d2:
                        st.metric("Confidence", f"{confidence * 100:.2f}%")
                    with d3:
                        st.metric("Case ID", case_id)

                    st.markdown("**Class Probabilities**")
                    prob_left, prob_right = st.columns(2)
                    normal_probability = float(probabilities.get("NORMAL", 0))
                    pneumonia_probability = float(probabilities.get("PNEUMONIA", 0))
                    with prob_left:
                        st.write(f"NORMAL: {normal_probability * 100:.2f}%")
                        st.progress(max(0.0, min(1.0, normal_probability)))
                    with prob_right:
                        st.write(f"PNEUMONIA: {pneumonia_probability * 100:.2f}%")
                        st.progress(max(0.0, min(1.0, pneumonia_probability)))

                    st.caption(f"Waktu analisis: {item.get('timestamp', '-')}")

                    if is_active_case:
                        st.success("Citra ini masih tersedia sebagai Active Chest X-Ray Case.")
                        st.image(
                            active_case.get("original_image"),
                            caption=filename,
                            use_container_width=True
                        )
                        cached_gradcam = active_case.get("gradcam_results", {})
                        if cached_gradcam:
                            st.caption(
                                "Cache Grad-CAM tersedia untuk: "
                                + ", ".join(sorted(cached_gradcam.keys()))
                            )
                    else:
                        st.info(
                            "Detail prediksi tersimpan, tetapi preview citra tidak tersedia "
                            "karena kasus ini bukan lagi citra aktif pada sesi sekarang."
                        )

            st.markdown('<div class="section-title">Ekspor dan Pengelolaan Riwayat</div>', unsafe_allow_html=True)
            export_rows = []
            for item in history:
                probabilities = item.get("probabilities", {}) or {}
                export_rows.append({
                    "timestamp": item.get("timestamp", ""),
                    "filename": item.get("filename", ""),
                    "predicted_class": item.get("predicted_class", ""),
                    "confidence": item.get("confidence", 0),
                    "normal_probability": probabilities.get("NORMAL", 0),
                    "pneumonia_probability": probabilities.get("PNEUMONIA", 0),
                    "case_id": item.get("case_id", ""),
                    "image_hash": item.get("image_hash", "")
                })

            export_col, delete_col = st.columns([1, 1])
            with export_col:
                csv_data = pd.DataFrame(export_rows).to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    "DOWNLOAD HISTORY CSV",
                    data=csv_data,
                    file_name="PNEUMO_AI_prediction_history.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            with delete_col:
                delete_options = {
                    f"{item.get('timestamp', '-')} | {item.get('filename', '-')} | {item.get('case_id', '-')}": item.get("case_id")
                    for item in history
                }
                selected_label = st.selectbox(
                    "Pilih catatan yang akan dihapus",
                    list(delete_options.keys()),
                    key="history_delete_selection"
                )
                confirm_delete = st.checkbox(
                    "Saya yakin ingin menghapus catatan terpilih",
                    key="history_confirm_delete"
                )
                if st.button(
                    "HAPUS CATATAN TERPILIH",
                    type="secondary",
                    use_container_width=True,
                    disabled=not confirm_delete
                ):
                    selected_case_id = delete_options[selected_label]
                    st.session_state.prediction_history = [
                        item for item in st.session_state.prediction_history
                        if item.get("case_id") != selected_case_id
                    ]
                    if (
                        st.session_state.get("latest_analysis") is not None
                        and st.session_state.latest_analysis.get("case_id") == selected_case_id
                    ):
                        st.session_state.latest_analysis = None
                    st.session_state.history_confirm_delete = False
                    st.success("Catatan riwayat terpilih berhasil dihapus.")
                    st.rerun()

        else:
            st.info("Tidak ada riwayat yang sesuai dengan filter atau kata pencarian.")

        st.info(
            "Riwayat bersifat sementara dan hanya tersedia selama sesi Streamlit aktif. "
            "Menghapus catatan riwayat tidak menghapus file model atau dataset penelitian."
        )

    else:
        st.info("Belum ada riwayat prediksi. Silakan lakukan analisis pada menu X-Ray Analysis.")


elif page == "Model Information":

    st.markdown(
        '<div class="main-title">Model Information</div>'
        '<div class="sub-title">Research profile and validation results of the selected model</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="info-card">
        <div class="info-title">Selected Research Model · S2_011</div>
        <div class="info-description">
            MobileNetV2 transfer learning model selected from the S2 V2 experiment.
            Selection was based on the highest validation F1-score among 24 completed configurations.
            The metrics below are validation metrics, not test-set performance.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Selected Model Performance · Validation Set</div>', unsafe_allow_html=True)
    metric_cols = st.columns(4)
    validation_metrics = [
        ("Precision", "98.59%"),
        ("Recall", "98.59%"),
        ("F1-score", "98.59%"),
        ("ROC-AUC", "99.82%"),
    ]
    for col, (label, value) in zip(metric_cols, validation_metrics):
        with col:
            st.metric(label, value)

    st.caption(
        "Validation F1-score is the primary model-selection metric. "
        "Threshold: 0.50 · Best epoch: 14 · Validation loss: 0.050301."
    )

    st.markdown('<div class="section-title">Experiment Configuration</div>', unsafe_allow_html=True)
    config_left, config_right = st.columns(2)
    with config_left:
        st.markdown("""
        <div class="info-card">
            <div class="info-title">Architecture & Training</div>
            <div class="info-description">
                <b>Architecture:</b> MobileNetV2 (ImageNet pretrained)<br>
                <b>Experiment:</b> S2_MobileNetV2_PREPROCESS_V2<br>
                <b>Optimizer:</b> Adam<br>
                <b>Learning rate:</b> 0.001<br>
                <b>Batch size:</b> 32<br>
                <b>Maximum epochs:</b> 50<br>
                <b>Epoch at best validation F1:</b> 14<br>
                <b>Completed epochs:</b> 24
            </div>
        </div>
        """, unsafe_allow_html=True)
    with config_right:
        st.markdown("""
        <div class="info-card">
            <div class="info-title">Optimization & Preprocessing</div>
            <div class="info-description">
                <b>Dropout:</b> 0.30<br>
                <b>Data augmentation:</b> Enabled (training only)<br>
                <b>Fine-tuning:</b> Enabled<br>
                <b>Fine-tuning layers:</b> block_16 and Conv_1<br>
                <b>Batch normalization:</b> Frozen<br>
                <b>Input size:</b> 224 × 224 × 3<br>
                <b>Preprocessing:</b> MobileNetV2 preprocess_input<br>
                <b>Expected pixel range:</b> [-1, 1]
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Model Structure</div>', unsafe_allow_html=True)
    structure_cols = st.columns(3)
    structure_data = [
        ("Total parameters", "2,259,265"),
        ("Input shape", "224 × 224 × 3"),
        ("Output shape", "1 sigmoid unit"),
    ]
    for col, (label, value) in zip(structure_cols, structure_data):
        with col:
            st.metric(label, value)

    st.markdown('<div class="section-title">Model Selection Protocol</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
        <div class="info-title">S2 V2 Ranking</div>
        <div class="info-description">
            The S2 V2 experiment evaluated 24 configurations. S2_011 ranked first
            using validation_f1_score as the primary selection metric, with validation
            loss as the tie-breaker. The classification threshold was 0.50.
            The experiment manifest records that the test set was not used for tuning.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Evaluation Scope & Research Notes</div>', unsafe_allow_html=True)
    st.info(
        "This page reports the documented validation metrics for S2_011. "
        "Accuracy and a validation confusion matrix are not included here because "
        "the available S2_011 V2 ranking artifact reports precision, recall, F1-score, "
        "ROC-AUC, and validation loss. Test-set metrics must be added only after "
        "the separate final test evaluation artifact has been verified."
    )
    st.warning(
        "PNEUMO-AI is a research prototype for educational and research purposes. "
        "Predictions and Grad-CAM visualizations are not medical diagnoses and "
        "must not replace assessment by qualified healthcare professionals."
    )


elif page == "Dataset Gallery":

    st.markdown(
        '<div class="main-title">Dataset Gallery</div>'
        '<div class="sub-title">Selected examples from the training dataset</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="info-card">
        <div class="info-title">Training Dataset Reference</div>
        <div class="info-description">
            Galeri ini menampilkan contoh citra X-Ray dari subset training
            yang digunakan dalam penelitian PNEUMO-AI. Sampel ditampilkan
            sebagai referensi visual kelas NORMAL dan PNEUMONIA, bukan sebagai
            data evaluasi dan bukan sebagai alat diagnosis.
        </div>
    </div>
    """, unsafe_allow_html=True)

    gallery_root = Path(__file__).resolve().parent / "dataset_gallery"
    manifest_path = gallery_root / "manifest.csv"

    if not manifest_path.is_file():
        st.error("Manifest galeri tidak ditemukan. Periksa folder dataset_gallery.")
    else:
        records = []
        try:
            with manifest_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    label = str(row.get("Class", "")).strip().upper()
                    filename = str(row.get("Filename", "")).strip()
                    if label in {"NORMAL", "PNEUMONIA"} and filename:
                        image_path = gallery_root / label / filename
                        if image_path.is_file():
                            records.append((label, filename, image_path))
        except Exception as exc:
            st.error(f"Manifest galeri gagal dibaca: {exc}")
            records = []

        normal_records = [item for item in records if item[0] == "NORMAL"]
        pneumonia_records = [item for item in records if item[0] == "PNEUMONIA"]

        metric_a, metric_b, metric_c = st.columns(3)
        metric_a.metric("NORMAL SAMPLES", len(normal_records))
        metric_b.metric("PNEUMONIA SAMPLES", len(pneumonia_records))
        metric_c.metric("TOTAL DISPLAYED", len(records))

        def render_gallery_section(section_title, section_description, items):
            st.markdown(f'<div class="section-title">{section_title}</div>', unsafe_allow_html=True)
            st.caption(section_description)
            if not items:
                st.warning("Belum ada citra yang dapat ditampilkan pada kategori ini.")
                return
            columns = st.columns(4)
            for index, (label, filename, image_path) in enumerate(items):
                with columns[index % 4]:
                    try:
                        with Image.open(image_path) as source_image:
                            st.image(
                                source_image.convert("RGB"),
                                caption=filename,
                                use_container_width=True
                            )
                    except Exception as exc:
                        st.warning(f"Citra {filename} tidak dapat dibuka: {exc}")

        render_gallery_section(
            "NORMAL", "Contoh citra pada kategori NORMAL.", normal_records
        )
        render_gallery_section(
            "PNEUMONIA", "Contoh citra pada kategori PNEUMONIA.", pneumonia_records
        )

        st.info(
            "Catatan: gambar pada halaman ini merupakan sampel terpilih dari subset "
            "training. Galeri tidak menunjukkan keseluruhan dataset, distribusi kelas "
            "secara lengkap, ataupun performa model pada data validasi dan pengujian."
        )

elif page == "About & Disclaimer":

    st.markdown(
        '<div class="main-title">About PNEUMO-AI</div>'
        '<div class="sub-title">Research profile, methodology, and responsible-use information</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="hero">
        <div class="hero-label">RESEARCH PROTOTYPE · EXPLAINABLE ARTIFICIAL INTELLIGENCE</div>
        <div class="hero-title">PNEUMO-AI</div>
        <div class="hero-description">
            Intelligent Chest X-Ray Classification with Explainable AI
            <br><br>
            A research application for binary classification of chest X-ray images
            into NORMAL and PNEUMONIA categories, supported by Grad-CAM
            visual explanations.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Research Overview</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
        <div class="info-title">Research Topic</div>
        <div class="info-description">
            <b>Optimasi Transfer Learning untuk Klasifikasi Pneumonia pada Citra
            X-Ray Menggunakan MobileNetV2 dan EfficientNetB0 dengan Explainable AI.</b>
            <br><br>
            Penelitian ini berfokus pada pemanfaatan transfer learning untuk
            klasifikasi citra X-Ray dada ke dalam dua kelas, yaitu NORMAL dan
            PNEUMONIA. Optimasi konfigurasi model dilakukan melalui skenario
            eksperimen, sedangkan Explainable AI digunakan untuk membantu
            menginterpretasikan area citra yang berkontribusi terhadap keluaran model.
        </div>
    </div>
    """, unsafe_allow_html=True)

    overview_left, overview_right = st.columns(2)
    with overview_left:
        st.markdown("""
        <div class="info-card">
            <div class="info-title">Research Objectives</div>
            <div class="info-description">
                • Mengembangkan model klasifikasi citra X-Ray dada berbasis transfer learning.<br>
                • Membandingkan dan mengoptimalkan konfigurasi model yang diteliti.<br>
                • Menggunakan F1-score sebagai metrik utama pemilihan model.<br>
                • Menyediakan visualisasi Grad-CAM untuk mendukung interpretasi prediksi.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with overview_right:
        st.markdown("""
        <div class="info-card">
            <div class="info-title">Classification Scope</div>
            <div class="info-description">
                <b>NORMAL</b><br>
                Citra yang termasuk kategori NORMAL pada dataset penelitian.<br><br>
                <b>PNEUMONIA</b><br>
                Citra yang termasuk kategori PNEUMONIA pada dataset penelitian.<br><br>
                Sistem ini menjalankan klasifikasi biner sesuai ruang lingkup model.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Technology & Method</div>', unsafe_allow_html=True)
    tech_cols = st.columns(3)
    tech_items = [
        ("🧠", "Deep Learning", "TensorFlow / Keras", "Framework pembelajaran mendalam yang digunakan untuk menjalankan model klasifikasi."),
        ("◈", "Selected Model", "MobileNetV2 · S2_011", "Konfigurasi terpilih berdasarkan F1-score validasi tertinggi pada eksperimen S2 V2."),
        ("✳", "Explainability", "Grad-CAM", "Visualisasi area kontribusi relatif untuk membantu interpretasi keluaran model."),
    ]
    for col, (icon, label, value, description) in zip(tech_cols, tech_items):
        with col:
            st.markdown(
                f'<div class="feature-card"><div class="feature-icon">{icon}</div>'
                f'<div class="feature-title">{label}</div>'
                f'<div style="color:#0D9488;font-size:12px;font-weight:800;margin-bottom:7px;">{value}</div>'
                f'<div class="feature-copy">{description}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown('<div class="section-title">How PNEUMO-AI Works</div>', unsafe_allow_html=True)
    workflow_cols = st.columns(4)
    workflow = [
        ("01", "⇧", "Upload", "Pengguna memasukkan citra X-Ray dada berformat JPG, JPEG, atau PNG."),
        ("02", "⌁", "Preprocess", "Citra dikonversi ke RGB, diubah ukurannya menjadi 224 × 224, lalu diproses dengan MobileNetV2 preprocess_input."),
        ("03", "◉", "Classify", "Model menghasilkan probabilitas NORMAL dan PNEUMONIA serta kelas prediksi berdasarkan threshold 0.50."),
        ("04", "✳", "Explain", "Grad-CAM menghasilkan heatmap dan overlay untuk membantu interpretasi kontribusi area citra."),
    ]
    for col, (number, icon, heading, description) in zip(workflow_cols, workflow):
        with col:
            st.markdown(
                f'<div class="step-card"><div class="step-number">PHASE {number}</div>'
                f'<div class="step-icon">{icon}</div><div class="step-title">{heading}</div>'
                f'<div class="step-copy">{description}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown('<div class="section-title">Responsible Use & Medical Disclaimer</div>', unsafe_allow_html=True)
    st.error(
        "PNEUMO-AI merupakan prototipe penelitian dan pendidikan, bukan perangkat "
        "medis atau sistem diagnosis klinis. Hasil klasifikasi, probabilitas, dan "
        "visualisasi Grad-CAM tidak boleh digunakan sebagai dasar tunggal untuk "
        "menentukan diagnosis, pengobatan, atau keputusan medis."
    )
    st.warning(
        "Prediksi model dapat keliru, termasuk menghasilkan false positive atau "
        "false negative. Kinerja pada satu citra tidak mewakili kinerja keseluruhan "
        "model. Interpretasi citra dan keputusan klinis harus dilakukan oleh tenaga "
        "kesehatan yang kompeten dengan mempertimbangkan pemeriksaan dan informasi "
        "klinis yang relevan."
    )
    st.info(
        "Grad-CAM merupakan visualisasi penjelas yang bersifat pendukung. "
        "Heatmap bukan segmentasi kelainan, bukan penanda lokasi pneumonia yang "
        "tervalidasi secara klinis, dan tidak membuktikan hubungan sebab-akibat "
        "antara area citra dengan prediksi model."
    )

    st.markdown('<div class="section-title">Research Information</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
        <div class="info-title">Academic Research Prototype</div>
        <div class="info-description">
            <b>Research field:</b> Computer Science · Data Science<br>
            <b>Application:</b> PNEUMO-AI<br>
            <b>Selected experiment:</b> S2_011 · MobileNetV2<br>
            <b>Model input:</b> 224 × 224 × 3 RGB<br>
            <b>Output classes:</b> NORMAL and PNEUMONIA<br>
            <b>Explainability method:</b> Grad-CAM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        "PNEUMO-AI · Intelligent Chest X-Ray Analysis · Research Prototype"
    )

else:

    st.markdown(
        f'<div class="main-title">{page}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">PNEUMO-AI Research Application</div>',
        unsafe_allow_html=True
    )

    st.info(
        f"Halaman **{page}** sudah terdaftar dalam navigasi. "
        "Fitur halaman ini akan kita bangun pada tahap berikutnya."
    )
