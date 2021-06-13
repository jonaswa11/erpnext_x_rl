import gym
import gym_stock


from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env


# Parallel environments
env = make_vec_env('gym_stock:StockEnv-v0', n_envs=1)

env.reset()

loaded_model = PPO.load("ppo_stock1")
# Create the model, the training environment
# and the test environment (for evaluation)
loaded_model.set_env(env)





# Evaluate the model every 1000 steps on 5 test episodes
# and save the evaluation to the "logs/" folder
loaded_model.learn(total_timesteps=100, log_interval=1, tb_log_name="Logs", reset_num_timesteps=True)

# save the model
loaded_model.save("ppo_stock2")
