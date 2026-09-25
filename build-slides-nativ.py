# -*- coding: utf-8 -*-
"""בונה את סט התמונות של נתיב מתוך תיק העבודות.

  python build-slides-nativ.py
"""
from PIL import Image
import pathlib, os, sys

sys.stdout.reconfigure(encoding="utf-8")

SRC = pathlib.Path(r"C:\Users\orben\OneDrive\Desktop\work\תיק עבודות\apps\Nativ")
DEST = pathlib.Path(__file__).parent / "slides-nativ"
MAX_W, QUALITY, BG = 1500, 82, (17, 17, 17)

# מסכים מלאים
FULL = [
    ("Desktop/דיווח שעות/flow 1_main_pop_up.jpg", "01-report-start.jpg"),
    ("Desktop/טבלה דיווח שעות/hours report table open- edit- error.jpg", "02-table-edit.jpg"),
    ("Desktop/שיבוץ לבית דין/Scheduling_BD_MAIN.png", "03-court.jpg"),
    ("Desktop/שיבוץ משפחות מלוות/Host Families_ search- map click.jpg", "04-families.jpg"),
]

# שלבי הפלואו — רק חלון המודאל, כי רק הוא משתנה בין השלבים
MODAL_BOX = (58, 55, 578, 1130)
MODAL_STEPS = [
    ("Desktop/דיווח שעות/flow 2_main_pop_up-4.jpg", "step-1.jpg"),
    ("Desktop/דיווח שעות/flow 2_main_pop_up-6.jpg", "step-2.jpg"),
    ("Desktop/דיווח שעות/flow 2_main_pop_up-8.jpg", "step-3.jpg"),
]

MOBILE_ROW = ["Mobile/main_mobile.jpg", "Mobile/class_mobile.jpg", "Mobile/main side menu_mobile.jpg"]


def save(img, name, max_w=MAX_W):
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGB")
    if img.width > max_w:
        img = img.resize((max_w, round(img.height * max_w / img.width)), Image.LANCZOS)
    DEST.mkdir(parents=True, exist_ok=True)
    dest = DEST / name
    img.save(dest, "JPEG", quality=QUALITY, optimize=True)
    print(f"  {name}  {os.path.getsize(dest)//1024}KB")


def row(paths, gap=48, pad=64):
    """מרכיב מסכי מובייל לשורה אחת על רקע כהה, בגובה אחיד."""
    imgs = [Image.open(p).convert("RGB") for p in paths]
    h = max(i.height for i in imgs)
    imgs = [i if i.height == h else i.resize((round(i.width * h / i.height), h), Image.LANCZOS)
            for i in imgs]
    w = sum(i.width for i in imgs) + gap * (len(imgs) - 1)
    canvas = Image.new("RGB", (w + pad * 2, h + pad * 2), BG)
    x = pad
    for i in imgs:
        canvas.paste(i, (x, pad))
        x += i.width + gap
    return canvas


def main():
    print("Nativ — full screens:")
    for rel, name in FULL:
        p = SRC / rel
        if not p.exists():
            print(f"  ! missing: {rel}")
            continue
        save(Image.open(p), name)

    print("Nativ — flow steps (modal crop):")
    for rel, name in MODAL_STEPS:
        p = SRC / rel
        if not p.exists():
            print(f"  ! missing: {rel}")
            continue
        save(Image.open(p).convert("RGB").crop(MODAL_BOX), name, max_w=640)

    print("Nativ — mobile row:")
    paths = [SRC / x for x in MOBILE_ROW]
    missing = [p.name for p in paths if not p.exists()]
    if missing:
        print(f"  ! missing: {missing}")
    else:
        save(row(paths), "05-mobile.jpg")

    print(f"\n-> {DEST}")


if __name__ == "__main__":
    main()
