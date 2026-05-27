"""Shared styles, constants, map search, and model helpers."""

import os
import sys
import time
from pathlib import Path

import folium
import requests
import streamlit as st
from folium.plugins import MarkerCluster
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from PIL import Image
from streamlit_folium import st_folium
APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

NOMINATIM_AGENT = "ewaste_recycling_guidance/1.0"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
DEFAULT_MODEL_PATH = str(APP_DIR / "best.pt")

CONDITIONS = ["Usable", "Better", "Trash"]
ICONS = {"Usable": "✅", "Better": "🔧", "Trash": "♻️"}
MEANINGS = {
    "Usable": "Works fine — ready to reuse as-is.",
    "Better": "Repairable — has salvage value with some work.",
    "Trash": "Beyond repair — send to recycling only.",
}
DEVICES = [
    "Battery", "Keyboard", "Microwave", "Mobile", "Mouse",
    "PCB", "Player", "Printer", "Television",
]
# Multipage routes (do not use st.page_link on app.py — it causes KeyError)
PAGE_ROUTES = {
    "Home": "app.py",
    "Map Search": "pages/2_Map_Search.py",
    "ML Classifier": "pages/3_ML_Classifier.py",
    "About E-Waste": "pages/4_About_E-Waste.py",
    "Contribution": "pages/5_Contribution.py",
}

SEARCH_QUERIES = {
    "Recycling Center": [
        "e-waste recycling",
        "electronic waste recycling",
        "e waste collection center",
    ],
    "Scrap Dealer": [
        "scrap dealer electronic waste",
        "e-waste scrap dealer",
        "kabadi scrap metal",
    ],
    "All": [
        "e-waste recycling",
        "electronic waste recycling",
        "scrap dealer electronic waste",
        "e-waste scrap",
    ],
}


def apply_styles():
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%); }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 1rem; max-width: 1100px; }

.page-hero {
    background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 24px 28px; margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(15,23,42,0.06);
}
.page-hero h1 { font-size: 1.85rem; font-weight: 700; color: #0f172a; margin: 0 0 8px 0; }
.page-hero h1 span { color: #0d9488; }
.page-hero p { color: #64748b; font-size: 0.92rem; line-height: 1.6; margin: 0; }

.section-panel {
    background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 20px 22px; margin-bottom: 18px;
    box-shadow: 0 1px 3px rgba(15,23,42,0.05);
}
.info-card {
    background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px;
    padding: 16px 18px; height: 100%;
}
.info-card h3 { font-size: 1rem; color: #0f172a; margin: 0 0 8px 0; }
.info-card p { font-size: 0.85rem; color: #64748b; line-height: 1.55; margin: 0; }

.feature-card {
    background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 20px; text-align: center; height: 100%;
    transition: box-shadow 0.2s;
}
.feature-card:hover { box-shadow: 0 4px 12px rgba(13,148,136,0.12); }
.feature-icon { font-size: 2rem; margin-bottom: 8px; }
.feature-title { font-weight: 700; color: #0f172a; font-size: 1rem; margin-bottom: 6px; }
.feature-desc { font-size: 0.82rem; color: #64748b; line-height: 1.5; }

.result-card, .recycle-card, .place-card, .empty-box {
    background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px;
    padding: 18px 20px; margin-top: 12px;
}
.condition-usable { color: #059669; }
.condition-better { color: #d97706; }
.condition-trash { color: #dc2626; }
.condition-title { font-size: 1.6rem; font-weight: 700; margin-bottom: 4px; }
.conf-label {
    font-size: 0.68rem; letter-spacing: 0.08em; text-transform: uppercase;
    color: #94a3b8; margin: 14px 0 8px;
}
.bar-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.bar-name { width: 56px; font-size: 0.75rem; color: #64748b; font-weight: 500; }
.bar-track { flex: 1; height: 8px; background: #e2e8f0; border-radius: 4px; overflow: hidden; }
.bar-fill-usable { height: 100%; background: #10b981; border-radius: 4px; }
.bar-fill-better { height: 100%; background: #f59e0b; border-radius: 4px; }
.bar-fill-trash { height: 100%; background: #ef4444; border-radius: 4px; }
.bar-pct { width: 44px; text-align: right; font-size: 0.75rem; color: #64748b; }
.divider { border: none; border-top: 1px solid #e2e8f0; margin: 14px 0; }
.result-meta { font-size: 0.88rem; color: #64748b; }
.recycle-guidance {
    background: #fef2f2; border-left: 3px solid #ef4444;
    padding: 12px 14px; border-radius: 0 8px 8px 0;
    font-size: 0.86rem; color: #475569; line-height: 1.55;
}
.place-row { padding: 10px 0; border-bottom: 1px solid #e2e8f0; font-size: 0.85rem; color: #334155; }
.place-row:last-child { border-bottom: none; }
.place-meta { color: #94a3b8; font-size: 0.78rem; }
.place-dist { color: #0d9488; font-weight: 700; }
.tag {
    display: inline-block; background: #f1f5f9; border: 1px solid #e2e8f0;
    border-radius: 6px; padding: 4px 9px; font-size: 0.68rem; color: #64748b; margin: 3px;
}
.stat-box {
    background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%);
    border-radius: 10px; padding: 16px; color: #fff; text-align: center;
}
.stat-num { font-size: 1.5rem; font-weight: 700; }
.stat-lbl { font-size: 0.72rem; opacity: 0.9; margin-top: 4px; }

div[data-testid="stButton"] > button {
    background: #0d9488 !important; color: #fff !important; border: none !important;
    border-radius: 8px !important; font-weight: 600 !important;
}
div[data-testid="stButton"] > button:hover { background: #0f766e !important; }
[data-testid="stSidebar"] { background: #fff !important; border-right: 1px solid #e2e8f0 !important; }
[data-testid="stImage"] img { border-radius: 10px; border: 1px solid #e2e8f0; }

.site-footer {
    text-align: center; padding: 20px; margin-top: 28px;
    font-size: 0.78rem; color: #94a3b8;
    border-top: 1px solid #e2e8f0;
}
</style>
        """,
        unsafe_allow_html=True,
    )


def page_banner(title: str, subtitle: str, icon: str = "♻"):
    st.markdown(
        f"""
        <div class="page-hero">
            <h1>{icon} {title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        """
        <div class="site-footer">
            Smart E-Waste Guide · Minor Engineering Project ·
            YOLOv8 + OpenStreetMap · No login required
        </div>
        """,
        unsafe_allow_html=True,
    )


def init_session_state():
    """Default session keys so every page works on first visit."""
    defaults = {
        "map_query": "Pune, Maharashtra, India",
        "map_geo": None,
        "map_places": [],
        "map_error": None,
        "has_result": False,
        "result": None,
        "conf": None,
        "last_upload_id": None,
        "feedbacks": [],
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def go_to_page(page_name: str):
    """Navigate between pages using st.switch_page (works with app.py as home)."""
    path = PAGE_ROUTES.get(page_name)
    if path:
        st.switch_page(path)


def nav_button(label: str, page_name: str, key=None):
    """Render a button that navigates to another page."""
    if st.button(label, key=key, use_container_width=True):
        go_to_page(page_name)


def render_sidebar():
    """Sidebar: status, navigation (users upload images on ML page — not model files)."""
    with st.sidebar:
        st.markdown("### ♻ E-Waste Guide")
        path = get_model_path()
        if path:
            st.success("AI model ready")
        else:
            st.error("AI model not installed")

        st.info(
            "📷 To classify a device, open **ML Classifier** and upload your "
            "**photo** (JPG, PNG, JPEG) — not here in the sidebar."
        )
        if st.button("→ Go to ML Classifier", key="sidebar_go_ml", use_container_width=True):
            go_to_page("ML Classifier")

        st.divider()
        st.markdown("**Navigate**")
        st.caption("Or use the page list above in this sidebar.")
        page_choice = st.selectbox(
            "Go to page",
            list(PAGE_ROUTES.keys()),
            key="sidebar_nav_select",
            label_visibility="collapsed",
        )
        if st.button("Go →", key="sidebar_nav_go", use_container_width=True):
            go_to_page(page_choice)

        st.divider()
        st.caption("Map data: OpenStreetMap")

    return get_model_path()


def get_model_path():
    """Resolve YOLO weights path (default file or sidebar upload)."""
    if st.session_state.get("model_path") and os.path.exists(st.session_state["model_path"]):
        return st.session_state["model_path"]
    if os.path.exists(DEFAULT_MODEL_PATH):
        return DEFAULT_MODEL_PATH
    return None


def init_page():
    """Call at top of every page."""
    init_session_state()
    apply_styles()
    return render_sidebar()


@st.cache_resource
def load_model(path: str):
    from ultralytics import YOLO
    return YOLO(path)


@st.cache_resource
def get_geocoder():
    return Nominatim(user_agent=NOMINATIM_AGENT)


@st.cache_data(ttl=3600, show_spinner=False)
def geocode_location(query: str):
    geo = get_geocoder()
    loc = geo.geocode(query, country_codes="in", timeout=15)
    if loc is None:
        loc = geo.geocode(query, timeout=15)
    if loc is None:
        return None
    return {
        "lat": loc.latitude,
        "lon": loc.longitude,
        "address": loc.address,
        "display": loc.address.split(",")[0] if loc.address else query,
    }


def _place_key(lat, lon):
    return (round(lat, 4), round(lon, 4))


def _tags_name(tags: dict, fallback: str) -> str:
    return (
        tags.get("name") or tags.get("brand") or tags.get("operator")
        or tags.get("shop") or tags.get("amenity") or fallback
    )


@st.cache_data(ttl=1800, show_spinner=False)
def search_overpass(lat: float, lon: float, radius_km: int, search_type: str):
    radius_m = int(radius_km * 1000)
    filters = []
    if search_type in ("Recycling Center", "All"):
        filters.extend([
            f'node["amenity"="recycling"](around:{radius_m},{lat},{lon});',
            f'way["amenity"="recycling"](around:{radius_m},{lat},{lon});',
            f'node["recycling_type"](around:{radius_m},{lat},{lon});',
        ])
    if search_type in ("Scrap Dealer", "All"):
        filters.extend([
            f'node["shop"="scrap"](around:{radius_m},{lat},{lon});',
            f'node["shop"="scrap_metal"](around:{radius_m},{lat},{lon});',
            f'node["craft"="scrap_metal"](around:{radius_m},{lat},{lon});',
        ])
    if not filters:
        return []
    body = f"[out:json][timeout:45]; ( {"".join(filters)} ); out center 60;"
    try:
        resp = requests.post(
            OVERPASS_URL, data={"data": body}, timeout=50,
            headers={"User-Agent": NOMINATIM_AGENT},
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException:
        return []

    places = []
    for el in data.get("elements", []):
        tags = el.get("tags") or {}
        if el["type"] == "node":
            plat, plon = el["lat"], el["lon"]
        elif "center" in el:
            plat, plon = el["center"]["lat"], el["center"]["lon"]
        else:
            continue
        kind = "Scrap Dealer" if tags.get("shop") in ("scrap", "scrap_metal") else "Recycling Center"
        addr = ", ".join(
            p for p in [tags.get("addr:street"), tags.get("addr:city")] if p
        ) or tags.get("addr:full", "OpenStreetMap listing")
        places.append({
            "name": _tags_name(tags, kind), "lat": plat, "lon": plon,
            "type": kind, "address": addr, "source": "OpenStreetMap",
        })
    return places


@st.cache_data(ttl=1800, show_spinner=False)
def search_nominatim_pois(lat: float, lon: float, search_type: str, city_hint: str):
    queries = SEARCH_QUERIES.get(search_type, SEARCH_QUERIES["All"])
    found = []
    headers = {"User-Agent": NOMINATIM_AGENT}
    for q in queries:
        params = {"q": f"{q} {city_hint}", "format": "json", "limit": 8,
                  "addressdetails": 1, "lat": lat, "lon": lon}
        try:
            r = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params=params, headers=headers, timeout=15,
            )
            r.raise_for_status()
            time.sleep(1.05)
        except requests.RequestException:
            continue
        for item in r.json():
            try:
                plat, plon = float(item["lat"]), float(item["lon"])
            except (KeyError, ValueError):
                continue
            found.append({
                "name": item.get("display_name", "").split(",")[0] or q.title(),
                "lat": plat, "lon": plon,
                "type": search_type if search_type != "All" else "Recycling Center",
                "address": item.get("display_name", ""),
                "source": "Nominatim",
            })
    return found


def merge_and_rank_places(user_coords, places, limit=15):
    seen, ranked = set(), []
    for p in places:
        key = _place_key(p["lat"], p["lon"])
        if key in seen:
            continue
        seen.add(key)
        p["distance_km"] = geodesic(user_coords, (p["lat"], p["lon"])).km
        ranked.append(p)
    ranked.sort(key=lambda x: x["distance_km"])
    return ranked[:limit]


def find_real_nearby_centers(location_query: str, search_type: str, radius_km: int):
    geo = geocode_location(location_query.strip())
    if geo is None:
        return None, [], "Could not find that location. Try Pune, Mumbai, Delhi, etc."

    user_coords = (geo["lat"], geo["lon"])
    city_hint = geo.get("display", location_query)
    combined = (
        search_overpass(geo["lat"], geo["lon"], radius_km, search_type)
        + search_nominatim_pois(geo["lat"], geo["lon"], search_type, city_hint)
    )
    ranked = merge_and_rank_places(user_coords, combined)
    if not ranked and radius_km < 50:
        combined = search_overpass(geo["lat"], geo["lon"], min(radius_km * 2, 50), search_type) + combined
        ranked = merge_and_rank_places(user_coords, combined)
    if not ranked:
        return geo, [], f"No places found within {radius_km} km. Try a larger radius or bigger city."
    return geo, ranked, None


def build_results_map(user_coords, places):
    user_lat, user_lon = user_coords
    zoom = 13 if places and places[0]["distance_km"] < 5 else 11
    fmap = folium.Map(location=[user_lat, user_lon], zoom_start=zoom, tiles="OpenStreetMap")
    folium.Marker(
        [user_lat, user_lon], popup="Your location", tooltip="You are here",
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(fmap)
    cluster = MarkerCluster().add_to(fmap)
    for i, p in enumerate(places):
        folium.Marker(
            [p["lat"], p["lon"]],
            popup=folium.Popup(
                f"<b>{p['name']}</b><br>{p.get('address','')}<br>{p['distance_km']:.2f} km",
                max_width=280,
            ),
            tooltip=f"{p['name']} ({p['distance_km']:.1f} km)",
            icon=folium.Icon(color="green" if i == 0 else "lightgray", icon="leaf"),
        ).add_to(cluster)
    if places:
        n = places[0]
        folium.PolyLine(
            [[user_lat, user_lon], [n["lat"], n["lon"]]],
            color="#0d9488", weight=4, opacity=0.85, dash_array="8",
        ).add_to(fmap)
    return fmap


def render_map_search_page():
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        location_query = st.text_input(
            "Your city or area",
            value=st.session_state.get("map_query", "Pune, Maharashtra, India"),
            placeholder="e.g. Pune, Mumbai, Delhi",
        )
    with c2:
        search_type = st.selectbox("Search for", ["All", "Recycling Center", "Scrap Dealer"])
    with c3:
        radius_km = st.slider("Radius (km)", 5, 50, 25)

    if st.button("🔎 Search Nearest Centers", type="primary", use_container_width=True):
        if not location_query.strip():
            st.warning("Please enter a city or area first.")
        else:
            st.session_state["map_query"] = location_query.strip()
            with st.spinner("Searching OpenStreetMap… (may take 15–30 seconds)"):
                geo, places, err = find_real_nearby_centers(
                    location_query.strip(), search_type, radius_km
                )
            st.session_state["map_geo"] = geo
            st.session_state["map_places"] = places
            st.session_state["map_error"] = err

    geo = st.session_state.get("map_geo")
    places = st.session_state.get("map_places") or []
    err = st.session_state.get("map_error")
    query_display = st.session_state.get("map_query", location_query)

    if err:
        st.error(err)
    elif geo and places:
        user_coords = (geo["lat"], geo["lon"])
        nearest = places[0]
        st.markdown(
            f"""
            <div class="recycle-card">
                <div class="recycle-guidance" style="border-color:#0d9488;background:#f0fdfa">
                    Found <strong>{len(places)}</strong> place(s) near
                    <strong>{geo.get('address', query_display)}</strong>.
                    Nearest: <strong>{nearest['name']}</strong>
                    (<span class="place-dist">{nearest['distance_km']:.2f} km</span>)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        lc, mc = st.columns([1, 1.4])
        with lc:
            st.markdown("**Top results**")
            rows = ""
            for i, p in enumerate(places[:10]):
                badge = "🟢 Nearest" if i == 0 else f"#{i+1}"
                rows += f"""<div class="place-row"><strong>{badge} {p['name']}</strong><br>
                <span class="place-meta">{p.get('type','')} · {p.get('source','')}</span><br>
                {p.get('address','')[:90]}<br>
                <span class="place-dist">{p['distance_km']:.2f} km</span></div>"""
            st.markdown(f'<div class="place-card">{rows}</div>', unsafe_allow_html=True)
        with mc:
            st_folium(build_results_map(user_coords, places), width=None, height=500, returned_objects=[])
    else:
        st.info("Enter your city and click **Search Nearest Centers**.")


def render_ml_classifier_page(model):
    st.markdown(
        """
        <div class="section-panel">
            <p style="margin:0;color:#64748b;font-size:0.9rem">
            Upload a <strong>photo of your electronic device</strong> (JPG, PNG, WEBP).
            You do <strong>not</strong> upload any model file — the AI is already loaded in the app.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_gallery, tab_camera = st.tabs(["📁 Upload image", "📷 Use camera"])

    device_image = None
    image_label = ""

    with tab_gallery:
        gallery_img = st.file_uploader(
            "Choose a device photo from your device",
            type=["jpg", "jpeg", "png", "webp", "bmp"],
            help="Image of phone, laptop, keyboard, TV, battery, etc.",
            key="ml_image_gallery",
        )
        if gallery_img is not None:
            device_image = gallery_img
            image_label = gallery_img.name

    with tab_camera:
        camera_img = st.camera_input(
            "Take a picture of the e-waste device",
            key="ml_image_camera",
        )
        if camera_img is not None:
            device_image = camera_img
            image_label = "Camera capture"

    if device_image is None:
        st.session_state["has_result"] = False
        st.markdown(
            """<div class="empty-box" style="text-align:center;padding:36px">
            <div style="font-size:2.2rem">📷</div>
            <p style="color:#94a3b8;margin-top:8px">
            Upload an image or use your camera — then click Analyse</p></div>""",
            unsafe_allow_html=True,
        )
        return

    upload_id = f"{image_label}_{getattr(device_image, 'size', 0)}"
    if st.session_state.get("last_upload_id") != upload_id:
        st.session_state["last_upload_id"] = upload_id
        st.session_state["has_result"] = False

    img = Image.open(device_image).convert("RGB")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.image(img, caption=image_label, use_container_width=True)
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Analyse Condition", type="primary", use_container_width=True):
            with st.spinner("Running YOLOv8..."):
                try:
                    time.sleep(0.2)
                    r = model.predict(img, imgsz=224, verbose=False)[0]
                    if r.probs is None:
                        st.error("Model output is not classification format. Check your `best.pt` file.")
                    else:
                        probs = r.probs
                        top_cond = CONDITIONS[int(probs.top1)]
                        conf = {CONDITIONS[i]: float(probs.data[i]) for i in range(3)}
                        st.session_state["result"] = top_cond
                        st.session_state["conf"] = conf
                        st.session_state["has_result"] = True
                except Exception as exc:
                    st.error(f"Prediction failed: {exc}")

    if st.session_state.get("has_result") and st.session_state.get("conf"):
        top_cond = st.session_state["result"]
        conf = st.session_state["conf"]
        css = f"condition-{top_cond.lower()}"
        st.markdown(
            f"""<div class="result-card"><div class="conf-label">Result</div>
            <div class="condition-title {css}">{ICONS[top_cond]} {top_cond}</div>
            <div class="result-meta">{MEANINGS[top_cond]}</div><hr class="divider">
            <div class="conf-label">Confidence</div>
            <div class="bar-row"><div class="bar-name">Usable</div>
            <div class="bar-track"><div class="bar-fill-usable" style="width:{conf['Usable']*100:.1f}%"></div></div>
            <div class="bar-pct">{conf['Usable']*100:.1f}%</div></div>
            <div class="bar-row"><div class="bar-name">Better</div>
            <div class="bar-track"><div class="bar-fill-better" style="width:{conf['Better']*100:.1f}%"></div></div>
            <div class="bar-pct">{conf['Better']*100:.1f}%</div></div>
            <div class="bar-row"><div class="bar-name">Trash</div>
            <div class="bar-track"><div class="bar-fill-trash" style="width:{conf['Trash']*100:.1f}%"></div></div>
            <div class="bar-pct">{conf['Trash']*100:.1f}%</div></div></div>""",
            unsafe_allow_html=True,
        )
        if top_cond == "Trash":
            st.warning("Device is **Trash** — find a recycling center on the Map Search page.")
            nav_button("Go to Map Search →", "Map Search", key="trash_to_map")
