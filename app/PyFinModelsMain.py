import sys
from PyQt4 import QtGui, QtCore
from MainWindow import Ui_MainWindow
from models.BinomialTreeModel import BinomialTreeModel


class PyFinModelsApp(QtGui.QMainWindow):
  def __init__(self):
    QtGui.QMainWindow.__init__(self)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.chartrow = 0
    self.chartcol = 0
    self.ui.frmNotify.hide()
    self.sheetrow = 0

  def getSheet(self):
    return self.ui.tblSheet

  def getCodeEditor(self):
    return self.ui.txtCode

  def getModelHintsTextbox(self):
    return self.ui.txtModelHints

  def addProperties(self, propList):
    col = 0
    for x in propList:
      itemKey = QtGui.QTableWidgetItem(x[0])
      itemKey.setBackground(QtGui.QBrush(QtGui.QColor(200, 200, 200)))
      fnt = itemKey.font()
      itemKey.setToolTip(x[2])
      fnt.setWeight(QtGui.QFont.Bold)
      itemKey.setFont(fnt)
      itemKey.setFlags(QtCore.Qt.ItemIsEnabled)
      self.getSheet().setItem(self.sheetrow, col, itemKey)

      itemVal = QtGui.QTableWidgetItem(str(x[1]))
      itemVal.setBackground(QtGui.QBrush(QtGui.QColor(200, 50, 10)))
      itemVal.setToolTip(x[2])
      self.getSheet().setItem(self.sheetrow, col+1, itemVal)
      self.sheetrow += 1

  def addModelActions(self, actionDict):
    col = 0

    for x in actionDict:
      btn = QtGui.QPushButton(x, self.getSheet())
      btn.setFont(self.getSheet().font())
      self.connect(btn, QtCore.SIGNAL('clicked(bool)'), actionDict[x])
      self.getSheet().setCellWidget(self.sheetrow, col, btn)
      col += 1        

  def add1DData(self, name, data):
    self.sheetrow += 1
    col = 0
    for x in data:
      item = QtGui.QTableWidgetItem(x)
      item.setBackground(QtGui.QBrush(QtGui.QColor(0, 150, 150)))
      item.setFlags(QtCore.Qt.ItemIsEnabled)
      self.getSheet().setItem(self.sheetrow, col, item)
      col += 1

  def showOutputHeading(self, name):
    self.sheetrow += 1
    itemKey = QtGui.QTableWidgetItem(name)
    itemKey.setBackground(QtGui.QBrush(QtGui.QColor(200, 100, 100)))
    fnt = itemKey.font()
    fnt.setWeight(QtGui.QFont.Bold)
    itemKey.setFont(fnt)
    itemKey.setFlags(QtCore.Qt.ItemIsEnabled)
    self.getSheet().setItem(self.sheetrow, 0, itemKey)


  def add2DData(self, name, data):
    self.showOutputHeading(name)
    col = 0
    for x in data:
      self.sheetrow += 1
      col = 0
      for y in x:
        item = QtGui.QTableWidgetItem(str(y))
        item.setBackground(QtGui.QBrush(QtGui.QColor(255, 100, 100)))
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.getSheet().setItem(self.sheetrow, col, item)
        col += 1

  def add2DChart(self, name, pyFinChart):
    self.ui.chartGrid.addWidget(chart, self.chartrow, self.chartcol)
    if (self.chartcol == 3):
      self.chartrow += 1
      self.chartcol = 0
    else:
      self.chartcol += 1

  def loadModel(self, model):
    self.getSheet().clearContents()
    self.addProperties(model.getProperties())
    self.addModelActions(model.getActions())


if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  window = PyFinModelsApp()
  model = BinomialTreeModel(window)
  window.loadModel(model)
  window.show()
  sys.exit(app.exec_())