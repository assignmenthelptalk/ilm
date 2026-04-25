"""
generate_headers_photo.py — ILM Assignment Help new-page header images
Produces 1200x400 WebP headers using the ILM input photo collage as background.
Brand: deep forest green #14532D + gold #EAB308
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os

INPUT_PHOTO = r"C:\Users\jobmu\agentic-workflow\semantic-seo-workflow\client_data\New-sites\ilm-assignment-help\input image\Gemini_Generated_Image_rog8iwrog8iwrog8.png"

CLIENT = {
    "brand":      (20,  83,  45),
    "accent":     (234, 179,   8),
    "panel":      (10,  40,  20),
    "logo_line1": "ILM",
    "logo_line2": "Assignment Help",
    "output_dir": r"C:\Users\jobmu\my-second-projects\ilm-assignment-help\public",
}

# Five different horizontal crop offsets so each header shows a different
# section of the collage (image is 1408px wide; crop window is 768px wide)
PAGES = [
    {
        "slug":    "header_ilm-assignment-help",
        "title":   "ILM\nASSIGNMENT\nHELP",
        "crop_x":  0,
    },
    {
        "slug":    "header_ilm-level-3-assignment-help",
        "title":   "ILM LEVEL 3\nASSIGNMENT\nHELP",
        "crop_x":  160,
    },
    {
        "slug":    "header_ilm-level-5-assignment-help",
        "title":   "ILM LEVEL 5\nASSIGNMENT\nHELP",
        "crop_x":  320,
    },
    {
        "slug":    "header_ilm-level-7-assignment-help",
        "title":   "ILM LEVEL 7\nASSIGNMENT\nHELP",
        "crop_x":  480,
    },
    {
        "slug":    "header_ilm-coaching-mentoring-assignment-help",
        "title":   "ILM COACHING\n& MENTORING\nASSIGNMENT HELP",
        "crop_x":  640,
    },
]

W, H       = 1200, 400
BORDER     = 24
PANEL_W    = 450
TILE       = 24


def get_font(size, bold=True):
    candidates = (
        [r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\calibrib.ttf",
         r"C:\Windows\Fonts\verdanab.ttf", r"C:\Windows\Fonts\trebucbd.ttf"]
        if bold else
        [r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\calibri.ttf"]
    )
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()


def draw_diamond_tile(draw, cx, cy, radius, fill, dot):
    r = radius
    pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
    draw.polygon(pts, fill=fill)
    d = max(2, radius // 4)
    draw.ellipse([(cx - d, cy - d), (cx + d, cy + d)], fill=dot)


def draw_border(draw, brand, accent):
    draw.rectangle([(0, 0),        (W, BORDER)],      fill=brand)
    draw.rectangle([(0, H-BORDER), (W, H)],            fill=brand)
    draw.rectangle([(0, 0),        (BORDER, H)],       fill=brand)
    draw.rectangle([(W-BORDER, 0), (W, H)],            fill=brand)

    r    = TILE // 2 - 2
    dot  = (255, 255, 255)
    half = TILE // 2
    for x in range(half, W, TILE):
        draw_diamond_tile(draw, x, BORDER // 2,     r, accent, dot)
        draw_diamond_tile(draw, x, H - BORDER // 2, r, accent, dot)
    for y in range(BORDER + half, H - BORDER, TILE):
        draw_diamond_tile(draw, BORDER // 2,     y, r, accent, dot)
        draw_diamond_tile(draw, W - BORDER // 2, y, r, accent, dot)


def panel_gradient(draw, px, py, pw, ph):
    fade_w = 80
    for i in range(fade_w):
        alpha = int(255 * (1 - i / fade_w))
        x = px + pw - fade_w + i
        draw.rectangle([(x, py), (x + 1, py + ph)], fill=(10, 40, 20, alpha))


def place_photo(canvas, photo, crop_x, dest_x, dest_y, dest_w, dest_h):
    """Crop a dest_w:dest_h section from photo at crop_x, paste onto canvas."""
    pw, ph = photo.size
    # Window in the source image that matches the dest aspect ratio
    win_w = int(ph * dest_w / dest_h)
    win_w = min(win_w, pw)
    crop_x = min(crop_x, pw - win_w)
    section = photo.crop((crop_x, 0, crop_x + win_w, ph))
    section = section.resize((dest_w, dest_h), Image.LANCZOS)
    section = ImageEnhance.Brightness(section).enhance(0.82)
    section = ImageEnhance.Contrast(section).enhance(1.08)
    # Convert RGBA to RGB so paste works cleanly
    if section.mode == "RGBA":
        bg = Image.new("RGB", section.size, (14, 58, 30))
        bg.paste(section, mask=section.split()[3])
        section = bg
    canvas.paste(section, (dest_x, dest_y))


def generate(photo, page, client):
    brand  = client["brand"]
    accent = client["accent"]
    panel  = client["panel"]

    inner_x = BORDER
    inner_y = BORDER
    inner_w = W - 2 * BORDER
    inner_h = H - 2 * BORDER

    canvas = Image.new("RGB", (W, H), brand)

    # Photo fills the right panel area
    photo_x = inner_x + PANEL_W
    photo_w = inner_w - PANEL_W
    photo_h = inner_h
    place_photo(canvas, photo, page["crop_x"], photo_x, inner_y, photo_w, photo_h)

    # Dark text panel (left side)
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle(
        [(inner_x, inner_y), (inner_x + PANEL_W, inner_y + inner_h)],
        fill=(*panel, 255),
    )
    panel_gradient(draw, inner_x, inner_y, PANEL_W, inner_h)

    draw = ImageDraw.Draw(canvas)

    # Gold accent stripe at top of panel
    draw.rectangle(
        [(inner_x, inner_y), (inner_x + PANEL_W, inner_y + 6)],
        fill=accent,
    )

    # Title text
    title_font = get_font(38, bold=True)
    lines  = page["title"].split("\n")
    line_h = 50
    tx = inner_x + 32
    ty = inner_y + 28

    for line in lines:
        draw.text((tx + 2, ty + 2), line, fill=(0, 0, 0),      font=title_font)
        draw.text((tx,     ty),     line, fill=(255, 255, 255), font=title_font)
        ty += line_h

    rule_y = ty + 10
    draw.rectangle([(tx, rule_y), (tx + 56, rule_y + 4)], fill=accent)

    # Logo block
    logo1_font = get_font(22, bold=True)
    logo2_font = get_font(13, bold=False)
    logo_y     = inner_y + inner_h - 64
    draw.text((tx, logo_y),      client["logo_line1"], fill=accent,          font=logo1_font)
    draw.text((tx, logo_y + 28), client["logo_line2"], fill=(180, 220, 195), font=logo2_font)

    # Border drawn last
    draw_border(draw, brand, accent)

    out_path = os.path.join(client["output_dir"], page["slug"] + ".webp")
    canvas.save(out_path, "WEBP", quality=92)
    print(f"  OK  {page['slug']}.webp")


if __name__ == "__main__":
    print("Loading input photo...")
    photo = Image.open(INPUT_PHOTO).convert("RGBA")
    print(f"  Size: {photo.size}")

    print(f"\nGenerating {len(PAGES)} header images...\n")
    for page in PAGES:
        generate(photo, page, CLIENT)
    print(f"\nDone -> {CLIENT['output_dir']}")
