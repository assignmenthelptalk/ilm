"""
generate_headers_photo.py — ILM Assignment Help new-page header images
Produces 1200x400 WebP headers using individually selected cells from the
ILM input photo grid (4 cols x 3 rows).  Each page gets one cell chosen
for relevance to the page topic.

Grid cell reference (row, col) — 0-indexed:
  r0c0  ILM building exterior
  r0c1  Large formal conference/presentation  → Level 5
  r0c2  Group meeting, "Unlocking Potential"  → Hub
  r0c3  ILM Scotland networking evening
  r1c0  Graduate holding FELLOW certificate
  r1c1  ILM outdoor team activity             → Level 3
  r1c2  ILM Apprenticeship presentation
  r1c3  Professional man on laptop
  r2c0  Professional man on laptop (wide)
  r2c1  Woman working on laptop at home desk
  r2c2  Library study, ILM book               → Coaching & Mentoring
  r2c3  Leadership Award ceremony             → Level 7

Brand: deep forest green #14532D + gold #EAB308
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os

INPUT_PHOTO = r"C:\Users\jobmu\agentic-workflow\semantic-seo-workflow\client_data\New-sites\ilm-assignment-help\input image\Gemini_Generated_Image_rog8iwrog8iwrog8.png"

# Grid layout of the input collage
GRID_COLS = 4
GRID_ROWS = 3

CLIENT = {
    "brand":      (20,  83,  45),
    "accent":     (234, 179,   8),
    "panel":      (10,  40,  20),
    "logo_line1": "ILM",
    "logo_line2": "Assignment Help",
    "output_dir": r"C:\Users\jobmu\my-second-projects\ilm-assignment-help\public",
}

# cell_row / cell_col select which grid cell to use as the photo.
# crop_y_frac (0.0–1.0) shifts the vertical crop within the cell:
#   0.0 = top-aligned, 0.5 = centred, 1.0 = bottom-aligned.
PAGES = [
    {
        "slug":       "header_ilm-assignment-help",
        "title":      "ILM\nASSIGNMENT\nHELP",
        "cell_row":   0,
        "cell_col":   2,   # group meeting with "Unlocking Potential" banner
        "crop_y_frac": 0.3,
    },
    {
        "slug":       "header_ilm-level-3-assignment-help",
        "title":      "ILM LEVEL 3\nASSIGNMENT\nHELP",
        "cell_row":   1,
        "cell_col":   1,   # ILM branded outdoor team activity — team leaders
        "crop_y_frac": 0.4,
    },
    {
        "slug":       "header_ilm-level-5-assignment-help",
        "title":      "ILM LEVEL 5\nASSIGNMENT\nHELP",
        "cell_row":   0,
        "cell_col":   1,   # large formal conference / presentation room
        "crop_y_frac": 0.3,
    },
    {
        "slug":       "header_ilm-level-7-assignment-help",
        "title":      "ILM LEVEL 7\nASSIGNMENT\nHELP",
        "cell_row":   2,
        "cell_col":   3,   # ILM Leadership Award ceremony — senior leader on stage
        "crop_y_frac": 0.2,
    },
    {
        "slug":       "header_ilm-coaching-mentoring-assignment-help",
        "title":      "ILM COACHING\n& MENTORING\nASSIGNMENT HELP",
        "cell_row":   2,
        "cell_col":   2,   # library study scene with ILM book
        "crop_y_frac": 0.4,
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


def extract_cell(photo, grid_cols, grid_rows, cell_col, cell_row):
    """Return a single grid cell from the collage image."""
    pw, ph = photo.size
    cw = pw // grid_cols
    ch = ph // grid_rows
    x1 = cell_col * cw
    y1 = cell_row * ch
    return photo.crop((x1, y1, x1 + cw, y1 + ch))


def place_cell(canvas, cell, crop_y_frac, dest_x, dest_y, dest_w, dest_h):
    """
    Scale the cell to fill dest_w (panel width), then crop vertically.
    crop_y_frac controls which part of the cell is kept:
      0.0 = top, 0.5 = centre, 1.0 = bottom.
    """
    cw, ch = cell.size
    # Scale so the cell fills the destination width
    scale = dest_w / cw
    scaled_w = dest_w
    scaled_h = int(ch * scale)

    if scaled_h < dest_h:
        # Cell too short even at full width — scale by height instead
        scale = dest_h / ch
        scaled_w = int(cw * scale)
        scaled_h = dest_h

    section = cell.resize((scaled_w, scaled_h), Image.LANCZOS)

    # Vertical crop
    excess_h = scaled_h - dest_h
    y_off = int(excess_h * crop_y_frac)
    section = section.crop((0, y_off, dest_w, y_off + dest_h))

    section = ImageEnhance.Brightness(section).enhance(0.82)
    section = ImageEnhance.Contrast(section).enhance(1.08)

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

    # Extract the selected grid cell and place it in the right panel
    cell = extract_cell(photo, GRID_COLS, GRID_ROWS,
                        page["cell_col"], page["cell_row"])
    photo_x = inner_x + PANEL_W
    photo_w = inner_w - PANEL_W
    photo_h = inner_h
    place_cell(canvas, cell, page.get("crop_y_frac", 0.3),
               photo_x, inner_y, photo_w, photo_h)

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
    print("Loading input collage...")
    photo = Image.open(INPUT_PHOTO).convert("RGBA")
    cw, ch = photo.size[0] // GRID_COLS, photo.size[1] // GRID_ROWS
    print(f"  Collage: {photo.size}  |  Cell size: {cw}x{ch}")

    print(f"\nGenerating {len(PAGES)} header images...\n")
    for page in PAGES:
        print(f"  {page['slug']}  (cell r{page['cell_row']}c{page['cell_col']})")
        generate(photo, page, CLIENT)
    print(f"\nDone -> {CLIENT['output_dir']}")
