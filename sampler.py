"""Visual sampler: font styles & toggle designs for the Settings tab theme switch."""
import streamlit as st
import base64, os

LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "logos", "fist_white_fill.png")
with open(LOGO_PATH, "rb") as _lf:
    LOGO_B64 = base64.b64encode(_lf.read()).decode()
LOGO_SRC = f"data:image/png;base64,{LOGO_B64}"

st.set_page_config(page_title="Adrenaline – Sampler", page_icon=LOGO_PATH, layout="wide")

AC = "#d32f2f"
BG = "#0d0d0d"
CARD = "#111"
BORDER = "#1a1a1a"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Russo+One&family=Nunito+Sans:wght@300;400;600;700;800&family=Inter:wght@400;500;600;700&family=Bebas+Neue&family=Rajdhani:wght@400;500;600;700&family=Orbitron:wght@400;500;600;700;800&family=Barlow+Condensed:wght@400;500;600;700&family=Teko:wght@400;500;600;700&family=Oswald:wght@400;500;600;700&family=Exo+2:wght@400;500;600;700&display=swap');

#MainMenu, footer, header {{ visibility: hidden; }}

.stApp {{
    background: {BG};
    color: #e0e0e0;
    font-family: 'Nunito Sans', sans-serif;
}}

.sampler-section {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 2rem;
    margin: 1rem 0;
}}
.sampler-section h2 {{
    font-family: 'Russo One', sans-serif;
    color: {AC};
    font-size: 1.2rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid {BORDER};
    padding-bottom: 0.8rem;
}}

.font-row {{
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding: 1rem 0;
    border-bottom: 1px solid {BORDER};
}}
.font-row:last-child {{ border-bottom: none; }}
.font-num {{
    font-family: 'Russo One', sans-serif;
    color: {AC};
    font-size: 1.5rem;
    width: 40px;
    text-align: center;
    flex-shrink: 0;
}}
.font-preview {{
    flex: 1;
}}
.font-meta {{
    font-family: 'Nunito Sans', sans-serif;
    color: #555;
    font-size: 0.65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}}

/* ── Toggle Designs ───────────────────────────── */

.toggle-row {{
    display: flex;
    align-items: center;
    gap: 2rem;
    padding: 1.2rem 0;
    border-bottom: 1px solid {BORDER};
}}
.toggle-row:last-child {{ border-bottom: none; }}
.toggle-num {{
    font-family: 'Russo One', sans-serif;
    color: {AC};
    font-size: 1.5rem;
    width: 40px;
    text-align: center;
    flex-shrink: 0;
}}
.toggle-demo {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}
.toggle-desc {{
    font-family: 'Nunito Sans', sans-serif;
    color: #777;
    font-size: 0.75rem;
    letter-spacing: 1px;
    max-width: 260px;
}}

/* --- Toggle A: Pill slider (classic iOS) --- */
.toggle-a {{
    position: relative;
    width: 52px; height: 28px;
    background: #333;
    border-radius: 14px;
    cursor: pointer;
    transition: background 0.3s;
    flex-shrink: 0;
}}
.toggle-a.on {{ background: {AC}; }}
.toggle-a .knob {{
    position: absolute;
    top: 3px; left: 3px;
    width: 22px; height: 22px;
    background: #fff;
    border-radius: 50%;
    transition: left 0.3s;
}}
.toggle-a.on .knob {{ left: 27px; }}

/* --- Toggle B: Segmented pill --- */
.toggle-b {{
    display: flex;
    background: #1a1a1a;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #333;
    flex-shrink: 0;
}}
.toggle-b .seg {{
    padding: 0.45rem 1rem;
    font-family: 'Nunito Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #555;
    transition: all 0.2s;
    cursor: pointer;
}}
.toggle-b .seg.active {{
    background: {AC};
    color: #fff;
}}

/* --- Toggle C: Icon pill (sun/moon) --- */
.toggle-c {{
    position: relative;
    width: 56px; height: 28px;
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 14px;
    cursor: pointer;
    transition: all 0.3s;
    flex-shrink: 0;
}}
.toggle-c.on {{
    background: #1a1a1a;
    border-color: {AC};
}}
.toggle-c .icon-knob {{
    position: absolute;
    top: 2px; left: 2px;
    width: 22px; height: 22px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    transition: left 0.3s;
    background: #222;
}}
.toggle-c.on .icon-knob {{
    left: 30px;
    background: {AC};
}}

/* --- Toggle D: Outlined ghost button pair --- */
.toggle-d {{
    display: flex;
    gap: 0;
    flex-shrink: 0;
}}
.toggle-d .btn {{
    padding: 0.4rem 1rem;
    font-family: 'Nunito Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    border: 1px solid #333;
    color: #555;
    cursor: pointer;
    transition: all 0.2s;
    background: transparent;
}}
.toggle-d .btn:first-child {{ border-radius: 8px 0 0 8px; border-right: none; }}
.toggle-d .btn:last-child {{ border-radius: 0 8px 8px 0; }}
.toggle-d .btn.active {{
    border-color: {AC};
    color: {AC};
    background: rgba(211,47,47,0.08);
}}

/* --- Toggle E: Minimal underline tabs --- */
.toggle-e {{
    display: flex;
    gap: 1.5rem;
    flex-shrink: 0;
}}
.toggle-e .tab {{
    font-family: 'Nunito Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #555;
    padding-bottom: 0.4rem;
    cursor: pointer;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
}}
.toggle-e .tab.active {{
    color: {AC};
    border-bottom-color: {AC};
}}

/* --- Toggle F: Glow pill slider --- */
.toggle-f {{
    position: relative;
    width: 52px; height: 28px;
    background: #222;
    border-radius: 14px;
    cursor: pointer;
    transition: all 0.3s;
    flex-shrink: 0;
    border: 1px solid #333;
}}
.toggle-f.on {{
    background: rgba(211,47,47,0.15);
    border-color: {AC};
    box-shadow: 0 0 12px rgba(211,47,47,0.3), 0 0 4px rgba(211,47,47,0.2);
}}
.toggle-f .knob {{
    position: absolute;
    top: 3px; left: 3px;
    width: 20px; height: 20px;
    background: #666;
    border-radius: 50%;
    transition: all 0.3s;
}}
.toggle-f.on .knob {{
    left: 27px;
    background: {AC};
    box-shadow: 0 0 6px rgba(211,47,47,0.5);
}}

/* --- Toggle G: Rounded chip select --- */
.toggle-g {{
    display: flex;
    gap: 0.5rem;
    flex-shrink: 0;
}}
.toggle-g .chip {{
    padding: 0.35rem 1rem;
    font-family: 'Nunito Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    border-radius: 20px;
    border: 1px solid #333;
    color: #555;
    cursor: pointer;
    transition: all 0.2s;
    background: transparent;
}}
.toggle-g .chip.active {{
    border-color: {AC};
    color: #fff;
    background: {AC};
}}

/* --- Toggle H: Slim bar with dot --- */
.toggle-h {{
    position: relative;
    width: 44px; height: 6px;
    background: #333;
    border-radius: 3px;
    cursor: pointer;
    flex-shrink: 0;
    margin: 11px 0;
}}
.toggle-h .dot {{
    position: absolute;
    top: -9px;
    left: -3px;
    width: 24px; height: 24px;
    border-radius: 50%;
    background: #444;
    border: 2px solid #555;
    transition: all 0.3s;
}}
.toggle-h.on .dot {{
    left: 23px;
    background: {AC};
    border-color: {AC};
    box-shadow: 0 0 8px rgba(211,47,47,0.4);
}}
.toggle-h.on {{
    background: rgba(211,47,47,0.3);
}}

</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown(f"""
<div style="display:flex;align-items:center;gap:0.8rem;padding:1rem 0 0.5rem 0;border-bottom:1px solid {BORDER};margin-bottom:1.5rem;">
    <img src="{LOGO_SRC}" style="width:36px;height:36px;object-fit:contain;filter:drop-shadow(0 0 4px rgba(211,47,47,0.5));">
    <div style="font-family:'Russo One',sans-serif;color:{AC};font-size:1.2rem;letter-spacing:2px;">ADRENALINE — VISUAL SAMPLER</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# SECTION 1: FONT SAMPLES
# ══════════════════════════════════════════════════════════════════════

fonts = [
    ("Russo One",         "'Russo One', sans-serif",          "700", "1px"),
    ("Nunito Sans",       "'Nunito Sans', sans-serif",        "800", "1.5px"),
    ("Bebas Neue",        "'Bebas Neue', sans-serif",         "400", "2px"),
    ("Orbitron",          "'Orbitron', sans-serif",            "700", "2px"),
    ("Rajdhani",          "'Rajdhani', sans-serif",            "700", "1px"),
    ("Barlow Condensed",  "'Barlow Condensed', sans-serif",   "700", "2px"),
    ("Teko",              "'Teko', sans-serif",                "600", "2px"),
    ("Oswald",            "'Oswald', sans-serif",              "600", "1.5px"),
    ("Exo 2",             "'Exo 2', sans-serif",              "700", "1px"),
    ("Inter",             "'Inter', sans-serif",               "700", "1.5px"),
]

font_rows = ""
for i, (name, family, weight, spacing) in enumerate(fonts, 1):
    font_rows += f"""
    <div class="font-row">
        <div class="font-num">{i}</div>
        <div class="font-preview">
            <div class="font-meta">{name} · weight {weight} · spacing {spacing}</div>
            <div style="font-family:{family};font-weight:{weight};letter-spacing:{spacing};font-size:1rem;color:#e0e0e0;text-transform:uppercase;">Dark Mode</div>
            <div style="font-family:{family};font-weight:{weight};letter-spacing:{spacing};font-size:0.85rem;color:#999;text-transform:uppercase;margin-top:0.2rem;">Appearance</div>
        </div>
        <div style="font-family:{family};font-weight:{weight};letter-spacing:{spacing};font-size:0.7rem;color:#555;text-transform:uppercase;">settings label style</div>
    </div>"""

st.markdown(f"""
<div class="sampler-section">
    <h2>1 — Font Styles for "Dark Mode" Label</h2>
    {font_rows}
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# SECTION 2: TOGGLE / SWITCH DESIGNS
# ══════════════════════════════════════════════════════════════════════

toggles_html = f"""
<div class="sampler-section">
    <h2>2 — Toggle / Switch Designs</h2>

    <!-- A: Classic pill slider -->
    <div class="toggle-row">
        <div class="toggle-num">A</div>
        <div class="toggle-demo">
            <div class="toggle-a"><div class="knob"></div></div>
            <div style="width:20px;"></div>
            <div class="toggle-a on"><div class="knob"></div></div>
        </div>
        <div class="toggle-desc">Classic pill slider — minimal, familiar. Off = grey, On = red.</div>
    </div>

    <!-- B: Segmented pill -->
    <div class="toggle-row">
        <div class="toggle-num">B</div>
        <div class="toggle-demo">
            <div class="toggle-b">
                <div class="seg active">Dark</div>
                <div class="seg">Light</div>
            </div>
            <div style="width:20px;"></div>
            <div class="toggle-b">
                <div class="seg">Dark</div>
                <div class="seg active">Light</div>
            </div>
        </div>
        <div class="toggle-desc">Segmented pill — explicit labels, clear state.</div>
    </div>

    <!-- C: Icon pill (sun/moon) -->
    <div class="toggle-row">
        <div class="toggle-num">C</div>
        <div class="toggle-demo">
            <div class="toggle-c"><div class="icon-knob">🌙</div></div>
            <div style="width:20px;"></div>
            <div class="toggle-c on"><div class="icon-knob">☀️</div></div>
        </div>
        <div class="toggle-desc">Icon slider — moon/sun icons show mode at a glance.</div>
    </div>

    <!-- D: Ghost button pair -->
    <div class="toggle-row">
        <div class="toggle-num">D</div>
        <div class="toggle-demo">
            <div class="toggle-d">
                <div class="btn active">Dark</div>
                <div class="btn">Light</div>
            </div>
            <div style="width:20px;"></div>
            <div class="toggle-d">
                <div class="btn">Dark</div>
                <div class="btn active">Light</div>
            </div>
        </div>
        <div class="toggle-desc">Ghost button pair — matches your existing ghost button style.</div>
    </div>

    <!-- E: Minimal underline tabs -->
    <div class="toggle-row">
        <div class="toggle-num">E</div>
        <div class="toggle-demo">
            <div class="toggle-e">
                <div class="tab active">Dark</div>
                <div class="tab">Light</div>
            </div>
            <div style="width:30px;"></div>
            <div class="toggle-e">
                <div class="tab">Dark</div>
                <div class="tab active">Light</div>
            </div>
        </div>
        <div class="toggle-desc">Underline tabs — matches your nav tab style for consistency.</div>
    </div>

    <!-- F: Glow pill slider -->
    <div class="toggle-row">
        <div class="toggle-num">F</div>
        <div class="toggle-demo">
            <div class="toggle-f"><div class="knob"></div></div>
            <div style="width:20px;"></div>
            <div class="toggle-f on"><div class="knob"></div></div>
        </div>
        <div class="toggle-desc">Glow slider — red glow effect on active state, matches Adrenaline branding.</div>
    </div>

    <!-- G: Rounded chip select -->
    <div class="toggle-row">
        <div class="toggle-num">G</div>
        <div class="toggle-demo">
            <div class="toggle-g">
                <div class="chip active">Dark</div>
                <div class="chip">Light</div>
            </div>
            <div style="width:20px;"></div>
            <div class="toggle-g">
                <div class="chip">Dark</div>
                <div class="chip active">Light</div>
            </div>
        </div>
        <div class="toggle-desc">Rounded chips — pill-shaped buttons, clean and modern.</div>
    </div>

    <!-- H: Slim bar with dot -->
    <div class="toggle-row">
        <div class="toggle-num">H</div>
        <div class="toggle-demo">
            <div class="toggle-h"><div class="dot"></div></div>
            <div style="width:30px;"></div>
            <div class="toggle-h on"><div class="dot"></div></div>
        </div>
        <div class="toggle-desc">Slim bar — material-style rail with floating dot, glow on active.</div>
    </div>
</div>
"""

st.markdown(toggles_html, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# SECTION 3: COMBINED PREVIEWS
# ══════════════════════════════════════════════════════════════════════

combos = [
    ("Russo One + Glow Slider (F)",    "'Russo One', sans-serif",        "700", "1px",   "toggle-f on"),
    ("Bebas Neue + Segmented Pill (B)", "'Bebas Neue', sans-serif",      "400", "2px",   "toggle-b"),
    ("Orbitron + Ghost Buttons (D)",   "'Orbitron', sans-serif",          "700", "2px",   "toggle-d"),
    ("Barlow Cond + Chips (G)",        "'Barlow Condensed', sans-serif", "700", "2px",   "toggle-g"),
    ("Rajdhani + Icon Slider (C)",     "'Rajdhani', sans-serif",          "700", "1px",   "toggle-c on"),
    ("Nunito Sans + Underline (E)",    "'Nunito Sans', sans-serif",      "800", "1.5px", "toggle-e"),
]

combo_html = ""
for name, family, weight, spacing, toggle_class in combos:
    # Build inline toggle preview
    if "toggle-f" in toggle_class:
        toggle_el = '<div class="toggle-f on"><div class="knob"></div></div>'
    elif "toggle-b" in toggle_class:
        toggle_el = '<div class="toggle-b"><div class="seg active">Dark</div><div class="seg">Light</div></div>'
    elif "toggle-d" in toggle_class:
        toggle_el = '<div class="toggle-d"><div class="btn active">Dark</div><div class="btn">Light</div></div>'
    elif "toggle-g" in toggle_class:
        toggle_el = '<div class="toggle-g"><div class="chip active">Dark</div><div class="chip">Light</div></div>'
    elif "toggle-c" in toggle_class:
        toggle_el = '<div class="toggle-c on"><div class="icon-knob">☀️</div></div>'
    elif "toggle-e" in toggle_class:
        toggle_el = '<div class="toggle-e"><div class="tab active">Dark</div><div class="tab">Light</div></div>'
    else:
        toggle_el = '<div class="toggle-a on"><div class="knob"></div></div>'

    combo_html += f"""
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:14px;padding:1.5rem 2rem;margin:0.8rem 0;">
        <div style="font-family:'Nunito Sans',sans-serif;color:#555;font-size:0.6rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:1rem;">{name}</div>
        <div style="display:flex;align-items:center;justify-content:space-between;">
            <div>
                <div style="font-family:'Russo One',sans-serif;color:{AC};font-size:0.8rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:0.8rem;">Appearance</div>
                <div style="display:flex;align-items:center;gap:1rem;">
                    <div style="font-family:{family};font-weight:{weight};letter-spacing:{spacing};font-size:1rem;color:#e0e0e0;text-transform:uppercase;">Dark Mode</div>
                    {toggle_el}
                </div>
            </div>
        </div>
    </div>"""

st.markdown(f"""
<div class="sampler-section">
    <h2>3 — Combined Previews (Font + Toggle)</h2>
    {combo_html}
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align:center;padding:2rem 0;font-family:'Nunito Sans',sans-serif;color:#555;font-size:0.75rem;letter-spacing:1px;">
    Tell me the font number (1–10) and toggle letter (A–H) you like best.
</div>
""", unsafe_allow_html=True)
