import sys
from PyQt4 import QtGui, QtCore
from MainWindow import Ui_MainWindow
from models.BinomialTreeModel import BinomialTreeModel
from functools import partial as functools_partial

class QPropertyVal(QtGui.QTableWidgetItem):
  def __init__(self, text):
    QtGui.QTableWidgetItem.__init__(self, text)

  def setAssociatedProperty(self, name):
    self.name = name

  def associatedProperty(self):
    return self.name

class PyFinModelsApp(QtGui.QMainWindow) :
  def __init__(self) :
    QtGui.QMainWindow.__init__(self)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.chartrow = 0
    self.chartcol = 0
    self.ui.frmNotify.hide()
    self.sheetrow = 0
    self.propertyChanged = functools_partial(PyFinModelsApp.propertyChangeEvent, self)
    self.connect(self.ui.tblSheet, QtCore.SIGNAL('itemChanged(QTableWidgetItem *)'), self.propertyChangeEvent)

  def propertyChangeEvent(self, item):
    if isinstance(item, QPropertyVal):
      self.modelProperties.setPropVal(item.associatedProperty(), item.text())
  
  def getSheet(self) :
    return self.ui.tblSheet

  def getCodeEditor(self) :
    return self.ui.txtCode

  def getModelHintsTextbox(self) :
    return self.ui.txtModelHints

  def addProperties(self, mprops) :
    col = 0
    self.modelProperties = mprops
    props = mprops.getProps()
    for key in props :
      itemKey = QtGui.QTableWidgetItem(key)
      itemKey.setBackground(QtGui.QBrush(QtGui.QColor('Gray')))
      fnt = itemKey.font()
      itemKey.setToolTip(mprops.getPropHelp(key))
      fnt.setWeight(QtGui.QFont.Bold)
      itemKey.setFont(fnt)
      itemKey.setFlags(QtCore.Qt.ItemIsEnabled)
      self.getSheet().setItem(self.sheetrow, col, itemKey)

      itemVal = QPropertyVal(str(mprops.getPropVal(key)))
      itemVal.setAssociatedProperty(key)
      itemVal.setBackground(QtGui.QBrush(QtGui.QColor("Red")))
      itemVal.setToolTip(mprops.getPropHelp(key))
      self.getSheet().setItem(self.sheetrow, col + 1, itemVal)
      self.sheetrow += 1

  def addModelActions(self, actionDict) :
    col = 0
    for x in actionDict :
      btn = QtGui.QPushButton(x, self.getSheet())
      btn.setFont(self.getSheet().font())
      ahandler = functools_partial(PyFinModelsApp.actionHandler, self, actionDict[x])
      self.connect(btn, QtCore.SIGNAL('clicked(bool)'), ahandler)
      self.getSheet().setCellWidget(self.sheetrow, col, btn)
      col += 1

  def actionHandler(self, actionTarget):
    actionTarget(self.modelProperties)
    pass
  
  def add1DData(self, name, data) :
    self.sheetrow += 1
    col = 0
    for x in data :
      item = QtGui.QTableWidgetItem(x)
      item.setBackground(QtGui.QBrush(QtGui.QColor("Brown")))
      item.setFlags(QtCore.Qt.ItemIsEnabled)
      self.getSheet().setItem(self.sheetrow, col, item)
      col += 1

  def showOutputHeading(self, name) :
    self.sheetrow += 1
    itemKey = QtGui.QTableWidgetItem(name)
    itemKey.setBackground(QtGui.QBrush(QtGui.QColor("Pink")))
    fnt = itemKey.font()
    fnt.setWeight(QtGui.QFont.Bold)
    itemKey.setFont(fnt)
    itemKey.setFlags(QtCore.Qt.ItemIsEnabled)
    self.getSheet().setItem(self.sheetrow, 0, itemKey)

  def add2DData(self, name, data) :
    self.showOutputHeading(name)
    col = 0
    for x in data :
      self.sheetrow += 1
      col = 0
      for y in x :
        item = QtGui.QTableWidgetItem(str(y))
        item.setBackground(QtGui.QBrush(QtGui.QColor(255, 100, 100)))
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.getSheet().setItem(self.sheetrow, col, item)
        col += 1

  def add2DChart(self, name, pyFinChart) :
    self.ui.chartGrid.addWidget(pyFinChart, self.chartrow, self.chartcol)
    if self.chartcol == 3 :
      self.chartrow += 1
      self.chartcol = 0
    else :
      self.chartcol += 1

  def loadModel(self, model) :
    self.getSheet().clearContents()
    self.addProperties(model.getProperties())
    self.addModelActions(model.getModelActions())

def main():
  app = QtGui.QApplication(sys.argv)
  window = PyFinModelsApp()
  model = BinomialTreeModel(window)
  window.loadModel(model)
  window.show()
  sys.exit(app.exec_())
  
if __name__ == "__main__" :
  main()