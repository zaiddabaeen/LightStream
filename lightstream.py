#!/usr/bin/python
import sys, os, gtk
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from subprocess import call

padding = 32
size = 512
_path = os.path.split(os.path.abspath(__file__))[0] + "/"

print(_path)
class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
        QShortcut(QKeySequence("Ctrl+W"), self, self.close)

        size = gtk.gdk.screen_width()/6

        self.setWindowTitle('Light Stream')
        self.setFixedSize(size, size)
        self.createWidgets()
        self.setAcceptDrops(True)

    def createWidgets(self):
        self.resize(size, size)
        self.pic = QLabel(self)
        self.pic.move(padding, padding)
        self.setMagnetImage(False)
        self.setWidgetSize()

        self.status = QLabel(self)
        self.status.setText("Drag a magnet or torrent")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setFixedWidth(size + 2 * padding)
        self.status.setStyleSheet("QLabel { background-color: #ddd; }")
        self.status.setFixedHeight(50)
        self.status.move(0, 0)

    def setStatus(self, text):
        self.status.setText(text)

    def setMagnetImage(self, enabled):
        if enabled:
            self.qpixmap = QPixmap(_path + "magnet.png")
        else:
            self.qpixmap = QPixmap(_path + "magnet_x.png")

        self.pic.setPixmap(self.qpixmap)
        self.setWidgetSize()

    def dragEnterEvent(self, e):
        self.setStatus("Drag a magnet or torrent")

        if e.mimeData().hasFormat('text/plain'):
            e.accept()

            self.setMagnetImage(True)
        else:
            e.ignore()

    def dragLeaveEvent(self, QDragLeaveEvent):
        self.setMagnetImage(False)
        self.setWidgetSize()

    def dropEvent(self, e):
        magnet = e.mimeData().text()
        if "magnet:" in magnet:
            call([_path + "torrentstream", "\""+ magnet + "\""])

        elif e.mimeData().hasUrls():
            path = None
            for url in e.mimeData().urls():
                path = url.toLocalFile().toLocal8Bit().data()
                print(path)
                break

            if path is None or ".torrent" not in path:
                self.setStatus("Not a valid torrent or magnet")
            else:
                call([_path + "./torrentstream", path])

        else:
            self.setStatus("Not a valid torrent or magnet")

        # self.setWindowTitle(e.mimeData().text())

        self.setMagnetImage(False)
        self.setWidgetSize()

    def resizeEvent(self, e):
        # Does not work
        if self.width() < 200:
            e.ignore
            return

        self.resize(self.width(), self.width())
        self.setWidgetSize()

    def setWidgetSize(self):
        self.pic.resize(self.width()-padding*2, self.height()-padding*2)
        self.qpixmap = self.qpixmap.scaledToWidth(self.width()-padding*2).scaledToHeight(self.height()-padding*2)
        self.pic.setPixmap(self.qpixmap)


# create our window
app = QApplication(sys.argv)
app.setWindowIcon(QIcon(_path + "magnet.png"))
w = Window()
# Show the window and run the app
w.show()
app.exec_()