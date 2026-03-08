from moviepy.editor import *
import sys

def generate_video(text):
    # Background color
    clip = ColorClip(size=(1080, 1920), color=(20, 20, 20), duration=8)

    # Text overlay
    txt = TextClip(text, fontsize=80, color='white', font='Arial-Bold', method='pillow')
    txt = txt.set_position('center').set_duration(8)

    # Composite
    final = CompositeVideoClip([clip, txt])
    final.write_videofile("output.mp4", fps=30)

if __name__ == "__main__":
    input_text = sys.argv[1] if len(sys.argv) > 1 else "No text provided"
    generate_video(input_text)
