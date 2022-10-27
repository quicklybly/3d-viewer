from PyQt6.QtCore import QObject, pyqtSlot


class Controller(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model
        self._order_of_operations = []

        self._resize_coefficient = 1
        self._resize_for_point_flag = False
        self._resize_for_point_x = 0
        self._resize_for_point_y = 0
        self._resize_for_point_z = 0

        self._move_x = 0
        self._move_y = 0
        self._move_z = 0

        self._shrink_x = 1
        self._shrink_y = 1
        self._shrink_z = 1
        self._shrink_for_point_flag = False
        self._shrink_for_point_x = 0
        self._shrink_for_point_y = 0
        self._shrink_for_point_z = 0

        self._rotate_axis = 0  # x:0 y:1 z:2
        self._rotate_angle = 0
        self._rotate_custom_axis_flag = False
        self._rotate_custom_axis_x = 0
        self._rotate_custom_axis_y = 0
        self._rotate_custom_axis_z = 0

        self._resize_flag = False
        self._move_flag = False
        self._shrink_flag = False
        self._rotate_flag = False

    def __change_operation_flag(self, flag, operation):
        if flag:
            self._order_of_operations.append(operation)
        else:
            self._order_of_operations.remove(operation)

    # ================RESIZE===============
    @pyqtSlot(float)
    def resize_coefficient_changed(self, c):
        self._resize_coefficient = c

    @pyqtSlot()
    def resize_flag_change(self):
        self._resize_flag = not self._resize_flag
        self.__change_operation_flag(self._resize_flag, "resize")

    @pyqtSlot()
    def resize_clicked(self):
        self._resize()
        self._model.emit_update_model_signal()

    def _resize(self):
        if self._resize_for_point_flag:
            self._model.resize_around_point(
                self._resize_for_point_x,
                self._resize_for_point_y,
                self._resize_for_point_z,
                self._resize_coefficient
            )
        else:
            self._model.resize(self._resize_coefficient)

    @pyqtSlot(int)
    def resize_for_point_changed(self):
        self._resize_for_point_flag = not self._resize_for_point_flag

    @pyqtSlot(float)
    def resize_for_point_x_changed(self, x):
        self._resize_for_point_x = x

    @pyqtSlot(float)
    def resize_for_point_y_changed(self, y):
        self._resize_for_point_y = y

    @pyqtSlot(float)
    def resize_for_point_z_changed(self, z):
        self._resize_for_point_z = z

    # ================MOVE===============
    @pyqtSlot(float)
    def move_x_changed(self, mx):
        self._move_x = mx

    @pyqtSlot(float)
    def move_y_changed(self, my):
        self._move_y = my

    @pyqtSlot(float)
    def move_z_changed(self, mz):
        self._move_z = mz

    @pyqtSlot()
    def move_flag_change(self):
        self._move_flag = not self._move_flag
        self.__change_operation_flag(self._move_flag, "move")

    @pyqtSlot()
    def move_clicked(self):
        self._move()
        self._model.emit_update_model_signal()

    def _move(self):
        self._model.move(self._move_x, self._move_y, self._move_z)

    # ================ROTATE===============
    @pyqtSlot(float)
    def rotate_angle_changed(self, angle):
        self._rotate_angle = angle

    @pyqtSlot(int)
    def rotate_axis_changed(self, axis):
        self._rotate_axis = axis

    @pyqtSlot()
    def rotate_flag_change(self):
        self._rotate_flag = not self._rotate_flag
        self.__change_operation_flag(self._rotate_flag, "rotate")

    @pyqtSlot()
    def rotate_clicked(self):
        self._rotate()
        self._model.emit_update_model_signal()

    def _rotate(self):
        if self._rotate_custom_axis_flag:
            self._model.rotate_along_free_axis(
                self._rotate_custom_axis_x,
                self._rotate_custom_axis_y,
                self._rotate_custom_axis_z,
                self._rotate_angle
            )
        else:
            self._model.rotate(self._rotate_axis, self._rotate_angle)

    @pyqtSlot(int)
    def rotate_custom_axis_changed(self):
        self._rotate_custom_axis_flag = not self._rotate_custom_axis_flag

    @pyqtSlot(float)
    def rotate_custom_axis_x_changed(self, x):
        self._rotate_custom_axis_x = x

    @pyqtSlot(float)
    def rotate_custom_axis_y_changed(self, y):
        self._rotate_custom_axis_y = y

    @pyqtSlot(float)
    def rotate_custom_axis_z_changed(self, z):
        self._rotate_custom_axis_z = z

    # ================SHRINK===============
    @pyqtSlot(float)
    def shrink_x_changed(self, mx):
        self._shrink_x = mx

    @pyqtSlot(float)
    def shrink_y_changed(self, my):
        self._shrink_y = my

    @pyqtSlot(float)
    def shrink_z_changed(self, mz):
        self._shrink_z = mz

    @pyqtSlot()
    def shrink_flag_change(self):
        self._shrink_flag = not self._shrink_flag
        self.__change_operation_flag(self._shrink_flag, "shrink")

    @pyqtSlot()
    def shrink_clicked(self):
        self._shrink()
        self._model.emit_update_model_signal()

    def _shrink(self):
        if self._shrink_for_point_flag:
            self._model.shrink_along_free_axis(
                self._shrink_for_point_x,
                self._shrink_for_point_y,
                self._shrink_for_point_z,
                self._shrink_x,
                self._shrink_y,
                self._shrink_z,
            )
        else:
            self._model.shrink(self._shrink_x, self._shrink_y, self._shrink_z)

    @pyqtSlot(int)
    def shrink_for_point_changed(self):
        self._shrink_for_point_flag = not self._shrink_for_point_flag

    @pyqtSlot(float)
    def shrink_for_point_x_changed(self, x):
        self._shrink_for_point_x = x

    @pyqtSlot(float)
    def shrink_for_point_y_changed(self, y):
        self._shrink_for_point_y = y

    @pyqtSlot(float)
    def shrink_for_point_z_changed(self, z):
        self._shrink_for_point_z = z

    # ================EXECUTE=============
    @pyqtSlot()
    def execute_clicked(self):
        for elem in self._order_of_operations:
            if elem == "resize":
                self._resize()
            elif elem == "move":
                self._move()
            elif elem == "rotate":
                self._rotate()
            elif elem == "shrink":
                self._shrink()
        self._model.emit_update_model_signal()

    # ================FILES===============

    @pyqtSlot(str)
    def file_picked(self, url):
        self._model.parse_for_url(url)

    @pyqtSlot(str)
    def texture_picked(self, url):
        self._model.set_texture(url)

    @pyqtSlot(str)
    def write_to_file(self, url):
        self._model.load_to_file(url)
