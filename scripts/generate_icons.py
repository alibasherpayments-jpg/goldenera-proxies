import math
from PIL import Image, ImageDraw, ImageFont

def generate_png_and_ico():
    size = 512
    scale = 2
    actual_size = size * scale  # 1024 for supersampling

    img = Image.new("RGBA", (actual_size, actual_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outer squircle
    pad = 36 * scale
    rad = 110 * scale

    # Dark cyber background
    draw.rounded_rectangle(
        [pad, pad, actual_size - pad, actual_size - pad],
        radius=rad,
        fill=(12, 14, 20, 255),
        outline=(245, 158, 11, 255),
        width=14 * scale,
    )

    # Inner subtle gold border
    draw.rounded_rectangle(
        [pad + 18 * scale, pad + 18 * scale, actual_size - pad - 18 * scale, actual_size - pad - 18 * scale],
        radius=rad - 18 * scale,
        outline=(251, 191, 36, 90),
        width=3 * scale,
    )

    # Draw "G" in Gold
    # Center: (512 * scale, 512 * scale)
    cx, cy = 250 * scale, 256 * scale
    r_outer = 160 * scale
    r_inner = 95 * scale
    
    # Outer circle arc for G (from ~45 deg to 360 deg)
    draw.arc(
        [cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer],
        start=40,
        end=340,
        fill=(245, 158, 11, 255),
        width=int(r_outer - r_inner),
    )

    # Horizontal bar for G
    bar_y = cy
    bar_h = int(r_outer - r_inner)
    draw.rectangle(
        [cx - 10 * scale, bar_y - bar_h // 2, cx + 130 * scale, bar_y + bar_h // 2],
        fill=(245, 158, 11, 255),
    )

    # Vertical right cap for G
    draw.rectangle(
        [cx + 100 * scale, bar_y - bar_h // 2, cx + 130 * scale, cy + r_outer - 30 * scale],
        fill=(245, 158, 11, 255),
    )

    # 5G arcs in emerald green
    arc_cx, arc_cy = cx + 30 * scale, cy - 40 * scale
    for r_arc, w_arc in [(45 * scale, 10 * scale), (75 * scale, 12 * scale), (105 * scale, 14 * scale)]:
        draw.arc(
            [arc_cx - r_arc, arc_cy - r_arc, arc_cx + r_arc, arc_cy + r_arc],
            start=290,
            end=360,
            fill=(16, 185, 129, 255),
            width=w_arc,
        )

    # 5G Badge pill at bottom right
    bx, by = 300 * scale, 340 * scale
    bw, bh = 145 * scale, 65 * scale
    draw.rounded_rectangle(
        [bx, by, bx + bw, by + bh],
        radius=14 * scale,
        fill=(9, 10, 15, 255),
        outline=(16, 185, 129, 255),
        width=4 * scale,
    )

    # Draw "5G" text inside pill
    try:
        font = ImageFont.truetype("arialbd.ttf", 36 * scale)
    except:
        font = ImageFont.load_default()

    draw.text((bx + 16 * scale, by + 10 * scale), "5G", fill=(16, 185, 129, 255), font=font)

    # Downsample with high quality Lanczos antialiasing
    final_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
    final_512.save("static/logo.png", format="PNG")
    print("Saved static/logo.png")

    # Generate multi-resolution ICO file
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    final_512.save("static/favicon.ico", format="ICO", sizes=icon_sizes)
    print("Saved static/favicon.ico")

if __name__ == "__main__":
    generate_png_and_ico()
