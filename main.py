import numpy as np
import pyqtgraph as pg
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QMainWindow, QApplication

from ui.main_window_init import Ui_population_main_window


class PopulationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_population_main_window()
        self.ui.setupUi(self)

        # Set up the plot
        plot_area = self.ui.plot_area_layout
        plot_widget = pg.PlotWidget()
        plot_area.addWidget(plot_widget)
        self.plot_item: pg.PlotItem = plot_widget.getPlotItem()

        # Set up validators for the line edits to allow only float values
        float_validator = QDoubleValidator(self)
        self.ui.y_scale_line_edit.setValidator(float_validator)
        self.ui.y_offset_line_edit.setValidator(float_validator)
        self.ui.x_scale_line_edit.setValidator(float_validator)
        self.ui.x_offset_line_edit.setValidator(float_validator)

        # Connecting signals
        self.ui.y_scale_line_edit.editingFinished.connect(self.factors_changed)
        self.ui.y_offset_line_edit.editingFinished.connect(self.factors_changed)
        self.ui.x_scale_line_edit.editingFinished.connect(self.factors_changed)
        self.ui.x_offset_line_edit.editingFinished.connect(self.factors_changed)
        self.ui.reset_button.pressed.connect(self.reset)

        # Variables for plotting
        self.x: np.ndarray | None = None
        self.y: np.ndarray | None = None

        # Initialize default values
        self.default_y_scale = self.y_scale = 1
        self.default_y_offset = self.y_offset = 0
        self.default_x_scale = self.x_scale = 1
        self.default_x_offset = self.x_offset = 0

        # Populate the plot initially
        self.factors_changed()

    def factors_changed(self, override_text: bool = False):
        self.plot_item.clear()
        if override_text:
            self.ui.y_offset_line_edit.setText(str(self.y_offset))
            self.ui.y_scale_line_edit.setText(str(self.y_scale))
            self.ui.x_offset_line_edit.setText(str(self.x_offset))
            self.ui.x_scale_line_edit.setText(str(self.x_scale))
        else:
            self.y_offset = float(self.ui.y_offset_line_edit.text())
            self.y_scale = float(self.ui.y_scale_line_edit.text())
            self.x_offset = float(self.ui.x_offset_line_edit.text())
            self.x_scale = float(self.ui.x_scale_line_edit.text())

        self.x = np.linspace(0, 100, 1000)
        self.y = self.y_scale * np.sin(self.x * self.x_scale + self.x_offset) + self.y_offset
        self.plot_item.plot(self.x, self.y)

    def reset(self):
        self.x_offset = self.default_x_offset
        self.y_offset = self.default_y_offset
        self.x_scale = self.default_x_scale
        self.y_scale = self.default_y_scale
        self.factors_changed(True)


if __name__ == "__main__":
    app = QApplication([])
    window = PopulationWindow()
    window.show()
    app.exec_()
