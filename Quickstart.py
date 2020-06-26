import io, os, sys, types
from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell
import logging
import tensorflow as tf
from tensorforce.agents import Agent
from tensorforce.environments import Environment
from tensorforce.execution import Runner

import custom_env

from sim import GameSim

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logger = tf.get_logger()
logger.setLevel(logging.ERROR)

# Copyright 2018 Tensorforce Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

### Create an OpenAI-Gym environment-Talks to our custom_env file and class ###
environment = Environment.create(
    environment='custom_env.CustomEnvironment', max_episode_timesteps=40
)

### Create a PPO agent ###
agent = Agent.create(
    agent='ppo', environment=environment,
    # Automatically configured network
    network='auto',
    # Optimization
    batch_size=10, update_frequency=2, learning_rate=1e-3, subsampling_fraction=0.2,
    optimization_steps=5,
    # Preprocessing
    preprocessing=None,
    # Exploration
    exploration=0.22, variable_noise=0.0,
    # Regularization
    l2_regularization=0.0, entropy_regularization=0.0,
    # TensorFlow etc
    name='agent', device=None, parallel_interactions=1, seed=None, execution=None, saver=None,
    summarizer=dict(
        directory='data/summaries',
        # list of labels, or 'all'
        labels=['all'],
        frequency=20), recorder=None
)

### Initialize the runner ###
runner = Runner(agent=agent, environment=environment)

### Start the runner ###
runner.run(num_episodes=100)
runner.close()
