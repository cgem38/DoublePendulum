from PyQt5.QtWidgets import (QSlider)
from PyQt5.QtCore import Qt

class Slider(QSlider):
    def __init__(self, min: float, max: float, orientation: str):
        super(QSlider, self).__init__()
        horizontal = ["Horizontal", "horizontal", "H", "h"]
        vertical = ["Vertical", "vertical", "V", "v"]
        if orientation in horizontal:
            self.setOrientation(Qt.Orientation.Horizontal)
        elif orientation in vertical:
            self.setOrientation(Qt.Orientation.Vertical)

        min = 100 * min
        max = 100 * max
        self.setMinimum(int(min))
        self.setMaximum(int(max))


