import numpy as np
from PyQt6 import uic
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QFileDialog
from pyqtgraph.opengl import GLMeshItem, GLViewWidget, MeshData


# def clear_layout(layout):
#     for _ in range(layout.count()):
#         layout.itemAt(0).layout().widget().setParent(None)


class MainWindow(QMainWindow):
    _is_plot_inited = False

    def __init__(self, model, controller):
        super().__init__()
        self._mesh_data = None
        self._model = model
        self._controller = controller

        uic.loadUi('resources/gui/gui.ui', self)

        # connect widgets to controller
        self.resize_sb.valueChanged.connect(self._controller.resize_coefficient_changed)
        self.resize_btn.clicked.connect(self._controller.resize_clicked)

        self.move_x_sb.valueChanged.connect(self._controller.move_x_changed)
        self.move_y_sb.valueChanged.connect(self._controller.move_y_changed)
        self.move_z_sb.valueChanged.connect(self._controller.move_z_changed)
        self.move_btn.clicked.connect(self._controller.move_clicked)

        self.shrink_x_sb.valueChanged.connect(self._controller.shrink_x_changed)
        self.shrink_y_sb.valueChanged.connect(self._controller.shrink_y_changed)
        self.shrink_z_sb.valueChanged.connect(self._controller.shrink_z_changed)
        self.shrink_btn.clicked.connect(self._controller.shrink_clicked)

        self.axis_cb.currentIndexChanged.connect(self._controller.rotate_axis_changed)
        self.angle_sb.valueChanged.connect(self._controller.rotate_angle_changed)
        self.rotate_btn.clicked.connect(self._controller.rotate_clicked)

        self.open_file.clicked.connect(lambda: self._controller.file_picked(self.get_file()))
        self.save_file.clicked.connect(lambda: self._controller.file_picked(self.file_save()))

        # listen for model event signals
        self._model.enable_actions.connect(lambda flag: self.aciton_widget.setEnabled(flag))
        self._model.on_mesh_changed.connect(self.update_mesh)

    # TODO set file type: obj
    def get_file(self):
        return QFileDialog.getOpenFileName(self, 'Open file', None, "Image files (*.*)")

    def file_save(self):
        return QFileDialog.getSaveFileName(self, 'Save File')

    @pyqtSlot(MeshData)
    def update_mesh(self, mesh_data):
        self._mesh_data = mesh_data
        if not self._is_plot_inited:
            self._is_plot_inited = True
            view = GLViewWidget()

            mesh = GLMeshItem(
                meshdata=self._mesh_data, smooth=True, drawFaces=False, drawEdges=True, edgeColor=(0, 1, 0, 1))

            view.addItem(mesh)
            self.model_layout.addWidget(view)
