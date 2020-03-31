#!/usr/bin/env python
# coding: utf-8

# # 迷路描画

# In[1]:


from PIL import Image, ImageDraw
from Reinforcement_Learning import Action


# In[2]:


class DrawMaze:
    PATH = 0 #道
    WALL = 1 #壁
    STR = 'S' #スタート
    GOL = 'G' #ゴール
    wallColor = (16, 16, 16) #壁の色
    pathColor = (255, 255, 255) #道の色
    qMaxColor = (255, 165, 0) # Q値の色
    thisStateColor = (0, 255, 0) # 現在ステートの枠の色
    nextStateColor = (0, 128, 0) # 次回ステートの枠の色
    textColor = (0, 0, 0) # テキストの色
    outLineWidth = 4
    
    def __init__(self, imgW, imgH, maze):
        self.imgW = imgW
        self.imgH = imgH
        self.mazeW = len(maze)
        self.mazeH = len(maze[0])
        self.maze = maze
        # ひとマスのサイズ
        self.cW = self.imgW / self.mazeW 
        self.cH = self.imgH / self.mazeH
        # 文字定義
        im = Image.new('RGB', (self.imgW, self.imgH), pathColor)
        draw = ImageDraw.Draw(im)
        msg = ['↑', '↓', '→', '←', 'S', 'G']
        self.textData = []
        for i in range(0, len(msg)):
            w, h = draw.textsize(msg)
            self.textData.append([msg[i], w, h])
        
    def drawMaze(self, qVal, qMax, sx, sy, nx, ny):
        im = Image.new('RGB', (self.imgW, self.imgH), pathColor)
        draw = ImageDraw.Draw(im)
        
        for x in range(0, self.mazeW):
            for y in range(0, self.mazeH):
                m = self.maze[x][y]
                if m == WALL:
                    draw.rectangle((x * self.cW, y * self.cH, (x + 1) * self.cW, (y + 1) * self.cH), fill=wallColor, outline=wallColor)
                else:
                    v = qVal[x][y]
                    color = [pc * v + qc * (qMax - v) for (pc, qc) in zip(pathColor, qMaxColor)]
                    color = list(map(lambda c: c / qMax, color))
                    # マス描画
                    if x == sx and y == sy:
                        draw.rectangle((x * self.cW, y * self.cH, (x + 1) * self.cW, (y + 1) * self.cH), fill=thisStateColor, outline=thisStateColor)
                        draw.rectangle((x * self.cW + outLineWidth, y * self.cH + outLineWidth, (x + 1) * self.cW - outLineWidth, (y + 1) * self.cH - outLineWidth), fill=color, outline=color)
                    elif x == nx and y == ny:
                        draw.rectangle((x * self.cW, y * self.cH, (x + 1) * self.cW, (y + 1) * self.cH), fill=nextStateColor, outline=nextStateColor)
                        draw.rectangle((x * self.cW + outLineWidth, y * self.cH + outLineWidth, (x + 1) * self.cW - outLineWidth, (y + 1) * self.cH - outLineWidth), fill=color, outline=color)
                    else:
                        draw.rectangle((x * self.cW, y * self.cH, (x + 1) * self.cW, (y + 1) * self.cH), fill=color, outline=color)
                        
                    # 文字描画
                    if self.maze[x][y] == STR: #スタート
                        draw.text((x * self.cW + (self.cW - self.textData[4][1]) / 2, draw_y + (self.cH - self.textData[4][2]) / 2), self.textData[4][0], font=font, fill=textColor)
                    elif self.maze[x][y] == GOL: #ゴール
                        draw.text((x * self.cW + (self.cW - self.textData[5][1]) / 2, draw_y + (self.cH - self.textData[5][2]) / 2), self.textData[5][0], font=font, fill=textColor)
                    
                    actionMax = qVal[x][y][Action.MAX]
                    if actionMax & Action.UP > 0: #UP
                        draw.text((x * self.cW + (self.cW - self.textData[0][1]) / 2, draw_y + (self.cH - self.textData[0][2]) / 2), self.textData[0][0], font=font, fill=textColor)
                    if actionMax & Action.DOWN > 0: #DOWN
                        draw.text((x * self.cW + (self.cW - self.textData[1][1]) / 2, draw_y + (self.cH - self.textData[1][2]) / 2), self.textData[1][0], font=font, fill=textColor)
                    if actionMax & Action.RIGHT > 0: #RIGHT
                        draw.text((x * self.cW + (self.cW - self.textData[2][1]) / 2, draw_y + (self.cH - self.textData[2][2]) / 2), self.textData[2][0], font=font, fill=textColor)
                    if actionMax & Action.LEFT > 0: #LEFT
                        draw.text((x * self.cW + (self.cW - self.textData[3][1]) / 2, draw_y + (self.cH - self.textData[3][2]) / 2), self.textData[3][0], font=font, fill=textColor)


# In[ ]:




