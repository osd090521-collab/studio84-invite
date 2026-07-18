"""Generates qr.png and og.png for the Studio 84 invite page.
Re-run after swapping WHATSAPP_NUMBER for the real digits.
"""
import urllib.parse
import qrcode
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "/Users/getyobreadup/Brain Flow/studio84-invite"

WHATSAPP_NUMBER = "447504828622"
MESSAGE = "Hello Omar, I would like to inquire about alterations"

WA_LINK = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(MESSAGE)}"
print("wa.me link:", WA_LINK)

BONE = "#F3EEE5"
CARBON = "#1C1A17"
TOBACCO = "#8A6F52"

# --- QR code ---
qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=20,
    border=2,
)
qr.add_data(WA_LINK)
qr.make(fit=True)
img = qr.make_image(fill_color=CARBON, back_color=BONE).convert("RGB")
img.save(f"{OUT_DIR}/qr.png")
print("wrote qr.png", img.size)

# --- OG image 1200x630 ---
W, H = 1200, 630
canvas = Image.new("RGB", (W, H), BONE)
draw = ImageDraw.Draw(canvas)

cormorant = ImageFont.truetype(f"{OUT_DIR}/fonts-src/Cormorant.ttf", 96)
try:
    cormorant.set_variation_by_axes([500])  # Medium
except Exception as e:
    print("variation axis skip:", e)

inter = ImageFont.truetype(f"{OUT_DIR}/fonts-src/Inter.ttf", 28)
try:
    inter.set_variation_by_axes([14, 500])  # opsz, weight
except Exception as e:
    print("inter variation skip:", e)


def letterspaced(text, spacing):
    return (" " * spacing).join(list(text))


wordmark = letterspaced("STUDIO 84°", 1)
sub = letterspaced("LONDON", 2)

bbox = draw.textbbox((0, 0), wordmark, font=cormorant)
w = bbox[2] - bbox[0]
draw.text(((W - w) / 2 - bbox[0], H / 2 - 90), wordmark, font=cormorant, fill=CARBON)

bbox2 = draw.textbbox((0, 0), sub, font=inter)
w2 = bbox2[2] - bbox2[0]
draw.text(((W - w2) / 2 - bbox2[0], H / 2 + 30), sub, font=inter, fill=TOBACCO)

rule_w = 90
draw.line(
    [(W / 2 - rule_w / 2, H / 2 + 90), (W / 2 + rule_w / 2, H / 2 + 90)],
    fill=TOBACCO,
    width=1,
)

canvas.save(f"{OUT_DIR}/og.png")
print("wrote og.png", canvas.size)
