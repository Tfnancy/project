# Pastor Cosmus Muema

A Streamlit site about community care and ways to support children and families in Kenya.

## Run locally

```sh
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Prepare gallery illustrations

```sh
python images/anonymize.py
```

Keep source photos in `images/`. Git ignores them. The script reduces each
photo to one average color and draws new shapes in a fresh PNG under `assets/`.
The result carries no faces, source filenames, location metadata, or source
image geometry.

## Deploy

In [Streamlit Community Cloud](https://share.streamlit.io/), choose **Create app**
and select `Tfnancy/project`, the branch containing this code, and `app.py`.
