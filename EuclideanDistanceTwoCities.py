# EuclideanDistanceTwoCities Class
import math


class EuclideanDistanceTwoCities:
    def __init__(self, originCity, targetCity, euclideanDistance):
        self.originCity = originCity
        self.targetCity = targetCity
        self.euclideanDistance = euclideanDistance

    def __repr__(self):
        text = 'Origin: ' + self.originCity \
               + '\n' \
               + 'Target: ' + self.targetCity \
               + '\n' \
               + 'Distance: ' + str(self.euclideanDistance)
        return text

    # def calculateDosePercentage(self):
    #     self.percentOfDose_0 = self.numberOfDose_0 / self.population
    #     self.percentOfDose_1 = self.numberOfDose_1 / self.population
    #     self.percentOfDose_2 = self.numberOfDose_2 / self.population
    #     self.percentOfDose_3 = self.numberOfDose_3 / self.population
    #     self.percentOfDose_4 = self.numberOfDose_4 / self.population

    # calculate the euclidean distance between two cities
    @staticmethod
    def calculateEuclideanDistanceTwoCities(originCity, targetCity):
        # calculating the distance
        distance = math.sqrt( \
            math.pow((originCity.percentOfDose_0 - targetCity.percentOfDose_0), 2) \
            + math.pow((originCity.percentOfDose_1 - targetCity.percentOfDose_1), 2) \
            + math.pow((originCity.percentOfDose_2 - targetCity.percentOfDose_2), 2) \
            + math.pow((originCity.percentOfDose_3 - targetCity.percentOfDose_3), 2) \
            + math.pow((originCity.percentOfDose_4 - targetCity.percentOfDose_4), 2) \
            )

        # returning the distance
        return distance

    @staticmethod
    def hasLinkOfTwoCities(originCity, targetCity, euclideanDistancesOfCities):
        for euclideanDistanceOfCity in euclideanDistancesOfCities:
            if euclideanDistanceOfCity.originCity.idIBGE == targetCity.idIBGE and \
                    euclideanDistanceOfCity.targetCity.idIBGE == originCity.idIBGE:
                return True

        # returning the link does not exist yet
        return False

    # @staticmethod
    # def removeDuplicateCities(euclideanDistancesOfCities):
    #     resultsList = []
    #     for firstEuclideanDistanceOfCity in euclideanDistancesOfCities:
    #
    #         # adding iten to the results list
    #         resultsList.append(firstEuclideanDistanceOfCity)
    #
    #         # checking if the cities pair already in the results list
    #         for secondEuclideanDistanceOfCity in euclideanDistancesOfCities:
    #             if firstEuclideanDistanceOfCity.originCity.idIBGE == secondEuclideanDistanceOfCity.targetCity.idIBGE and \
    #                     firstEuclideanDistanceOfCity.targetCity.idIBGE == secondEuclideanDistanceOfCity.originCity.idIBGE:
    #                 continue
    #
    #             # adding iten to the results list
    #             resultsList.append(secondEuclideanDistanceOfCity)
    #
    #     # returning the link does not exist yet
    #     return resultsList

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
