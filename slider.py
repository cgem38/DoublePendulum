from PyQt5.QtWidgets import (QSlider)
from PyQt5.QtCore import Qt

class Slider(QSlider):
    def __init__(self, min: float, max: float, orientation: str):

        horizontal = ["Horizontal", "horizontal", "H", "h"]
        vertical = ["Vertical", "vertical", "V", "v"]
        if orientation in horizontal:
            slider = QSlider(Qt.Orientation.Horizontal)
        elif orientation in vertical:
            slider = QSlider(Qt.Orientation.Vertical)
        
        formattedMin = "{:.2f}".format(min)
        formattedMax = "{:.2f}".format(max)
        slider.setMinimum(int(100 * formattedMin))
        slider.setMaximum(int(100 * formattedMax))


