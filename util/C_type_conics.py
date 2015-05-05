from numpy import *

import printAsMatlab


def cone():


    '''
    % -------------------------------------------------------------------------
    % Ploting line from i*l to (i+1)*l and so on.
    % The parametric equation of the line is
    % x=t; y=a*t+b;
    % t\in[i*l,(i+1)*l]; u0=1;
    % -------------------------------------------------------------------------
    %         a = input('Please input the coefficency of quadratic item a:');
    %         b = input('Please input the coefficency of linear item b:');
    %         c = input('Please input the constant item c:');
    %         l = input('Please input the interval length l:');
    %         i0= input('Please input the start interval number i0:');
    %         n = input('Please input the number of pieces you want to plot n:');
    '''
    a = -1
    b = 0
    l = pi / 2
    i0 = 0
    n = 2

    omega = 1
    u0 = cos(omega * l / 2.0)
    P = empty((1, i0 + n + 2, 3))

    indexs = range(i0 + n + 2)
    max = len(indexs) - 1
    indexs.reverse()
    for i in indexs:
        P[0, max - i, 0] = (i ) * l
        P[0, max - i, 1] = (i ) * l * a + b
        P[0, max - i, 2] = 0
    return (P, u0)


def cylinder():
    '''
	% -------------------------------------------------------------------------
	   % Ploting line from i*l to (i+1)*l and so on. 
	   % The parametric equation of the line is
	   % x=c; y=t;
	   % t\in[i*l,(i+1)*l]; u0=1;
	   % -------------------------------------------------------------------------
	%         a = input('Please input the coefficency of quadratic item a:');
	%         b = input('Please input the coefficency of linear item b:');
	%         c = input('Please input the constant item c:');
	%         l = input('Please input the interval length l:');
	%         i0= input('Please input the start interval number i0:');
	%         n = input('Please input the number of pieces you want to plot n:');
	'''
    c = 1
    l = pi / 2
    i0 = -1
    n = 1

    omega = 1
    u0 = cos(omega * l / 2)
    P = empty((1, 3, 3))
    indexs = range(3)

    for i in indexs:
        P[0, i, 0] = c
        P[0, i, 1] = (i - 1 - 1 / 2.0) * l
        P[0, i, 2] = 0
    return P, u0


def circular():
    '''
	% -------------------------------------------------------------------------
        % Ploting Lissajous curve from i*l to (i+1)*l and so on. 
        % The parametric equation of the arc is:
        % x=r1*sin(omega*t+omega*det); y=r2*sin(omega*t);
        % t\in[i*l,(i+1)*l]; u0=cos(omega*l/2);
        % -------------------------------------------------------------------------
	'''
    omega = 1
    det = pi / 2
    r1 = 1
    r2 = 1
    l = pi / 2
    i0 = 0
    n = 2
    u0 = cos(omega * l / 2)  # computing the initial subdivision parameter
    dett = -2 * sin(omega * l / 2) / (omega * l * (u0 ** 2))  # omega*l*sin(omega*l/2)/(2*u0^2)
    P = empty((1, i0 + n + 1 + 1, 3))
    indexs = range(i0 + n + 1 + 1)
    max = len(indexs) - 1
    indexs.reverse()
    for i in indexs:
        P[0, i, 0] = r1 * dett * sin(omega * ((i - 1 / 2.0) * l + det))
        P[0, i, 1] = r2 * dett * sin(omega * ((i - 1 / 2.0) * l))
        P[0, i, 2] = 0

    P[0,:,:]

    return P, u0


def hyperbola():
    '''
	 % -------------------------------------------------------------------------
        % Ploting hyperbola from i*l to (i+1)*l and so on. 
        % The parametric equation of the arc is:
        % x=a*cosh(omega*t); y=b*sinh(omega*t);
        % t\in[i*l,(i+1)*l]; u0=cosh(omega*l/2);
        % -------------------------------------------------------------------------
	'''
    omega = 1
    a = 1
    b = 1
    l = pi / 2
    i0 = -1
    n = 2
    u0 = cosh(omega * l / 2)
    dett = (omega * l * sinh(omega * l / 2)) / (sinh(omega * l) - cosh(omega * l))
    P = zeros((1, 4, 3))

    indexs = range(4)
    max = len(indexs) - 1
    indexs.reverse()
    for i in indexs:
        P[0, max - i, 0] = a * dett * cosh(omega * ((i - 1 - 1 / 2.0) * l))
        P[0, max - i, 1] = b * dett * sinh(omega * ((i - 1 - 1 / 2.0) * l))

    return P, u0


def parabola():
    '''
        % -------------------------------------------------------------------------
        % Ploting parabola curve from i*l to (i+1)*l and so on. 
        % The parametric equation of the arc is
        % x=t; y=a*t^2;
        % t\in[i*l,(i+1)*l]; u0=1;
        % -------------------------------------------------------------------------
%         a = input('Please input the coefficency of quadratic item a:');
%         b = input('Please input the coefficency of linear item b:');
%         c = input('Please input the constant item c:');
%         l = input('Please input the interval length l:');
%         i0= input('Please input the start interval number i0:');
%         n = input('Please input the number of pieces you want to plot n:');
	'''
    a = 0.5
    l = pi / 2
    i0 = 0
    n = 2

    omega = 0
    u0 = cos(omega * l / 2)
    P = zeros((1, i0 + n + 1 + 1, 3))
    indexs = range(4)
    max = len(indexs) - 1
    indexs.reverse()
    for i in indexs:
        P[0, max - i, 0] = (i ) * l
        P[0, max - i, 1] = -(i ) * i * l ** 2 * a


    return P, u0


def C_type_conics(conicstype):
    '''
	% This program outputs the control polygon and the tension parameter of 
	% a conical curve represented by degree 2 C-type splines plots the subdivision conical curve
	% type=1: line (the genetrix of a cone)
	% type=2: line (the genetrix of a cylinder)
	% type=3: circlular arc
	% type=4: hyperbola
	% type=5: parabola

	% type=others: no definition
	'''
    return {'cone': cone, 'cylinder': cylinder, 'circular': circular, 'hyperbola': hyperbola, 'parabola': parabola}[
        conicstype]()


if __name__ == '__main__':
    List = ['cone', 'cylinder', 'circular', 'hyperbola', 'parabola']
    Dict = {}
    for typestr in List:
        Dict[typestr] = C_type_conics(typestr)
    for typestr in List:
        print typestr
        printAsMatlab(Dict[typestr][0])
        print '\n'
