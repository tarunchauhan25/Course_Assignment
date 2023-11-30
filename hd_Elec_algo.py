# importing the required package 
import copy 
import numpy as np 
ans_final = []
class Faculty:
    def __init__(self, name, id, maxload, prefl,ele_pref,hd_cdc_pref,hd_elec_pref):
        self.name = name
        self.id = id
        self.maxload = maxload
        self.pref = []
        self.ele_pref = []
        self.hd_cdc_pref = []
        self.hd_elec_pref = []
        for i in prefl:
            self.pref.append([int(i), 0])
        for i in ele_pref:    
            self.ele_pref.append([int(i),0])
        for i in hd_cdc_pref:    
            self.hd_cdc_pref.append([int(i),0])
        for i in hd_elec_pref:
            self.hd_elec_pref.append([int(i),0])

class Initial_hdelec:
    def __init__(self, Faculties):
        self.faculties = Faculties
        self.totalCourses = 0
        self.matrix = []
        self.demands = []
        self.supply = []

    # find total number of courses 
    def findTotalCourses(self):
        n = len(self.faculties)
        self.totalCourses = 0
        for i in range(n):
            for j in range(len(self.faculties[i].hd_elec_pref)):
                self.totalCourses = max(self.totalCourses, self.faculties[i].hd_elec_pref[j][0])
        return self.generateMatrix()
    
    def generateMatrix(self):
        self.matrix = [[float('inf') for _ in range(self.totalCourses)] for _ in range(len(self.faculties))]
        for i in range(len(self.faculties)):
            for j in range(len(self.faculties[i].hd_elec_pref)):
                self.matrix[i][self.faculties[i].hd_elec_pref[j][0] - 1] = -1 
        return self.createDemand()

    def createDemand(self):
        self.demands = [2 for _ in range(self.totalCourses)]
        return self.createSupply()

    def createSupply(self):
        self.supply = [self.faculties[i].maxload for i in range(len(self.faculties))]
        return [self.matrix, self.demands, self.supply]

    
class Tricks_hdelec:
    def __init__(self, matrix, demand, supply, infinity):
            self.totalCourses = 0
            self.matrix = matrix
            self.demand = demand 
            self.originalDemand = len(copy.deepcopy(demand))
            self.originalSupply = len(copy.deepcopy(supply))
            self.supply = supply 
            self.infinity = infinity 
            self.rows = len(matrix)
            self.columns = len(matrix[0])
            self.ans = [[0 for _ in range(self.columns)] for _ in range(self.rows)]  # contains the assignment
            self.sleepingPenalties = []
            self.standingPenalties = []
            self.allAns = []
            self.complete = False

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
        return self.penalties()

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
        if (len(self.allAns)==0):
            if self.standingPenalties.count(0) == self.rows or self.rows == 0 or self.columns == 0:
                if self.ans not in self.allAns:
                    new = np.array(self.ans)
                    course_count = 0
                    for i in range(len(self.demand)-1): # for each course
                        divisions = 0
                        divisions = sum(new[:, i])
                        if(divisions==1):
                            new[:,i] = 0
                        elif(divisions!=0):
                            course_count+=1
                    self.coursesAssigned = course_count
                    self.allAns.append(new.tolist()) 
            else:
                if len(self.allAns) <= 3:
                    if self.complete == True:
                        return self.final()
                    else:
                        return self.operation()
                else:
                    return self.final()
        else:
            if self.standingPenalties.count(0) == self.rows or self.rows == 0 or self.columns == 0:
                if self.ans not in self.allAns:
                    for i in range(self.originalDemand): # for each course
                        divisions = 0
                        course_count = 0
                        for j in range(self.originalSupply): # iterate throught each professors
                            divisions += self.ans[j][i]
                        if divisions != 1:
                            if divisions != 0:
                                return
                        else:
                            course_count = course_count +1    
                    self.allAns.append(copy.deepcopy(self.ans)) 
            else:
                if len(self.allAns) <= 3:
                    if self.complete == True:
                        return self.final()
                    else:
                        return self.operation()
                else:
                    return self.final()
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
        self.complete = True 
        if self.complete == True:
            return self.final()

    def final(self):
        return self.allAns[-1],self.coursesAssigned
