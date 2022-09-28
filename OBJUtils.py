import numpy as np
from pyqtgraph.opengl import MeshData


def url_to_mesh_data(url) -> MeshData:
    #########################################
    vertices = np.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [1.0, 1.0],
        [0.0, 1.0]
    ])
    faces = np.array([
        [0, 1, 2],
        [0, 2, 3]
    ])
    #########################################

    return MeshData(vertexes=vertices, faces=faces)


def mesh_data_to_file(mesh_data, url):
    # mesh_data.faces; mesh_data.vertexes.....
    pass
