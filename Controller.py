from PyQt6.QtCore import QObject, pyqtSlot


class Controller(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model

    # ================RESIZE===============
    @pyqtSlot(float)
    def resize_coefficient_changed(self, c):
        print(c)
        pass

    # ================MOVE===============
    @pyqtSlot(float)
    def move_x_changed(self, mx):
        print(mx)
        pass

    @pyqtSlot(float)
    def move_y_changed(self, my):
        print(my)
        pass

    @pyqtSlot(float)
    def move_z_changed(self, mz):
        print(mz)
        pass

    # ================ROTATE===============
    @pyqtSlot(float)
    def rotate_angle_changed(self, angle):
        print(angle)
        pass

    @pyqtSlot(int)
    def rotate_axis_changed(self, axis):
        print(axis)
        pass

    # ================SHRINK===============
    @pyqtSlot(float)
    def shrink_x_changed(self, mx):
        print(mx)
        pass

    @pyqtSlot(float)
    def shrink_y_changed(self, my):
        print(my)
        pass

    @pyqtSlot(float)
    def shrink_z_changed(self, mz):
        print(mz)
        pass
