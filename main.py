import sys

from PyQt6.QtWidgets import QApplication

from Model import Model
from Controller import Controller
from View import MainWindow


def main():
    app = QApplication(sys.argv)

    model = Model()
    controller = Controller(model)
    view = MainWindow(model, controller)
    view.show()

    app.exec()


if __name__ == '__main__':
    main()