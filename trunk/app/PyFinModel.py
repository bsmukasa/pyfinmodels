from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt4 import QtGui, QtCore

import matplotlib as mpl

class ModelProperties:
  def __init__(self, list):
    self.list = list
    self.keyval = {}
    for x in list:
      self.keyval[x[0]] = x[1]

  def getPropertyList(self):
    return self.list

  def getPropertyValue(self, key):
    try:
      return self.keyval[key] 
    except KeyError:
      raise NameError

  def setPropertyValue(self, key, val):
    self.keyval[key] = val
    pass

class PyFinChart(FigureCanvas):
  def __init__(self):
    mpl.rcParams['font.size'] = 6
    mpl.rcParams['axes.grid'] = True
    self.fig = Figure(figsize=(3, 3), dpi=100)
    FigureCanvas.__init__(self, self.fig)
    self.setSizePolicy(QtGui.QSizePolicy.Expanding,
                       QtGui.QSizePolicy.Expanding)
    self.axes = self.fig.add_subplot(111)
    self.axes.set_aspect('equal')
    FigureCanvas.updateGeometry(self)

  def addLinePlot(self, xval, yval):
    self.axes.plot(xval, yval)

class PyFinModel:
  def __init__(self, appWindow):
    self.appWindow = appWindow

  def raiseABCError(self):
    raise "Abstract Method Invoked!"

  def getModelName(self):
    self.raiseABCError()

  def getModelLink(self):
    self.raiseABCError()

  def getProperties(self):
    self.raiseABCError()

  def getActions(self):
    self.raiseABCError()

  def show1DData(self, name, array):
    self.appWindow.add1DData(name, array)

  def show2DData(self, name, array):
    self.appWindow.add2DData(name, array)

  def addGraph(self, name, pyFinChart):
    self.appWindow.add2DGraph(name, pyFinChart)

  def notifyState(self, pct, text):
    self.raiseABCError()