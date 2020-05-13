#!/usr/bin/env python

import gym
import argparse
import gym_dgame

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
# from keras.optimizers import Adam

from rl.agents.cem import CEMAgent
from rl.agents.dqn import DQNAgent
from rl.agents.dqn import NAFAgent
from rl.agents.ddpg import DDPGAgent
from rl.agents.sarsa import SARSAAgent

from rl.memory import EpisodeParameterMemory

from postgres_executor import postgres_executor
# from sqlserver_executor import sqlserver_executor

# Parse the commandline arguments
parser = argparse.ArgumentParser()


parser.add_argument('--verbose', type=int, default=2)
# Workload parameters
parser.add_argument('--backend', type=int, default=0, help='database to use: {0=postgres, 1=sqlserver}')
parser.add_argument('--workload_size', type=int, default=5, help='size of workload')
parser.add_argument('--index_limit', type=int, default=3, help='maximum number of index that can be created')
parser.add_argument('--tpch_queries', type=int, nargs='+', default=[4, 5, 6],
                    help='tpc-h queries used to create workload', choices=[1, 3, 4, 5, 6, 13, 14])

# Model Hyperparameter
parser.add_argument('--batch_size', type=int, default=50)
parser.add_argument('--hidden_layers', type=int, default=4, help='number of hidden layers')
parser.add_argument('--hidden_units', type=int, default=8, help='number of hidden units in each hidden layer')
parser.add_argument('--agent', default='cem', choices=['cem', 'dqn', 'naf', 'ddpg', 'sarsa'],
                    help='rl agent used for learning')
parser.add_argument('--activation_function', default='relu', choices=['elu', 'relu', 'selu'],
                    help='activation function used in hidden layers')
parser.add_argument('--memory_limit', type=int, default=500, help='episode memory size')
parser.add_argument('--steps_warmup', type=int, default=1000, help='number of warmup steps')
parser.add_argument('--nb_steps_test', type=int, default=5, help='number of steps in test')
parser.add_argument('--elite_frac', type=float, default=0.005, help='elite fraction used in rl model')
parser.add_argument('--nb_steps_train', type=int, default=1000, help='number of steps in training')

# Database parameters
parser.add_argument('--host', default='localhost', help='hostname of database server')
parser.add_argument('--database', default='ankur', help='database name')
parser.add_argument('--user', default='postgres', help='database username')
parser.add_argument('--password', default='postgres', help='database password')

args = parser.parse_args()

# keras-rl agents
AGENT_DIC = {
        'cem': CEMAgent,
        'dqn': DQNAgent,
        'naf': NAFAgent,
        'ddpg': DDPGAgent,
        'sarsa': SARSAAgent
        }

# from random import randrange as rand

postgres_config = {
        'host': args.host,
        'database': args.database,
        'user': args.user,
        'password': args.password
        }

if __name__ == '__main__':

    workload_size = args.workload_size

    database = postgres_executor.TPCHExecutor(postgres_config)
    database.connect()

    ENV_NAME = 'dgame-v0'
    env = gym.make(ENV_NAME)

    env.initialize(database, workload_size, args.index_limit, 1, verbose=args.verbose)

    nb_actions = env.action_space.n
    observation_n = env.observation_space.n

    # create a model
    model = Sequential()
    model.add(Flatten(input_shape=(args.batch_size, observation_n)))

    # Simple model
    # model.add(Dense(nb_actions))
    # model.add(Activation('softmax'))

    # Complex Deep NN Model
    for i in range(args.hidden_layers):
        model.add(Dense(args.hidden_units))
        model.add(Activation(args.activation_function))

    model.add(Dense(nb_actions))
    model.add(Activation('softmax'))

    print(model.summary())

    Agent = AGENT_DIC[args.agent]

    memory = EpisodeParameterMemory(limit=args.memory_limit, window_length=args.batch_size)

    agent = Agent(
            model=model,
            nb_actions=nb_actions,
            memory=memory,
            batch_size=args.batch_size,
            nb_steps_warmup=args.steps_warmup,
            train_interval=args.batch_size,
            elite_frac=args.elite_frac
            )

    agent.compile()
    agent.fit(env, nb_steps=args.nb_steps_train, visualize=False, verbose=args.verbose)
    agent.save_weights('cem_{}_params.h5'.format(ENV_NAME), overwrite=True)
    env.train = False
    agent.test(env, nb_episodes=args.nb_steps_test, visualize=True)
