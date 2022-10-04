import re

import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal

from ObjModel import ObjModel


class Model(QObject):
    enable_actions = pyqtSignal(bool)
    on_mesh_changed = pyqtSignal(object, object, str, object)
    texture_url = ""

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
        self.on_mesh_changed.emit(self._obj_model.vertexes, self._obj_model.faces, self.texture_url,
                                  self._obj_model.textures)

    def parse_for_url(self, url):
        file = open(url[0], 'r')
        vertexes = np.empty((0, 3), float)
        faces = np.empty((0, 3), int)
        meta_text = list()
        texture = np.empty((0, 2), float)
        normals = False
        vertexes_parameter = False
        line_element = False
        for line in file.readlines():
            if re.fullmatch("v ([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?( )?){3}[ \n]?", line):
                vertexes = np.append(vertexes, [list(map(float, line[1:].split()))], axis=0)
            elif re.fullmatch("vt (([0-1]+([.][0-9]*)?|[.][0-9]+)( )?){3}[ \n]?", line):
                texture = np.append(texture, [list(map(float, line[2:].split()))[:2]], axis=0)
            elif re.fullmatch("vt ([+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)( )?){3}[ \n]?", line):
                normals = True
            elif re.fullmatch("vp ([+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)( )?){3}[ \n]?", line):
                vertexes_parameter = True
            elif re.fullmatch("l ([0-9]( )?)+", line):
                line_element = False
            elif re.fullmatch("f ([0-9]+(/[0-9]+)?(/[0-9]+)?(//[0-9]+)?( )?){3,}[ \n]?", line):
                current_face = list()
                if re.fullmatch("f ([0-9]+( )?){3,}[ \n]?", line):
                    line = list(map(int, line[1:].split()))
                    for item in line:
                        current_face.append(item - 1)
                elif re.fullmatch("f ([0-9]+(/[0-9]+)( )?){3,}[ \n]?", line) or re.fullmatch(
                        "f ([0-9]+(//[0-9]+)( )?){3,}[ \n]?", line):
                    line = line[1:].replace('/', ' ').split()
                    for i in range(0, len(line), 2):
                        current_face.append((int(line[i]) - 1))
                elif re.fullmatch("f ([0-9]+(/[0-9]+)(/[0-9]+)( )?){3,}[ \n]?", line):
                    line = line[1:].replace('/', ' ').split()
                    for i in range(0, len(line), 3):
                        current_face.append((int(line[i]) - 1))
                faces = np.append(faces, [current_face], axis=0)
            elif line.strip():
                meta_text.append(line)
        if len(texture) > len(vertexes):
            texture = texture[:len(vertexes)]
        if normals or line_element or vertexes_parameter:
            message = "Unfortunately our program does not support following items:\n"
            count = 1
            if normals:
                message += str(count) + "normals(vn)\n"
                count += 1
            if line_element:
                message += str(count) + "line elements(l v1, v2 ...)\n"
                count += 1
            if vertexes_parameter:
                message += str(count) + "parameter space vertices(vt)\n"
            print(message)
        self._obj_model = ObjModel(meta_text, vertexes, faces, texture)
        self.enable_actions.emit(True)
        self.update_model_signal()

    def load_to_file(self, url):
        file = open(url[0], 'w')
        file.write("#be careful it can be a bit different from original)\n")
        for meta_line in self._obj_model.meta_text:
            if meta_line.count("\n"):
                file.write(meta_line)
            else:
                file.write(meta_line + '\n')
        for vertex in self._obj_model.vertexes:
            current = "v "
            for coord in vertex:
                current += str(float(coord)) + ' '
            file.write(current + '\n')
        file.write('\n')
        for texture_coord in self._obj_model.textures:
            current = "vt "
            for coord in texture_coord:
                current += str(float(coord)) + ' '
            file.write(current + '0\n')
        for face in self._obj_model.faces:
            current = "f "
            for point_number in face:
                current += str(point_number + 1) + ' '
            file.write(current + '\n')
        file.close()

    def set_texture(self, url):
        self.texture_url = url
