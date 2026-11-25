from pathlib import Path
import re

import streamlit as st

ROOT = Path(__file__).resolve().parent
IMAGES = ROOT / "images"
originals = sorted(IMAGES.glob("WhatsApp Image *.jpeg"))
photos = originals or sorted((IMAGES / "anonymized").glob("people-*.png"))
PHOTO_DESCRIPTIONS = {
    "12.48.36 PM.jpeg": "Two children sitting on a bench",
    "12.48.38 PM.jpeg": "Children and adults standing outside a blue building",
    "12.48.39 PM.jpeg": "A group gathered outside beside stacked supplies",
    "12.48.40 PM (1).jpeg": "A bicycle decorated with balloons",
    "12.48.40 PM.jpeg": "A group working at an outdoor construction site",
    "12.48.41 PM.jpeg": "Children and adults gathered indoors on colorful mats",
}

st.set_page_config(page_title="Pastor Cosmus Muema | Children's Home", page_icon=":material/home:", layout="wide")
st.html(ROOT / "streamlit.css")

INFO_PAGES = {
    "about": "Who we are",
    "board": "The board",
    "founders": "The founders",
    "partners": "Community partners",
    "tour": "Tour the home",
    "impact": "Impact in action",
    "volunteer": "Volunteer",
    "contact": "Contact",
    "safeguarding": "Child safety and privacy",
}


def local_route(match: re.Match[str]) -> str:
    page, anchor = match.groups()
    return f'href="{"/" if page == "index" else "/" + page}{anchor or ""}"'


def info_page(slug: str):
    def render():
        # Reuse the standalone page body to keep both versions in sync.
        document = (ROOT / f"{slug}.html").read_text(encoding="utf-8")
        body = document.partition("<main")[2].partition(">")[2].partition("</main>")[0]
        content = re.sub(r'href="([a-z-]+)\.html(#[^"]+)?"', local_route, body)
        st.html(f'<div class="cosmus-info">{content}</div>')

    return st.Page(render, title=INFO_PAGES[slug], url_path=slug)


def home():
    with st.container(key="hero", horizontal=True, gap="large", vertical_alignment="center"):
        with st.container(width=380):
            st.caption("Children’s home and community care · Kenya")
            st.title("A safe place to grow")
            st.write("Children need dependable care, support at school, and time to play and build friendships.")
            st.page_link(giving, label="Ways to give", icon=":material/volunteer_activism:")
        if photos:
            cover = next((photo for photo in photos if photo.name.endswith("12.48.41 PM.jpeg")), photos[0])
            alt = PHOTO_DESCRIPTIONS.get(cover.name.split(" at ")[-1], "Illustration of figures standing together")
            st.image(str(cover), width=540, alt=alt)

    st.header("Daily care for children")
    with st.grid(min_column_width=220, gap="medium") as care:
        for title, description in [
            ("A safe home", "Regular meals, a comfortable place to sleep, and dependable adults."),
            ("Support at school", "Learning materials, time for homework, and encouragement."),
            ("Health and well-being", "Health checks, emotional support, and time to rest and play."),
            ("Family and community", "Support safe relationships with family and trusted adults."),
        ]:
            with care.container(border=True, height="stretch"):
                st.subheader(title)
                st.write(description)

    st.header("Get involved", anchor="help")
    with st.grid(min_column_width=230, gap="medium") as support:
        for target, title, description, link in [
            (giving, "Ways to give", "Help with meals, bedding, and school supplies.", "See giving options"),
            (details["volunteer"], "Volunteer", "Offer time, skills, or help with a collection.", "Explore volunteer roles"),
            (details["partners"], "Community partners", "Coordinate practical support with a local group.", "Explore partnerships"),
            (details["safeguarding"], "Child safety and privacy", "Read guidance for visitors and supporters.", "Read the guidance"),
        ]:
            with support.container(border=True, height="stretch"):
                st.subheader(title)
                st.write(description)
                st.page_link(target, label=link)

    st.header("Gallery")
    if photos:
        with st.container(key="photo-gallery"):
            with st.expander("View photos" if originals else "View illustrations", expanded=True):
                with st.grid(min_column_width=210, gap="small") as gallery:
                    for photo in photos:
                        fallback = "Photo from the home’s gallery" if originals else "Faceless illustration from the gallery"
                        alt = PHOTO_DESCRIPTIONS.get(photo.name.split(" at ")[-1], fallback)
                        gallery.image(str(photo), width="stretch", alt=alt)


def donate():
    with st.container(key="donation", horizontal=True, gap="large"):
        with st.container(width=385):
            st.title("Support the children’s home")
            st.write("Daily care takes steady support, from meals and bedding to school supplies and health checks.")
        with st.container(width=430, border=True):
            st.subheader("Online giving")
            frequency = st.radio("Giving frequency", ["One time", "Monthly"], horizontal=True)
            st.session_state.setdefault("donation_amount", 1000)
            with st.container(horizontal=True):
                for amount in (500, 1000, 2500, 5000):
                    st.button(
                        f"KES {amount:,}",
                        on_click=st.session_state.update,
                        kwargs={"donation_amount": amount},
                    )
            amount = st.number_input(
                "Donation amount (KES)", min_value=1, step=1, key="donation_amount",
                help="Enter a whole amount of at least KES 1, or choose a suggested amount.",
            )
            if amount is None:
                st.warning("Enter a whole amount of at least KES 1.")
            else:
                st.markdown(f"**Donation preview** · KES {amount:,} · {frequency}")
            st.caption("Online giving is coming soon. The amount shown is a preview.")
            st.button("Donate · Coming soon", type="primary", width="stretch", disabled=True)


giving = st.Page(donate, title="Ways to give", url_path="donate")
details = {slug: info_page(slug) for slug in INFO_PAGES}
page = st.navigation({
    "": [st.Page(home, title="Home", default=True), giving],
    "About the home": [details[slug] for slug in ("about", "board", "founders", "partners", "tour", "impact")],
    "Get involved": [details[slug] for slug in ("volunteer", "contact", "safeguarding")],
})
page.run()

st.divider()
st.caption("Pastor Cosmus Muema · 2020")
