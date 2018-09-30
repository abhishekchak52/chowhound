import numpy as np
from tqdm import trange
from lunch import items_list
from mess_env import serve, est_waste, input_vec, generate_menu, sigmoid
from lunch import dals, sabzis, sweets

from keras.models import load_model

from policy_nn import discount_rewards

num_inputs = len(items_list) # All food items
num_outputs = len(items_list) + 1 # All food items plus wastage
gamma = .99

def generate():
    training_model =  load_model('training.h5')
    prediction_model =  load_model('predict.h5')
    state = np.reshape(input_vec(serve()),[1,num_inputs])
    predicted = prediction_model.predict(state)[0]
    action = np.zeros(num_outputs)
    action[np.random.choice(range(len(predicted[:len(dals)])),p=predicted[:len(dals)]/np.sum(predicted[:len(dals)]))] = 1
    action[len(dals) + np.random.choice(range(len(predicted[len(dals):len(dals) + len(sabzis)])),p=(predicted[len(dals):len(dals) + len(sabzis)])/np.sum(predicted[len(dals):len(dals) + len(sabzis)]))] = 1
    action[len(dals) + len(sabzis) + np.random.choice(range(len(predicted[len(dals) + len(sabzis) :len(dals) + len(sabzis) + len(sweets)])),p=(predicted[len(dals) + len(sabzis) :len(dals) + len(sabzis) + len(sweets)])/np.sum(predicted[len(dals) + len(sabzis) :len(dals) + len(sabzis) + len(sweets)]))] = 1
    action[-1] =  predicted[-1]

