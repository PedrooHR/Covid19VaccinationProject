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
