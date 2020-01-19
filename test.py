from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import layout
import serial.tools.list_ports
import pyqtgraph
import time
import math
import pyqtgraph as pg
def SerialPorts():
    PortList = serial.tools.list_ports.comports()

    return [i.device for i in PortList]

class PIDApp(QtWidgets.QMainWindow, layout.Ui_MainWindow):
    def __init__(self, parent=None):
        super(PIDApp, self).__init__(parent)
        self.setupUi(self)
        self.StartButton.clicked.connect(self.StartButtonClick)
        self.StopButton.clicked.connect(self.StopButtonClick)
        self.RefreshPortButton.clicked.connect(self.RefreshPortList)
        self.PortDropDownList.activated[str].connect(self.PortDropDownListOption)
        self.SetPointSendButton.clicked.connect(self.SetPointSendButtonClick)
        self.KpSendButton.clicked.connect(self.KpSendButtonClick)
        self.KiSendButton.clicked.connect(self.KiSendButtonClick)
        self.KdSendButton.clicked.connect(self.KdSendButtonClick)
        self.SetPointSpinBox.valueChanged.connect(self.SetPointChanged)
        self.KpSpinBox.valueChanged.connect(self.KpChanged)
        self.KiSpinBox.valueChanged.connect(self.KiChanged)
        self.KdSpinBox.valueChanged.connect(self.KdChanged)
        self.SetPoint = 0
        self.Kp = 0
        self.Ki = 0
        self.Kd = 0
        self.timer = pg.QtCore.QTimer(self)
        self.prev_i = 0

    def update_plot(self):
        X = [float(i/0.01) for i in range(self.prev_i, self.prev_i+2000)]
        self.prev_i = self.prev_i + 2000
        Y = [math.sin(X[i]) for i in range(2000)]
        Y1 = [math.cos(X[i]) for i in range(2000)]
        CenterPoint = self.prev_i - 1000
        self.PlotWidgetUpLeft.setXRange(float(CenterPoint-5)/0.01, float(CenterPoint+5)/0.01)
        self.PlotWidgetUpRight.setXRange(float(CenterPoint-5)/0.01, float(CenterPoint+5)/0.01)
        self.PlotWidgetBottomLeft.setXRange(float(CenterPoint-5)/0.01, float(CenterPoint+5)/0.01)
        self.PlotWidgetBottomCenter.setXRange(float(CenterPoint-5)/0.01, float(CenterPoint+5)/0.01)
        self.PlotWidgetBottomRight.setXRange(float(CenterPoint-5)/0.01, float(CenterPoint+5)/0.01)
        
        time.sleep(0.01)
        self.PlotWidgetUpLeft.plot(X,Y, clear=True)
        self.PlotWidgetUpRight.plot(X,Y1, clear=True)
        self.PlotWidgetBottomLeft.plot(X,Y, clear=True)
        self.PlotWidgetBottomCenter.plot(X,Y1, clear=True)
        self.PlotWidgetBottomRight.plot(X,Y, clear=True)


    def StartButtonClick(self):
        print("start button clicked")
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(0)

    def StopButtonClick(self):
        self.timer.stop()
        print("stop button clicked")

    def RefreshPortList(self):
        self.PortDropDownList.clear()
        self.PortDropDownList.addItems(SerialPorts())

    def PortDropDownListOption(self, text):
        print("option selected: {}".format(text))

    def SetPointSendButtonClick(self):
        print("set point: {}".format(self.SetPoint))

    def KpSendButtonClick(self):
        self.KpLabel.setText(self.KpLabel.text()[0:8] + str(self.Kp))
        print("kp: {}".format(self.Kp))

    def KiSendButtonClick(self):
        self.KiLabel.setText(self.KiLabel.text()[0:8] + str(self.Ki))
        print("ki: {}".format(self.Ki))
    
    def KdSendButtonClick(self):
        self.KdLabel.setText(self.KdLabel.text()[0:8] + str(self.Kd))
        print("kd: {}".format(self.Kd))

    def SetPointChanged(self):
        self.SetPoint = self.SetPointSpinBox.value()

    def KpChanged(self):
        self.Kp = self.KpSpinBox.value()
   
    def KiChanged(self):
        self.Ki = self.KiSpinBox.value()

    def KdChanged(self):
        self.Kd = self.KdSpinBox.value()
# https://www.youtube.com/watch?v=Y-8N1dPFsVE to dynamically resize

def main():
    app = QApplication(sys.argv)
    form = PIDApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()