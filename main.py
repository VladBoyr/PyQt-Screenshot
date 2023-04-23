import keyboard
import os.path
import sys
from PIL import ImageGrab
from PyQt6 import QtCore, QtGui, QtWidgets


class SnippingWidget(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(SnippingWidget, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setStyleSheet("background:transparent;")
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

        self.outsideSquareColor = "red"
        self.squareThickness = 2

        self.start_point = QtCore.QPointF()
        self.end_point = QtCore.QPointF()

        self.screenshot_counter = 0

    def screenshot_file_name(self):
        file_name = "screenshot"
        file_ext = "png"
        full_file_name = f"{file_name}.{file_ext}"
        while 1 == 1:
            if os.path.exists(full_file_name):
                self.screenshot_counter += 1
                full_file_name = f"{file_name} ({self.screenshot_counter}).{file_ext}"
            else:
                return full_file_name

    def mousePressEvent(self, event):
        self.start_point = QtCore.QPointF(event.pos())
        self.end_point = QtCore.QPointF(event.pos())
        self.update()

    def mouseMoveEvent(self, event):
        self.end_point = QtCore.QPointF(event.pos())
        self.update()

    def mouseReleaseEvent(self, event):
        r = QtCore.QRectF(self.start_point, self.end_point).normalized()
        self.hide()
        img = ImageGrab.grab(bbox=r.getCoords())
        img.save(self.screenshot_file_name())
        QtWidgets.QApplication.restoreOverrideCursor()
        self.closed.emit()
        self.start_point = QtCore.QPointF()
        self.end_point = QtCore.QPointF()

    def paintEvent(self, event):
        trans = QtGui.QColor(22, 100, 233)
        r = QtCore.QRectF(self.start_point, self.end_point).normalized()
        qp = QtGui.QPainter(self)
        trans.setAlphaF(0.2)
        qp.setBrush(trans)
        outer = QtGui.QPainterPath()
        outer.addRect(QtCore.QRectF(self.rect()))
        inner = QtGui.QPainterPath()
        inner.addRect(r)
        r_path = outer - inner
        qp.drawPath(r_path)
        qp.setPen(QtGui.QPen(QtGui.QColor(self.outsideSquareColor), self.squareThickness))
        trans.setAlphaF(0)
        qp.setBrush(trans)
        qp.drawRect(r)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.button = QtWidgets.QPushButton()
        self.button.clicked.connect(self.activate_snipping)
        self.snipper = SnippingWidget()

    def activate_snipping(self):
        self.snipper.showFullScreen()
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.CrossCursor)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(400, 300)
    keyboard.add_hotkey("print screen", lambda: window.button.click())
    keyboard.add_hotkey("escape", lambda: app.exit())
    sys.exit(app.exec())
