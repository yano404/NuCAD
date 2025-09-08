import math
from OCP.gp import gp_XYZ, gp_Pnt, gp_Vec, gp_Dir, gp_Lin, gp_Ax1, gp_Ax2
from ..types import Real, Vector3


def pol2xyz(r: Real, theta: Real, phi: Real) -> Vector3:
    x = r * math.sin(theta) * math.cos(phi)
    y = r * math.sin(theta) * math.sin(phi)
    z = r * math.cos(theta)
    return (x, y, z)


def xyz2pol(x: Real, y: Real, z: Real) -> Vector3:
    r = math.sqrt(x**2 + y**2 + z**2)
    theta = 0.0
    phi = 0.0
    if r != 0:
        theta = math.acos(z / r)
        phi = math.copysign(1,y) * math.acos(x/math.sqrt(x**2+y**2))
    return (r, theta, phi)


def xyz(x: Real, y: Real, z: Real) -> Vector3:
    return (x,y,z)


def pol(r: Real, theta: Real, phi: Real) -> Vector3:
    return pol2xyz(r, theta, phi)


class XYZ(gp_XYZ):
    '''
    Wrapper of gp_XYZ
    '''
    pass


class Pnt(gp_Pnt):
    '''
    Wrapper of gp_Pnt
    '''
    pass


class Vec(gp_Vec):
    '''
    Wrapper of gp_Vec
    '''
    pass

class Dir(gp_Dir):
    '''
    Wrapper of gp_Dir
    '''
    pass


class Ax1(gp_Ax1):
    '''
    Wrapper of gp_Ax1
    '''
    pass


class Ax2(gp_Ax2):
    '''
    Wrapper of gp_Ax2
    '''
    pass


class Lin(gp_Lin):
    '''
    Wrapper of gp_Lin
    '''
    pass


