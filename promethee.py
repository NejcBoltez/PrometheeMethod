import numpy

class Promethee:
    def __init__(self, alternatives, weights, criterias, criteriasType, matrix):
        self.alternatives = alternatives
        self.weights=weights
        self.criterias=criterias
        self.matrix=matrix
        self.criteriasType = criteriasType
        #print(matrix)
        self.criteriaMax=[-999 for x in range(len(self.criterias))]
        self.criteriaMin=[-999 for x in range(len(self.criterias))]
        self.normalizedMatrix=[]
        self.findCriteriaMaxAndMin()
        self.normalizeMatrix()
        self.DifferencesMatrix()
        self.preferencesMatrix()
        self.aggregatedPreferencesMatrix()
        self.sumOfTheRows()
        self.comparisonMatrix()
        self.enteringFlow()
        self.leavingFlow()
        self.ranking()
    def findCriteriaMaxAndMin(self):
        self.criteriaMax = self.matrix[0][:]
        self.criteriaMin = self.matrix[0][:]
        
        for xMax in self.matrix:
            for iMax in range (len(xMax)):
                if (self.criteriaMax[iMax]<xMax[iMax]):
                    self.criteriaMax[iMax] = xMax[iMax]
        for xMin in self.matrix:
            for iMin in range (len(xMin)):
                if (self.criteriaMin[iMin]>xMin[iMin]):
                    self.criteriaMin[iMin] = xMin[iMin]
                    
        #print(self.criteriaMax)
        #print(self.criteriaMin)
        
    def normalizeMatrix(self):
        #Normalization
        self.normalizedMatrix=self.matrix[:]
        for x in range (len(self.matrix)):
            for i in range (len(self.matrix[x])):
                if (self.criteriaMax[i] - self.criteriaMin[i] == 0):
                    self.normalizedMatrix[x][i] = 0
                else:
                    if (str(self.criteriasType[i]).lower() == "non-beneficial"):
                        self.normalizedMatrix[x][i]=((self.criteriaMax[i] - self.matrix[x][i]) / (self.criteriaMax[i] - self.criteriaMin[i]))
                    else :
                        self.normalizedMatrix[x][i]=((self.matrix[x][i]-self.criteriaMin[i]) / (self.criteriaMax[i] - self.criteriaMin[i]))
       # print("NORMALIZED: " + str(self.normalizedMatrix))
    
    def DifferencesMatrix(self):
        #Diferences
        self.diferencesMatrix=[[0 for x in range(len(self.criterias))] for y in range(len(self.alternatives)*(len(self.alternatives)-1))] 
        self.TestdiferencesMatrix=[[0 for x in range(len(self.criterias))] for y in range(len(self.alternatives)*(len(self.alternatives)-1))] 
        #print(self.diferencesMatrix)
        linePosition = 0
        for i in range(len(self.alternatives)):
            for k in range(len(self.alternatives)):
                for c in range(len(self.criterias)):
                    values= []
                    selectedValue = 0;
                    for v in self.normalizedMatrix:
                        values.append(v[c])
                        selectedValue += 1
                    print(values)
                    for d in range(len(values)):
                        if (i != k):
                            self.diferencesMatrix[linePosition][c] = values[i] - values[k]
                            d += 1
                            #print(k)
                if (i != k):
                    linePosition += 1  
        #print(self.TestdiferencesMatrix)
        print(self.normalizedMatrix)
        print(self.diferencesMatrix)
        
    def preferencesMatrix(self):
        self.preferencesMatrix = self.diferencesMatrix[:]
        for p in range(len(self.preferencesMatrix)):
            for x in range(len(self.preferencesMatrix[p])):
                if (self.preferencesMatrix[p][x]<0):
                    self.preferencesMatrix[p][x] = 0
        print(self.preferencesMatrix)
        
    def aggregatedPreferencesMatrix(self):
        self.aggregatedPreferencesMatrix = self.preferencesMatrix[:]
        for p in range(len(self.aggregatedPreferencesMatrix)):
            for x in range(len(self.aggregatedPreferencesMatrix[p])):
                self.aggregatedPreferencesMatrix[p][x] = float(self.preferencesMatrix[p][x])*float(self.weights[x])
        print("AGGREGATED PREFERENCES MATRIX " + str(self.aggregatedPreferencesMatrix))
        
    def sumOfTheRows(self):
        self.sums = []
        for x in self.aggregatedPreferencesMatrix:
            self.sums.append(sum(x))
        print(self.sums)
        
    def comparisonMatrix(self):
        self.comparisonMatrix = [[1 for x in range(len(self.alternatives))] for y in range(len(self.alternatives))] 
        print(self.comparisonMatrix)
        for c in range(len(self.comparisonMatrix)):
            try:
                self.comparisonMatrix[c][c] = 0
                print(c)
            except: 
                continue
        print(self.comparisonMatrix)
        
        selectSum=0
        print(self.sums)
        for x in range(len(self.comparisonMatrix)):
            for i in range(len(self.comparisonMatrix[x])):
                if (self.comparisonMatrix[x][i] == 1):
                    self.comparisonMatrix[x][i] = self.sums[selectSum]
                    selectSum += 1
        #rowNumber = 0
        #for x in range(len(self.sums)):
        print("COMPARISON MATRIX: " + str(self.comparisonMatrix))
    def enteringFlow(self):
        self.enteringFlowArray = []
        for x in range(len(self.alternatives)):
            alternativesValues = []
            for i in range(len(self.comparisonMatrix)):
                alternativesValues.append(self.comparisonMatrix[i][x])
            print(alternativesValues)
            print(sum(alternativesValues)/3)
            self.enteringFlowArray.append(sum(alternativesValues)/3)
        print(self.enteringFlowArray)
    def leavingFlow(self):
        self.leavingFlowArray = []
        for x in range(len(self.alternatives)):
            alternativeValues = []
            for i in range(len(self.comparisonMatrix)):
                alternativeValues.append(self.comparisonMatrix[x][i])
            print(alternativeValues)
            print(sum(alternativeValues)/3)
            self.leavingFlowArray.append(sum(alternativeValues)/3)
        print(self.leavingFlowArray)
        
    def ranking(self):
        self.ranks = []
        self.calculatedValues = []
        for x in range(len(self.alternatives)):
            self.calculatedValues.append(self.leavingFlowArray[x]-self.enteringFlowArray[x])
        
        self.calculatedValuesSorted = sorted(self.calculatedValues, reverse=True)
        print(self.calculatedValuesSorted)
        
        self.recommendations = []
        for a in range(len(self.alternatives)):
            self.recommendations.append([self.alternatives[a], self.calculatedValues[a], self.calculatedValuesSorted.index(self.calculatedValues[a])+1])
        print(self.recommendations)
    def recommend(self):
        #Normalization
        self.normalizedMatrix=[]
        for x in self.matrix:
            print(x)
        #Diferences
        
        self.diferencesMatrix=[]
        for x in self.normalizedMatrix:
            print(x)
        ##first criterion
        ##second criterion
        ##third criterion
        
        #Preference function
        
        #Aggregated preference function
        
        #leaving and entering outranking laws
#pr = Promethee(["Alternative 1", "Alternative 2", "Alternative 3", "Alternative 4"], [0.35,0.25,0.25, 0.15],["Criterion 1", "Criterion 2", "Criterion 3", "Criterion 4"], ["Non-Beneficial","Beneficial","Beneficial","Beneficial"], [[250,16,12,5],[200,16,8,3],[300,32,16,4],[275,32,8,2]])
        