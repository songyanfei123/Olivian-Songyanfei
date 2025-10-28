# Dreamy Blue Star Poster (Streamlit + matplotlib)

Generate dreamy, low-saturation blue star posters with soft shadows, stardust, and aurora glow — rendered purely with **matplotlib** and controlled via **Streamlit**.

## Run locally
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy on Streamlit Cloud (GitHub flow)

1. **Create a GitHub repo** (public is easiest).
2. Add three files at the repo root:
   - `streamlit_app.py`  ← the app
   - `requirements.txt`  ← Python deps
   - `README.md`         ← (optional) docs
3. Go to **streamlit.io → Sign in → New app**.
4. Choose your repo, branch (e.g., `main`), and set **App file** to `streamlit_app.py`.
5. Click **Deploy**.

### Common pitfalls
- Wrong **App file path** → must be exactly `streamlit_app.py` if placed at repo root.
- Missing packages → ensure `requirements.txt` contains `streamlit`, `matplotlib`, `numpy`.
- Private repo → Streamlit Cloud needs access (grant when connecting).
- App shows **ModuleNotFoundError** → re-deploy after editing `requirements.txt`.
