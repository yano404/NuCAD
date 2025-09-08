

class Particle(object):
    def __init__(self, Z, A, mass=None, T=0, Ex=0) -> None:
        self.Z = Z
        self.A = A
        self.mass = mass
        self.T = T
        self.Ex = Ex