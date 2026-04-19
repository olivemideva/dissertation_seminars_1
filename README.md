# Aid Project Duration and Efficiency App

This repository hosts a Streamlit web application that predicts:
- Project duration
- Project efficiency

## Run locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the app:

```bash
streamlit run app.py
```

3. Open the URL shown in the terminal (usually http://localhost:8501).

## Share with other people

Use Streamlit Community Cloud:

1. Push this repository to your GitHub account.
2. Go to https://share.streamlit.io/ and sign in.
3. Click New app and select this repository.
4. Set the main file path to `app.py`.
5. Deploy and share the generated public URL.

## Notes

- Keep `duration_model.pkl` and `efficiency_model.pkl` in the same folder as `app.py`.
- The app expects the dataset at `../Data/iati-activities-in-kenya-no-location-information.csv` relative to this project folder.
