"""
Reinforcement learning maze example.
Writen by Morvan: https://morvanzhou.github.io/tutorials/
Modified by Weijian: weijiany@stud.ntnu.no

Red rectangle:         ship (explorer)
Black rectangles:     obstracte
Yellow bin circle:     goal
All other states:       open sea
"""


import numpy as np
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

UNIT = 40       # pixels: distance between 2 points
MAZE_H = 10     # grid height
MAZE_W = 10     # grid width
# Map Initialization
# Be careful to create origin
# Origin would be located at the upper left corner of the map.
# X-axis points to the right
# Y-axis points down
origin = np.array([20, 20])  # origin[X,Y]
obst1_center = origin + np.array([UNIT * 2, UNIT])
ship1_center = origin + np.array([UNIT * 4, 0])
goal1_center = origin + np.array([UNIT * 4, UNIT * 9])

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

        # create obstracte
        self.obst1 = self.canvas.create_rectangle(
            obst1_center[0] - 15, obst1_center[1] - 15,
            obst1_center[0] + 15, obst1_center[1] + 15,
            fill='black')

        # obst2_center = origin + np.array([UNIT, UNIT * 2])
        # self.obst2 = self.canvas.create_rectangle(
        #     obst2_center[0] - 15, obst2_center[1] - 15,
        #     obst2_center[0] + 15, obst2_center[1] + 15,
        #     fill='black')

        # create goal
        self.goal1 = self.canvas.create_oval(
            goal1_center[0] - 15, goal1_center[1] - 15,
            goal1_center[0] + 15, goal1_center[1] + 15,
            fill='yellow')

        # create ship
        self.ship1 = self.canvas.create_rectangle(
            ship1_center[0] - 15, ship1_center[1] - 15,
            ship1_center[0] + 15, ship1_center[1] + 15,
            fill='yellow')

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

        # return observation
        return self.canvas.coords(self.ship1)

    def step(self, action):
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
            reward1 = 1
            done1 = True
            ship1s_ = 'terminal'
        # elif s_ in [self.canvas.coords(self.obst1), self.canvas.coords(self.obst2)]:
        elif ship1s_ in [self.canvas.coords(self.obst1)]:
            reward1 = -1
            done1 = True
            ship1s_ = 'terminal'
        else:
            reward1 = 0
            done1 = False

        return ship1s_, reward1, done1

    def render(self):
        time.sleep(0.1)
        self.update()

def update():
    for t in range(10):
        env.reset()
        while True:
            env.render()
            a = 1
            ship1s, r1, done1 = env.step(a)
            if done1:
                break

if __name__ == '__main__':
    env = Maze()
    env.after(100, update)
    env.mainloop()