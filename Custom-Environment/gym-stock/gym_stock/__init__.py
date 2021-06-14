# Core Library
import logging

# Third party
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='StockEnv-v0',
    entry_point='gym_stock.envs:StockEnv'
)

register(
    id='StockEnvMultiProduct-v0',
    entry_point='gym_stock.envs:StockEnvMultiProduct'
)
