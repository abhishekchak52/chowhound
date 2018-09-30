import numpy as np
from tqdm import trange
from lunch import items_list
from mess_env import serve, est_waste, input_vec, generate_menu, sigmoid
from lunch import dals, sabzis, sweets

import keras.layers as layers
from keras.models import Model, load_model
from keras.optimizers import Adam
import keras.backend as K
from keras.initializers import glorot_normal

import matplotlib.pyplot as plt

def make_policy_model(hidden_layer_neurons, lr):
    num_inputs = len(items_list) # All food items
    num_outputs = len(items_list) + 1 # All food items plus wastage
    inp = layers.Input(shape=np.array(items_list).shape, name='Inputs')
    adv = layers.Input(shape=[1], name='Advantages')
    x1 = layers.Dense(hidden_layer_neurons,
                    activation='relu',
                    use_bias = False,
                    kernel_initializer=glorot_normal(seed=0),
                    name="Hidden1")(inp)
    x2 = layers.Dense(hidden_layer_neurons,
                    activation='relu',
                    use_bias = False,
                    kernel_initializer=glorot_normal(seed=0),
                    name="Hidden2")(x1)
    out = layers.Dense(num_outputs,
                    activation='relu',
                    use_bias = False,
                    kernel_initializer=glorot_normal(seed=0),
                    name="Out")(x2)
    model_train = Model(inputs=[inp,adv], outputs=[out])
    model_train.compile(loss='mean_squared_error', optimizer=Adam(lr))
    model_predict = Model(inputs=[inp], outputs=out)
    return model_train, model_predict

def discount_rewards(r, gamma=0.99):
    prior = 0
    out = []
    for val in r:
        new_val = val + prior * gamma
        out.append(new_val)
        prior = new_val
    return np.array(out[::-1])

def score_model(model, num_tests):
    scores = [] 
    for test in range(num_tests):
        reward_sum = 0 
        for _ in range(7): # Run for a week
            state = np.reshape(input_vec(serve()),[1,num_inputs])
            predicted = model.predict(state)[0]
            action = np.zeros(num_outputs)[:-1]
            action[np.argmax(predicted[:len(dals)])] = 1
            action[len(dals)+np.argmax(predicted[len(dals):len(dals)+len(sabzis)])] = 1
            action[len(dals)+len(sabzis)+np.argmax(predicted[len(sabzis):len(sabzis)+len(sweets)])] = 1
            suggested_menu = generate_menu(action)
            waste = est_waste(suggested_menu)
            reward_sum += 1/waste
        scores.append(reward_sum)
    return np.mean(scores)

def run_model(num_weeks=10):
    training_model, prediction_model = make_policy_model(30, 1e-2)
    reward = reward_sum = 0
    losses = []
    scores = []
    
    # Placeholders for our observations, outputs and rewards
    states = np.empty(0).reshape(0,num_inputs)
    actions = np.empty(0).reshape(0,num_outputs)
    rewards = np.empty(0).reshape(0,1)
    discounted_rewards = np.empty(0).reshape(0,1)

    for day in trange(7*num_weeks):
        state = np.reshape(input_vec(serve()),[1,num_inputs])
        predicted = prediction_model.predict(state)[0]

        # choosing the proposed move
        action = np.zeros(num_outputs)
        action[np.random.choice(range(len(predicted[:len(dals)])),p=predicted[:len(dals)]/np.sum(predicted[:len(dals)]))] = 1
        action[len(dals) + np.random.choice(range(len(predicted[len(dals):len(dals) + len(sabzis)])),p=(predicted[len(dals):len(dals) + len(sabzis)])/np.sum(predicted[len(dals):len(dals) + len(sabzis)]))] = 1
        action[len(dals) + len(sabzis) + np.random.choice(range(len(predicted[len(dals) + len(sabzis) :len(dals) + len(sabzis) + len(sweets)])),p=(predicted[len(dals) + len(sabzis) :len(dals) + len(sabzis) + len(sweets)])/np.sum(predicted[len(dals) + len(sabzis) :len(dals) + len(sabzis) + len(sweets)]))] = 1
        action[-1] =  predicted[-1]

        states = np.vstack([states, state])
        actions = np.vstack([actions, action])
        suggested_menu = generate_menu(action[:-1])
        waste = est_waste(suggested_menu)
    #     reward = 1/(sigmoid(waste)+0.01)
        reward = 1/waste
        reward_sum += reward
        rewards = np.vstack([rewards, reward])

        if (day + 1) % 7 == 0: # End of week

            discounted_rewards_episode = discount_rewards(rewards, gamma)       
            discounted_rewards = np.vstack([discounted_rewards, discounted_rewards_episode])
            rewards = np.empty(0).reshape(0,1)

            discounted_rewards -= discounted_rewards.mean()
            discounted_rewards /= discounted_rewards.std()

            loss = training_model.train_on_batch([states,discounted_rewards],actions)
            losses.append(loss)

            states = np.empty(0).reshape(0,num_inputs)
            actions = np.empty(0).reshape(0,num_outputs)
            discounted_rewards = np.empty(0).reshape(0,1)
            
        if (day + 1) % print_every == 0:
            score = score_model(prediction_model,50)
            scores.append(score)

    return losses, scores

if __name__=='__main__':
    # Constants defining our neural network
    hidden_layer_neurons = 60
    num_inputs = len(items_list) # All food items
    num_outputs = len(items_list) + 1 # All food items plus wastage
    gamma = .99
    print_every = 14
    batch_size = 7

    num_weeks = 10
    lr = 1e-2
    goal = 0.15
 
    losses, scores = run_model(500)
    plt.clf()
    plt.plot(losses)
    plt.savefig('losses.png')
    
    meal = serve()
    state = np.reshape(input_vec(meal),[1,num_inputs])
    prediction_model = load_model('predict.h5')
    prediction_model.compile(loss='mean_squared_error', optimizer=Adam(lr))
    predicted = prediction_model.predict(state)[0]
    
    food = generate_menu(predicted[:-1])
    print(meal)
    print( food)
    print(predicted[-1])
    print(est_waste(meal))

    

