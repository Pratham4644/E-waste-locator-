"""Page 2 — Map Search."""

import streamlit as st
from shared.utils import init_page, page_banner, render_footer, render_map_search_page

init_page()

page_banner(
    "Find Nearest E-Waste Center",
    "Search real recycling centers and scrap dealers using OpenStreetMap (free, no API key).",
    "📍",
)

render_map_search_page()
render_footer()
