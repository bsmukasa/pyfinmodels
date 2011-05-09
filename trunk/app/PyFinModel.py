from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt4 import QtGui, QtCore

import matplotlib as mpl

class MdlProp:
  data_type = {0: str, 1: int, 2: long, 3: float}
  def __init__(self, name, val, type, tooltip):
    self._name = name
    self._val = val
    self._type = type
    self._tooltip = tooltip
    pass

  def name(self):
    return self._name

  def tooltip(self):
    return self._tooltip

  def type(self):
    return self._type
  
  def setVal(self, val):
    self._val = MdlProp.data_type[self.type()](val)

  def val(self):
    return MdlProp.data_type[self.type()](self._val)

class ModelProperties:
  def __init__(self, props):
    self.propval = {}
    for prop in props:
      self.propval[prop.name()] = prop
      
  def getProps(self):
    return self.propval.iterkeys()

  def getPropHelp(self, key):
    return self.propval[key].tooltip()
  
  def getPropVal(self, key):
    try:
      return self.propval[key].val()
    except KeyError:
      raise NameError

  def setPropVal(self, key, val):
    self.propval[key].setVal(val)
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
  def __init__(self, properties, appWindow):
    self._appWindow = appWindow
    self._properties = properties

  def setupProperties(self, prop):
    for x in prop.getProps():
      self.__dict__[x] = prop.getPropVal(x)

  def raiseABCError(self):
    raise 'Abstract Method Invoked!'

  def hasGraphs(self):
    return False
  
  def getModelName(self):
    self.raiseABCError()

  def getModelLink(self):
    self.raiseABCError()

  def getModelActions(self):
    self.raiseABCError()

  def show1DData(self, name, array):
    self._appWindow.add1DData(name, array)

  def show2DData(self, name, array):
    self._appWindow.add2DData(name, array)

  def addGraph(self, name, pyFinChart):
    self._appWindow.add2DGraph(name, pyFinChart)

  def getProperties(self):
    return self._properties
  
  def notifyState(self, pct, text):
    self.raiseABCError()