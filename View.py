import numpy as np
from PyQt6 import uic
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QFrame
from pyqtgraph.opengl import GLMeshItem, GLViewWidget, MeshData

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vedo import Plotter, Mesh


class MainWindow(QMainWindow):
    _is_plot_inited = False

    def __init__(self, model, controller):
        super().__init__()
        self._mesh_data = None
        self._model = model
        self._controller = controller

        uic.loadUi('resources/gui/gui.ui', self)

        self.vtkWidget = QVTKRenderWindowInteractor(self.vtk_frame)
        self.plt = Plotter(qtWidget=self.vtkWidget, bg="black")
        self.model_layout.addWidget(self.vtkWidget)
        self.plt.show()

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
        self.open_texture.clicked.connect(lambda: self._controller.texture_picked(self.get_texture()))

        self.save_file.clicked.connect(lambda: self._controller.write_to_file(self.file_save()))

        # listen for model event signals
        self._model.enable_actions.connect(lambda flag: self.aciton_widget.setEnabled(flag))
        self._model.on_mesh_changed.connect(self.update_mesh)

    # TODO set file type: obj
    def get_file(self):
        return QFileDialog.getOpenFileName(self, 'Open file', None, "Image files (*.*)")

    # TODO set file type: mtl
    def get_texture(self):
        return QFileDialog.getOpenFileName(self, 'Open file', None, "Image files (*.*)")

    def file_save(self):
        return QFileDialog.getSaveFileName(self, 'Save File')

    @pyqtSlot(object, object, str, object)
    def update_mesh(self, vertexes, faces, texture_url, textures):
        self.plt.clear()
        mesh = Mesh([vertexes, faces])
        if texture_url != "":
            mesh.texture(texture_url, tcoords=textures)
        self.plt += mesh
        self.plt.show()
