from typing import Optional
import numpy as np
from nucad.types import Real

class Particle(object):
    def __init__(
            self,
            mass, # MeV
            charge,
            T=0, # MeV
            charge_state=None):
        self.mass = mass
        self.charge = charge
        self.kinetic_energy = T
        self.charge_state = charge
        if charge_state:
            self.charge_state = charge_state
    
    @property
    def A(self):
        return self.mass / 931.49410372 # MeV/u

    @A.setter
    def A(self, a):
        self.mass = a * 931.49410372 # MeV/u

    @property
    def Z(self):
        return self.charge

    @Z.setter
    def Z(self, z):
        self.charge = z
        self.charge_state = z
    
    def T(self, t: Optional[Real] = None):
        if t is None:
            return self.kinetic_energy
        else:
            self.kinetic_energy = t
            return self
    
    def p(self, k: Optional[Real] = None):
        if k is None:
            return self.T2p(self.kinetic_energy)
        else:
            self.kinetic_energy = self.p2T(k)
            return self
    
    def beta(self, b: Optional[Real] = None):
        if b is None:
            return self.T2b(self.kinetic_energy)
        else:
            self.kinetic_energy = self.b2T(b)
            return self

    def T2p(self, T) -> Real:
        m = self.mass
        return np.sqrt(np.square(T+m) - np.square(m))
    
    def p2T(self, p) -> Real:
        m = self.mass
        return np.sqrt(np.square(p) + np.square(m)) - m
    
    def T2b(self, T) -> Real:
        m = self.mass
        g = (T+m) / m
        return np.sqrt(1 - 1/np.square(g))
    
    def b2T(self, b) -> Real:
        m = self.mass
        g = 1 / np.sqrt(1 - np.square(b))
        return (g - 1) * m

    def gamma(self) -> Real:
        m = self.mass
        t = self.kinetic_energy
        return (t+m) / m
    
    def tof(self, L: Real, beta = None) -> Real:
        b = self.beta()
        if beta:
            b = beta
        return L * 1e6 / (b * 299_792_458.0) # ns
