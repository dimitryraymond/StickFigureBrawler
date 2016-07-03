class ImportCircles(object):
    def __init__(self, filename):
        object.__init__(self)
        self.importDatav2(filename)

    #this one is for parenthesis
    def importData(self, filename):
        self.data = []
        i = 0
        file = open(filename, 'r')
        for line in file:
            start = line.find("[")
            end = line.find("]")
            line = line[start + 3:end - 1]
            values = line.split("), ((")
            dataLine = []
            for value in values:
                circle = []
                parts = value.split("), ")
                center = parts[0].split(", ")
                if center != ['']:
                    center[0] = int(center[0])
                    center[1] = int(center[1])
                    radius = int(parts[1])
                    circle.append(center)
                    circle.append(radius)
                    dataLine.append(circle)
            i+=1
            #print(i, dataLine)
            self.data.append(dataLine)
        return self.data

    #this one if for files with just brackets
    def importDatav2(self, filename):
        self.data = []
        i = 0
        file = open(filename, 'r')
        for line in file:
            start = line.find("[")
            line = line[start + 3:len(line) - 3]
            values = line.split("], [[")
            dataLine = []
            for value in values:
                circle = []
                parts = value.split("], ")
                center = parts[0].split(", ")
                if center != ['']:
                    center[0] = int(center[0])
                    center[1] = int(center[1])
                    radius = int(parts[1])
                    circle.append(center)
                    circle.append(radius)
                    dataLine.append(circle)
            self.data.append(dataLine)
        file.close()
        return self.data

                


allData = ImportCircles("jedi hitboxes.txt")
data = allData.data


