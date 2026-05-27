# What I Did

This project is an e-waste condition classifier built as a Streamlit web app. The app uses a trained YOLOv8 model to classify uploaded device images into one of three condition stages: **Usable**, **Better**, or **Trash**.

## Key components I created or configured

- `ewaste_app/app.py`
  - Built the main Streamlit application.
  - Added a custom dark theme using CSS injected into Streamlit with `st.markdown(..., unsafe_allow_html=True)`.
  - Configured page metadata with `st.set_page_config(...)`.
  - Implemented a model loader that uses `ultralytics.YOLO` to load the YOLOv8 model file.
  - Added a sidebar where the user can upload `best.pt` if it is not already present.
  - Added an image uploader that accepts `jpg`, `jpeg`, `png`, `webp`, and `bmp` files.
  - Implemented the classification flow:
    - user uploads an image
    - user clicks **Analyse Condition**
    - the model predicts device condition probabilities
    - the app displays the predicted condition and confidence bars
  - Stored prediction results in `st.session_state` so the result persists while the user interacts with the page.
  - Added a helpful no-model prompt when `best.pt` is missing and a no-image prompt when an image has not yet been uploaded.

- `ewaste_app/README.md`
  - Documented how to install dependencies and run the app.
  - Explained where to place the `best.pt` file.
  - Described the app workflow and supported device categories.

## What the app does

- Loads a YOLOv8 model from `best.pt`.
- Supports uploading a model file in the sidebar.
- Allows users to upload an e-waste device image.
- Runs the model on the uploaded image and calculates condition probabilities.
- Displays the predicted condition stage with:
  - a large condition label
  - an icon for the stage
  - a textual meaning of the stage
  - confidence bars for all three stages

## Supported device categories

- Battery
- Keyboard
- Microwave
- Mobile
- Mouse
- PCB
- Player
- Printer
- Television

## Condition stage meanings

- **Usable** — Works fine, ready to reuse as-is.
- **Better** — Repairable, has salvage value with some work.
- **Trash** — Beyond repair, recycle only.

## How to run the project

1. Activate your Python environment.
2. Install dependencies from `ewaste_app/requirements.txt`.
3. Run the app with:
   ```bash
   streamlit run ewaste_app/app.py
   ```
4. Open the app in the browser at `http://localhost:8501`.

## Notes on implementation

- The app uses `ultralytics.YOLO` for inference.
- It uses PIL to load uploaded images and convert them to RGB.
- It uses a small UX delay with `time.sleep(0.4)` before showing results.
- The app applies custom styling to create a polished dark interface with branded colors.

## Files present in the project

- `ewaste_app/app.py` — main Streamlit app code
- `ewaste_app/README.md` — app instructions and overview
- `ewaste_app/best.pt` — trained YOLOv8 model file
- `ewaste_app/requirements.txt` — Python dependencies for the app
- `ewaste_project_all_files/` — supporting project files and model outputs
- `ewaste_project_all_files/class_labels.json` — class label mapping data
- `ewaste_project_all_files/last.pt` — additional model checkpoint
- `ewaste_project_all_files/results.csv` — result data export
