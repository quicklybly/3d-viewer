import sys

from PyQt6.QtWidgets import QApplication

from Model import Model
from OBJUtils import url_to_mesh_data
from Presenter import Presenter
from View import MainWindow


def main():
    app = QApplication(sys.argv)
    view = MainWindow()
    presenter = Presenter(view, Model())

    view.update_mesh_data(url_to_mesh_data(""))

    view.show()
    app.exec()


if __name__ == '__main__':
    main()