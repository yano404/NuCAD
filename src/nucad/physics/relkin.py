import numpy as np

class kinema():
    def __init__(self, m1, m2, m3, m4, num=1000):
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        self.m4 = m4
        self.theta_cm = np.linspace(1e-5, np.pi-1e-5, num)
        self.p_cm = 0.0
        self.T3_cm = 0.0
        self.T4_cm = 0.0
        self.theta3_lab = np.zeros(num)
        self.theta4_lab = np.zeros(num)
        self.T3_lab = np.zeros(num)
        self.T4_lab = np.zeros(num)
        self.p3_lab = np.zeros(num)
        self.p4_lab = np.zeros(num)
        self.beta3_lab = np.zeros(num)
        self.beta4_lab = np.zeros(num)

    def calc(self, T):
        m1 = self.m1
        m2 = self.m2
        m3 = self.m3
        m4 = self.m4
        theta_cm = self.theta_cm
        
        sq = lambda x : np.power(x,2)

        # mandelstam variable s
        s = sq(m1 + m2) + 2*m1*T
        # Momentum in the CM
        pcm12 = np.sqrt( (sq(s - sq(m1) - sq(m2)) - 4*sq(m1)*sq(m2)) / (4*s) )
        gamma = np.sqrt(sq(m1) + sq(pcm12)) / m1 # coshX
        beta_gamma = pcm12 / m1 # sinhX

        # Energy of particles 3 & 4 in CM
        E3_cm = ( s + (sq(m3) - sq(m4)) ) / (2 * np.sqrt(s))
        E4_cm = ( s - (sq(m3) - sq(m4)) ) / (2 * np.sqrt(s))
        
        # Kinetic energy of particles 3 & 4 in CM
        self.T3_cm = E3_cm - m3
        self.T4_cm = E4_cm - m4
        
        # Momentum in the CM
        self.p_cm = np.sqrt( (sq(s - sq(m3) - sq(m4)) - 4*sq(m3)*sq(m4)) / (4*s) )
        p_cm = self.p_cm
        
        # Energy of particles 3 & 4 in Lab
        E3_lab = gamma * E3_cm + beta_gamma * p_cm * np.cos(theta_cm)
        E4_lab = gamma * E4_cm - beta_gamma * p_cm * np.cos(theta_cm)
        
        # Kinetic energy of particles 3 & 4 in Lab
        self.T3_lab = E3_lab - m3
        self.T4_lab = E4_lab - m4
        
        # Momentum in Lab
        p3cos = gamma * p_cm * np.cos(theta_cm) + E3_cm * beta_gamma
        p4cos = - gamma * p_cm * np.cos(theta_cm) + E4_cm * beta_gamma
        p3sin = p_cm * np.sin(theta_cm)
        p4sin = p_cm * np.sin(theta_cm)
        self.p3_lab = np.sqrt(sq(p3cos) + sq(p3sin))
        self.p4_lab = np.sqrt(sq(p4cos) + sq(p4sin))

        # Beta in Lab
        gamma3_lab = E3_lab/m3
        gamma4_lab = E4_lab/m4
        self.beta3_lab = np.sqrt( (sq(gamma3_lab) - 1)/sq(gamma3_lab) )
        self.beta4_lab = np.sqrt( (sq(gamma4_lab) - 1)/sq(gamma4_lab) )

        # Theta in Lab
        self.theta3_lab = np.arctan(p3sin/p3cos)
        self.theta4_lab = np.arctan(p4sin/p4cos)