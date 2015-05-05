from numpy import *

from C_type_conics import C_type_conics


def Revol_Tangent(revol_type, tang_alpha, blend_num):
    '''
    % ------------------------------------------------------------------------------------------------
    % Revol_Tangent function generate the control mesh of revolution
    % Revolutions can be seen as a surface obtained by revoluting a curve
    % round one coordinate axis (only condering a curve in XY-plane revoluting around y-axis
    % input parameters:
    % revol_type: the type of revolution conic(1), cylinder(2), sphere(3),
    % hyperbola(4), parabola(5)
    % blend_num: the order of this revolution as a base surface for blending
    % (taking values 1 or 2)
    % ------------------------------------------------------------------------------------------------
    '''

    '''
    % constructing the control mesh of the revolution surface according to the
    % control polygon of a curve
    '''
    P,u0 = C_type_conics(revol_type)

    v = u0
    l = len(P[0,:,0])
    RevolCP = zeros( (l, 6, 3) )
    for i in range(6):
        RevolCP[:,i,:] = P[:,:,:]

    for i in range(6):
        theta = i * pi / 2 + pi / 4
        t = transpose
        RevolCP[:,i,0] = t(P[0,:,0]) * cos(theta) + t(P[0,:,2])*sin(theta)
        RevolCP[:,i,2] = t(P[0,:,0]) * (-sin(theta)) + t(P[0,:,2])*cos(theta)
    #TangCP = empty( ( 1,6,3) )
    TangCP = tang_alpha * ( RevolCP[-1,:,:] - RevolCP[-2, :, :]) + RevolCP[-2,:,:]

    #if revol_type == 'circular':
        #RevolCP = RevolCP[:,::-1,:]
    # if revol_type == 'parabola':
    #     print(RevolCP)

        # RevolCP = RevolCP[::-1, ::-1, :]
        # print("revoled: ")
        # print(RevolCP)

    return RevolCP,v
