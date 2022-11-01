from PyQt6 import uic
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QFrame

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vedo import Plotter, Mesh


class MainWindow_ver1(QMainWindow):
    def __init__(self, model, controller):
        super().__init__()
        self._mesh_data = None
        self._model = model
        self._controller = controller

        uic.loadUi('resources/gui/gui_1.ui', self)

        self.vtkWidget = QVTKRenderWindowInteractor(self.vtk_frame)
        self.plt = Plotter(qt_widget=self.vtkWidget)
        self.model_layout.addWidget(self.vtkWidget)
        self.plt.show()

        # connect widgets to controller
        # ================RESIZE===============
        self.resize_sb.valueChanged.connect(self._controller.resize_coefficient_changed)
        self.resize_btn.clicked.connect(self._controller.resize_clicked)
        self.resize_cb.stateChanged.connect(self._controller.resize_flag_change)

        self.resize_for_point_cb.stateChanged.connect(self._controller.resize_for_point_changed)
        self.resize_for_point_x_sb.valueChanged.connect(self._controller.resize_for_point_x_changed)
        self.resize_for_point_y_sb.valueChanged.connect(self._controller.resize_for_point_y_changed)
        self.resize_for_point_z_sb.valueChanged.connect(self._controller.resize_for_point_z_changed)

        self.resize_for_point_fr.setEnabled(False)
        self.resize_for_point_cb.stateChanged.connect(self.resize_for_point_cb_state_changed)

        # ================MOVE================
        self.move_x_sb.valueChanged.connect(self._controller.move_x_changed)
        self.move_y_sb.valueChanged.connect(self._controller.move_y_changed)
        self.move_z_sb.valueChanged.connect(self._controller.move_z_changed)
        self.move_btn.clicked.connect(self._controller.move_clicked)
        self.move_cb.stateChanged.connect(self._controller.move_flag_change)

        # ================SHRINK===============
        self.shrink_x_sb.valueChanged.connect(self._controller.shrink_x_changed)
        self.shrink_y_sb.valueChanged.connect(self._controller.shrink_y_changed)
        self.shrink_z_sb.valueChanged.connect(self._controller.shrink_z_changed)
        self.shrink_btn.clicked.connect(self._controller.shrink_clicked)
        self.shrink_cb.stateChanged.connect(self._controller.shrink_flag_change)

        self.shrink_for_point_cb.stateChanged.connect(self._controller.shrink_for_point_changed)
        self.shrink_for_point_x_sb.valueChanged.connect(self._controller.shrink_for_point_x_changed)
        self.shrink_for_point_y_sb.valueChanged.connect(self._controller.shrink_for_point_y_changed)
        self.shrink_for_point_z_sb.valueChanged.connect(self._controller.shrink_for_point_z_changed)

        self.shrink_for_point_fr.setEnabled(False)
        self.shrink_for_point_cb.stateChanged.connect(self.shrink_for_point_cb_state_changed)

        # ================ROTATE===============
        self.axis_cb.currentIndexChanged.connect(self._controller.rotate_axis_changed)
        self.angle_sb.valueChanged.connect(self._controller.rotate_angle_changed)
        self.rotate_btn.clicked.connect(self._controller.rotate_clicked)
        self.rotate_cb.stateChanged.connect(self._controller.rotate_flag_change)

        self.rotate_custom_axis_cb.stateChanged.connect(self._controller.rotate_custom_axis_changed)
        self.rotate_custom_axis_x_sb.valueChanged.connect(self._controller.rotate_custom_axis_x_changed)
        self.rotate_custom_axis_y_sb.valueChanged.connect(self._controller.rotate_custom_axis_y_changed)
        self.rotate_custom_axis_z_sb.valueChanged.connect(self._controller.rotate_custom_axis_z_changed)

        self.rotate_custom_axis_fr.setEnabled(False)
        self.rotate_custom_axis_cb.stateChanged.connect(self.rotate_custom_axis_cb_state_changed)

        # ================EXECUTE===============
        self.execute_btn.clicked.connect(self._controller.execute_clicked)

        # ================FILES===============
        self.open_file.clicked.connect(lambda: self._controller.file_picked(self.get_file()))
        self.open_texture.clicked.connect(lambda: self._controller.texture_picked(self.get_texture()))

        self.save_file.clicked.connect(lambda: self._controller.write_to_file(self.file_save()))

        # listen for model event signals
        self._model.enable_actions.connect(lambda flag: self.aciton_widget.setEnabled(flag))
        self._model.on_mesh_changed.connect(self.update_mesh)

    def get_file(self):
        return QFileDialog.getOpenFileName(self, 'Open file', None, "Image files (*.obj)")

    def get_texture(self):
        return QFileDialog.getOpenFileName(self, 'Open file', None, "Image files (*.jpg)")

    def file_save(self):
        return QFileDialog.getSaveFileName(self, 'Save File')

    @pyqtSlot(object, object, str, object)
    def update_mesh(self, vertexes, faces, texture_url, textures):
        for _ in range(len(self.plt.getMeshes())):
            self.plt.pop()
        mesh = Mesh([vertexes, faces])
        if texture_url != "":
            mesh.texture(texture_url, tcoords=textures)
        self.plt += mesh
        self.plt.show(axes=1)

    def resize_for_point_cb_state_changed(self, val):
        if val:
            self.resize_for_point_fr.setEnabled(True)
        else:
            self.resize_for_point_fr.setEnabled(False)

    def rotate_custom_axis_cb_state_changed(self, val):
        if val:
            self.rotate_custom_axis_fr.setEnabled(True)
            self.rotate_default_axis_fr.setEnabled(False)
        else:
            self.rotate_custom_axis_fr.setEnabled(False)
            self.rotate_default_axis_fr.setEnabled(True)

    def shrink_for_point_cb_state_changed(self, val):
        if val:
            self.shrink_for_point_fr.setEnabled(True)
        else:
            self.shrink_for_point_fr.setEnabled(False)
