import gym

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import CheckpointCallback

# Parallel environments
env = make_vec_env('gym_stock:StockEnvMultiProduct-v0', n_envs=4)

# Save a checkpoint every 1000 steps
checkpoint_callback = CheckpointCallback(save_freq=200000, save_path='./logs/test3',
                                         name_prefix='rl_model')

# tensorboard --logdir ./ppo_StockEnvMultiProduct_tensorboard/
model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./ppo_StockEnvMultiProduct_tensorboard/")
model.learn(total_timesteps=800000, callback=checkpoint_callback)
model.save("ppo_stock1")