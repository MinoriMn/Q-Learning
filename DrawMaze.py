#!/usr/bin/env python
# coding: utf-8

# # 迷路描画

# In[1]:


from PIL import Image, ImageDraw, ImageFont
from Reinforcement_Learning import Action
import numpy as np


# In[2]:


class DrawMaze:
    PATH = 0 #道
    WALL = 1 #壁
    STR = 'S' #スタート
    GOL = 'G' #ゴール
    def __init__(self, imgW, imgH, maze):
        self.wallColor = (16, 16, 16) #壁の色
        self.pathColor = (255, 255, 255) #道の色
        self.qMaxColor = (255, 165, 0) # Q値の色
        self.thisStateColor = (0, 255, 0) # 現在ステートの枠の色
        self.nextStateColor = (0, 128, 0) # 次回ステートの枠の色
        self.textColor = (0, 0, 0) # テキストの色
        self.outLineWidth = 4
        
        self.imgW = imgW
        self.imgH = imgH
        self.mazeW = len(maze)
        self.mazeH = len(maze[0])
        self.maze = maze
        # ひとマスのサイズ
        self.cW = int(self.imgW / self.mazeW)
        self.cH = int(self.imgH / self.mazeH)
        # 文字定義
        im = Image.new('RGB', (self.imgW, self.imgH), self.pathColor)
        draw = ImageDraw.Draw(im)
        texts = ["↑", "↓", "→", "←", "S", "G"]
        self.textData = []
        self.font_ttf = "/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc"
        draw.font = ImageFont.truetype(self.font_ttf, min(self.cW, self.cH))
        for text in texts:
            w, h = draw.textsize(text)
            self.textData.append([text, w, h])
        # 出力画像
        self.imgIdx = 0
        
    # 迷路描画
    def drawMaze(self, learning, qMax, sx, sy, nx, ny):
        im = Image.new('RGB', (self.imgW, self.imgH), self.pathColor)
        draw = ImageDraw.Draw(im)
        draw.font = ImageFont.truetype(self.font_ttf, min(self.cW, self.cH))
        
        # マスごとに描画
        for x in range(0, self.mazeW):
            for y in range(0, self.mazeH):
                m = self.maze[x][y]
                if m == self.WALL:
                    draw.rectangle((x * self.cW, y * self.cH, (x + 1) * self.cW, (y + 1) * self.cH), fill=self.wallColor, outline=self.wallColor)
                else:
                    _action, v = learning.get_q_max_val(x, y)
                    color = [qc * v + pc * (qMax - v) for (qc, pc) in zip(self.qMaxColor, self.pathColor)]
                    color = tuple(map(lambda c: int(c / qMax), color))
                    # マス描画
                    if x == sx and y == sy:
                        draw.rectangle((x * self.cW, y * self.cH, (x + 1) * self.cW, (y + 1) * self.cH), fill=self.thisStateColor, outline=self.thisStateColor)
                        draw.rectangle((x * self.cW + self.outLineWidth, y * self.cH + self.outLineWidth, (x + 1) * self.cW - self.outLineWidth, (y + 1) * self.cH - self.outLineWidth), fill=color, outline=color)
                    elif x == nx and y == ny:
                        draw.rectangle((x * self.cW, y * self.cH, (x + 1) * self.cW, (y + 1) * self.cH), fill=self.nextStateColor, outline=self.nextStateColor)
                        draw.rectangle((x * self.cW + self.outLineWidth, y * self.cH + self.outLineWidth, (x + 1) * self.cW - self.outLineWidth, (y + 1) * self.cH - self.outLineWidth), fill=color, outline=color)
                    else:
                        draw.rectangle((x * self.cW, y * self.cH, (x + 1) * self.cW, (y + 1) * self.cH), fill=color, outline=color)
                        
                    # 文字描画
                    if self.maze[x][y] == self.STR: #スタート
                        draw.text((x * self.cW + (self.cW - self.textData[4][1]) / 2, y * self.cH + (self.cH - self.textData[4][2]) / 2), self.textData[4][0], fill=self.textColor)
                    elif self.maze[x][y] == self.GOL: #ゴール
                        draw.text((x * self.cW + (self.cW - self.textData[5][1]) / 2, y * self.cH + (self.cH - self.textData[5][2]) / 2), self.textData[5][0], fill=self.textColor)
                    
                    actionMax = learning.qVal[x][y][Action.MAX]
                    actions = Action.max_to_actions(actionMax)
                    if Action.UP in actions: #UP
                        draw.text((x * self.cW + (self.cW - self.textData[0][1]) / 2, y * self.cH + (self.cH - self.textData[0][2]) / 2), self.textData[0][0], fill=self.textColor)
                    if Action.DOWN in actions: #DOWN
                        draw.text((x * self.cW + (self.cW - self.textData[1][1]) / 2, y * self.cH + (self.cH - self.textData[1][2]) / 2), self.textData[1][0], fill=self.textColor)
                    if Action.RIGHT in actions: #RIGHT
                        draw.text((x * self.cW + (self.cW - self.textData[2][1]) / 2, y * self.cH + (self.cH - self.textData[2][2]) / 2), self.textData[2][0], fill=self.textColor)
                    if Action.LEFT in actions: #LEFT
                        draw.text((x * self.cW + (self.cW - self.textData[3][1]) / 2, y * self.cH + (self.cH - self.textData[3][2]) / 2), self.textData[3][0], fill=self.textColor)
        im.save('output/images/img_' + str(self.imgIdx)+ '.jpg')
        self.imgIdx = self.imgIdx + 1


# In[3]:


# maze = [
#     [1, 1, 1, 1, 1],
#     [1, 'S', 1, 1, 1],
#     [1, 0, 0, 1, 1],
#     [1, 1, 0, 'G', 1],
#     [1, 1, 1, 1, 1]
# ]
# # 迷路描画機能
# imgW = 800
# imgH = 800
# draw = DrawMaze(imgW, imgH, maze)


# In[ ]:




