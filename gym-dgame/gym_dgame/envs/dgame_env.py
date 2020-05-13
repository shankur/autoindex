"""
This module creates a GYM ENV that can be used to train a Reinforcement Learned NN that is capable
of tuning indexes in a Database.

Testing new gameplay mechanics
"""
import gym
import random
import numpy as np
from gym.spaces import Discrete
from lineitem_query import lineitem_query


class DatabaseGameEnv(gym.Env):
    """
    This class provides an Environment for tuning database indexes for a particular worload
    """
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self):
        # flag to tell the env whether its used for training or test
        self.train = True

        self.step_limit = 0
        self.limit = 0
        self.repeat_size = 0
        self.chances_left = 0
        self.train_step = 0
        self.workload_size = 0
        self.train_episode_count = 0

        self.database = None

        self.workload = []
        self.index_list = []
        self.query_list = []

        self.original_state = None
        self.current_state = None

        # query generator
        self.query_gen = lineitem_query.LineitemQuery()
        self.columns = ['' for i in range(15)]
        col_dict = self.query_gen.column_dict()
        for k, v in col_dict.items():
            self.columns[v] = k
        self.no_index_cost = np.finfo('float').max

        # Index spaces
        self.action_space = Discrete(len(self.columns))

    def _generate_frame_matrix(self):
        # generate a new workload
        frame = []
        self.query_list = []
        for i in range(self.workload_size):
            sel, q = self.query_gen.get_query(random.randint(4, 6))
            # sel, q = self.query_gen.get_query(random.randint(1, 1))

            # Save the selectivities and queries
            frame.append(sel)
            self.query_list.append(q)

        index_stat = np.array([0.0 for i in range(len(frame[0]))])
        # set index stat to 1 if the column is not used by any query

        frame = np.array(frame)
        min_array = np.amin(frame, axis=0)

        for i in range(len(min_array)):
            if min_array[i] == 1:
                index_stat[i] = 1

        frame = np.vstack((frame, np.array(index_stat))).astype(np.float32)
        # print(frame.shape)
        return frame.flatten('F')

    def initialize(self, database, workload_size: int, limit=3, repeat_size=10, step_limit=150, verbose=2):
        """
        This method initializes the ENV.
        """
        self.limit = limit
        self.verbose = verbose
        self.step_limit = step_limit
        self.chances_left = self.limit
        self.database = database
        self.repeat_size = repeat_size
        self.workload_size = workload_size
        self.original_state = self._generate_frame_matrix()
        self.current_state = np.copy(self.original_state)
        self.observation_space = Discrete(len(self.columns) * (self.workload_size + 1) + 1)
        self.database.drop_all_indexes()
        self.no_index_cost = self._get_workload_cost()

    def _get_state(self):
        return np.hstack((self.current_state, self.train_step))
        # return self.current_state

    def _seed(self, seed=None):
        """
        Seed the ENV Randomizer
        """
        random.seed(seed)

    def _print_index_list(self):
        # print the set of indexes
        # print the cost without indexes and cost with indexes
        if self.verbose == 2 or not self.train:
            print('---------------------------------------------------------------')
            print('Original Cost Estimate: {}, Optimized Cost Estimate: {}'.format(
                self.no_index_cost, self._get_workload_cost()
                ))
            print(self.index_list)
            print('***************************************************************')

    def _step(self, action):
        self.train_step += 1
        # check if the action is valid
        assert(action <= 15)

        if self.train_step > self.step_limit:
            self._print_index_list()
            return self._get_state(), 0, True, {}


        # check if the index is already created
        if self.current_state[(action + 1) * (self.workload_size + 1) - 1] == 1:
            # index was already created or no query is using it
#           self._print_index_list()
#           return self._get_state(), 0, True, {}
            return self._get_state(), 0, False, {}

        self.chances_left -= 1
        game_over = not (self.chances_left > 0)

        self._take_action(action)

        reward = self._reward()

        for i in range(action * (self.workload_size + 1), (action + 1) * (self.workload_size + 1)):
            self.current_state[i] = 1

        if game_over:
            self._print_index_list()

        return self._get_state(), reward, game_over, {}

    def _take_action(self, column_id: int):
        column_name = self.columns[column_id]
        self.index_list.append(self.columns[column_id])
        self.database.create_index(column_name)

    def _reset(self):
        # @return: state after reset
        self.database.drop_all_indexes()
        if (not self.train) or (self.train_episode_count % self.repeat_size == 0):
            self.original_state = self._generate_frame_matrix()
            self.no_index_cost = self._get_workload_cost()
        self.index_list = []
        self.train_step = 0
        self.train_episode_count += 1
        self.current_state = np.copy(self.original_state)
        self.chances_left = self.limit
        if not self.train:
            print('workload: {}'.format(self.query_list))
        return self._get_state()

    def _get_workload_cost(self):
        # Get the total cost estimate for the workload
        cost_estimate = 0.0
        for query in self.query_list:
            cost_estimate += self.database.cost(query)
        return cost_estimate

    def _reward(self):
        # @return: the reward or last action
        return (self.no_index_cost / self._get_workload_cost()) - 1.0
