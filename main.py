import keyboard
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
        img.save("testImage.png")
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
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        self.label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.button = QtWidgets.QPushButton('Делать скриншот')
        self.button.clicked.connect(self.activate_snipping)

        layout = QtWidgets.QVBoxLayout(self.centralWidget)
        layout.addWidget(self.label, 1)
        layout.addWidget(self.button, 0)

        self.snipper = SnippingWidget()
        self.snipper.closed.connect(self.on_closed)
        keyboard.add_hotkey("print screen", lambda: self.button.click())

    def activate_snipping(self):
        self.snipper.showFullScreen()
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.CrossCursor)
        self.hide()

    def on_closed(self):
        pixmap = QtGui.QPixmap("testImage.png")
        self.label.setPixmap(pixmap)
        self.show()
        self.adjustSize()


def test(main_window):
    print(main_window.button)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec())
