import numpy as np
from PyQt6 import uic
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QMainWindow
from pyqtgraph.opengl import GLMeshItem, GLViewWidget, MeshData


def _clear_layout(layout):
    for _ in range(layout.count()):
        layout.itemAt(0).layout().widget().setParent(None)


class MainWindow(QMainWindow):
    def __init__(self, model, controller):
        super().__init__()
        self._model = model
        self._controller = controller

        uic.loadUi('resources/gui/gui.ui', self)

        self.resize_sb.valueChanged.connect(self._controller.resize_coefficient_changed)

        self.move_x_sb.valueChanged.connect(self._controller.move_x_changed)
        self.move_y_sb.valueChanged.connect(self._controller.move_y_changed)
        self.move_z_sb.valueChanged.connect(self._controller.move_z_changed)

        self.shrink_x_sb.valueChanged.connect(self._controller.shrink_x_changed)
        self.shrink_y_sb.valueChanged.connect(self._controller.shrink_y_changed)
        self.shrink_z_sb.valueChanged.connect(self._controller.shrink_z_changed)

        self.axis_cb.currentIndexChanged.connect(self._controller.rotate_axis_changed)
        self.angle_sb.valueChanged.connect(self._controller.rotate_angle_changed)

    @pyqtSlot(MeshData)
    def update_mesh_data(self, mesh_data):
        _clear_layout(self.model_layout)

        view = GLViewWidget()

        mesh = GLMeshItem(meshdata=mesh_data, smooth=True, drawFaces=False, drawEdges=True, edgeColor=(0, 1, 0, 1))
        view.addItem(mesh)

        self.model_layout.addWidget(view)
