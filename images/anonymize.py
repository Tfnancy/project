"""Make illustrations using one averaged color per private source image."""

from argparse import ArgumentParser
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "images"
OUTPUT = ROOT / "assets"
EXTENSIONS = {".jpeg", ".jpg", ".png", ".webp"}
PEOPLE_OUTPUT = SOURCE / "anonymized"
FIGURE_LAYOUTS = [
    (300, 215, 250),
    (215, 290),
    (275, 220, 220, 265),
    (230, 290, 205),
    (260, 205, 245, 290),
    (290, 225),
]


def average_color(source: Path) -> tuple[int, int, int]:
    with Image.open(source) as original:
        return original.convert("RGB").resize((1, 1), Image.Resampling.BOX).getpixel((0, 0))


def make_illustration(source: Path, destination: Path) -> None:
    color = average_color(source)
    artwork = Image.new("RGB", (800, 520), "#F5EBD6")
    draw = ImageDraw.Draw(artwork)
    draw.ellipse((545, 48, 675, 178), fill="#EDAA63")
    draw.polygon([(0, 340), (245, 145), (540, 360), (800, 250), (800, 520), (0, 520)], fill=color)
    draw.polygon([(0, 445), (280, 330), (570, 465), (800, 320), (800, 520), (0, 520)], fill="#26584C")
    artwork.save(destination)


def make_people_illustration(source: Path, destination: Path, heights: tuple[int, ...]) -> None:
    """Draw stock figure shapes using only a muted accent from the photo."""
    artwork = Image.new("RGB", (1000, 650), "#f8eedb")
    draw = ImageDraw.Draw(artwork)
    accent = tuple((channel + paper) // 2 for channel, paper in zip(average_color(source), (232, 217, 184)))
    draw.ellipse((640, 65, 815, 240), fill="#eaae67")
    draw.polygon([(0, 365), (270, 235), (610, 375), (1000, 275), (1000, 650), (0, 650)], fill=accent)
    draw.rectangle((0, 490, 1000, 650), fill="#dce5d3")

    palette = ("#255449", "#a34e3e", "#435d76", "#87602e")
    spacing = 160
    start = 500 - spacing * (len(heights) - 1) // 2
    for index, height in enumerate(heights):
        x = start + spacing * index
        ground = 520
        top = ground - height
        radius = height // 7
        shoulder = top + 2 * radius + 12
        half_width = height // 5
        fill = palette[index]
        draw.ellipse((x - half_width - 10, ground - 10, x + half_width + 10, ground + 14), fill="#b8cbb7")
        draw.ellipse((x - radius, top, x + radius, top + 2 * radius), fill=fill)
        draw.rounded_rectangle((x - half_width, shoulder, x + half_width, ground - height // 4), radius=30, fill=fill)
        for leg in (-1, 1):
            center = x + leg * (half_width // 2)
            draw.rounded_rectangle((center - 13, ground - height // 3, center + 13, ground), radius=13, fill=fill)

    artwork.save(destination)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--people", action="store_true", help="Remake the WhatsApp photos as generic faceless figures.")
    args = parser.parse_args()
    if args.people:
        PEOPLE_OUTPUT.mkdir(exist_ok=True)
        sources = sorted(path for path in SOURCE.glob("WhatsApp Image *") if path.is_file() and path.suffix.lower() in EXTENSIONS)
        for index, source in enumerate(sources):
            heights = FIGURE_LAYOUTS[index % len(FIGURE_LAYOUTS)]
            make_people_illustration(source, PEOPLE_OUTPUT / f"people-{index + 1:02}.png", heights)
    else:
        OUTPUT.mkdir(exist_ok=True)
        sources = sorted(path for path in SOURCE.iterdir() if path.is_file() and path.suffix.lower() in EXTENSIONS)
        for index, source in enumerate(sources, start=1):
            make_illustration(source, OUTPUT / f"gallery-{index:02}.png")
