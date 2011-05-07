from PyFinModel import PyFinModel, ModelProperties
from functools import partial as functools_partial
from math import exp, sqrt
from numpy import zeros, flipud

class BinomialTreeModel(PyFinModel):
  def __init__(self, data):
    self.properties = ModelProperties([["s0", 100, "Spot Price"], ["r", 0.06, "Interest Rate"], 
                                       ["v", 0.2, "Volatility"], ["t", 1, "Time to Maturity"], 
                                       ["k", 100, "Strike Price"], ["n", 150, "Number of steps in the Binomial tree"]])
    PyFinModel.__init__(self, data)
  
  def getProperties(self):
    return self.properties.getPropertyList()
  
  def getModelName(self):
    return "Binomial Tree Model"
  
  def getModelLink(self):
    return "http://www.google.com"
  
  def getActions(self):
    runModel = functools_partial(BinomialTreeModel.runModel, self)
    return {"Run Model": runModel}
  
  def setupProperties(self, prop):
    for x in prop.keyval:
      self.__dict__[x] = prop.keyval[x]
      
    
  def runModel(self, prop):
    self.setupProperties(self.properties)

    dt = float(self.t)/self.n
    nu = self.r - 0.5 * pow(self.v, 2)
    dxu = sqrt(pow(self.v, 2) * dt + pow((nu * dt), 2))
    dxd = -dxu
    pu = 0.0
    pu = round(0.5 + 0.5 * nu * dt/dxu, 4)
    pd = round(1 - pu, 4)
    
    disc = round(exp(-self.r * dt), 4)
    nodes = self.n + 1
    
    ##initialize asset prices at maturity
    st = zeros(nodes)
    
    st[0] = self.s0 * exp(self.n * dxd)
    for i in range(1, nodes):
      st[i] = st[i-1] * exp(dxu - dxd)
    
    ##initialize options value at maturity
    C = zeros((nodes, nodes))
    for i in range(0, nodes):
      C[i, self.n] = max(0.0, st[i] - self.k)
    
    ##step back in the tree
    for timestep in range (self.n - 1, -2, -1):
      for node in range(0, timestep + 1):
        C[node, timestep] = disc * ((pu * C[node + 1, timestep + 1]) + (pd * C[node, timestep + 1]))
        
    C = flipud(C)
    self.show2DData("European Call Option Prices", C)
    