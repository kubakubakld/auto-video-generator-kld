from moviepy.editor import ColorClip, ImageClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
import sys
import textwrap
import os

def create_text_image(text, out_path, size=(1080, 1920), bg_color=(20,20,20), text_color=(255,255,255), fontsize=80, margin=80):
    img = Image.new("RGB", size, color=bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", fontsize)
    except Exception:
        font = ImageFont.load_default()

    # Wrap text to reasonable line length
    lines = []
    for paragraph in text.split("\n"):
        wrapped = textwrap.wrap(paragraph, width=40)
        if not wrapped:
            lines.append("")
        else:
            lines.extend(wrapped)

    # Calculate line height using textbbox
    bbox = draw.textbbox((0, 0), "Ay", font=font)
    line_height = (bbox[3] - bbox[1]) + 10

    total_height = line_height * len(lines)

    y = (size[1] - total_height) // 2
    for line in lines:
        bbox_line = draw.textbbox((0, 0), line, font=font)
        w = bbox_line[2] - bbox_line[0]
        x = (size[0] - w) // 2
        draw.text((x, y), line, font=font, fill=text_color)
        y += line_height

    img.save(out_path, format="PNG")

def generate_video(text):
    os.makedirs("tmp", exist_ok=True)
    img_path = "tmp/text.png"
    create_text_image(text, img_path)

    duration = 8
    bg = ColorClip(size=(1080,1920), color=(20,20,20), duration=duration)
    img_clip = ImageClip(img_path).set_duration(duration).set_position("center")

    final = CompositeVideoClip([bg, img_clip])
    final.write_videofile("output.mp4", fps=30, codec="libx264", audio=False)

if __name__ == "__main__":
    input_text = sys.argv[1] if len(sys.argv) > 1 else "No text provided"
    generate_video(input_text)
