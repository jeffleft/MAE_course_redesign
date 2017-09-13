class Course:

    cList = []

    def __init__(self, name, title, units, category, prereq, coreq):
        self.name = name
        self.title = title
        self.units = units
        self.prereq = prereq
        self.coreq = coreq
        self.category = category

        self.cList.append(self)

    def findDependencies(self):

        self.dList = []
        
        for aCourse in self.cList:
            if self.name in aCourse.prereq:
                self.dList.append(aCourse.name)
                aCourse.print()

    def findCourse(self, name):
        for aCourse in self.cList:
            if name == aCourse.name:
                return(aCourse)
        
    def clearList(self):
        self.cList = []
        
    def print(self):
        print(self.name, ". ", self.title, " (", self.units, ")", sep="")
        print("Prerequisites:", self.prereq)