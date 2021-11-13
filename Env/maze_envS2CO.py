"""
Reinforcement learning (Q-learning) maze example.
This script is used to build the environment (the maze map).

Writen by Morvan: https://morvanzhou.github.io/tutorials/
Modified by Weijian: weijiany@stud.ntnu.no

Version: 2 ship, 2 goals and 2 obstacles (consider collision)
Red rectangle:         ship (explorer)
Black rectangles:      obstacle
Yellow bin circle:     goal
All other states:      open sea
"""


import numpy as np
import time
import sys

if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

UNIT = 40       # pixels: distance between 2 points
MAZE_H = 7     # grid height
MAZE_W = 7     # grid width
# Map Initialization
# Be careful to create origin
# Origin would be located at the upper left corner of the map.
# X-axis points to the right
# Y-axis points down

origin = np.array([20, 20])  # origin[X,Y]
obst1_center = origin + np.array([UNIT * 2, UNIT * 2])
obst2_center = origin + np.array([UNIT *2, UNIT * 4])
ship1_center = origin + np.array([UNIT * 3, 0])
goal1_center = origin + np.array([UNIT * 3, UNIT * 6])
ship2_center = origin + np.array([0, UNIT * 3])
goal2_center = origin + np.array([UNIT * 6, UNIT * 3])
distance1 = (ship1_center[0] - goal1_center[0]) ** 2 + (ship1_center[1] - goal1_center[1]) ** 2
distance2 = (ship2_center[0] - goal2_center[0]) ** 2 + (ship2_center[1] - goal2_center[1]) ** 2
dangerdis = 8 * UNIT

class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                                height=MAZE_H * UNIT,
                                width=MAZE_W * UNIT)

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        # create obstacles
        self.obst1 = self.canvas.create_rectangle(
            obst1_center[0] - 15, obst1_center[1] - 15,
            obst1_center[0] + 15, obst1_center[1] + 15,
            fill='black')
        
        self.obst2 = self.canvas.create_rectangle(
            obst2_center[0] - 15, obst2_center[1] - 15,
            obst2_center[0] + 15, obst2_center[1] + 15,
            fill='black')

        # create goals
        self.goal1 = self.canvas.create_oval(
            goal1_center[0] - 15, goal1_center[1] - 15,
            goal1_center[0] + 15, goal1_center[1] + 15,
            fill='yellow')

        self.goal2 = self.canvas.create_oval(
            goal2_center[0] - 15, goal2_center[1] - 15,
            goal2_center[0] + 15, goal2_center[1] + 15,
            fill='green')

        # create ships
        self.ship1 = self.canvas.create_rectangle(
            ship1_center[0] - 15, ship1_center[1] - 15,
            ship1_center[0] + 15, ship1_center[1] + 15,
            fill='yellow')

        self.ship2 = self.canvas.create_rectangle(
            ship2_center[0] - 15, ship2_center[1] - 15,
            ship2_center[0] + 15, ship2_center[1] + 15,
            fill='green')

        # pack all
        self.canvas.pack()

    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.ship1)
        self.ship1 = self.canvas.create_rectangle(
            ship1_center[0] - 15, ship1_center[1] - 15,
            ship1_center[0] + 15, ship1_center[1] + 15,
            fill='yellow')

        self.canvas.delete(self.ship2)
        self.ship2 = self.canvas.create_rectangle(
            ship2_center[0] - 15, ship2_center[1] - 15,
            ship2_center[0] + 15, ship2_center[1] + 15,
            fill='green')

        # return observation
        return self.canvas.coords(self.ship1),self.canvas.coords(self.ship2)

    def step1(self, action):
        ship1s = self.canvas.coords(self.ship1)
        base_action = np.array([0, 0])
        if action == 0:   # up
            if ship1s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if ship1s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if ship1s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # left
            if ship1s[0] > UNIT:
                base_action[0] -= UNIT
        self.canvas.move(self.ship1, base_action[0], base_action[1])  # move agent
        ship1s_ = self.canvas.coords(self.ship1)  # next state
        # reward function
        if ship1s_ == self.canvas.coords(self.goal1):
            reward1 = 10
            done1 = False
            ship1s_ = 'terminal'
        elif ship1s_ == self.canvas.coords(self.goal2):
            reward1 = -10
            done1 = False
        elif ship1s_ in [self.canvas.coords(self.obst1),self.canvas.coords(self.obst2)]:
            reward1 = -10
            done1 = True
            ship1s_ = 'terminal'
        else:
            reward1 = 0
            done1 = False
        return ship1s_, reward1, done1

    def step2(self, action):
        ship2s = self.canvas.coords(self.ship2)
        base_action = np.array([0, 0])
        if action == 0:  # up
            if ship2s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:  # down
            if ship2s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:  # right
            if ship2s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:  # left
            if ship2s[0] > UNIT:
                base_action[0] -= UNIT
        self.canvas.move(self.ship2, base_action[0], base_action[1])  # move agent
        ship2s_ = self.canvas.coords(self.ship2)  # next state

        if ship2s_ == self.canvas.coords(self.goal2):
            reward2 = 10
            done2 = False
            ship2s_ = 'terminal'
        elif ship2s_ == self.canvas.coords(self.goal1):
            reward2 = -10
            done2 = False
        elif ship2s_ in [self.canvas.coords(self.obst1),self.canvas.coords(self.obst2)]:
            reward2 = -10
            done2 = True
            ship2s_ = 'terminal'
        else:
            reward2 = 0
            done2 = False
        return ship2s_, reward2, done2

    def checkcollison(self, ship1s, reward1, done1, ship2s, reward2, done2):
        if ship1s == 'terminal' and ship2s == 'terminal':
            done1=True
            done2=True
            return reward1, done1, reward2, done2
        elif ship1s == 'terminal' or ship2s == 'terminal':
            return reward1, done1, reward2, done2
        else:
            ship1s_center = np.array([ship1s[0] - 15, ship1s[1] + 15])
            ship2s_center = np.array([ship2s[0] - 15, ship2s[1] + 15])
            if (ship1s_center == ship2s_center).all():
                reward1 -= 10
                reward2 -= 10
                done1 = True
                done2 = True
                return reward1, done1, reward2, done2
            elif (ship1s_center[0] - ship2s_center[0]) ** 2 + (ship1s_center[1] - ship2s_center[1]) ** 2 <= dangerdis:
                reward1 -=  (dangerdis - (ship1s_center[0] - ship2s_center[0]) ** 2 - (ship1s_center[1] - ship2s_center[1]) ** 2) / dangerdis
                reward2 -=  (dangerdis - (ship1s_center[0] - ship2s_center[0]) ** 2 - (ship1s_center[1] - ship2s_center[1]) ** 2) / dangerdis
                done1 = False
                done2 = False
                return reward1, done1, reward2, done2
            else:
                reward1 -= 0
                reward2 -= 0
                done1 = False
                done2 = False
                return reward1, done1, reward2, done2

    def checkgoal(self, ship1s, reward1, ship2s, reward2):
        if ship1s == 'terminal' and ship2s == 'terminal':
            return reward1, reward2
        elif ship1s == 'terminal' and ship2s != 'terminal':
            ship2s_center = np.array([ship2s[0] - 15, ship2s[1] + 15])
            sdistance2 = (ship2s_center[0] - goal2_center[0]) ** 2 + (ship2s_center[1] - goal2_center[1]) ** 2
            reward2 += 100 * (distance2 - sdistance2) / distance2
            return reward1, reward2
        elif ship2s == 'terminal' and ship1s != 'terminal':
            ship1s_center = np.array([ship1s[0] - 15, ship1s[1] + 15])
            sdistance1 = (ship1s_center[0] - goal1_center[0]) ** 2 + (ship1s_center[1] - goal1_center[1]) ** 2
            reward1 += 100 *  (distance1 - sdistance1) / distance1
            return reward1, reward2
        else:
            ship1s_center = np.array([ship1s[0] - 15, ship1s[1] + 15])
            ship2s_center = np.array([ship2s[0] - 15, ship2s[1] + 15])
            sdistance1 = (ship1s_center[0] - goal1_center[0]) ** 2 + (ship1s_center[1] - goal1_center[1]) ** 2
            sdistance2 = (ship2s_center[0] - goal2_center[0]) ** 2 + (ship2s_center[1] - goal2_center[1]) ** 2
            reward1 +=  (distance1 - sdistance1) / distance1
            reward2 +=  (distance2 - sdistance2) / distance2
            return reward1, reward2

    def render(self):
        time.sleep(0.1)
        self.update()

def update():
    time.sleep(5)
    for t in range(10):
        env.reset()
        while True:
            env.render()
            a = 1
            ship1s, r1, done1 = env.step1(a)
            b = 2
            ship2s, r2, done2 = env.step2(b)
            r1, r2 = env.checkgoal(ship1s, r1, ship2s, r2)
            r1, done1, r2, done2 = env.checkcollison(ship1s, r1, done1, ship2s, r2, done2)

            if done1 and done2:
                break

if __name__ == '__main__':
    env = Maze()
    env.after(100, update)
    env.mainloop()