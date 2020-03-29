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

# In[2]:


from abc import ABCMeta, abstractmethod
import random
from enum import Enum
from operator import itemgetter


# In[3]:


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
        if qMax & 1 > 0: 
            actions.append(Action.UP)
        elif qMax & 2 > 0: 
            actions.append(Action.DOWN)
        elif qMax & 4 > 0: 
            actions.append(Action.LEFT)
        elif qMax & 8 > 0: 
            actions.append(Action.RIGHT)
        return actions


# In[4]:


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


# In[5]:


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


# In[6]:


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
                qRow.append({Action.UP : 0, Action.DOWN : 0, Action.RIGHT : 0, Action.LEFT : 0, Action.MAX : 0})
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
        l = itemgetter(Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT)(self.qVal[x][y])
        self.qVal[x][y][Action.MAX] = sum([2 ** i for i, v in enumerate(l) if v == max(l)])
        
    def is_in_maze(self, x, y):
        if (x < 0) or (y < 0) or (x > self.width) or (y > self.height):
            return False
        else:
            return True


# In[ ]:




