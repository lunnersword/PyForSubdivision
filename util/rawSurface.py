from numpy import *
class RawSurface:
    def __init__(self, blendCP, name):
        if type(blendCP) is not ndarray:
            raise TypeError

        self.name = name
        self.sharpEdges = []
        self.setBlendCP(blendCP)
    def setBlendCP(self, blendCP):
        if type(blendCP) is not ndarray:
            raise TypeError
        if self.name == 'circular':

            P = blendCP[-2:,:,:]
            print("circ")
            print(P)
            print("circ")

        # elif self.name == 'parabola':
        #     P = blendCP[:-1,:,:]
        #     print("rawed:")
        #     print(P)
            #P = vstack( (CP.blendCP[0,:,:], CP.blendCP[2:,:,:]) )
            '''
            ilen = len(CP.blendCP[:,0,0])
            P = zeros( (ilen-1,6,3) )
            P[0,:,:] = CP.blendCP[0,:,:]
            P[1:,:,:]= CP.blendCP[2:,:,:]
            '''
        else:
            P = blendCP
        self.blendCP = P
    def setName(self, name):
        self.name = name

    def setSharpEdges(self, num):
        ilen = len(self.blendCP[:,0,0])
        for item in num:
            if item > ilen-1:
                raise ValueError
            if item >= 0:
                self.sharpEdges.append(item)
            if item < 0 :
                self.sharpEdges.append(ilen + item)


