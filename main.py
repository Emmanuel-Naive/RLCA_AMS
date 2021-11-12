"""
Reinforcement learning (Q-learning) maze example.
This script is the main part which controls the update method of this example.

Writen by Morvan: https://morvanzhou.github.io/tutorials/
Modified by Weijian: weijiany@stud.ntnu.no

Version: 2 ship, 2 goals and 2 obstacles (consider collision)
Red rectangle:         ship (explorer)
Black rectangles:      obstacle
Yellow bin circle:     goal
All other states:      open sea
"""

from Env.maze_envS2CO import Maze
from RL_brain import QLearningTable


def update():
    for episode in range(100):
        # initial observation
        observation1 = env.reset()
        observation2 = env.reset()
        while True:
            # fresh env
            env.render()
            if observation1 != 'terminal':
                # RL choose action based on observation
                action1 = RL.choose_action(str(observation1))
                # RL take action and get next observation and reward
                observation1_, reward1, done1 = env.step1(action1)
            if observation2 != 'terminal':
                # RL choose action based on observation
                action2 = RL.choose_action(str(observation2))
                # RL take action and get next observation and reward
                observation2_, reward2, done2 = env.step2(action2)

            reward1, reward2 = env.checkgoal(observation1_, reward1, observation2_, reward2)
            reward1, done1, reward2, done2 = env.checkcollison(observation1_, reward1, done1, observation2_, reward2, done2)
            # RL learn from this transition
            RL.learn(str(observation1), action1, reward1, str(observation1_))
            RL.learn(str(observation2), action2, reward2, str(observation2_))

            # swap observation
            observation1 = observation1_
            observation2 = observation2_

            # break while loop when end of this episode
            if done1 and done2:
                break

    # end of game
    print('game over')
    env.destroy()

if __name__ == "__main__":
    env = Maze()
    RL = QLearningTable(actions=list(range(env.n_actions)))

    env.after(100, update)
    env.mainloop()