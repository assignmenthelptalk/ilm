"""
generate_favicon.py — ILM Assignment Help favicon generator
Produces:
  public/favicon.ico  — multi-size ICO (16, 32, 48)
  public/favicon.svg  — vector version for modern browsers
Brand: deep green #14532D + gold #EAB308
"""

from PIL import Image, ImageDraw, ImageFont
import struct, io, os

GREEN = (20,  83, 45)    # #14532D
GOLD  = (234, 179,  8)   # #EAB308
WHITE = (255, 255, 255)

OUT_DIR = r"C:\Users\jobmu\my-second-projects\ilm-assignment-help\public"


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


def make_frame(size):
    """Render a single favicon frame at the given pixel size."""
    s = size
    img  = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded green background
    radius = max(2, s // 6)
    draw.rounded_rectangle([(0, 0), (s - 1, s - 1)], radius=radius, fill=(*GREEN, 255))

    # Gold accent bar at bottom (1/8 height)
    bar_h = max(2, s // 8)
    draw.rounded_rectangle(
        [(0, s - bar_h), (s - 1, s - 1)],
        radius=radius,
        fill=(*GOLD, 255),
    )

    # Text
    if size >= 48:
        font = get_font(size // 3, bold=True)
        text = "ILM"
    elif size >= 32:
        font = get_font(size // 3 - 1, bold=True)
        text = "ILM"
    else:
        font = get_font(size // 2, bold=True)
        text = "I"

    # Centre text
    bbox = draw.textbbox((0, 0), text, font=font)
    tw   = bbox[2] - bbox[0]
    th   = bbox[3] - bbox[1]
    tx   = (s - tw) // 2 - bbox[0]
    ty   = (s - th) // 2 - bbox[1] - bar_h // 2

    draw.text((tx, ty), text, fill=WHITE, font=font)

    return img


def build_ico(sizes=(16, 32, 48)):
    """Build a proper multi-size ICO file and return raw bytes."""
    frames = [make_frame(s) for s in sizes]
    images_data = []
    for img in frames:
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        images_data.append(buf.getvalue())

    # ICO header
    n = len(sizes)
    header  = struct.pack("<HHH", 0, 1, n)   # reserved, type=1(ICO), count
    dir_offset = 6 + n * 16
    directory = b""
    image_offset = dir_offset
    for i, (s, data) in enumerate(zip(sizes, images_data)):
        w = s if s < 256 else 0
        h = s if s < 256 else 0
        directory += struct.pack(
            "<BBBBHHII",
            w, h,       # width, height (0 = 256)
            0, 0,       # color count, reserved
            1, 32,      # planes, bit count
            len(data),  # size of image data
            image_offset,
        )
        image_offset += len(data)

    ico = header + directory + b"".join(images_data)
    return ico


def build_svg():
    """Return SVG markup for the favicon."""
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="5" fill="#14532D"/>
  <rect x="0" y="26" width="32" height="6" rx="5" fill="#EAB308"/>
  <text x="16" y="22" font-family="Arial,sans-serif" font-size="14"
        font-weight="bold" text-anchor="middle" fill="#FFFFFF">ILM</text>
</svg>'''


def main():
    # ICO
    ico_bytes = build_ico(sizes=(16, 32, 48))
    ico_path  = os.path.join(OUT_DIR, "favicon.ico")
    with open(ico_path, "wb") as f:
        f.write(ico_bytes)
    print(f"  OK  {ico_path}  ({len(ico_bytes)} bytes, 3 sizes: 16/32/48)")

    # SVG
    svg_path = os.path.join(OUT_DIR, "favicon.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(build_svg())
    print(f"  OK  {svg_path}")


if __name__ == "__main__":
    print("Generating ILM favicons...\n")
    main()
    print("\nDone.")
