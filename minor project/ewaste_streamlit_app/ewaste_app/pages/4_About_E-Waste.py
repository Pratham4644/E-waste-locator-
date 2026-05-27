"""Page 4 — E-waste awareness."""

import streamlit as st
from shared.utils import init_page, nav_button, page_banner, render_footer

init_page()

page_banner(
    "About E-Waste",
    "Why electronic waste matters — and how this project helps you recycle responsibly.",
    "📚",
)

st.markdown("### 🌍 The current problem")
p1, p2 = st.columns(2)
with p1:
    st.markdown(
        """<div class="info-card"><h3>Growing global waste</h3>
        <p>Millions of tonnes of e-waste are produced yearly. Devices are discarded faster than they are recycled.</p></div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<div class="info-card" style="margin-top:12px"><h3>Toxic materials</h3>
        <p>Lead, mercury, and cadmium in electronics pollute soil and water when dumped improperly.</p></div>""",
        unsafe_allow_html=True,
    )
with p2:
    st.markdown(
        """<div class="info-card"><h3>Health impact</h3>
        <p>Informal recycling exposes workers to harmful chemicals. Certified centers are safer.</p></div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<div class="info-card" style="margin-top:12px"><h3>Lost resources</h3>
        <p>Gold, copper, and rare metals are wasted when devices are not recovered.</p></div>""",
        unsafe_allow_html=True,
    )

st.markdown("### ✅ How our app helps you")
a, b, c = st.columns(3)
with a:
    st.markdown("**🤖 Classify** — Know if a device is reusable, repairable, or trash.")
    nav_button("Try classifier →", "ML Classifier", key="about_ml")
with b:
    st.markdown("**📍 Locate** — Find real recyclers and scrap dealers on a map.")
    nav_button("Try map search →", "Map Search", key="about_map")
with c:
    st.markdown("**♻️ Act** — Follow clear guidance for each condition stage.")

st.success(
    "**Usable** → Reuse or donate  \n"
    "**Better** → Repair or refurbish  \n"
    "**Trash** → Recycle at a proper center (use Map Search)"
)

render_footer()
