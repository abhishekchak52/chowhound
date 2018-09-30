import numpy as np
from tqdm import trange
from lunch import items_list
from mess_env import serve, est_waste, input_vec, generate_menu, sigmoid
from lunch import dals, sabzis, sweets

from keras.models import load_model

from policy_nn import discount_rewards

def load_models():
    return load_model('training.h5'), load_model('predict.h5')