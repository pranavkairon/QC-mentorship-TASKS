from pyquil.quil import Program
import pyquil.api as api
from pyquil.gates import *
qvm = api.QVMConnection()
from grove.pyvqe.vqe import VQE
from scipy.optimize import minimize
import numpy as np
#Ansatz ie. Psi(theta)
def ansatz(p):
    return Program(H(0),RZ(p,0),CNOT(0, 1),X(1))
#Given matrix in its Pauli decoposition form
from pyquil.paulis import sZ,sX,sY,sI
initial_angle = 0
hamiltonian = (sY(0)*sY(1)+sX(0)*sX(1)+sZ(0)*sZ(1)-sI(0)*sI(1))*0.5
print(hamiltonian)

#Running the VQE minimizer
vqe_inst = VQE(minimizer=minimize,
               minimizer_kwargs={'method': 'nelder-mead'})
angle_range = np.linspace(0, 2 * np.pi, 20)
data = [vqe_inst.expectation(ansatz(angle), hamiltonian, None, qvm)
        for angle in angle_range]
#plotting the graph between parameter theta and Expectation value <psi(theta)|H|psi(theta)>
import matplotlib.pyplot as plt
plt.xlabel('Angle [radians]')
plt.ylabel('Expectation value')
plt.plot(angle_range, data)
plt.show()
print("Minimum Eignenvalue possible :",np.min(data))