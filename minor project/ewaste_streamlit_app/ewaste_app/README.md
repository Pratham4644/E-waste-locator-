# ♻️ Smart E-Waste Guide — Multi-Page Streamlit App

## Pages (sidebar navigation)

| Page | Description |
|------|-------------|
| **Home** | Welcome, overview, quick links |
| **Map Search** | Find real recyclers & scrap dealers (OpenStreetMap) |
| **ML Classifier** | YOLOv8 — Usable / Better / Trash |
| **About E-Waste** | Problems, impact, how we help |
| **Contribution** | Project credits & how you can support |

No login or authentication required.

## Setup & Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open **http://localhost:8501** — use the **left sidebar** to switch pages.

## Project structure

```
ewaste_app/
├── app.py                 # Page 1 — Home
├── pages/
│   ├── 2_Map_Search.py
│   ├── 3_ML_Classifier.py
│   ├── 4_About_E-Waste.py
│   └── 5_Contribution.py
├── shared/utils.py        # Styles, map search, ML helpers
├── best.pt
└── requirements.txt
```
