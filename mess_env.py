from lunch import dals, sabzis, sweets, items_list
import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def serve():
    menu = {}
    menu['dal'] = list(dals)[np.random.randint(0,len(dals))]
    menu['sabzi'] = list(sabzis)[np.random.randint(0,len(sabzis))]
    menu['sweet'] = list(sweets)[np.random.randint(0,len(sweets))]
    return menu

def generate_menu(vec):
    menu = {}
    dal, sabzi, sweet = [items_list[i] for i in range(len(vec)) if vec[i]]
    menu['dal']  = dal
    menu['sabzi'] = sabzi
    menu['sweet'] = sweet
    return menu


def est_waste(menu):
    x = dals[menu['dal']] + 2*sabzis[menu['sabzi']] + 0.1*sweets[menu['sweet']] - 10
    return np.round(sigmoid(x),2)+0.01 if x < -2 else 0.26

def input_vec(menu):
    menu_items = list(menu.values())
    vec = np.zeros_like(items_list)
    for i in range(len(items_list)):
        vec[i] = 1 if items_list[i] in menu_items else 0
    return np.array(vec,dtype='int')

if __name__=='__main__':
    menu = serve()
    print(menu)
    print(est_waste(menu))
    print(input_vec(menu))
