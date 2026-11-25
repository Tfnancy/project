from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"

st.set_page_config(page_title="Pastor Cosmus Muema", page_icon="🌿", layout="wide")
st.html("""
<style>
.block-container { max-width: 1180px; padding-top: 3rem; }
.st-key-hero { background: #19382e; border-radius: 24px; padding: clamp(1.5rem, 5vw, 4rem); }
.st-key-hero h1 { color: #fff4db; font-family: Georgia, serif; font-weight: 500;
  font-size: clamp(2.9rem, 7vw, 6rem); line-height: 1; letter-spacing: -.055em; }
.st-key-hero p { color: #f3e4c6; max-width: 36ch; font-size: 1.15rem; }
.st-key-hero img, .stImage img { border-radius: 14px; }
h2 { font-family: Georgia, serif; }
</style>
""")

with st.container(key="hero"):
    introduction, visual = st.columns([1.15, 1], vertical_alignment="center")
    with introduction:
        st.title("Pastor Cosmus Muema")
        st.write("Faith, service, and practical ways to support children and families in Kenya.")
    with visual:
        cover = ASSETS / "gallery-01.png"
        if cover.is_file():
            st.image(str(cover), width="stretch")

overview, gallery, involvement = st.tabs(["Community care", "Gallery", "Get involved"])

with overview:
    st.header("Helping children thrive")
    st.write("A safe home, an education, and access to healthcare give children room to grow.")
    for column, (title, description) in zip(st.columns(3), [
        ("Education", "Help children access learning and build skills for their future."),
        ("Shelter", "Support work that gives children a safe and caring place to live."),
        ("Healthcare", "Help children get the care they need to grow up healthy."),
    ]):
        with column.container(border=True):
            st.subheader(title)
            st.write(description)

with gallery:
    st.header("Gallery")
    illustrations = sorted(ASSETS.glob("gallery-*.png"))
    if illustrations:
        st.caption("Illustrations made from the average colors of private photographs.")
        columns = st.columns(3)
        for index, illustration in enumerate(illustrations):
            columns[index % len(columns)].image(str(illustration), width="stretch")
    else:
        st.info("Gallery illustrations are being prepared.")

with involvement:
    st.header("Support children in Kenya")
    st.write("Visit Upendo Kids to learn about their village, volunteer opportunities, and ways to give.")
    st.link_button("Visit Upendo Kids", "https://www.upendokids.org/", type="primary")

st.divider()
st.caption("Pastor Cosmus Muema · 2020")
