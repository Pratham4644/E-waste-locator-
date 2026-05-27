"""
Page 1 — Home
Smart E-Waste Identification and Recycling Guidance System
"""

import streamlit as st
from shared.utils import DEVICES, get_model_path, init_page, nav_button, page_banner, render_footer

st.set_page_config(
    page_title="Home | E-Waste Smart Guide",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_page()

page_banner(
    "Smart E-Waste Guide",
    "AI device condition check + live recycling center search. "
    "Engineering minor project — free, no login.",
    "🏠",
)

if get_model_path():
    st.success("✓ AI is ready — go to **ML Classifier** and upload a **device photo** (image).")
else:
    st.warning("AI model not installed — classifier page needs `best.pt` in the app folder (developer setup).")

s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown('<div class="stat-box"><div class="stat-num">3</div><div class="stat-lbl">Condition stages</div></div>', unsafe_allow_html=True)
with s2:
    st.markdown('<div class="stat-box"><div class="stat-num">9+</div><div class="stat-lbl">Device types</div></div>', unsafe_allow_html=True)
with s3:
    st.markdown('<div class="stat-box"><div class="stat-num">YOLOv8</div><div class="stat-lbl">ML classifier</div></div>', unsafe_allow_html=True)
with s4:
    st.markdown('<div class="stat-box"><div class="stat-num">OSM</div><div class="stat-lbl">Live map search</div></div>', unsafe_allow_html=True)

st.markdown("### Explore the app")
r1c1, r1c2, r1c3 = st.columns(3)
with r1c1:
    st.markdown("**📍 Map Search** — Find real recyclers & scrap dealers near you.")
    nav_button("Open Map Search →", "Map Search", key="home_map")
with r1c2:
    st.markdown("**🤖 ML Classifier** — Upload a device **image** → Usable / Better / Trash.")
    nav_button("Open Classifier →", "ML Classifier", key="home_ml")
with r1c3:
    st.markdown("**📚 About E-Waste** — Problems, impact & how we help.")
    nav_button("Learn more →", "About E-Waste", key="home_about")

r2c1, r2c2 = st.columns(2)
with r2c1:
    st.markdown("**🙏 Contribution** — Project info, tech stack & feedback.")
    nav_button("View contribution →", "Contribution", key="home_contrib")
with r2c2:
    st.markdown(
        """
        <div class="info-card">
            <h3>Quick tip</h3>
            <p>Classify your device first. If result is <strong>Trash</strong>, use Map Search to find where to recycle it.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="section-panel">
        <h2 style="color:#0f172a;font-size:1.15rem;margin:0 0 12px 0">How it works</h2>
        <ol style="color:#64748b;line-height:1.9;font-size:0.9rem;padding-left:20px">
            <li>Upload a device image on <strong>ML Classifier</strong></li>
            <li>Get <strong>Usable</strong>, <strong>Better</strong>, or <strong>Trash</strong> with confidence scores</li>
            <li>If Trash, open <strong>Map Search</strong> and find a nearby center</li>
            <li>Read <strong>About E-Waste</strong> to understand why recycling matters</li>
        </ol>
    </div>
    """,
    unsafe_allow_html=True,
)

tags = " ".join(f'<span class="tag">{d}</span>' for d in DEVICES)
st.markdown(f"<p style='font-size:0.85rem;color:#64748b'><strong>Supported devices:</strong> {tags}</p>", unsafe_allow_html=True)

render_footer()
