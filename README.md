# Pastor Cosmus Muema

A Streamlit site about community care and ways to support children and families in Kenya.

## Open locally

Double-click `index.html` to open the standalone site in your browser. Keep
`styles.css` and the original JPEGs in `images/` in place. The site and photos
work offline. The six gallery JPEGs are included in the repository and are used
by both versions of the site.

## Connect online donations

Set `donationCheckout` in `donations.js` to the public HTTPS donation checkout
URL issued to the home's payment account. Configure donation amounts, currency,
and receipts with the payment provider. The donation page sends visitors there
to complete payment.

## Run the Streamlit version

```sh
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Prepare gallery illustrations

```sh
python images/anonymize.py --people
```

Keep source photos in `images/`. The script reduces each
WhatsApp photo to one average color and draws generic figures in a fresh PNG
under `images/anonymized/`.
The result carries no faces, source filenames, location metadata, or source
image geometry.

## Deploy

In [Streamlit Community Cloud](https://share.streamlit.io/), choose **Create app**
and select `Tfnancy/project`, the branch containing this code, and `app.py`.
