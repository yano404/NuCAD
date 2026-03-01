import numpy as np

class kinema():
    def __init__(self, m1, m2, m3, m4):
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        self.m4 = m4
        self.theta_cm = None
        self.p_cm = None
        self.T3_cm = None
        self.T4_cm = None
        self.theta3_lab = None
        self.theta4_lab = None
        self.T3_lab = None
        self.T4_lab = None
        self.p3_lab = None
        self.p4_lab = None
        self.beta3_lab = None
        self.beta4_lab = None

    def calc(self, T, num=1000, theta_cm=None, theta3_lab=None, theta4_lab=None):
        m1 = self.m1
        m2 = self.m2
        m3 = self.m3
        m4 = self.m4

        # Initialize
        self.__init__(m1, m2, m3, m4)
        
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

        # Calculate theta in the CM
        if theta_cm is not None:
            self.theta_cm = theta_cm
        elif theta3_lab is not None:
            tan3 = np.tan(theta3_lab)
            gtan3 = gamma * tan3
            alpha = np.arctan(1 / gtan3)
            cos_theta_alpha = (- beta_gamma * E3_cm * tan3) / (p_cm * np.sqrt(sq(gtan3)+1))
            mask = np.abs(cos_theta_alpha)<=1
            theta_cm_alpha = np.arccos(cos_theta_alpha[mask])
            alpha = alpha[mask]
            self.theta_cm = np.sort(
                np.concatenate((theta_cm_alpha - alpha, 2*np.pi - theta_cm_alpha - alpha))
            )
        elif theta4_lab is not None:
            tan4 = np.tan(theta4_lab)
            gtan4 = gamma * tan4
            alpha = np.arctan(1 / gtan4)
            cos_theta_alpha = (beta_gamma * E4_cm * tan4) / (p_cm * np.sqrt(sq(gtan4)+1))
            mask = np.abs(cos_theta_alpha)<=1
            theta_cm_alpha = np.arccos(cos_theta_alpha[mask])
            alpha = alpha[mask]
            self.theta_cm =  np.sort(
                np.concatenate((theta_cm_alpha + alpha, - theta_cm_alpha + alpha))
            )
        else:
            self.theta_cm = np.linspace(1e-5, np.pi-1e-5, num)
        theta_cm = self.theta_cm
        
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