class ObjModel:
    def __init__(self, meta_text=None, mesh_data=None, textures=None):
        self._meta_text = meta_text
        self._mesh_data = mesh_data
        self._textures = textures

    @property
    def meta_text(self):
        return self._meta_text

    @property
    def mesh_data(self):
        return self._mesh_data

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
