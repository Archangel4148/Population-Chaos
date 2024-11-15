from PyQt5.QtWidgets import QMainWindow, QApplication
from ui.main_window_init import Ui_population_main_window

class PopulationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_population_main_window()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication([])
    window = PopulationWindow()
    window.show()
    app.exec_()
