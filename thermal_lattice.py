import fault_tolerance_simulations.toric_lattice as toric_lattice
import random
import math


class ThermalLattice(toric_lattice.PlanarLattice):

  def __init__(self,size):
    toric_lattice.PlanarLattice.__init__(self,size)
    self.arraySize = 2*self.size

    self.probability_array={}
    self.probability_list=[]
    self.qubits_for_plaquette={} # qubits associated with each plaquette site
    self.plaquettes_for_qubit={} # plaquettes touching each qubit
    self.dt = 0

    for q in self.positions_Q: 
      self.plaquettes_for_qubit[q]=[]

    for p in self.positions_P:
      p0,p1=p
      qubit_positions=[(p0,(p1+1)%self.arraySize),(p0,(p1-1)%self.arraySize),((p0+1)%self.arraySize,p1),((p0-1)%self.arraySize,p1)]
      self.qubits_for_plaquette[p]=qubit_positions
      for q in qubit_positions:
        self.plaquettes_for_qubit[q]+=[p]


  def gamma(self,beta,omega):
    if omega==0:
      return 1/float(beta)
    else:
      return omega/(1-math.exp(-beta*omega))

  def updateProbabilityList(self,beta=1):
    # takes the probability array and updates it to return a cumulative probability list
    tot = sum([self.gamma(beta,w) for w in self.probability_array.values()])
    self.dt = -math.log(random.random())/tot
    new_array = []
    total = 0
    for q in self.probability_array.keys():
      qval = self.gamma(beta,self.probability_array[q])/tot
      total += qval
      new_array += [[q,total]]
    self.probability_list = new_array

  def updateProbabilityArray(self):
    p_array = {}
    plaquette_values = {}
    for p in self.positions_P:
      pval = 1
      for q in self.qubits_for_plaquette[p]:
        pval = pval *self.array[q[0]][q[1]][0]
      plaquette_values[p]=pval 
       
    for q in self.positions_Q:
      plaquettes = [plaquette_values[p] for p in self.plaquettes_for_qubit[q]]

      if plaquettes in [[1,-1],[-1,1]]:
        p_array[q]= 0
      elif plaquettes == [1,1]:
        p_array[q]=-1
      elif plaquettes==[-1,-1]:
        p_array[q]=1

    self.probability_array=p_array


  def applyThermalNoise(self,beta,time):

    time_count = 0
    for t in range(1000):

      self.updateProbabilityArray()
      self.updateProbabilityList(beta)

      r = random.random()
      qubit_site = None
      for q,v in self.probability_list:
        if r<v:
          qubit_site = q
          break
      self.array[qubit_site[0]][qubit_site[1]][0]*=-1

      time_count += self.dt
      if time_count>time: break

   










