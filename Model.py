import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal
from pyqtgraph.opengl import MeshData

from ObjModel import ObjModel


class Model(QObject):
    enable_actions = pyqtSignal(bool)
    on_mesh_changed = pyqtSignal(MeshData)

    def __init__(self):
        super().__init__()
        self._obj_model = ObjModel()

    def move(self, x, y, z):
        print(x, y, z)
        self._obj_model.move(x, y, z)
        self.update_model_signal()

    def resize(self, c):
        print(c)
        self._obj_model.resize(c)
        self.update_model_signal()

    def rotate(self, axis, angle):
        print(axis, angle)
        self._obj_model.rotate(axis, angle)
        self.update_model_signal()

    def shrink(self, cx, cy, cz):
        print(cx, cy, cz)
        self._obj_model.shrink(cx, cy, cz)
        self.update_model_signal()

    def update_model_signal(self):
        self.on_mesh_changed.emit(self._obj_model.mesh_data)

    def parse_for_url(self, url):
        vertexes = np.array([
            [0.0, 0.0],
            [1.0, 0.0],
            [1.0, 1.0],
            [0.0, 1.0]
        ])
        faces = np.array([
            [0, 1, 2],
            [0, 2, 3]
        ])

        self._obj_model = ObjModel(
            None,
            MeshData(vertexes=vertexes, faces=faces),
            None
        )
        self.enable_actions.emit(True)
        self.update_model_signal()

    def load_to_file(self, url):
        pass
