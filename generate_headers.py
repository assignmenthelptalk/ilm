"""
generate_headers.py — ILM Assignment Help Phase 2 header images
Produces 1200×400 WebP headers for Tier 2 pages.
Brand: deep forest green #14532D + gold #EAB308
No input photos — uses geometric leadership/strategy motif on right panel.
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

CLIENT = {
    "brand":       (20,  83,  45),    # Deep green  #14532D
    "accent":      (234, 179,   8),   # Gold        #EAB308
    "panel":       (10,  40,  20),    # Darker green for text panel
    "logo_line1":  "ILM",
    "logo_line2":  "Assignment Help",
    "output_dir":  r"C:\Users\jobmu\my-second-projects\ilm-assignment-help\public",
}

PAGES = [
    {
        "slug":  "header_ilm-reflective-account-writing-help",
        "title": "ILM REFLECTIVE\nACCOUNT WRITING\nHELP",
    },
    {
        "slug":  "header_ilm-work-based-evidence-guide",
        "title": "ILM WORK-BASED\nEVIDENCE\nGUIDE",
    },
    {
        "slug":  "header_ilm-level-5-leadership-unit-assignment-help",
        "title": "ILM LEVEL 5\nLEADERSHIP UNIT\nASSIGNMENT HELP",
    },
    {
        "slug":  "header_ilm-level-5-management-unit-assignment-help",
        "title": "ILM LEVEL 5\nMANAGEMENT UNIT\nASSIGNMENT HELP",
    },
    {
        "slug":  "header_ilm-level-7-strategic-leadership-assignment-help",
        "title": "ILM LEVEL 7\nSTRATEGIC LEADERSHIP\nASSIGNMENT HELP",
    },
    {
        "slug":  "header_ilm-level-3-team-leader-assignment-help",
        "title": "ILM LEVEL 3\nTEAM LEADER\nASSIGNMENT HELP",
    },
    {
        "slug":  "header_ilm-assignment-referral-and-resubmission-guide",
        "title": "ILM ASSIGNMENT\nREFERRAL &\nRESUBMISSION GUIDE",
    },
    {
        "slug":  "header_leadership-styles-and-theories-for-ilm-assignments",
        "title": "LEADERSHIP STYLES\n& THEORIES FOR\nILM ASSIGNMENTS",
    },
    {
        "slug":  "header_ilm-level-4-assignment-help",
        "title": "ILM LEVEL 4\nASSIGNMENT\nHELP",
    },
    {
        "slug":  "header_ilm-assignment-harvard-referencing-guide",
        "title": "ILM ASSIGNMENT\nHARVARD REFERENCING\nGUIDE",
    },
]

W, H        = 1200, 400
BORDER      = 24
PANEL_W     = 450
TILE        = 24


def get_font(size, bold=True):
    candidates = (
        [r"C:\Windows\Fonts\arialbd.ttf",   r"C:\Windows\Fonts\calibrib.ttf",
         r"C:\Windows\Fonts\verdanab.ttf",  r"C:\Windows\Fonts\trebucbd.ttf"]
        if bold else
        [r"C:\Windows\Fonts\arial.ttf",     r"C:\Windows\Fonts\calibri.ttf",
         r"C:\Windows\Fonts\verdana.ttf"]
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
    draw.rectangle([(0, 0),        (W, BORDER)],       fill=brand)
    draw.rectangle([(0, H-BORDER), (W, H)],             fill=brand)
    draw.rectangle([(0, 0),        (BORDER, H)],        fill=brand)
    draw.rectangle([(W-BORDER, 0), (W, H)],             fill=brand)

    r    = TILE // 2 - 2
    dot  = (255, 255, 255)
    half = TILE // 2
    for x in range(half, W, TILE):
        draw_diamond_tile(draw, x, BORDER // 2,     r, accent, dot)
        draw_diamond_tile(draw, x, H - BORDER // 2, r, accent, dot)
    for y in range(BORDER + half, H - BORDER, TILE):
        draw_diamond_tile(draw, BORDER // 2,     y, r, accent, dot)
        draw_diamond_tile(draw, W - BORDER // 2, y, r, accent, dot)


def draw_right_panel(canvas, inner_x, inner_y, inner_w, inner_h, brand, accent, panel_w):
    """Draw geometric leadership/strategy motif on the right portion."""
    right_x = inner_x + panel_w
    right_w  = inner_w - panel_w
    right_h  = inner_h

    # Right panel background — slightly darker green
    bg_layer = Image.new("RGB", (right_w, right_h), (14, 58, 30))
    canvas.paste(bg_layer, (right_x, inner_y))

    draw = ImageDraw.Draw(canvas, "RGBA")

    # Subtle diagonal line grid (very faint)
    step = 28
    for i in range(-right_h, right_w + right_h, step):
        x1 = right_x + i
        y1 = inner_y
        x2 = right_x + i + right_h
        y2 = inner_y + right_h
        draw.line([(x1, y1), (x2, y2)], fill=(234, 179, 8, 20), width=1)

    # Concentric rings — centred in the right panel, leadership "target" motif
    cx = right_x + right_w // 2
    cy = inner_y + right_h // 2
    for r in range(30, 320, 44):
        draw.ellipse(
            [(cx - r, cy - r), (cx + r, cy + r)],
            outline=(234, 179, 8, 45),
            width=2,
        )

    # Four radiating spokes (cross + diagonal)
    spoke_len = 260
    for angle_deg in [0, 45, 90, 135]:
        angle = math.radians(angle_deg)
        x1 = cx + int(math.cos(angle) * 30)
        y1 = cy + int(math.sin(angle) * 30)
        x2 = cx + int(math.cos(angle) * spoke_len)
        y2 = cy + int(math.sin(angle) * spoke_len)
        draw.line([(x1, y1), (x2, y2)], fill=(234, 179, 8, 35), width=1)
        x1 = cx - int(math.cos(angle) * 30)
        y1 = cy - int(math.sin(angle) * 30)
        x2 = cx - int(math.cos(angle) * spoke_len)
        y2 = cy - int(math.sin(angle) * spoke_len)
        draw.line([(x1, y1), (x2, y2)], fill=(234, 179, 8, 35), width=1)

    # Small bright circle at centre
    draw.ellipse(
        [(cx - 10, cy - 10), (cx + 10, cy + 10)],
        fill=(234, 179, 8, 120),
    )


def panel_gradient(draw, px, py, pw, ph):
    fade_w = 70
    for i in range(fade_w):
        alpha = int(255 * (1 - i / fade_w))
        x = px + pw - fade_w + i
        draw.rectangle([(x, py), (x + 1, py + ph)], fill=(10, 40, 20, alpha))


def generate(page, client):
    brand  = client["brand"]
    accent = client["accent"]
    panel  = client["panel"]

    inner_x = BORDER
    inner_y = BORDER
    inner_w = W - 2 * BORDER
    inner_h = H - 2 * BORDER

    canvas = Image.new("RGB", (W, H), brand)

    # Right decorative panel (no photo)
    draw_right_panel(canvas, inner_x, inner_y, inner_w, inner_h, brand, accent, PANEL_W)

    # Dark text panel
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle(
        [(inner_x, inner_y), (inner_x + PANEL_W, inner_y + inner_h)],
        fill=(*panel, 255),
    )
    panel_gradient(draw, inner_x, inner_y, PANEL_W, inner_h)

    draw = ImageDraw.Draw(canvas)

    # Accent stripe at top of panel
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
        draw.text((tx + 2, ty + 2), line, fill=(0, 0, 0),           font=title_font)
        draw.text((tx,     ty),     line, fill=(255, 255, 255),      font=title_font)
        ty += line_h

    rule_y = ty + 10
    draw.rectangle([(tx, rule_y), (tx + 56, rule_y + 4)], fill=accent)

    # Logo block
    logo1_font = get_font(22, bold=True)
    logo2_font = get_font(13, bold=False)
    logo_y     = inner_y + inner_h - 64

    draw.text((tx, logo_y),      client["logo_line1"], fill=accent,          font=logo1_font)
    draw.text((tx, logo_y + 28), client["logo_line2"], fill=(180, 220, 195), font=logo2_font)

    # Border (drawn last)
    draw_border(draw, brand, accent)

    os.makedirs(client["output_dir"], exist_ok=True)
    out_path = os.path.join(client["output_dir"], page["slug"] + ".webp")
    canvas.save(out_path, "WEBP", quality=92)
    print(f"  OK  {page['slug']}.webp")


if __name__ == "__main__":
    print(f"Generating {len(PAGES)} ILM header images...\n")
    for page in PAGES:
        generate(page, CLIENT)
    print(f"\nDone -> {CLIENT['output_dir']}")
