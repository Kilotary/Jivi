import random
class Field:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.field = self.CreateRandomMatrix(row, column)
        self.prevField = 0

    @staticmethod
    def CreateNullMatrix(row, column):
        fieldTemp = []
        for i in range(row):
            fieldTemp.append([])
            for j in range(column):
                fieldTemp[i].append(0)
        return fieldTemp

    @staticmethod
    def CreateRandomMatrix(row, column):
        fieldTemp = []
        for i in range(row):
            fieldTemp.append([])
            for j in range(column):
                fieldTemp[i].append(random.randint(0,1))

        return fieldTemp

    def ComputeNextMatrix(self):
        tempMat = self.CreateNullMatrix(self.row, self.column)
        sum = 0

        for i in range(self.row):
            for j in range(self.column):
                for k in range(i-1,i+2,1):
                    for n in range(j-1,j+2,1):

                        if k < 0:
                            k=self.row-1
                        elif k > self.row-1:
                            k=0

                        if n < 0:
                            n = self.column- 1
                        elif n > self.row - 1:
                            n = 0

                        if k == i and n == j:continue

                        if self.field[k][n] == 1:
                            sum +=1

                if self.field[i][j] == 1 and (sum == 2 or sum == 3):
                    tempMat[i][j] = 1
                elif self.field[i][j] == 0 and sum == 3:
                    tempMat[i][j] = 1
                else: tempMat[i][j] = 0

                sum = 0
        self.prevField = self.field
        self.field = tempMat