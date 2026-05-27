"""Page 5 — Contribution & feedback."""

import streamlit as st
from shared.utils import init_page, nav_button, page_banner, render_footer

init_page()

page_banner(
    "Contribution & Feedback",
    "Project credits, technologies used, and how you can support this work.",
    "🙏",
)

st.markdown("### 👨‍💻 What we built")
c1, c2 = st.columns(2)
with c1:
    st.markdown(
        """
        - YOLOv8 image classification (Usable / Better / Trash)
        - Multi-page Streamlit web application
        - Live map search (Nominatim + Overpass / OpenStreetMap)
        - E-waste awareness content
        - No login — open for everyone
        """
    )
with c2:
    st.markdown(
        """
        | Component | Technology |
        |-----------|------------|
        | UI | Streamlit |
        | ML | Ultralytics YOLOv8 |
        | Maps | Folium |
        | Geo | Geopy, OSM |
        """
    )

st.markdown("### 📬 Send feedback (works in this session)")
with st.form("feedback_form", clear_on_submit=True):
    fb_name = st.text_input("Your name (optional)")
    fb_email = st.text_input("Email (optional)")
    fb_msg = st.text_area("Message", placeholder="Suggestions, bugs, or cities to add…", height=120)
    submitted = st.form_submit_button("Submit feedback", type="primary", use_container_width=True)

if submitted:
    if not fb_msg.strip():
        st.warning("Please write a message before submitting.")
    else:
        st.session_state.feedbacks.append({
            "name": fb_name or "Anonymous",
            "email": fb_email or "—",
            "message": fb_msg.strip(),
        })
        st.success("Thank you! Your feedback was recorded.")

if st.session_state.feedbacks:
    st.markdown("#### Recent feedback (this session)")
    for i, fb in enumerate(reversed(st.session_state.feedbacks[-5:]), 1):
        st.markdown(
            f"**{i}. {fb['name']}** ({fb['email']})  \n{fb['message']}"
        )

st.markdown("### 🤝 How you can help")
st.markdown(
    """
    - **Share** this app with others  
    - **Recycle** using the classifier + map together  
    - **Improve OSM data** by adding missing centers on [OpenStreetMap](https://www.openstreetmap.org)  
    """
)

st.markdown("### 🏫 Project details (edit with your info)")
st.text_input("Institution", value="Your College Name", key="inst")
st.text_input("Team members", value="Name 1, Name 2", key="team")
st.text_input("Project guide", value="Guide Name", key="guide")
st.text_input("Contact email", value="your.email@college.edu", key="email")

st.divider()
nav_button("← Back to Home", "Home", key="contrib_home")
render_footer()
