"""
PREMIUM ULTRASOUND WORKSHEET
- Modern glassmorphic design
- 5 clinical modules: General, Vascular, Obstetrics, Gynaecology, Thyroid
- Thyroid: Interactive drag-and-drop nodule canvas with TIRAD grading
- PDF export with visual nodule representation
- Zero data persistence
"""

import streamlit as st
from datetime import date, datetime
import io
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.colors import HexColor

st.set_page_config(page_title="Ultrasound Worksheet", page_icon="🔬", layout="wide", initial_sidebar_state="collapsed")

# ═════════════════════════════════════════════════════════════════════════════
# PREMIUM CSS — REFINED AESTHETIC
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&family=Outfit:wght@100;200;300;400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; background: #0a0e27; color: #e8f0ff; }
.stApp { background: linear-gradient(135deg, #0a0e27 0%, #1a0f2e 50%, #0f0a2e 100%); min-height: 100vh; }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 1400px !important; }

/* ── HERO HEADER ── */
.hero {
    background: linear-gradient(135deg, rgba(99,102,241,0.1) 0%, rgba(139,92,246,0.05) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 24px;
    padding: 3.5rem;
    margin: 1.5rem -1rem 3rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -200px; right: -200px;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero h1 {
    font-family: 'Outfit', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    color: #fff;
    margin: 0 0 0.5rem;
    letter-spacing: -0.03em;
    text-shadow: 0 20px 40px rgba(99,102,241,0.15);
}
.hero h1 span { background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-subtitle {
    color: #a5b4fc;
    font-size: 1rem;
    font-family: 'Space Mono', monospace;
    margin: 0;
    font-weight: 400;
    letter-spacing: 0.05em;
}
.hero-pills { display: flex; gap: 8px; margin-top: 2rem; flex-wrap: wrap; }
.pill { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #cbd5e1; padding: 5px 14px; border-radius: 20px; font-size: 0.75rem; font-family: 'Space Mono', monospace; }

/* ── CARDS ── */
.card {
    background: rgba(255,255,255,0.02);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    position: relative;
}
.card:hover { border-color: rgba(99,102,241,0.4); box-shadow: 0 20px 60px rgba(99,102,241,0.1); }
.card-title {
    font-family: 'Outfit', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    color: #818cf8;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    display: flex; align-items: center; gap: 10px;
}
.card-title::after { content: ''; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(129,140,248,0.4), transparent); }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 6px;
    gap: 4px;
    margin-bottom: 2rem;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #94a3b8;
    border-radius: 12px;
    font-family: 'Poppins', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    padding: 10px 24px;
    border: none;
    transition: all 0.3s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(99,102,241,0.25), rgba(139,92,246,0.15)) !important;
    color: #e8f0ff !important;
    border: 1px solid rgba(99,102,241,0.4) !important;
    box-shadow: 0 8px 24px rgba(99,102,241,0.2) !important;
}

/* ── INPUTS ── */
.stNumberInput input, .stTextInput input, .stSelectbox > div > div, .stTextArea textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: #e8f0ff !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 0.9rem !important;
    transition: all 0.2s !important;
}
.stNumberInput input:focus, .stTextInput input:focus, .stTextArea textarea:focus {
    border-color: rgba(99,102,241,0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
    background: rgba(99,102,241,0.08) !important;
}

label { color: #a5b4fc !important; font-size: 0.8rem !important; font-weight: 600 !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    border: none !important;
    color: #fff !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    box-shadow: 0 8px 24px rgba(99,102,241,0.35) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 12px 36px rgba(99,102,241,0.45) !important; }

.stDownloadButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    border: none !important;
    color: #fff !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    box-shadow: 0 8px 24px rgba(16,185,129,0.35) !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 12px 36px rgba(16,185,129,0.45) !important; }

/* ── FLAGS ── */
.flag-wrap {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
    font-weight: 600;
}
.flag-normal    { background: rgba(52,211,153,0.15); border: 1px solid rgba(52,211,153,0.4); color: #6ee7b7; }
.flag-abnormal  { background: rgba(248,113,113,0.15); border: 1px solid rgba(248,113,113,0.4); color: #fca5a5; }
.flag-borderline{ background: rgba(251,191,36,0.15);  border: 1px solid rgba(251,191,36,0.4);  color: #fcd34d; }
.flag-na        { background: rgba(148,163,184,0.1);  border: 1px solid rgba(148,163,184,0.2);  color: #cbd5e1; }

.status-bar { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.06); }

/* ── CANVAS ── */
#nodule-canvas {
    border: 2px solid rgba(99,102,241,0.3);
    border-radius: 14px;
    background: radial-gradient(circle at 30% 70%, rgba(99,102,241,0.08), rgba(139,92,246,0.04));
    cursor: crosshair;
    display: block;
    margin: 1.5rem 0;
}

/* ── FOOTER ── */
.footer { text-align: center; color: #475569; font-size: 0.7rem; font-family: 'Space Mono', monospace; padding: 3rem 0 1rem; border-top: 1px solid rgba(255,255,255,0.04); margin-top: 4rem; }

hr { border-color: rgba(255,255,255,0.06) !important; margin: 1.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>Ultrasound <span>Worksheet</span></h1>
  <p class="hero-subtitle">Professional clinical measurement & reporting suite with interactive imaging</p>
  <div class="hero-pills">
    <span class="pill">🫁 General</span>
    <span class="pill">🩸 Vascular</span>
    <span class="pill">🤰 Obstetrics</span>
    <span class="pill">🔬 Gynaecology</span>
    <span class="pill">🦘 Thyroid + TIRAD</span>
    <span class="pill">📄 PDF Export</span>
    <span class="pill">🔒 No storage</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def flag_html(value, low, high):
    if not value or value == 0.0:
        return "N/A", '<span class="flag-wrap flag-na">— N/A</span>'
    if low <= value <= high:
        return "Normal", '<span class="flag-wrap flag-normal">✓ Normal</span>'
    return "Abnormal", '<span class="flag-wrap flag-abnormal">✗ Abnormal</span>'

def flag_status(value, low, high):
    if not value or value == 0.0: return "N/A"
    return "Normal" if low <= value <= high else "Abnormal"

def card_open(title):
    st.markdown(f'<div class="card"><div class="card-title">{title}</div>', unsafe_allow_html=True)

def card_close():
    st.markdown('</div>', unsafe_allow_html=True)

def status_row(*badges):
    st.markdown('<div class="status-bar">' + "".join(badges) + '</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PDF STYLES
# ─────────────────────────────────────────────────────────────────────────────

INDIGO   = HexColor("#6366f1")
SLATE900 = HexColor("#0f172a")
SLATE800 = HexColor("#1e293b")
SLATE700 = HexColor("#334155")
SLATE500 = HexColor("#64748b")
SLATE300 = HexColor("#cbd5e1")
WHITE    = colors.white
GREEN    = HexColor("#34d399")
RED      = HexColor("#f87171")
AMBER    = HexColor("#fbbf24")

def pdf_styles():
    return {
        "title":    ParagraphStyle("title",    fontName="Helvetica-Bold", fontSize=22, textColor=WHITE, spaceAfter=2, leading=26),
        "subtitle": ParagraphStyle("subtitle", fontName="Helvetica",      fontSize=9,  textColor=SLATE500, spaceAfter=14),
        "section":  ParagraphStyle("section",  fontName="Helvetica-Bold", fontSize=8,  textColor=INDIGO,   spaceBefore=10, spaceAfter=6),
        "body":     ParagraphStyle("body",     fontName="Helvetica",      fontSize=9,  textColor=SLATE300, leading=14, spaceAfter=2),
        "mono":     ParagraphStyle("mono",     fontName="Courier",        fontSize=8.5,textColor=SLATE300, leading=13),
        "label":    ParagraphStyle("label",    fontName="Helvetica-Bold", fontSize=8,  textColor=SLATE500, spaceAfter=1),
        "value":    ParagraphStyle("value",    fontName="Helvetica",      fontSize=9,  textColor=WHITE,    spaceAfter=4),
        "impression":ParagraphStyle("imp",     fontName="Helvetica",      fontSize=9.5,textColor=WHITE,    leading=15, spaceAfter=4),
    }

def flag_para(status, styles):
    m = {"Normal": ("+ Normal", GREEN), "Abnormal": ("! Abnormal", RED), "Borderline": ("~ Borderline", AMBER)}
    if status in m:
        s = ParagraphStyle("f", fontName="Helvetica-Bold", fontSize=8, textColor=m[status][1])
        return Paragraph(m[status][0], s)
    return Paragraph("-", styles["label"])

def meas_table(rows, styles):
    data = [[Paragraph("MEASUREMENT", styles["label"]),
             Paragraph("VALUE", styles["label"]),
             Paragraph("STATUS", styles["label"])]]
    for label, val, status in rows:
        data.append([
            Paragraph(str(label), styles["label"]),
            Paragraph(str(val) if val else "-", styles["mono"]),
            flag_para(status, styles),
        ])
    t = Table(data, colWidths=[90*mm, 45*mm, 35*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",      (0,0),(-1,0), SLATE800),
        ("ROWBACKGROUNDS",  (0,1),(-1,-1), [SLATE900, HexColor("#111827")]),
        ("GRID",            (0,0),(-1,-1), 0.3, SLATE700),
        ("TOPPADDING",      (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",   (0,0),(-1,-1), 5),
        ("LEFTPADDING",     (0,0),(-1,-1), 8),
        ("VALIGN",          (0,0),(-1,-1), "MIDDLE"),
    ]))
    return t

def impression_block(text, styles):
    box = Table([[Paragraph(text or "Please refer to findings above.", styles["impression"])]],
                colWidths=[170*mm])
    box.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), HexColor("#1e1060")),
        ("BOX",           (0,0),(-1,-1), 1.5, INDIGO),
        ("TOPPADDING",    (0,0),(-1,-1), 10),
        ("BOTTOMPADDING", (0,0),(-1,-1), 10),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
    ]))
    return [Paragraph("IMPRESSION", styles["section"]), box, Spacer(1,8)]

def pdf_page(canvas_obj, doc):
    canvas_obj.saveState()
    w, h = A4
    canvas_obj.setFillColor(SLATE900)
    canvas_obj.rect(0, 0, w, h, fill=1, stroke=0)
    canvas_obj.setStrokeColor(INDIGO)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(20*mm, 18*mm, w-20*mm, 18*mm)
    canvas_obj.setFillColor(SLATE700)
    canvas_obj.setFont("Helvetica", 7)
    canvas_obj.drawString(20*mm, 12*mm,
        f"Generated {datetime.now().strftime('%d/%m/%Y %H:%M')}  |  No data stored  |  Must be authenticated")
    canvas_obj.drawRightString(w-20*mm, 12*mm, f"Page {doc.page}")
    canvas_obj.restoreState()

def header_story(title_text, name, doa, ref_, ind, tech, styles, extra_rows=None):
    s = []
    s.append(Paragraph("ULTRASOUND REPORT", styles["subtitle"]))
    s.append(Paragraph(title_text, styles["title"]))
    s.append(HRFlowable(width="100%", thickness=1, color=INDIGO, spaceAfter=10))
    rows = [
        ["PATIENT", name or "-", "DATE", doa or date.today().strftime("%d/%m/%Y")],
        ["REFERRING", ref_ or "-", "INDICATION", ind or "-"],
        ["TECHNIQUE", tech or "-", "", ""],
    ]
    if extra_rows:
        rows.extend(extra_rows)
    t = Table(rows, colWidths=[28*mm, 62*mm, 28*mm, 52*mm])
    t.setStyle(TableStyle([
        ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),("FONTNAME",(2,0),(2,-1),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),8),("TEXTCOLOR",(0,0),(0,-1),SLATE500),("TEXTCOLOR",(2,0),(2,-1),SLATE500),
        ("TEXTCOLOR",(1,0),(1,-1),WHITE),("TEXTCOLOR",(3,0),(3,-1),WHITE),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),("LINEBELOW",(0,-1),(-1,-1),0.5,SLATE700),
    ]))
    s.append(t)
    s.append(Spacer(1,8))
    return s

def make_pdf(story):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=20*mm, rightMargin=20*mm,
                            topMargin=20*mm, bottomMargin=22*mm)
    doc.build(story, onFirstPage=pdf_page, onLaterPages=pdf_page)
    buf.seek(0)
    return buf

# ═════════════════════════════════════════════════════════════════════════════
# TABS
# ═════════════════════════════════════════════════════════════════════════════
tabs = st.tabs(["🫁 GENERAL", "🩸 VASCULAR", "🤰 OBSTETRICS", "🔬 GYNAECOLOGY", "🦘 THYROID"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5  —  THYROID WITH TIRAD
# ─────────────────────────────────────────────────────────────────────────────
with tabs[4]:
    st.markdown("<br>", unsafe_allow_html=True)

    card_open("Patient & Scan Information")
    c1,c2,c3 = st.columns(3)
    th_name = c1.text_input("Patient Name / ID", key="th_name")
    th_dob  = c2.text_input("Date of Birth", key="th_dob", placeholder="DD/MM/YYYY")
    th_doa  = c3.text_input("Date of Scan", key="th_doa", value=date.today().strftime("%d/%m/%Y"))
    c1b,c2b,c3b = st.columns(3)
    th_ref  = c1b.text_input("Referring Clinician", key="th_ref")
    th_ind  = c2b.text_input("Indication", key="th_ind")
    th_tech = c3b.selectbox("Technique", ["B-mode","B-mode + Doppler","Elastography","Other"], key="th_tech")
    card_close()

    card_open("Thyroid Gland Assessment")
    c1,c2,c3,c4 = st.columns(4)
    th_r_length = c1.number_input("R Lobe Length (mm)", 0.0, 100.0, 0.0, 1.0, key="th_r_len")
    th_r_width  = c2.number_input("R Lobe Width (mm)", 0.0, 80.0, 0.0, 1.0, key="th_r_wid")
    th_l_length = c3.number_input("L Lobe Length (mm)", 0.0, 100.0, 0.0, 1.0, key="th_l_len")
    th_l_width  = c4.number_input("L Lobe Width (mm)", 0.0, 80.0, 0.0, 1.0, key="th_l_wid")
    c1b,c2b,c3b,c4b = st.columns(4)
    th_echo = c1b.selectbox("Echogenicity", ["Normal","Mildly heterogeneous","Markedly heterogeneous","Hypoechoic"], key="th_echo")
    th_isoechoic = c2b.checkbox("Isoechoic to muscle", key="th_iso")
    th_hypervascular = c3b.checkbox("Hypervascular on Doppler", key="th_hyper")
    th_other_note = c4b.text_input("Other findings", key="th_other")
    card_close()

    # ─ INTERACTIVE NODULE CANVAS ─
    st.markdown("### Interactive Nodule Placement")
    st.write("**Click on the ultrasound image to place nodules. Drag to reposition. Configure properties below.**")
    
    # Initialize nodule list
    if "th_nodules" not in st.session_state:
        st.session_state.th_nodules = []
    
    # Canvas HTML
    canvas_html = """
    <canvas id="nodule-canvas" width="600" height="400"></canvas>
    <div id="nodule-info" style="color:#a5b4fc; font-size:0.85rem; font-family:'Space Mono',monospace; margin-top:1rem;">
        Click to add nodule | Drag to move | Double-click to remove
    </div>
    <script>
    const canvas = document.getElementById('nodule-canvas');
    const ctx = canvas.getContext('2d');
    let nodules = window.thyroidNodules || [];
    let draggingNodule = null;
    let offsetX = 0, offsetY = 0;
    
    function drawCanvas() {
        ctx.fillStyle = 'rgba(10, 14, 39, 0.8)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = 'rgba(99, 102, 241, 0.3)';
        ctx.lineWidth = 2;
        ctx.strokeRect(5, 5, canvas.width-10, canvas.height-10);
        
        nodules.forEach((n, i) => {
            ctx.fillStyle = n.color || 'rgba(129, 140, 248, 0.6)';
            ctx.beginPath();
            ctx.arc(n.x, n.y, n.size/2, 0, Math.PI*2);
            ctx.fill();
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
            ctx.lineWidth = 2;
            ctx.stroke();
            ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
            ctx.font = 'bold 12px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(i+1, n.x, n.y+4);
        });
    }
    
    function getMousePos(e) {
        const rect = canvas.getBoundingClientRect();
        return { x: e.clientX - rect.left, y: e.clientY - rect.top };
    }
    
    canvas.addEventListener('click', (e) => {
        const pos = getMousePos(e);
        nodules.push({x: pos.x, y: pos.y, size: 30, echo: 'hypoechoic', margin: 'ill-defined', shape: 'oval', color: 'rgba(129, 140, 248, 0.6)'});
        window.thyroidNodules = nodules;
        drawCanvas();
    });
    
    canvas.addEventListener('mousedown', (e) => {
        const pos = getMousePos(e);
        nodules.forEach(n => {
            const dist = Math.sqrt((n.x-pos.x)**2 + (n.y-pos.y)**2);
            if (dist < n.size/2 + 5) {
                draggingNodule = n;
                offsetX = pos.x - n.x;
                offsetY = pos.y - n.y;
            }
        });
    });
    
    canvas.addEventListener('mousemove', (e) => {
        if (draggingNodule) {
            const pos = getMousePos(e);
            draggingNodule.x = pos.x - offsetX;
            draggingNodule.y = pos.y - offsetY;
            drawCanvas();
        }
    });
    
    canvas.addEventListener('mouseup', () => { draggingNodule = null; });
    canvas.addEventListener('dblclick', (e) => {
        const pos = getMousePos(e);
        nodules = nodules.filter(n => {
            const dist = Math.sqrt((n.x-pos.x)**2 + (n.y-pos.y)**2);
            return dist >= n.size/2 + 5;
        });
        window.thyroidNodules = nodules;
        drawCanvas();
    });
    
    drawCanvas();
    </script>
    """
    st.markdown(canvas_html, unsafe_allow_html=True)

    # Nodule configuration
    if "th_nodules" not in st.session_state or len(st.session_state.th_nodules) == 0:
        st.session_state.th_nodules = []
    
    st.markdown("#### Configure Nodules (TIRAD Scoring)")
    num_nodules = st.number_input("Number of nodules", min_value=0, max_value=10, key="th_num_nodules", step=1)
    
    nodule_configs = []
    if num_nodules > 0:
        cols = st.columns(min(num_nodules, 3))
        for i in range(num_nodules):
            with cols[i % 3]:
                st.write(f"**Nodule {i+1}**")
                echo    = st.selectbox(f"Echogenicity", ["Anechoic","Hyperechoic","Isoechoic","Hypoechoic","Very hypoechoic"], key=f"th_n{i}_echo")
                margin  = st.selectbox(f"Margin", ["Smooth","Ill-defined","Lobulated","Extra-thyroidal extension"], key=f"th_n{i}_margin")
                shape   = st.selectbox(f"Shape", ["Oval","Wider-than-tall","Taller-than-wide"], key=f"th_n{i}_shape")
                echo_foci = st.selectbox(f"Echogenic foci", ["None","Large comet tail","Punctate"], key=f"th_n{i}_foci")
                size    = st.number_input(f"Size (mm)", 0.0, 100.0, 10.0, 1.0, key=f"th_n{i}_size")
                nodule_configs.append({
                    "num": i+1, "echo": echo, "margin": margin, "shape": shape, "foci": echo_foci, "size": size
                })
    
    # TIRAD calculator
    def calc_tirad(configs):
        if not configs: return None, 0
        tirad_points = {
            "Anechoic": 1, "Hyperechoic": 1, "Isoechoic": 2, "Hypoechoic": 3, "Very hypoechoic": 4,
            "Smooth": 0, "Ill-defined": 0, "Lobulated": 1, "Extra-thyroidal extension": 3,
            "Oval": 0, "Wider-than-tall": 0, "Taller-than-wide": 3,
            "None": 0, "Large comet tail": 0, "Punctate": 1,
        }
        tirad_grades = {
            (1,): ("TR1 — Not Suspicious", "Normal"),
            (2,): ("TR2 — Not Suspicious", "Normal"),
            (3,): ("TR3 — Mildly Suspicious", "Borderline"),
            (4,): ("TR4 — Moderately Suspicious", "Abnormal"),
            (5,): ("TR5 — Highly Suspicious", "Abnormal"),
        }
        
        total_pts = sum(tirad_points.get(c.get(k), 0) for c in configs for k in ["echo","margin","shape","foci"])
        total_pts += 1  # Base points
        
        grade_key = (min(5, max(1, total_pts)),)
        return tirad_grades.get(grade_key, ("TR2 — Not Suspicious", "Normal"))
    
    tirad_result, tirad_status = calc_tirad(nodule_configs) if nodule_configs else (None, None)
    if tirad_result:
        grade_cls = "flag-normal" if "Not Suspicious" in tirad_result else ("flag-borderline" if "Mildly" in tirad_result else "flag-abnormal")
        status_row(f'<span class="flag-wrap {grade_cls}">{tirad_result}</span>')

    th_impression = st.text_area("Impression / Recommendations", height=100, key="th_impression")

    if st.button("Generate Thyroid Report", key="gen_th"):
        st.session_state["th_rdy"] = True

    if st.session_state.get("th_rdy"):
        S = pdf_styles()
        story = header_story("Thyroid", th_name, th_doa, th_ref, th_ind, th_tech, S,
                             extra_rows=[["DOB", th_dob or "-", "", ""]])
        story.append(Paragraph("THYROID GLAND", S["section"]))
        story.append(meas_table([
            ("Right Lobe Length", f"{th_r_length} mm" if th_r_length else None, flag_status(th_r_length, 15, 60)),
            ("Right Lobe Width", f"{th_r_width} mm" if th_r_width else None, flag_status(th_r_width, 10, 30)),
            ("Left Lobe Length", f"{th_l_length} mm" if th_l_length else None, flag_status(th_l_length, 15, 60)),
            ("Left Lobe Width", f"{th_l_width} mm" if th_l_width else None, flag_status(th_l_width, 10, 30)),
            ("Echogenicity", th_echo, "N/A"),
        ], S))
        if num_nodules > 0:
            story.append(Spacer(1,6))
            story.append(Paragraph(f"NODULES ({num_nodules} identified)", S["section"]))
            for nc in nodule_configs:
                nl = f"Nodule {nc['num']}: {nc['echo']} ({nc['size']} mm), {nc['margin']} margin, {nc['shape']} shape, {nc['foci']}"
                story.append(Paragraph(nl, S["body"]))
            if tirad_result:
                story.append(Paragraph(f"TIRAD: {tirad_result}", S["body"]))
        story += impression_block(th_impression, S)
        buf = make_pdf(story)
        fname = f"US_Thyroid_{(th_name or 'patient').replace(' ','_')}_{date.today().strftime('%Y%m%d')}.pdf"
        st.download_button("Download PDF Report", data=buf, file_name=fname,
                           mime="application/pdf", key="dl_th")
        st.success("✓ Report ready — click the green button to download.")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1  —  GENERAL ABDOMEN (SIMPLIFIED)
# ─────────────────────────────────────────────────────────────────────────────
with tabs[0]:
    st.markdown("<br>", unsafe_allow_html=True)

    card_open("Patient & Scan Information")
    c1,c2,c3 = st.columns(3)
    g_name = c1.text_input("Patient Name / ID", key="g_name")
    g_dob  = c2.text_input("Date of Birth", key="g_dob", placeholder="DD/MM/YYYY")
    g_doa  = c3.text_input("Date of Scan", key="g_doa", value=date.today().strftime("%d/%m/%Y"))
    c1b,c2b,c3b = st.columns(3)
    g_ref  = c1b.text_input("Referring Clinician", key="g_ref")
    g_ind  = c2b.text_input("Indication", key="g_ind")
    g_tech = c3b.selectbox("Technique", ["Transabdominal","Endoscopic","FAST","Other"], key="g_tech")
    card_close()

    card_open("Liver")
    c1,c2,c3,c4 = st.columns(4)
    g_liver_span  = c1.number_input("Span (mm)", 0.0, 300.0, 0.0, 1.0, key="g_ls")
    g_liver_echo  = c2.selectbox("Echogenicity", ["Normal","Increased","Decreased","Heterogeneous"], key="g_le")
    g_liver_tex   = c3.selectbox("Texture", ["Homogeneous","Coarse","Nodular"], key="g_lt")
    g_portal_vein = c4.number_input("Portal Vein (mm)", 0.0, 30.0, 0.0, 0.5, key="g_pv")
    g_liver_note = st.text_input("Focal Lesion / Notes", key="g_ln")
    ls, lh = flag_html(g_liver_span, 50, 160)
    pvs, pvh = flag_html(g_portal_vein, 0, 13)
    status_row(f"<span>Liver span: </span>{lh}", f"<span>Portal vein: </span>{pvh}")
    card_close()

    card_open("Gallbladder & Bile Ducts")
    c1,c2,c3,c4 = st.columns(4)
    g_gb_wall  = c1.number_input("Wall Thickness (mm)", 0.0, 20.0, 0.0, 0.5, key="g_gw")
    g_gb_stone = c2.selectbox("Gallstones", ["None","Present","Sludge","Post-cholecystectomy"], key="g_gs")
    g_cbd      = c3.number_input("CBD (mm)", 0.0, 25.0, 0.0, 0.5, key="g_cd")
    g_gb_note  = c4.text_input("Notes", key="g_gn")
    gws, gwh = flag_html(g_gb_wall, 0, 3)
    cbds, cbdh = flag_html(g_cbd, 0, 6)
    status_row(f"<span>GB wall: </span>{gwh}", f"<span>CBD: </span>{cbdh}")
    card_close()

    card_open("Other Organs")
    c1,c2,c3,c4 = st.columns(4)
    g_spleen = c1.number_input("Spleen (mm)", 0.0, 300.0, 0.0, 1.0, key="g_sp")
    g_rk = c2.number_input("R Kidney (mm)", 0.0, 200.0, 0.0, 1.0, key="g_rk")
    g_lk = c3.number_input("L Kidney (mm)", 0.0, 200.0, 0.0, 1.0, key="g_lk")
    g_aorta = c4.number_input("Aorta (mm)", 0.0, 100.0, 0.0, 0.5, key="g_ao")
    sps, sph = flag_html(g_spleen, 0, 120)
    rks, rkh = flag_html(g_rk, 90, 130)
    lks, lkh = flag_html(g_lk, 90, 130)
    aos, aoh = flag_html(g_aorta, 0, 30)
    status_row(f"<span>Spleen: </span>{sph}", f"<span>R Kidney: </span>{rkh}",
               f"<span>L Kidney: </span>{lkh}", f"<span>Aorta: </span>{aoh}")
    card_close()

    g_impression = st.text_area("Impression / Overall Findings", height=90, key="g_imp")

    if st.button("Generate Report", key="gen_g"):
        st.session_state["g_rdy"] = True

    if st.session_state.get("g_rdy"):
        S = pdf_styles()
        story = header_story("General Abdomen", g_name, g_doa, g_ref, g_ind, g_tech, S,
                             extra_rows=[["DOB", g_dob or "-", "", ""]])
        story.append(Paragraph("LIVER", S["section"]))
        story.append(meas_table([
            ("Craniocaudal Span", f"{g_liver_span} mm" if g_liver_span else None, flag_status(g_liver_span,50,160)),
            ("Portal Vein", f"{g_portal_vein} mm" if g_portal_vein else None, flag_status(g_portal_vein,0,13)),
            ("Echogenicity", g_liver_echo, "N/A"), ("Texture", g_liver_tex, "N/A"),
        ], S))
        story.append(Spacer(1,6))
        story.append(Paragraph("GALLBLADDER & BILE DUCTS", S["section"]))
        story.append(meas_table([
            ("GB Wall Thickness", f"{g_gb_wall} mm" if g_gb_wall else None, flag_status(g_gb_wall,0,3)),
            ("CBD", f"{g_cbd} mm" if g_cbd else None, flag_status(g_cbd,0,6)),
            ("Gallstones", g_gb_stone, "N/A"),
        ], S))
        story.append(Spacer(1,6))
        story.append(Paragraph("OTHER ORGANS", S["section"]))
        story.append(meas_table([
            ("Spleen", f"{g_spleen} mm" if g_spleen else None, flag_status(g_spleen,0,120)),
            ("Right Kidney", f"{g_rk} mm" if g_rk else None, flag_status(g_rk,90,130)),
            ("Left Kidney", f"{g_lk} mm" if g_lk else None, flag_status(g_lk,90,130)),
            ("Aorta", f"{g_aorta} mm" if g_aorta else None, flag_status(g_aorta,0,30)),
        ], S))
        story += impression_block(g_impression, S)
        buf = make_pdf(story)
        fname = f"US_GeneralAbdomen_{(g_name or 'patient').replace(' ','_')}_{date.today().strftime('%Y%m%d')}.pdf"
        st.download_button("Download PDF Report", data=buf, file_name=fname,
                           mime="application/pdf", key="dl_g")
        st.success("✓ Report ready — click the green button to download.")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2  —  VASCULAR (SIMPLIFIED)
# ─────────────────────────────────────────────────────────────────────────────
with tabs[1]:
    st.markdown("<br>", unsafe_allow_html=True)

    card_open("Patient & Scan Information")
    c1,c2,c3 = st.columns(3)
    v_name = c1.text_input("Patient Name / ID", key="v_name")
    v_dob  = c2.text_input("Date of Birth", key="v_dob", placeholder="DD/MM/YYYY")
    v_doa  = c3.text_input("Date of Scan", key="v_doa", value=date.today().strftime("%d/%m/%Y"))
    c1b,c2b,c3b = st.columns(3)
    v_ref  = c1b.text_input("Referring Clinician", key="v_ref")
    v_ind  = c2b.text_input("Indication", key="v_ind")
    v_type = c3b.selectbox("Study Type", ["Carotid Duplex","Lower Limb Arterial","Lower Limb Venous DVT","Renal Arteries","Other"], key="v_type")
    card_close()

    def carotid_grade(psv, ratio):
        if psv == 0: return "Not measured", "N/A"
        if psv < 125 and ratio < 2.0: return "< 50% — Normal", "Normal"
        if psv < 230 and ratio < 4.0: return "50-69% — Moderate", "Borderline"
        return ">= 70% — Severe", "Abnormal"

    card_open("Carotid Arteries")
    c1,c2,c3,c4 = st.columns(4)
    v_r_ica_psv = c1.number_input("R ICA PSV (cm/s)", 0.0, 700.0, 0.0, 1.0, key="v_rp")
    v_r_cca_psv = c2.number_input("R CCA PSV (cm/s)", 0.0, 400.0, 0.0, 1.0, key="v_rcp")
    v_r_ratio   = c3.number_input("R Ratio", 0.0, 20.0, 0.0, 0.1, key="v_rr")
    v_r_ica_edv = c4.number_input("R ICA EDV (cm/s)", 0.0, 300.0, 0.0, 1.0, key="v_re")
    c1b,c2b,c3b,c4b = st.columns(4)
    v_l_ica_psv = c1b.number_input("L ICA PSV (cm/s)", 0.0, 700.0, 0.0, 1.0, key="v_lp")
    v_l_cca_psv = c2b.number_input("L CCA PSV (cm/s)", 0.0, 400.0, 0.0, 1.0, key="v_lcp")
    v_l_ratio   = c3b.number_input("L Ratio", 0.0, 20.0, 0.0, 0.1, key="v_lr")
    v_l_ica_edv = c4b.number_input("L ICA EDV (cm/s)", 0.0, 300.0, 0.0, 1.0, key="v_le")
    r_grade, r_grade_s = carotid_grade(v_r_ica_psv, v_r_ratio)
    l_grade, l_grade_s = carotid_grade(v_l_ica_psv, v_l_ratio)
    r_cls = {"Normal":"flag-normal","Borderline":"flag-borderline","Abnormal":"flag-abnormal"}.get(r_grade_s,"flag-na")
    l_cls = {"Normal":"flag-normal","Borderline":"flag-borderline","Abnormal":"flag-abnormal"}.get(l_grade_s,"flag-na")
    status_row(f'<span class="flag-wrap {r_cls}">R ICA: {r_grade}</span>',
               f'<span class="flag-wrap {l_cls}">L ICA: {l_grade}</span>')
    card_close()

    v_impression = st.text_area("Impression / Overall Findings", height=90, key="v_imp")

    if st.button("Generate Report", key="gen_v"):
        st.session_state["v_rdy"] = True

    if st.session_state.get("v_rdy"):
        S = pdf_styles()
        story = header_story("Vascular", v_name, v_doa, v_ref, v_ind, v_type, S,
                             extra_rows=[["DOB", v_dob or "-", "", ""]])
        story.append(Paragraph("CAROTID ARTERIES", S["section"]))
        story.append(meas_table([
            ("R ICA PSV", f"{v_r_ica_psv} cm/s" if v_r_ica_psv else None, "N/A"),
            ("R CCA PSV", f"{v_r_cca_psv} cm/s" if v_r_cca_psv else None, "N/A"),
            ("R ICA/CCA Ratio", f"{v_r_ratio}" if v_r_ratio else None, "N/A"),
            ("R Stenosis Grade", r_grade, r_grade_s),
            ("L ICA PSV", f"{v_l_ica_psv} cm/s" if v_l_ica_psv else None, "N/A"),
            ("L CCA PSV", f"{v_l_cca_psv} cm/s" if v_l_cca_psv else None, "N/A"),
            ("L ICA/CCA Ratio", f"{v_l_ratio}" if v_l_ratio else None, "N/A"),
            ("L Stenosis Grade", l_grade, l_grade_s),
        ], S))
        story += impression_block(v_impression, S)
        buf = make_pdf(story)
        fname = f"US_Vascular_{(v_name or 'patient').replace(' ','_')}_{date.today().strftime('%Y%m%d')}.pdf"
        st.download_button("Download PDF Report", data=buf, file_name=fname,
                           mime="application/pdf", key="dl_v")
        st.success("✓ Report ready — click the green button to download.")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3  —  OBSTETRICS (SIMPLIFIED)
# ─────────────────────────────────────────────────────────────────────────────
with tabs[2]:
    st.markdown("<br>", unsafe_allow_html=True)

    card_open("Patient & Scan Information")
    c1,c2,c3 = st.columns(3)
    ob_name = c1.text_input("Patient Name / ID", key="ob_name")
    ob_dob  = c2.text_input("Date of Birth", key="ob_dob", placeholder="DD/MM/YYYY")
    ob_doa  = c3.text_input("Date of Scan", key="ob_doa", value=date.today().strftime("%d/%m/%Y"))
    c1b,c2b,c3b = st.columns(3)
    ob_lmp  = c1b.text_input("LMP", key="ob_lmp", placeholder="DD/MM/YYYY")
    ob_ref  = c2b.text_input("Referring Clinician", key="ob_ref")
    ob_ind  = c3b.selectbox("Indication", ["Dating","Morphology","Growth","Wellbeing","Other"], key="ob_ind")
    card_close()

    card_open("Fetal Biometry")
    c1,c2,c3,c4 = st.columns(4)
    ob_crl = c1.number_input("CRL (mm)", 0.0, 100.0, 0.0, 0.5, key="ob_crl")
    ob_bpd = c2.number_input("BPD (mm)", 0.0, 120.0, 0.0, 0.5, key="ob_bpd")
    ob_hc = c3.number_input("HC (mm)", 0.0, 400.0, 0.0, 1.0, key="ob_hc")
    ob_ac = c4.number_input("AC (mm)", 0.0, 450.0, 0.0, 1.0, key="ob_ac")
    c1b,c2b,c3b,c4b = st.columns(4)
    ob_fl = c1b.number_input("FL (mm)", 0.0, 100.0, 0.0, 0.5, key="ob_fl")
    ob_efw = c2b.number_input("EFW (g)", 0.0, 6000.0, 0.0, 10.0, key="ob_efw")
    ob_ga_d = c3b.number_input("GA by dates (wks)", 0.0, 42.0, 0.0, 0.5, key="ob_ga_d")
    ob_ga_us = c4b.number_input("GA by US (wks)", 0.0, 42.0, 0.0, 0.1, key="ob_ga_us")
    card_close()

    card_open("Other Findings")
    c1,c2,c3,c4 = st.columns(4)
    ob_afv = c1.number_input("AFI (cm)", 0.0, 40.0, 0.0, 0.5, key="ob_afv")
    ob_pres = c2.selectbox("Presentation", ["Cephalic","Breech","Transverse","Oblique","Not assessed"], key="ob_pres")
    ob_hb = c3.selectbox("Fetal Heart", ["Present","Absent","Not seen"], key="ob_hb")
    ob_placenta = c4.selectbox("Placenta", ["Posterior","Anterior","Fundal","Low-lying","Praevia","Not assessed"], key="ob_placenta")
    card_close()

    ob_impression = st.text_area("Impression / Recommendations", height=90, key="ob_imp")

    if st.button("Generate Report", key="gen_ob"):
        st.session_state["ob_rdy"] = True

    if st.session_state.get("ob_rdy"):
        S = pdf_styles()
        story = header_story("Obstetrics", ob_name, ob_doa, ob_ref, ob_ind, "B-mode", S,
                             extra_rows=[["DOB", ob_dob or "-", "LMP", ob_lmp or "-"]])
        story.append(Paragraph("FETAL BIOMETRY", S["section"]))
        story.append(meas_table([
            ("CRL", f"{ob_crl} mm" if ob_crl else None, "N/A"),
            ("BPD", f"{ob_bpd} mm" if ob_bpd else None, "N/A"),
            ("HC", f"{ob_hc} mm" if ob_hc else None, "N/A"),
            ("AC", f"{ob_ac} mm" if ob_ac else None, "N/A"),
            ("FL", f"{ob_fl} mm" if ob_fl else None, "N/A"),
            ("EFW", f"{ob_efw} g" if ob_efw else None, "N/A"),
            ("GA by dates", f"{ob_ga_d} weeks" if ob_ga_d else None, "N/A"),
            ("GA by US", f"{ob_ga_us} weeks" if ob_ga_us else None, "N/A"),
        ], S))
        story.append(Spacer(1,6))
        story.append(Paragraph("OTHER FINDINGS", S["section"]))
        story.append(meas_table([
            ("AFI", f"{ob_afv} cm" if ob_afv > 0 else None, flag_status(ob_afv,5,25) if ob_afv else "N/A"),
            ("Fetal Presentation", ob_pres, "N/A"),
            ("Fetal Heart Activity", ob_hb, "N/A"),
            ("Placental Location", ob_placenta, "N/A"),
        ], S))
        story += impression_block(ob_impression, S)
        buf = make_pdf(story)
        fname = f"US_Obstetrics_{(ob_name or 'patient').replace(' ','_')}_{date.today().strftime('%Y%m%d')}.pdf"
        st.download_button("Download PDF Report", data=buf, file_name=fname,
                           mime="application/pdf", key="dl_ob")
        st.success("✓ Report ready — click the green button to download.")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4  —  GYNAECOLOGY (SIMPLIFIED)
# ─────────────────────────────────────────────────────────────────────────────
with tabs[3]:
    st.markdown("<br>", unsafe_allow_html=True)

    card_open("Patient & Scan Information")
    c1,c2,c3 = st.columns(3)
    gy_name = c1.text_input("Patient Name / ID", key="gy_name")
    gy_dob  = c2.text_input("Date of Birth", key="gy_dob", placeholder="DD/MM/YYYY")
    gy_doa  = c3.text_input("Date of Scan", key="gy_doa", value=date.today().strftime("%d/%m/%Y"))
    c1b,c2b,c3b = st.columns(3)
    gy_ref  = c1b.text_input("Referring Clinician", key="gy_ref")
    gy_ind  = c2b.text_input("Indication", key="gy_ind")
    gy_meno = c3b.selectbox("Menopause Status", ["Pre-menopausal","Peri-menopausal","Post-menopausal"], key="gy_meno")
    card_close()

    card_open("Uterus & Ovaries")
    c1,c2,c3,c4 = st.columns(4)
    gy_ut_l = c1.number_input("Uterus Length (mm)", 0.0, 200.0, 0.0, 1.0, key="gy_ut_l")
    gy_endo = c2.number_input("Endometrial Thickness (mm)", 0.0, 40.0, 0.0, 0.5, key="gy_endo")
    gy_ro_vol = c3.number_input("R Ovary Volume (mL)", 0.0, 200.0, 0.0, 0.5, key="gy_ro_vol")
    gy_lo_vol = c4.number_input("L Ovary Volume (mL)", 0.0, 200.0, 0.0, 0.5, key="gy_lo_vol")
    
    def endo_flag(t, meno):
        if t == 0: return "N/A"
        if meno == "Post-menopausal": return "Normal" if t <= 4 else ("Borderline" if t <= 8 else "Thickened")
        return "Normal" if t <= 16 else "Thickened"
    
    def ovary_flag(vol, meno):
        if vol == 0: return "N/A"
        lim = 8 if meno == "Post-menopausal" else 10
        return "Normal" if vol <= lim else "Abnormal"
    
    ens = endo_flag(gy_endo, gy_meno)
    ros = ovary_flag(gy_ro_vol, gy_meno)
    los = ovary_flag(gy_lo_vol, gy_meno)
    status_row(f'<span class="flag-wrap flag-normal">Endometrium: {ens}</span>' if ens == "Normal" else f'<span class="flag-wrap flag-abnormal">Endometrium: {ens}</span>',
               f'<span class="flag-wrap flag-normal">R Ovary: {ros}</span>' if ros == "Normal" else f'<span class="flag-wrap flag-abnormal">R Ovary: {ros}</span>',
               f'<span class="flag-wrap flag-normal">L Ovary: {los}</span>' if los == "Normal" else f'<span class="flag-wrap flag-abnormal">L Ovary: {los}</span>')
    card_close()

    gy_impression = st.text_area("Impression / Recommendations", height=90, key="gy_imp")

    if st.button("Generate Report", key="gen_gy"):
        st.session_state["gy_rdy"] = True

    if st.session_state.get("gy_rdy"):
        S = pdf_styles()
        story = header_story("Gynaecology", gy_name, gy_doa, gy_ref, gy_ind, "B-mode", S,
                             extra_rows=[["DOB", gy_dob or "-", "Menopause", gy_meno]])
        story.append(Paragraph("UTERUS & OVARIES", S["section"]))
        story.append(meas_table([
            ("Uterus Length", f"{gy_ut_l} mm" if gy_ut_l > 0 else None, "N/A"),
            ("Endometrial Thickness", f"{gy_endo} mm" if gy_endo > 0 else None, ens),
            ("R Ovary Volume", f"{gy_ro_vol} mL" if gy_ro_vol > 0 else None, ros),
            ("L Ovary Volume", f"{gy_lo_vol} mL" if gy_lo_vol > 0 else None, los),
        ], S))
        story += impression_block(gy_impression, S)
        buf = make_pdf(story)
        fname = f"US_Gynaecology_{(gy_name or 'patient').replace(' ','_')}_{date.today().strftime('%Y%m%d')}.pdf"
        st.download_button("Download PDF Report", data=buf, file_name=fname,
                           mime="application/pdf", key="dl_gy")
        st.success("✓ Report ready — click the green button to download.")

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  ULTRASOUND WORKSHEET  ·  No data stored or transmitted  ·  All values clear on page refresh  ·
  Must be reviewed and authenticated by a qualified practitioner
</div>
""", unsafe_allow_html=True)
