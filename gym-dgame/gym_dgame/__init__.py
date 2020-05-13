from gym.envs.registration import register

register(
        id='dgame-v0',
        entry_point='gym_dgame.envs:DatabaseGameEnv',
        )
