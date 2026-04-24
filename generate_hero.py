"""
generate_hero.py — ILM Assignment Help homepage hero image
Produces a 660×500 WebP hero image from a professional photo
with a UK flag badge and ILM brand framing.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os

INPUT_PHOTO = r"C:\Users\jobmu\agentic-workflow\semantic-seo-workflow\client_data\New-sites\btec-assignment-help\images\Screenshot_40.png"
OUTPUT      = r"C:\Users\jobmu\my-second-projects\ilm-assignment-help\public\hero-ilm.webp"

# ILM brand
GREEN       = (20,  83,  45)    # #14532D
GREEN_DARK  = (10,  40,  20)    # #0A2814
GOLD        = (234, 179,   8)   # #EAB308
WHITE       = (255, 255, 255)

W, H = 660, 500


# ── Helpers ──────────────────────────────────────────────────────────────────

def get_font(size, bold=True):
    candidates = (
        [r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\calibrib.ttf",
         r"C:\Windows\Fonts\verdanab.ttf"]
        if bold else
        [r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\calibri.ttf"]
    )
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()


def fit_crop(img, w, h):
    iw, ih = img.size
    scale  = max(w / iw, h / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img    = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - w) // 2
    y = max(0, (nh - h) // 4)      # crop slightly from top to favour faces
    y = min(y, nh - h)
    return img.crop((x, y, x + w, y + h))


def draw_union_jack(draw_target, canvas, x, y, fw, fh):
    """Draw a Union Jack flag at position (x,y) with size fw×fh."""
    flag = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
    fd   = ImageDraw.Draw(flag)

    BLUE  = (1,   33, 105, 255)   # #012169
    RED   = (200,  16,  46, 255)  # #C8102E
    W_    = (255, 255, 255, 255)

    # Blue field
    fd.rectangle([(0, 0), (fw, fh)], fill=BLUE)

    # --- St Andrew's cross (white diagonals, thick) ---
    diag_w = max(3, fh // 6)
    fd.line([(0, 0), (fw, fh)], fill=W_, width=diag_w)
    fd.line([(fw, 0), (0, fh)], fill=W_, width=diag_w)

    # --- St Patrick's cross (red diagonals, offset, thin) ---
    red_w = max(2, fh // 12)
    # Top-left to bottom-right diagonal: red on the lower-left side
    off = diag_w // 3
    for dx, dy in [(-off, off), (off, -off)]:
        fd.line([(0 + dx, 0 + dy), (fw + dx, fh + dy)], fill=RED, width=red_w)
    # Top-right to bottom-left diagonal: red on the upper-left side
    for dx, dy in [(-off, -off), (off, off)]:
        fd.line([(fw + dx, 0 + dy), (0 + dx, fh + dy)], fill=RED, width=red_w)

    # --- St George's cross (white + red, centred) ---
    cross_w = max(5, fh // 4)
    cx, cy  = fw // 2, fh // 2
    fd.rectangle([(0, cy - cross_w // 2), (fw, cy + cross_w // 2)], fill=W_)
    fd.rectangle([(cx - cross_w // 2, 0), (cx + cross_w // 2, fh)], fill=W_)

    red_cross_w = max(3, fh // 8)
    fd.rectangle([(0, cy - red_cross_w // 2), (fw, cy + red_cross_w // 2)], fill=RED)
    fd.rectangle([(cx - red_cross_w // 2, 0), (cx + red_cross_w // 2, fh)], fill=RED)

    # White border around flag
    fd.rectangle([(0, 0), (fw - 1, fh - 1)], outline=W_, width=2)

    canvas.paste(flag, (x, y), flag)


# ── Main ─────────────────────────────────────────────────────────────────────

def generate():
    # 1 — Load and crop photo
    photo = Image.open(INPUT_PHOTO).convert("RGB")
    photo = fit_crop(photo, W, H)

    # 2 — Slightly warm/brighten the photo for a professional look
    from PIL import ImageEnhance
    photo = ImageEnhance.Brightness(photo).enhance(1.08)
    photo = ImageEnhance.Contrast(photo).enhance(1.05)

    canvas = photo.copy()
    draw   = ImageDraw.Draw(canvas, "RGBA")

    # 3 — Subtle dark vignette on bottom-left (so any caption stays legible)
    for i in range(100):
        alpha = int(100 * (1 - i / 100) ** 2)
        draw.rectangle([(0, H - 100 + i), (W, H - 100 + i + 1)],
                        fill=(0, 0, 0, alpha))

    # 4 — ILM green accent bar at bottom
    bar_h = 8
    draw.rectangle([(0, H - bar_h), (W, H)], fill=(*GREEN, 255))

    # 5 — Gold accent stripe at top
    draw.rectangle([(0, 0), (W, 5)], fill=(*GOLD, 200))

    draw = ImageDraw.Draw(canvas)  # switch to RGB for text

    # 6 — "UK BASED EXPERTS" label strip above the flag
    badge_x = W - 130
    badge_y = H - 72

    label_font  = get_font(11, bold=True)
    label_text  = "UK BASED EXPERTS"
    label_bg_x1 = badge_x - 6
    label_bg_y1 = badge_y - 26
    label_bg_x2 = W - 8
    label_bg_y2 = badge_y - 4
    draw.rounded_rectangle(
        [(label_bg_x1, label_bg_y1), (label_bg_x2, label_bg_y2)],
        radius=4,
        fill=GREEN,
    )
    draw.text(
        (label_bg_x1 + 6, label_bg_y1 + 4),
        label_text,
        fill=WHITE,
        font=label_font,
    )

    # 7 — UK flag badge (bottom-right)
    fw, fh = 108, 66
    fx = W - fw - 10
    fy = H - fh - bar_h - 10

    # Shadow behind flag
    shadow_draw = ImageDraw.Draw(canvas, "RGBA")
    shadow_draw.rounded_rectangle(
        [(fx + 3, fy + 3), (fx + fw + 3, fy + fh + 3)],
        radius=4,
        fill=(0, 0, 0, 60),
    )
    draw = ImageDraw.Draw(canvas)

    draw_union_jack(draw, canvas, fx, fy, fw, fh)

    # 8 — Save
    canvas.save(OUTPUT, "WEBP", quality=92)
    print(f"  OK  {OUTPUT}")


if __name__ == "__main__":
    print("Generating ILM hero image...\n")
    generate()
    print("\nDone.")
