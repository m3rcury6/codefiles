'''
simple quick calculation to give you partial area of a sphere, given knowledge of sphere's parameters.

copy/paste me into latex:
$$ A_{sphere}=R^2\theta \int_{a}^{b}\cos\phi*d\phi $$
$$ A_{sphere}=R^2\theta (\sin{b} - \sin{a})$$

'''
import numpy as np

def AreaSpherePartial(radius=1,horizAngle=2*np.pi,
            vertAngle1=-np.pi/2,vertAngle2=np.pi/2):
    '''
    Return partial area of sphere, given radius, hAngle,vAngle start & finish
        (radians)
    '''
    return radius**2 * horizAngle * (np.sin(vertAngle2) - np.sin(vertAngle1))

if(__name__=='__main__'):
    params = (1,2*np.pi,-np.pi/2,np.pi/2)
    print('parameters:',params)
    print(AreaSpherePartial(*params))
