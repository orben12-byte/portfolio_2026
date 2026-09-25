# -*- coding: utf-8 -*-
"""בונה את סט השקופיות של Noviopus מתוך תיק העבודות.

מסכי הדסקטופ (1440x1000) עוברים דחיסה ישירה. מסכי המובייל (360x740) קטנים מדי
כדי למלא את רוחב הגלריה, אז הם מורכבים לשורה אחת על רקע כהה.

  python build-slides-noviopus.py
"""
from PIL import Image
import pathlib, os, sys

sys.stdout.reconfigure(encoding="utf-8")

SRC = pathlib.Path(r"C:\Users\orben\OneDrive\Desktop\work\תיק עבודות\apps\Noviopus")
DEST = pathlib.Path(__file__).parent / "slides-noviopus"
MAX_W, QUALITY, BG = 1400, 82, (17, 17, 17)

# רק המסכים שהעמוד באמת מציג במלואם. Work/Private/Starred מוצגים כחיתוכי
# עמודה (CATEGORY_CROPS) ולא כמסך מלא, אז אין טעם לייצר להם שקופית.
DESKTOP = [
    "Desktop_New_Messages.png",
    "Desktop_Compose_Messages.png",
    "Desktop_New_Messages_Time period filter.png",
]
MOBILE_ROWS = [
    ["Mobile_New_Messages.png", "Mobile_Messages_Time period filter_popup.png", "Chat op 4.png"],
    ["dropdown menue - overlay.png", "dropdown Messages menue - overlay.png"],
]


CATEGORY_CROPS = [
    ("Desktop_Work_Messages.png", "cat-work.jpg"),
    ("Desktop_Private_Messages.png", "cat-private.jpg"),
    ("Desktop_Starred_Messages.png", "cat-starred.jpg"),
]
CROP_BOX = (0, 0, 520, 1000)   # עמודות הניווט + הרשימה — האזור היחיד שמשתנה בין הקטגוריות


def categories():
    """חותך את עמודות הניווט לשורת ההשוואה בעמוד הפרויקט."""
    from PIL import Image
    print("Noviopus — category crops:")
    for name, out in CATEGORY_CROPS:
        src = SRC / "Chat - Desktop" / name
        if not src.exists():
            print(f"  ! missing: {name}")
            continue
        im = Image.open(src).convert("RGB").crop(CROP_BOX)
        DEST.mkdir(parents=True, exist_ok=True)
        im.save(DEST / out, "JPEG", quality=86, optimize=True)
        print(f"  {out}  {os.path.getsize(DEST / out)//1024}KB")


def save(img, dest):
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGB")
    if img.width > MAX_W:
        img = img.resize((MAX_W, round(img.height * MAX_W / img.width)), Image.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "JPEG", quality=QUALITY, optimize=True)
    print(f"  {dest.name}  {os.path.getsize(dest)//1024}KB")


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
    n = 0
    print("Noviopus — desktop:")
    for name in DESKTOP:
        src = SRC / "Chat - Desktop" / name
        if not src.exists():
            print(f"  ! missing: {name}")
            continue
        n += 1
        save(Image.open(src), DEST / f"{n:02d}.jpg")

    print("Noviopus — mobile rows:")
    for names in MOBILE_ROWS:
        paths = [SRC / "New folder" / x for x in names]
        missing = [p.name for p in paths if not p.exists()]
        if missing:
            print(f"  ! missing: {missing}")
            continue
        n += 1
        save(row(paths), DEST / f"{n:02d}.jpg")

    print(f"\n{n} slides -> {DEST}")


if __name__ == "__main__":
    main()
