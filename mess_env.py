from lunch import dals, sabzis, sweets
import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))


def serve():
    menu = {}
    menu['dal'] = list(dals)[np.random.randint(0,len(dals))]
    menu['sabzi'] = list(sabzis)[np.random.randint(0,len(sabzis))]
    menu['sweet'] = list(sweets)[np.random.randint(0,len(sweets))]
    return menu

def est_waste(menu):
    return sigmoid(dals[menu['dal']] + 2*sabzis[menu['sabzi']] + sweets[menu['sweet']] - 10)

if __name__=='__main__':
    for _ in range(20):
        menu = serve()
        print(est_waste(menu))



    

