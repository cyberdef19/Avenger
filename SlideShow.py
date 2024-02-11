import tkinter as tk
from itertools import cycle
from PIL import Image, ImageTk


class SlideShow:
    def __init__(self, root, image_files, delay):
        self.root = root
        self.image_files = image_files
        self.delay = delay

        self.images = cycle(self.load_images())
        self.image_label = tk.Label(root)
        self.image_label.pack()
        self.update_slideshow()

    def load_images(self):
        return [ImageTk.PhotoImage(Image.open(image)) for image in self.image_files]

    def update_slideshow(self):
        image = next(self.images)
        self.image_label.config(image=image)
        self.root.after(self.delay, self.update_slideshow)

