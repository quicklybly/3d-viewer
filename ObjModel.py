class ObjModel:
    def __init__(self, meta_text=None, vertexes=None, faces=None, textures=None):
        self._meta_text = meta_text
        self._vertexes = vertexes
        self._faces = faces
        self._textures = textures

    @property
    def meta_text(self):
        return self._meta_text

    @property
    def vertexes(self):
        return self._vertexes

    @property
    def faces(self):
        return self._faces

    @property
    def textures(self):
        return self._textures

    def rotate(self, axis, angle):
        pass

    def resize(self, coefficient):
        pass

    def move(self, x, y, z):
        pass

    def shrink(self, cx, cy, cz):
        pass
