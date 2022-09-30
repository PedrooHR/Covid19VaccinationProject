# City Class


class City:
    def __init__(self, idIBGE, name='', state='', population=0):
        self.idIBGE = idIBGE
        self.name = name
        self.state = state
        self.population = population
        self.numberOfDose_0 = 0
        self.numberOfDose_1 = 0
        self.numberOfDose_2 = 0
        self.numberOfDose_3 = 0
        self.numberOfDose_4 = 0
        self.percentOfDose_0 = 0
        self.percentOfDose_1 = 0
        self.percentOfDose_2 = 0
        self.percentOfDose_3 = 0
        self.percentOfDose_4 = 0

    def __repr__(self):
        text = 'City: ' + str(self.name) \
               + ', ' + str(self.state) \
               + ', ' + str(self.idIBGE) \
               + ', ' + str(self.population) \
               + ', ' + str(self.numberOfDose_0) \
               + ', ' + str(self.numberOfDose_1) \
               + ', ' + str(self.numberOfDose_2) \
               + ', ' + str(self.numberOfDose_3) \
               + ', ' + str(self.numberOfDose_4) \
               + ', ' + str(self.percentOfDose_0) \
               + ', ' + str(self.percentOfDose_1) \
               + ', ' + str(self.percentOfDose_2) \
               + ', ' + str(self.percentOfDose_3) \
               + ', ' + str(self.percentOfDose_4)

        return text

    def addDose(self, dose, numberOfDose):
        if dose == 0:
            self.numberOfDose_0 = self.numberOfDose_0 + numberOfDose
        elif dose == 1:
            self.numberOfDose_1 = self.numberOfDose_1 + numberOfDose
        elif dose == 2:
            self.numberOfDose_2 = self.numberOfDose_2 + numberOfDose
        elif dose == 3:
            self.numberOfDose_3 = self.numberOfDose_3 + numberOfDose
        elif dose == 4:
            self.numberOfDose_4 = self.numberOfDose_4 + numberOfDose

    def calculateDosePercentage(self):
        self.percentOfDose_0 = self.numberOfDose_0 / self.population
        self.percentOfDose_1 = self.numberOfDose_1 / self.population
        self.percentOfDose_2 = self.numberOfDose_2 / self.population
        self.percentOfDose_3 = self.numberOfDose_3 / self.population
        self.percentOfDose_4 = self.numberOfDose_4 / self.population

# @staticmethod
# def getValuesToPlot(nodes):
#     # initializing variables
#     maxDegree = 0
#     minDegree = 9999999
#
#     # getting the max value of degree
#     for node in nodes:
#         if node.numberOfLinks > maxDegree:
#             maxDegree = node.numberOfLinks
#
#         if node.numberOfLinks < minDegree:
#             minDegree = node.numberOfLinks
#
#     # creating the array of the possible values of degrees
#     degrees = [0 for i in range(maxDegree)]
#     for i in range(maxDegree):
#         degrees[i] = i + 1
#
#     # calculating total number of links in that degree
#     totalNumberOfLinks = [0 for i in range(maxDegree)]
#     for node in nodes:
#         totalNumberOfLinks[node.numberOfLinks - 1] += 1
#
#     # totalNumberOfNodes = 0
#     # for i in range(maxDegree + 1):
#     #     total = totalNumberOfNodes  + totalNumberOfLinks[i]
#
#     # calculating the degree probability
#     totalDegreeProbability = 0.0
#     degreesProbability = [0.0 for i in range(maxDegree)]
#     for i in range(maxDegree):
#         degreesProbability[i] = totalNumberOfLinks[i] / len(nodes)
#         totalDegreeProbability = totalDegreeProbability + degreesProbability[i]
#
#     #  returning the values of degrees, totalNumberOfLinks, degreesProbability
#     return degrees, totalNumberOfLinks, degreesProbability, minDegree, maxDegree
