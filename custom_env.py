import io, os, sys, types
from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell
import logging
import tensorflow as tf
import time

from tensorforce.agents import Agent
from tensorforce.environments import Environment
from tensorforce.execution import Runner

import sim

### Creates the custom environment that the AI will use to play the game ###

### Creates a class which is an object that the Tensorforce program uses to do certain things ###
class CustomEnvironment(Environment):
    
    ### Here we create an object from the class that WE made ###
    gameSimulation = sim.GameSim()
    
    ### We initialize the class ###
    def __init__(self):
        super().__init__()

    ### Here the Tensorforce program uses this attribute to figure out how many things the AI is given describing
    ### the world around it. It calls it like this custom_env.CustomEnvironment.states() ###
    def states(self):
        return dict(type='float', shape=(49,))
    
    ### Here we tell the Tensorforce program what decisions the AI can say ###
    def actions(self):
        return {"up": dict(type="float", min_value=0.0, max_value=1.0),
                 "down": dict(type="float", min_value=0.0, max_value=1.0),
                 "left": dict(type="float", min_value=0.0, max_value=1.0),
                 "right": dict(type="float", min_value=0.0, max_value=1.0),
                 }
    ### Here we tell it how many turns it gets in one game ###
    def max_episode_timesteps(self):
        return super().max_episode_timesteps()

    ### Here is where we shut down the AI ###
    def close(self):
        super().close()
    
    ### Here is where we reset the game for the AI ###
    def reset(self):
        ### Here we use the gameSimulation object instance and use its reset() function to reset the game ###
        self.gameSimulation.reset()
        return self.gameSimulation.get_state()

    ### Here is where the AI actually plays the game! ###
    def execute(self, actions):
        ### Here we check if the move the AI made is valid, passing the actions to the gameSimulation objects ###
        ### move_check() function ###
        if self.gameSimulation.move_check(actions):
            ### If the move is valid then we use the simulations movePlayer() function, passing it the actions ###
            ### and getting the AI's new_position back! We then set the new position as a variable so we can use it later ###
            new_position = self.gameSimulation.movePlayer(actions)
            ### We then use the simulation objects reward() function to set the AI's reward and check to see if the ###
            ### game is over, by passing in the AI's new position that we set earlier. We can do this by setting ###
            ### two variables that get returned by the reward() function. reward & gameOver. Reward is a number, and ###
            ### gameOver is True or False. ###
            reward, gameOver = self.gameSimulation.reward(new_position)
            ### Here we just print what is happening ###
            print(f"The AI decided to move to {new_position}, and was given a reward of {reward}")
            ### Finally, we check to see if the game is over or not, setting terminal to True or False accordingly. ###
            if gameOver is True:
                terminal = True
            else:
                terminal = False
        ### If the AI made an invalid move we just tell it to try again and take away 1 point ###
        else:
            reward = -1
            terminal = False
        ### Finally we return the new state of the game for the AI to look at for its next move. Along with the reward ###
        ### and whether it won or not with terminal. It uses all these things to try and make better decisions in the future ###
        return self.gameSimulation.get_state(), terminal, reward
