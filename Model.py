import numpy as np
from pyqtgraph.opengl import MeshData


class Model:
    def __init__(self):
        self._meta_text = None
        self._mesh_data = None
        self._textures = None

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
        self._meta_text = "None"
        self._mesh_data = MeshData(vertexes=vertexes, faces=faces)
        self._textures = "None"

    def load_to_file(self, url):
        pass
