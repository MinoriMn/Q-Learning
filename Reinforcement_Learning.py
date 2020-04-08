#!/usr/bin/env python
# coding: utf-8

# # Q学習用クラス
# ## Q data
# `Q[x座標][y座標]["上","下","右","左","B"]`
# 
# `"上","下","右","左"`->Q値
# 
# `"B"`->その時点での最大Q値の方向("上","下","右","左", "")
# 
# QData側では壁と道の区別はしない

# In[1]:


from abc import ABCMeta, abstractmethod
import random
from enum import Enum
from operator import itemgetter
import csv
import sys


# In[2]:


# 行動
class Action(Enum):
    UP = 1
    DOWN = 2
    LEFT = 4
    RIGHT = 8
    MAX = 64
    
    @staticmethod
    def action_to_transition(action):
        dx, dy = 0, 0
        if action == Action.UP:
            dx, dy = 0, -1
        elif action == Action.DOWN:
            dx, dy = 0, 1
        elif action == Action.LEFT:
            dx, dy = -1, 0
        elif action == Action.RIGHT:
            dx, dy = 1, 0
        return dx, dy
    
    @staticmethod
    def max_to_actions(qMax):
        actions = []
        qMax = int(qMax)
        if qMax & 1 > 0: 
            actions.append(Action.UP)
        elif qMax & 2 > 0: 
            actions.append(Action.DOWN)
        elif qMax & 4 > 0: 
            actions.append(Action.LEFT)
        elif qMax & 8 > 0: 
            actions.append(Action.RIGHT)
        return actions


# In[3]:


#Q値更新
class QUpdate(metaclass=ABCMeta):
    @abstractmethod
    def update_q_val(self, parameter):
        pass
    
#Q学習
class QLearning(QUpdate):
    def __init__(self, learningRate, discountRate):
        self.alpha = learningRate
        self.gamma = discountRate
    def set_learning_rate(learningRate):
        self.alpha = learningRate
    def set_learning_rate(discountRate):
        self.gamma = discountRate        

    def update_q_val(self, parameter):
        return self.__cal_q(*parameter)
    def __cal_q(self, qt, maxqt1, reward):
        return qt + self.alpha * (reward + self.gamma * maxqt1 - qt)


# In[4]:


# 行動選択方法
class ActionSelect(metaclass=ABCMeta):
    @abstractmethod
    def get_next_state(self, qData):
        pass
    
# ε-greedy
class EpGreedy(ActionSelect):
    def __init__(self, epsilon):
        self.epsilon = epsilon
    def set_epsilon(self, epsilon):
        self.epsilon = epsilon
        
    def get_next_state(self, qData):
        if (qData[Action.MAX] == 0) or (random.random() <= self.epsilon):
            return random.choice(list(Action))
        else:
            qMax = qData[Action.MAX]
            actions = Action.max_to_actions(qMax)
            return actions[random.randrange(len(actions))]


# In[3]:


class ReinforcementLearning:    
    # qUpdate ... Q値更新方法, actionSelect ... action選択方法
    def __init__(self, width, height, qUpdate, actionSelect):
        self.width = width
        self.height = height
        qVal = []
        self.qUpdate = qUpdate
        self.actionSelect = actionSelect

        for x in range(0, self.width):
            qRow = []
            for y in range(0, self.height):
                qRow.append({Action.UP : 0, Action.DOWN : 0, Action.RIGHT : 0, Action.LEFT : 0, Action.MAX : int(0)})
            qVal.append(qRow)
        
        self.qVal = qVal
        
    # 次のstateを選択し取得
    def get_next_state(self, x, y):
        while True:
            action = self.actionSelect.get_next_state(self.qVal[x][y])
            dx, dy = Action.action_to_transition(action)
            _x = x + dx
            _y = y + dy
            if self.is_in_maze(_x, _y):
                break
        return _x, _y, action
    
    # Q値取得
    def get_q_val(self, x, y, action):
        return self.qVal[x][y][action]
    # そのstateでの最大Q値を取得
    def get_q_max_val(self, x, y):
        qMax = self.qVal[x][y][Action.MAX]
        if qMax != 0:
            actions = Action.max_to_actions(qMax)
            return actions[0], self.qVal[x][y][actions[0]]
        else:
            return Action.UP, self.qVal[x][y][Action.UP]
        
    # Q値更新
    def update_q_val(self, x, y, action, parameter):
        self.qVal[x][y][action] = self.qUpdate.update_q_val(parameter)
        self.update_q_max(x, y)
    # 最大Q値更新
    def update_q_max(self, x, y):
        item = itemgetter(Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT)(self.qVal[x][y])
        mV = max(item)
        if mV != 0:
            self.qVal[x][y][Action.MAX] = sum([2 ** i for i, v in enumerate(item) if v == mV])
        
    def is_in_maze(self, x, y):
        if (x < 0) or (y < 0) or (x > self.width) or (y > self.height):
            return False
        else:
            return True
        
    def import_q_data(self, mainfilename, datafilename, addAction):
        # Mainデータ読み込み
        with open(mainfilename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
#                 print(row)
                if row[0] == 'action':
                    startAction = int(row[1]) # 開始行動数
                    finAction = startAction + addAction # 終了行動数
                elif row[0] == 'resetAction':
                    resetAction = int(row[1])
                elif row[0] == 'sx':
                    sx = int(row[1])
                elif row[0] == 'sy':
                    sy = int(row[1])
                elif row[0] == 'mWidth':
                    if self.width != int(row[1]):
                        sys.exit()
                elif row[0] == 'mHeight':
                    if self.height != int(row[1]):
                        sys.exit()
                
        print('startAction:%d, finAction:%d, resetAction:%d, sx:%d, sy:%d' % (startAction, finAction, resetAction, sx, sy))

        #　Q値読み込み
        with open(datafilename, 'r') as f:
            h = next(csv.reader(f))
            print(h)
            for idx, row in enumerate(csv.reader(f)):
                self.qVal[idx // self.width][idx % self.height] = {Action.UP : float(row[2]), Action.DOWN : float(row[3]), Action.RIGHT : float(row[4]), Action.LEFT : float(row[5]), Action.MAX : int(float(row[6]))}
                print(row)
                
        return startAction, finAction, resetAction, sx, sy
        
    def export_q_data(self, mainfilename, datafilename, action, resetAction, sx, sy):
        with open(mainfilename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['action', action]) #行動数
            writer.writerow(['resetAction', resetAction])
            writer.writerow(['sx', sx])
            writer.writerow(['sy', sy])
            writer.writerow(['mWidth', self.width])
            writer.writerow(['mHeight', self.height]) 
            writer.writerow(['mHeight', self.height]) 

        keys = self.qVal[0][0].keys()
        header = ['x', 'y'] + list(keys)#ヘッダー用のデータを作っておく
        print(header)
        
        with open(datafilename,"w") as f:
            # headerも渡してやる
            # 渡した順番が列の順番になる
            writer = csv.writer(f)

            # そのままだとヘッダーは書き込まれないので、ここで書く
            writer.writerow(header)

            for x,  row in enumerate(self.qVal):
                for y,  val in enumerate(row):
                    data = [x, y] + list(val.values())
                    writer.writerow(data)


# In[ ]:




