"""Page 3 — YOLOv8 ML classifier."""

import streamlit as st
from shared.utils import (
    DEVICES,
    get_model_path,
    init_page,
    load_model,
    page_banner,
    render_footer,
    render_ml_classifier_page,
)

init_page()

page_banner(
    "AI Condition Classification",
    "Upload a photo of your device (image only) — AI predicts Usable, Better, or Trash.",
    "🤖",
)

tags = " ".join(f'<span class="tag">{d}</span>' for d in DEVICES)
st.markdown(f"<p style='font-size:0.85rem;color:#64748b'><strong>Supported:</strong> {tags}</p>", unsafe_allow_html=True)

model_path = get_model_path()
if model_path is None:
    st.error("AI model is not installed on the server. Ask your developer to add `best.pt` to the app folder.")
    st.info("You only need to upload **device photos** here — not model files.")
else:
    try:
        model = load_model(model_path)
        render_ml_classifier_page(model)
    except Exception as exc:
        st.error(f"Could not load model: {exc}")
        st.caption("Ensure `best.pt` is a valid YOLOv8 classification weights file.")

render_footer()
