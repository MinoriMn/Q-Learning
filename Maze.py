#!/usr/bin/env python
# coding: utf-8

# # 迷路自動生成アルゴリズム
# 棒倒し法による生成
# https://yottagin.com/?p=1557

# In[3]:


# 迷路生成アルゴリズム(棒倒し法) https://yottagin.com/?p=1557
import random

# 迷路生成クラス
class Maze():
    PATH = 0 #道
    WALL = 1 #壁
    
    def __init__(self, width, height):
        self.maze = []
        self.width = width
        self.height = height
        # 迷路は、幅高さ5以上の奇数で生成する
        if(self.width < 5 or self.height < 5):
            print("幅、高さは5以上で指定してください")
            exit()
        if self.width % 2 == 0:
            self.width += 1
        if self.height % 2 == 0:
            self.height += 1
        
    # 迷路データ初期化
    def set_out_wall(self):
        for x in range(0, self.width):
            row = []
            for y in range(0, self.height):
                if (x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1):
                    cell = self.WALL
                else:
                    cell = self.PATH
                row.append(cell)
            self.maze.append(row)
        return self.maze
    
    # 棒倒し
    def set_inner_wall_botaoshi(self):
        for x in range(2, self.width - 1, 2):
            for y in range(2, self.height - 1, 2):
                self.maze[x][y] = self.WALL
                while True:
                    if y == 2:
                        direction = random.randrange(0, 4)
                    else:
                        direction = random.randrange(0, 3)
                    wall_x = x
                    wall_y = y
                    
                    if direction == 0: # 右
                        wall_x += 1
                    elif direction == 1: # 下
                        wall_y += 1
                    elif direction == 2: # 左
                        wall_x -= 1
                    else: # 上
                        wall_y -= 1
                    
                    # 壁にする方向が壁でない場合は壁にする
                    if self.maze[wall_x][wall_y] != self.WALL:
                        self.maze[wall_x][wall_y] = self.WALL
                        break
        return self.maze
    
    def set_start_goal(self):
        """ スタートとゴールを迷路にいれる。"""
        self.maze[1][1] = 'S'
        self.maze[self.width-2][self.height-2] = 'G'
        return self.maze
    def print_maze(self):
        """ 迷路を出力する。TODO 迷路の描画機能"""
        for row in self.maze:
            for cell in row:
                if cell == self.PATH:
                    print('   ', end='')
                elif cell == self.WALL:
                    print('###', end='')
                elif cell == 'S':
                    print('STR', end='')
                elif cell == 'G':
                    print('GOL', end='')
            print()
# maze = Maze(20, 20)
# maze.set_out_wall()
# maze.set_inner_wall_botaoshi()
# maze.set_start_goal()
# maze.print_maze()


# In[ ]:




