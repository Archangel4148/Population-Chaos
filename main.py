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
        pg.setConfigOptions(background='w', foreground='k')
        plot_area = self.ui.plot_area_layout
        plot_widget = pg.PlotWidget()
        plot_area.addWidget(plot_widget)
        self.plot_item: pg.PlotItem = plot_widget.getPlotItem()

        # Set up validators for the line edits to allow only float values
        float_validator = QDoubleValidator(self)
        self.ui.initial_population_line_edit.setValidator(float_validator)
        self.ui.max_population_line_edit.setValidator(float_validator)
        self.ui.growth_rate_line_edit.setValidator(float_validator)
        self.ui.steps_line_edit.setValidator(float_validator)

        # Connecting signals
        self.ui.initial_population_line_edit.editingFinished.connect(self.factors_changed)
        self.ui.max_population_line_edit.editingFinished.connect(self.factors_changed)
        self.ui.growth_rate_line_edit.editingFinished.connect(self.factors_changed)
        self.ui.steps_line_edit.editingFinished.connect(self.factors_changed)
        self.ui.reset_button.pressed.connect(self.reset)

        # Variables for plotting
        self.x: np.ndarray | None = None
        self.y: np.ndarray | None = None

        # Initialize default values
        self.default_initial_population = self.initial_population = 10
        self.default_max_population = self.max_population = 250
        self.default_growth_rate = self.growth_rate = 0.1
        self.default_num_steps = self.num_steps = 100

        # Populate the plot initially
        self.factors_changed(True)

    def factors_changed(self, override_text: bool = False):
        self.plot_item.clear()
        if override_text:
            self.ui.initial_population_line_edit.setText(str(self.initial_population))
            self.ui.max_population_line_edit.setText(str(self.max_population))
            self.ui.growth_rate_line_edit.setText(str(self.growth_rate))
            self.ui.steps_line_edit.setText(str(self.num_steps))
        else:
            self.initial_population = int(self.ui.initial_population_line_edit.text())
            self.max_population = int(self.ui.max_population_line_edit.text())
            self.growth_rate = float(self.ui.growth_rate_line_edit.text())
            self.num_steps = int(self.ui.steps_line_edit.text())

        self.x = np.linspace(0, self.num_steps, self.num_steps * 10)

        # Using logistic growth model
        self.y = self.max_population / (
                1 + ((self.max_population - self.initial_population) / self.initial_population) * np.exp(
            -self.growth_rate * self.x))

        self.plot_item.plot(self.x, self.y, pen=pg.mkPen('b'))

    def reset(self):
        self.initial_population = self.default_initial_population
        self.max_population = self.default_max_population
        self.growth_rate = self.default_growth_rate
        self.num_steps = self.default_num_steps
        self.factors_changed(True)


if __name__ == "__main__":
    app = QApplication([])
    window = PopulationWindow()
    window.show()
    app.exec_()
