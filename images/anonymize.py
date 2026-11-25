"""Make illustrations using one averaged color per private source image."""

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "images"
OUTPUT = ROOT / "assets"
EXTENSIONS = {".jpeg", ".jpg", ".png", ".webp"}


def make_illustration(source: Path, destination: Path) -> None:
    with Image.open(source) as original:
        color = original.convert("RGB").resize((1, 1), Image.Resampling.BOX).getpixel((0, 0))

    artwork = Image.new("RGB", (800, 520), "#F5EBD6")
    draw = ImageDraw.Draw(artwork)
    draw.ellipse((545, 48, 675, 178), fill="#EDAA63")
    draw.polygon([(0, 340), (245, 145), (540, 360), (800, 250), (800, 520), (0, 520)], fill=color)
    draw.polygon([(0, 445), (280, 330), (570, 465), (800, 320), (800, 520), (0, 520)], fill="#26584C")
    artwork.save(destination)


if __name__ == "__main__":
    OUTPUT.mkdir(exist_ok=True)
    sources = sorted(path for path in SOURCE.iterdir() if path.is_file() and path.suffix.lower() in EXTENSIONS)
    for index, source in enumerate(sources, start=1):
        make_illustration(source, OUTPUT / f"gallery-{index:02}.png")
