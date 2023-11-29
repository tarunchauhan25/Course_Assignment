import copy 

class Faculty:
    def __init__(self, name, id, maxload, prefl):
        self.name = name
        self.id = id
        self.maxload = maxload
        self.pref = []
        for i in prefl:
            self.pref.append([int(i), 0])
        # print(self.pref)

class Initial:
    def __init__(self, Faculties):
        self.faculties = Faculties
        self.totalCourses = 0
        self.matirx = []
        self.demands = []
        self.supply = []

    # find total number of courses 
    def findTotalCourses(self):
        n = len(self.faculties)
        self.totalCourses = 0
        for i in range(n):
            for j in range(len(self.faculties[i].pref)):
                self.totalCourses = max(self.totalCourses, self.faculties[i].pref[j][0])
        self.generateMatrix()
    
    def generateMatrix(self):
        self.matrix = [[float('inf') for _ in range(self.totalCourses)] for _ in range(len(self.faculties))]
        for i in range(len(self.faculties)):
            for j in range(len(self.faculties[i].pref)):
                self.matrix[i][self.faculties[i].pref[j][0] - 1] = 1 
        print(self.matrix)
        self.createDemand()

    def createDemand(self):
        self.demands = [1 for _ in range(self.totalCourses)]
        self.createSupply()

    def createSupply(self):
        self.supply = [self.faculties[i].maxload //2 for i in range(len(self.faculties))]
        ans = Tricks(self.matrix, self.demands, self.supply, float('inf'))
        ans.balance()
        ans.final()
        # return ans 


    
class Tricks:
    def __init__(self, matrix, demand, supply, infinity):
        self.totalCourses = 0
        self.matrix = matrix
        self.demand = demand 
        self.supply = supply 
        self.infinity = infinity 
        self.rows = len(matrix)
        self.columns = len(matrix[0])
        self.ans = [[0 for _ in range(self.columns)] for _ in range(self.rows)]  # contains the assignment
        self.sleepingPenalties = []
        self.standingPenalties = []
        self.allAns = []


    def balance(self):
        # balance an unbalanced matrix
        totalDemand = sum(self.demand)
        totalSupply = sum(self.supply)
        if totalDemand > totalSupply:
            # introduce dummy faculty
            self.matrix.append([self.infinity for _ in range(self.columns)])
            self.supply.append(totalDemand - totalSupply)
        elif totalDemand < totalSupply:
            # introduce dummy course
            for i in range(self.rows):
                self.matrix[i].append(self.infinity)
            self.demand.append(totalSupply - totalDemand)
        self.penalties()

    def penalties(self):
        # setting penalties for rows
        for i in range(self.rows):
            tempSet = set(self.matrix[i])
            tempList = list(tempSet)
            tempList.sort()
            if len(tempList) == 1:
                if tempList[0] == self.infinity:
                    self.standingPenalties.append(0)
                else:
                    self.standingPenalties.append(tempList[0])                    
            else:
                self.standingPenalties.append(tempList[1] - tempList[0])

        # setting penalties for columns
        for i in range(self.columns):
            tempVal = [self.matrix[j][i] for j in range(self.rows)]
            tempSet = set(tempVal)
            tempList = list(tempSet)
            if len(tempList) == 1:
                if tempList[0] == self.infinity:
                    self.sleepingPenalties.append(0)
                else:
                    self.sleepingPenalties.append(tempList[0])
            else:
                self.sleepingPenalties.append(tempList[1] - tempList[0])
        
        # condition to stop doing operation
        if self.standingPenalties.count(0) == self.rows or self.rows == 0 or self.columns == 0:
            if self.ans not in self.allAns:
                self.allAns.append(copy.deepcopy(self.ans)) 
        else:
            if len(self.allAns) <= 10:
                self.operation()
    
    # main algorithm
    def operation(self):
        maxPenalty = max(max(self.standingPenalties), max(self.sleepingPenalties))
        copyMatrix = copy.deepcopy(self.matrix)
        copyDemand = self.demand.copy()
        copySupply = self.supply.copy()
        copyRows = self.rows 
        copyColumns = self.columns 
        copyAns = copy.deepcopy(self.ans)
        copyStandingPenalty = self.standingPenalties.copy()
        copySleepingPenalty = self.sleepingPenalties.copy()

        # to check for every case
        for i in range(self.rows):
            if self.standingPenalties[i] == maxPenalty:
                minPref = min(self.matrix[i])
                if minPref != self.infinity:
                    courseIndex = self.matrix[i].index(minPref)
                    minSD = min(self.supply[i], self.demand[courseIndex])
                    self.ans[i][courseIndex] = minSD 
                    self.supply[i] -= minSD 
                    self.demand[courseIndex] -= minSD 
                    if self.supply[i] == 0:
                        self.matrix[i] = [self.infinity for _ in range(self.columns)]
                        self.supply[i] = 0
                    if self.demand[courseIndex] == 0:
                        for j in range(self.rows):
                            self.matrix[j][courseIndex] = self.infinity
                        self.demand[courseIndex] = self.infinity
                    self.standingPenalties = []
                    self.sleepingPenalties = []
                    self.penalties()

                    # setting them back to original values
                    self.matrix = copy.deepcopy(copyMatrix)
                    self.demand = copyDemand.copy()
                    self.supply = copySupply.copy()
                    self.rows = copyRows
                    self.columns = copyColumns 
                    self.ans = copy.deepcopy(copyAns)
                    self.standingPenalties = copyStandingPenalty.copy()
                    self.sleepingPenalties = copySleepingPenalty.copy()
                else:
                    pass 
        
        for i in range(self.columns):
            if self.sleepingPenalties[i] == maxPenalty:
                tempPrefs = [self.matrix[j][i] for j in range(self.rows)]
                minPref = min(tempPrefs)
                if minPref != self.infinity:
                    profIndex = tempPrefs.index(minPref)
                    minSD = min(self.supply[profIndex], self.demand[i])
                    self.ans[profIndex][i] = minSD 
                    self.supply[profIndex] -= minSD
                    self.demand[i] -= minSD 
                    if self.supply[profIndex] == 0:
                        self.matrix[profIndex] = [self.infinity for _ in range(self.columns)]
                        self.supply[profIndex] = 0
                    if self.demand[i] == 0:
                        for j in range(self.rows):
                            self.matrix[j][i] = self.infinity
                        self.demand[i] = 0
                    self.standingPenalties = []
                    self.sleepingPenalties = []
                    self.penalties()

                    self.matrix = copy.deepcopy(copyMatrix)
                    self.demand = copyDemand.copy()
                    self.supply = copySupply.copy()
                    self.rows = copyRows
                    self.columns = copyColumns 
                    self.ans = copy.deepcopy(copyAns)
                    self.standingPenalties = copyStandingPenalty.copy()
                    self.sleepingPenalties = copySleepingPenalty.copy()
                else:
                    pass 

    def final(self):
        print(self.allAns)


input =[Faculty("a", 1, 3, [3,2,1,5]),Faculty("b", 2, 3, [1 , 2 , 4 ,3]),Faculty("c", 3, 3, [4 , 2 , 1 , 3]),Faculty("d",4, 3, [4,2,1,5]),Faculty("e", 5,3,[2,3,1,5])]
t = Initial(input)
t.findTotalCourses()
# print((t))
# print(input[0])

# print(ans)

# infinite = float('inf')
# t = Tricks([[infinite, 1, infinite, 2, infinite], [1, 2, infinite, infinite, infinite], [1, 2, 3, 4, infinite]], [1, 1, 1, 1, 1], [1.5, 1.5, 1], infinite)
# t.penalties()
# t.final()

# t2 = Tricks([[1, 2, 3], [3, 1, 2], [3, 2, 1]], [1, 1, 1], [1.5, 1.5, 1.5], infinite)
# t2.balance()
# t2.final()

# t3 = Tricks([[1], [1]], [1], [1, 1], infinite)
# t3.balance() 
# t3.final()
