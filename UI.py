from Field import *
from tkinter import *
import threading
import time

class UI:
    def __init__(self):
        self.field = 0
        self.speed = 1
        self.mPress = 0
        self.hover = 0
        self.cells = []
        self.cellWidth = 32
        self.cellHeight = 32
        self.pause = 1
        self.start = 0
        self.InitUI()

    def InitUI(self):
        self.root = Tk()
        self.root.title("Jivi")
        self.root.resizable(False,False)
        self.canvas = Canvas(self.root, width = 319, height = 319,bg = "white",highlightbackground = "black",
                             highlightthickness=2)
        bFrame = Frame(self.root, bd = 20)

        startButton = Button( bFrame,text="Start",width = 5, command = self.Start)
        pauseButton = Button( bFrame, text="Pause",width = 5, command = self.Pause)
        nullMatButton = Button( bFrame, text="Null",width = 5, command = self.NullMat)
        randMatButton = Button( bFrame, text="Rand",width = 5, command = self.RandMat)
        frameScale = Scale(bFrame, orient=HORIZONTAL,from_=0.5, to_=2,resolution = 0.1, length = 45,
                           sliderlength = 20,command = self.ChangeFrameRate)
        frameScale.set(self.speed)
        startButton.grid(row=1,column=1)
        pauseButton.grid(row=2,column=1)
        nullMatButton.grid(row=3,column=1)
        randMatButton.grid(row=4,column=1)
        frameScale.grid(row = 5, column = 1)
        bFrame.pack(side="left")
        self.canvas.pack()

        self.canvas.bind("<Motion>", self.MouseMove)
        self.canvas.bind("<ButtonRelease>", self.MouseRelease)
        self.canvas.bind("<ButtonPress>", self.cellClk)
        self.CreateField(self.cellHeight, self.cellWidth,10)
        self.root.mainloop()


    def CreateField(self, row, column, s):
        self.field = Field(row, column)
        color = 0
        for i in range(row):
            for j in range(column):
                if self.field.field[i][j] == 0:
                    color = "white"
                else: color = "black"
                rect = self.canvas.create_rectangle(j*s, i*s, s*(j+1),s*(i+1), fill = color, outline = "black")
                self.cells.append([i,j])

    def cellClk(self,event):
        if self.start:
            return
        self.mPress=event.num

        cell = event.widget.find_withtag("current")[0]
        cellValue = self.field.field[self.cells[cell - 1][0]][self.cells[cell - 1][1]]
        nextCellValue = cellValue
        if self.mPress == 1 and cellValue==0:
            self.field.field[self.cells[cell - 1][0]][self.cells[cell - 1][1]] = 1
            nextCellValue = 1
        elif self.mPress==3 and cellValue==1:
            self.field.field[self.cells[cell - 1][0]][self.cells[cell - 1][1]] = 0
            nextCellValue = 0

        if cellValue ==0 and nextCellValue==1:
            self.canvas.itemconfig(cell, fill="black")
        elif cellValue ==1 and nextCellValue==0:
            self.canvas.itemconfig(cell, fill="white")

    def MouseMove(self,event):
        if self.start:
            return

        if self.mPress==0 or self.mPress==2:
            return
        cell = event.widget.find_closest(event.x,event.y)[0]
        if self.hover == cell:
            return

        self.hover = cell

        cellValue = self.field.field[self.cells[cell - 1][0]][self.cells[cell - 1][1]]
        nextCellValue = cellValue
        if self.mPress == 1 and cellValue == 0:
            self.field.field[self.cells[cell - 1][0]][self.cells[cell - 1][1]] = 1
            nextCellValue = 1
        elif self.mPress == 3 and cellValue == 1:
            self.field.field[self.cells[cell - 1][0]][self.cells[cell - 1][1]] = 0
            nextCellValue = 0

        if cellValue == 0 and nextCellValue == 1:
            self.canvas.itemconfig(cell, fill="black")
        elif cellValue == 1 and nextCellValue == 0:
            self.canvas.itemconfig(cell, fill="white")

        print(cell)

    def MouseRelease(self,event):
        self.mPress = 0

    def Start(self):
        if self.start == 0:
            self.start = 1
            self.pause = 0
        else: return
#======================ТОТ САМЫЙ ПОТОК==============================
        self.evolThread = threading.Thread(target=self.StartEvolution)
#===================================================================
        self.evolThread.daemon = True
        self.evolThread.start()

    def Pause(self):
        if self.pause == 0:
            self.pause = 1
            self.start = 0

    def NullMat(self):
        if self.pause != 1:
            return
        tempMat = Field.CreateNullMatrix(self.cellHeight, self.cellWidth)
        self.field.prevField =  self.field.field
        self.field.field = tempMat
        self.DrawCells()

    def RandMat(self):
        if self.pause != 1:
            return
        tempMat = Field.CreateRandomMatrix(self.cellHeight, self.cellWidth)
        self.field.prevField = self.field.field
        self.field.field = tempMat
        self.DrawCells()

    def ChangeFrameRate(self,event):
        self.speed = float(event)
        print(event)
#=============ФУНКЦИЯ В КОТОРОЙ СРАБАТЫВАЕТ МЕТОД DrawCells=============================
    def NextStep(self):
        self.field.ComputeNextMatrix()
        self.DrawCells()
#======================================================
#==============ТОТ САМЫЙ МЕТОД DrawCells===============
    def DrawCells(self):
        cell = 1
        for i in self.cells:
            cellValue = self.field.field[i[0]][i[1]]
            cellPrevValue = self.field.prevField[i[0]][i[1]]
            if cellValue == 1 and cellPrevValue == 0:
#=======Вот здесь, при работе метода айтемконфиг в потоке,почему-то обрабатывается в несколько раз дольше, чем без потока
                self.canvas.itemconfig(cell, fill="black")
            elif cellValue == 0 and cellPrevValue == 1:
                self.canvas.itemconfig(cell, fill="white")
            cell += 1
#=======================================================
#==========ФУНКЦИЯ ОБРАБАТЫВАЕМАЯ ТЕМ САМЫМ ПОТОКОМ===========
    def StartEvolution(self):
         while self.pause == 0:
             self.NextStep()
             time.sleep(self.speed)

#=============================================================
