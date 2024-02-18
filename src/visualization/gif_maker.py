import glob
from PIL import Image


def make_gif(frame_folder, duration=100, loop=0):
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.webp")]
    frame_one = frames[0]
    frame_one.save(
        "output.gif",
        format="GIF",
        append_images=frames[1:],
        save_all=True,
        duration=duration,
        loop=loop,
    )
