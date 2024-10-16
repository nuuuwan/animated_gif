"""Creates Animated GIFs"""
import os
import sys
import tempfile
import imageio
from utils import Log
from PIL import Image


log = Log("AnimatedGIF")


class AnimatedGIF:
    """Creates Animated GIFs"""

    def __init__(self, image_path_list):
        self.image_path_list = image_path_list

    def write(self, output_gif_path, duration_s=0.333):
        """
        Creates an animated GIF from a list of image paths and saves it 
        to the specified path.
        """
        images = [
            AnimatedGIF.get_image(image_path) 
            for image_path in self.image_path_list
        ]
        frames = images + images[::-1]
        duration = duration_s * 1000
        imageio.mimwrite(output_gif_path, frames, duration=duration, loop=0)
        log.info(f"Wrote {output_gif_path}")

    @classmethod
    def from_dir_path(cls, directory_path):
        """
        Creates an instance of the class from a directory path 
        containing PNG images.
        """
        image_path_list = [
            os.path.join(directory_path, file_name)
            for file_name in os.listdir(directory_path)
            if file_name.endswith(".png")
        ]
        log.debug(f"Found {len(image_path_list)} PNG images in {directory_path}")
        return cls(image_path_list)
    
    @staticmethod
    def get_image(image_path):
        """Reads an image from a file path."""
        im = Image.open(image_path)
        # resize 
        w, h= im.size
        max_dim = 800
        if w > max_dim or h > max_dim:
            ratio = min(max_dim/w, max_dim/h)
            new_size = (int(w*ratio), int(h*ratio))
            im = im.resize(new_size)
        temp_image_path = tempfile.mktemp(suffix=".png")
        im.save(temp_image_path)
        log.debug(f'Wrote resized image to {temp_image_path}')
        return imageio.imread(temp_image_path)

if __name__ == "__main__":
    dir_path = sys.argv[1]
    gif_path = os.path.join(dir_path, "animated.gif")
    AnimatedGIF.from_dir_path(dir_path).write(gif_path)
