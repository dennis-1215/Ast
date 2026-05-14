import os

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class ImageUtils:

    @staticmethod
    def get_image_path(filename):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir,"..", "..", "Images",filename)

    @staticmethod
    def load_pixmap(filename, width=None, height=None, keep_ratio=True):
        image_path = ImageUtils.get_image_path(filename)
        pixmap = QPixmap(image_path)

        if width and height:
            aspect = (Qt.KeepAspectRatio if keep_ratio else Qt.IgnoreAspectRatio)
            pixmap = pixmap.scaled(width, height, aspect, Qt.SmoothTransformation)

        return pixmap