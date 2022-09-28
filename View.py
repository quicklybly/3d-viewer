import numpy as np
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from pyqtgraph.opengl import GLMeshItem, GLViewWidget


def _clear_layout(layout):
    for _ in range(layout.count()):
        layout.itemAt(0).layout().widget().setParent(None)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('resources/gui/gui.ui', self)

    def update_mesh_data(self, mesh_data):
        _clear_layout(self.model_layout)

        view = GLViewWidget()

        mesh = GLMeshItem(meshdata=mesh_data, smooth=True, drawFaces=False, drawEdges=True, edgeColor=(0, 1, 0, 1))
        view.addItem(mesh)

        self.model_layout.addWidget(view)
