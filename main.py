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
        self.plot_item.addLegend()

        # Set axis labels
        self.plot_item.setLabel('left', 'Population', units='individuals')  # Label for y-axis
        self.plot_item.setLabel('bottom', 'Time', units='time steps')  # Label for x-axis

        # Set up validators for the line edits to allow only float values
        float_validator = QDoubleValidator(self)
        self.ui.initial_prey_population_line_edit.setValidator(float_validator)
        self.ui.initial_predator_population_line_edit.setValidator(float_validator)
        self.ui.growth_rate_line_edit.setValidator(float_validator)
        self.ui.starve_rate_line_edit.setValidator(float_validator)
        self.ui.predator_reproduction_rate_line_edit.setValidator(float_validator)
        self.ui.predation_rate_line_edit.setValidator(float_validator)
        self.ui.end_time_line_edit.setValidator(float_validator)
        self.ui.time_step_line_edit.setValidator(float_validator)

        # Connecting signals
        self.ui.initial_prey_population_line_edit.editingFinished.connect(self.factors_changed)
        self.ui.initial_predator_population_line_edit.editingFinished.connect(self.factors_changed)
        self.ui.growth_rate_line_edit.editingFinished.connect(self.factors_changed)
        self.ui.starve_rate_line_edit.editingFinished.connect(self.factors_changed)
        self.ui.predation_rate_line_edit.editingFinished.connect(self.factors_changed)
        self.ui.predator_reproduction_rate_line_edit.editingFinished.connect(self.factors_changed)
        self.ui.end_time_line_edit.editingFinished.connect(self.factors_changed)
        self.ui.time_step_line_edit.editingFinished.connect(self.factors_changed)

        self.ui.reset_button.pressed.connect(self.reset)

        # Variables for plotting
        self.prey_data: list[np.ndarray | None] = [None, None]
        self.predator_data: list[np.ndarray | None] = [None, None]

        # Initialize default values for predator-prey model
        self.default_initial_prey_population = self.initial_prey_population = 40
        self.default_initial_predator_population = self.initial_predator_population = 9
        self.default_prey_growth_rate = self.prey_growth_rate = 0.1
        self.default_predator_starve_rate = self.predator_starve_rate = 0.1
        self.default_predator_reproduction_rate = self.predator_reproduction_rate = 0.01
        self.default_predation_rate = self.predation_rate = 0.02
        self.default_end_time = self.end_time = 50
        self.default_time_step = self.time_step = 0.0001

        # Populate the plot initially
        self.factors_changed(True)

    def factors_changed(self, override_text: bool = False):
        if override_text:
            self.ui.initial_prey_population_line_edit.setText(str(self.initial_prey_population))
            self.ui.initial_predator_population_line_edit.setText(str(self.initial_predator_population))
            self.ui.growth_rate_line_edit.setText(str(self.prey_growth_rate))
            self.ui.starve_rate_line_edit.setText(str(self.predator_starve_rate))
            self.ui.predator_reproduction_rate_line_edit.setText(str(self.predator_reproduction_rate))
            self.ui.predation_rate_line_edit.setText(str(self.predation_rate))
            self.ui.end_time_line_edit.setText(str(self.end_time))
            self.ui.time_step_line_edit.setText(str(self.time_step))
        else:
            self.initial_prey_population = int(self.ui.initial_prey_population_line_edit.text())
            self.initial_predator_population = int(self.ui.initial_predator_population_line_edit.text())
            self.prey_growth_rate = float(self.ui.growth_rate_line_edit.text())
            self.predator_starve_rate = float(self.ui.starve_rate_line_edit.text())
            self.predator_reproduction_rate = float(self.ui.predator_reproduction_rate_line_edit.text())
            self.predation_rate = float(self.ui.predation_rate_line_edit.text())
            self.end_time = int(float(self.ui.end_time_line_edit.text()))
            self.time_step = float(self.ui.time_step_line_edit.text())

        time = np.arange(0, self.end_time, self.time_step)
        self.prey_data[0] = time
        self.predator_data[0] = time

        # Variables to store population values over time
        prey_population_values = [self.initial_prey_population]
        predator_population_values = [self.initial_predator_population]

        for i in range(1, len(time)):
            dN = prey_population_values[i - 1] * (
                        self.prey_growth_rate - self.predation_rate * predator_population_values[i - 1])
            dP = -predator_population_values[i - 1] * (
                        self.predator_starve_rate - self.predator_reproduction_rate * prey_population_values[i - 1])

            next_N = prey_population_values[i-1] + dN * self.time_step
            next_P = predator_population_values[i-1] + dP * self.time_step

            # Store populations for plotting
            prey_population_values.append(next_N)
            predator_population_values.append(next_P)

        self.prey_data[1] = prey_population_values
        self.predator_data[1] = predator_population_values

        # Plotting data
        self.plot_item.clear()
        self.plot_item.plot(*self.prey_data, pen=pg.mkPen('b'), name="Prey Population")
        self.plot_item.plot(*self.predator_data, pen=pg.mkPen('r'), name="Predator Population")

    def reset(self):
        self.initial_prey_population = self.default_initial_prey_population
        self.initial_predator_population = self.default_initial_predator_population
        self.prey_growth_rate = self.default_prey_growth_rate
        self.predator_starve_rate = self.default_predator_starve_rate
        self.predator_reproduction_rate = self.default_predator_reproduction_rate
        self.predation_rate = self.default_predation_rate
        self.end_time = self.default_end_time
        self.factors_changed(True)


if __name__ == "__main__":
    app = QApplication([])
    window = PopulationWindow()
    window.show()
    app.exec_()
