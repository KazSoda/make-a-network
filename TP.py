#   PROJET MAN (Make A Network)
#   Goal : Create a bus network with people getting in and out

#   Object : a bus
#   Owns :
#       - a max charge // Maximum capacity of the bus
#       - efficiency // How many people can get in/out per S
#       - speed // Speed in M per S
#       - path // Path consisting of "arrêts" objects to travel with the bus
class bus:
    def __init__(self, Type, MaxCharge, Efficiency, Speed, Path):
        self.Type = Type  # Transport type
        self.MaxCharge = MaxCharge  # Maximum charge of people
        self.Efficiency = Efficiency  # How many people can get in/out per second
        self.Speed = Speed  # Speed in M per S
        self.Path = Path  # List of "arrets", where is the bus from and where is he heading to
        self.Arrets = [] # List of "arrets" objects
        self.Position = []  # Current position of the bus (ex: 80% of trajet AB with 0.x distance already done) => ("AB",x,80)
        self.Queue = []  # Queue
        self.OnTheRoad = False # Is the bus on the road or is it at a stop

    def getType(self):
        return self.Type

    def getMaxCharge(self):
        return self.MaxCharge

    def getEfficiency(self):
        return self.Efficiency

    def getSpeed(self):
        return self.Speed

    def getPath(self):
        return self.Path

    def getArrets(self):
        return self.Arrets

    def getPosition(self):
        return self.Position

    def setQueue(self, Personne):
        self.Queue.append(Personne)

    def getQueue(self):
        return self.Queue
    
    def setPosition(self, pos, percent, progress):
        self.Position.clear()
        self.Position.append(pos)
        self.Position.append(percent)
        self.Position.append(progress)

    def getPercent(self, distance):
        return (self.getPosition()[2] * 100) / distance

    def getProgress(self, distance):
        self.Position[2] = self.getPosition()[2] + distance / self.Speed
        self.Position[1] = (self.getPercent(distance) / distance)
        return None


#   Object : arrêt (a stop)
#   Owns :
#       - routes // (Minimum 1) that get through this "arrêt"
#       - waiting list // People that are waiting to get in
class arret:
    def __init__(self, ID, CloseArret):
        self.ID = ID  # Letter
        self.CloseArret = CloseArret  # "Arrêts" that are close enough and have a "route" that goes by and make this "arret" accessible
        self.Queue = [] # Waiting list

    def getID(self):
        return self.ID

    def getCloseArret(self):
        return self.CloseArret

    def getQueue(self):
        return self.Queue



#   Object : route (a road)
#   Owns :
#       - two "arrêts" (stops)
#       - a distance (to travel) in M
class route:
    def __init__(self, Arrets, Distance):
        self.Arrets = Arrets  # "Arrets" objects that the road consists of
        self.Distance = Distance  # Distance in M

    def getArrets(self):
        return self.Arrets

    def getDistance(self):
        return self.Distance

    def getPath(self):
        return (self.Arrets[0] + self.Arrets[1])


#   Object : personne (a person)
#
#   Owns :
#       - one way travel // Hour and starting "arrêt", Hour and ending "arrêt"
#       - travel back // Hour and starting "arrêt", Hour and ending "arrêt"
#       - name // Identity
class personne:
    def __init__(self, Path, Name):
        self.Path = Path  # one way travel (Hour and starting "arrêt", Hour and ending "arrêt"), travel back (Hour and starting "arrêt", Hour and ending "arrêt")
        self.Name = Name  # Name, str
        self.isMoving = False # Is the person in a bus or not

    def getPath(self):
        return self.Path

    def getName(self):
        return self.Name

    def getPosition(self):
        return self.isMoving


#   Data
#   Arrets
Arrets = []
Arrets.append(arret("A", [("B", 10), ("C", 4)]))
Arrets.append(arret("B", [("A", 10), ("B", 0)]))
Arrets.append(arret("C", [("A", 4), ("D", 12), ("E", 4)]))
Arrets.append(arret("D", [("C", 12), ("D", 0)]))
Arrets.append(arret("E", [("C", 4), ("E", 0)]))


#   Bus
MyBus = []
MyBus.append(bus("Double", 10, 1, 30, ("B", "A", "C", "E", "C", "A")))
MyBus.append(bus("Double", 10, 1, 30, ("D", "C", "E", "C")))
MyBus.append(bus("Double", 10, 1, 30, ("B", "E", "D")))
MyBus.append(bus("Fast", 2, 1, 10, ("A", "C")))

#   Routes
Routes = []
Routes.append(route(("A", "B"), 10))
Routes.append(route(("A", "C"), 4))
Routes.append(route(("C", "D"), 12))
Routes.append(route(("C", "E"), 4))

p = 1
res = 0
#   Calculating how many routes can exist
for o in range(len(Arrets)):
    for u in range(len(Arrets)-p):
        res+=1
    p+=1

def FindMissingRoutes():
    #   Trying that each arrêt is accessible by another one, with the help of others routes
    while len(Routes) < res:
         for Arret1 in Arrets:
             for Arret2 in Arrets:
                 doesExist = False
                 if Arret1.getID() != Arret2.getID():
                     for i in range(len(Routes)):
                         if (Arret1.getID(),Arret2.getID()) == Routes[i].getArrets() or (Arret2.getID(),Arret1.getID()) == Routes[i].getArrets():
                            doesExist = True
                     if not doesExist:
                         # Calculating the road
                         for h in range(len(Arret1.getCloseArret())):
                             for s in range(len(Arret2.getCloseArret())):
                                 if Arret1.getCloseArret()[h][0] == Arret2.getCloseArret()[s][0]:
                                    RouteAlreadyExists = False
                                    Distance=0
                                    #  Creating new route
                                    for Route1 in Routes:
                                        if Route1.getArrets() == (Arret1.getID(),Arret1.getCloseArret()[h][0]) or Route1.getArrets() == (Arret1.getCloseArret()[h][0],Arret1.getID()):
                                            Distance+=Route1.getDistance()
                                    for Route2 in Routes:
                                        if Route2.getArrets() == (Arret2.getCloseArret()[s][0],Arret2.getID()) or Route2.getArrets() == (Arret2.getID(),Arret2.getCloseArret()[s][0]):
                                            Distance+=Route2.getDistance()
                                    RouteTemp = route((Arret1.getID(),Arret2.getID()),Distance)
                                    for Route3 in Routes:
                                        if Route3.getArrets() == RouteTemp.getArrets() or Route3.getArrets() == reversed(RouteTemp.getArrets()):
                                            RouteAlreadyExists = True
                                    if not RouteAlreadyExists:
                                        Routes.append(RouteTemp)
                                        # Adding new road to arrêts
                                        Arret1.getCloseArret().append((Arret2.getID(),Distance))
                                        Arret2.getCloseArret().append((Arret1.getID(),Distance))





#   Reading data file
data = open('file.txt', "r")
Lines = data.readlines()
data.close()

def getArretById(ID):
    for Arret in Arrets:
        if Arret.getID() == ID:
            return Arret
    return False

def InitializeBus():
    for ABus in MyBus:
        for i in range(len(ABus.getPath())):
            for Arret in Arrets:
                # If arrêt found, we add it to Bus path
                if Arret.getID() == ABus.getPath()[i]:
                    ABus.Arrets.append(Arret)
        # Destroying path data as it have no purpose from now on
        ABus.Path = None

def InitializePersonnes():
    #   Data found
    for i in range(len(dataLine)):
        #   How many persons concerned
        for j in range(int(dataLine[i][0])):
            Personnes.append(personne([[dataLine[i][2], dataLine[i][3]], [dataLine[i][4], dataLine[i][5][0]+dataLine[i][5][1]]], dataLine[i][1]+str(j+1)))
    # Placing people at their arrêt
    for Arret in Arrets:
        for Personne in Personnes:
            if Arret.getID() == Personne.getPath()[0][1][0]:
                Arret.Queue.append(Personne)

def ObliteratePersonne(UnePersonne):
    for i in range(len(Personnes)):
        if Personnes[i].getName() == UnePersonne.getName():
            del(Personnes[i])
            return

def PersonneFindPath(UnePersonne):
    #   In case someone has no bus that can make its path, the person must find a two times way
    #   We search bus that could do this path
    for Bus in MyBus:
        for i in range(len(Bus.getArrets())):
            #   We search a bus that has the same arrêt as person start
            if UnePersonne.getPath()[0][1][0] == Bus.getArrets()[i].getID():
                for AnotherBus in MyBus:
                    for j in range(len(AnotherBus.getArrets())):
                        #   We search a bus that goes to the same terminus as the person.
                        if UnePersonne.getPath()[0][1][1] == AnotherBus.getArrets()[j].getID():
                            # We search if both bus have a stop in common where the person can go to
                            for k in range(len(Bus.getArrets())):
                                for z in range(len(AnotherBus.getArrets())):
                                    if Bus.getArrets()[k].getID() == AnotherBus.getArrets()[z].getID() :
                                        # Found path : we add it to the person destination
                                        TimeOfStart = UnePersonne.getPath()[0][0]
                                        Start = UnePersonne.getPath()[0][1][0]
                                        End = UnePersonne.getPath()[0][1][1]
                                        del(UnePersonne.getPath()[0])
                                        UnePersonne.getPath().insert(0,[TimeOfStart,Bus.getArrets()[k].getID()+End])
                                        UnePersonne.getPath().insert(0,[TimeOfStart,Start+Bus.getArrets()[k].getID()])
                                        return True
    return False
def PersonneGetOut(UnBus):
    UnBus.OnTheRoad = True
    l = 0
    z = False
    Delete = []
    if len(UnBus.getQueue()) > 0:
        for k in range(len(UnBus.getQueue())):
            # Looking for people that needs to get out
            if UnBus.getQueue()[k].getPath()[0][1][1] == UnBus.getPosition()[0][0]:
                # Making people go out if needed (in the limit of bus efficiency)
                if l < UnBus.Efficiency:
                    # Making people going out
                    l += 1
                    # If someone is out, the bus is not moving
                    UnBus.OnTheRoad = True
                    UnBus.getQueue()[k].isMoving=False
                    logs.write("Le bus "+UnBus.getArrets()[0].getID()+UnBus.getArrets()[1].getID()+" fait descendre "+UnBus.getQueue()[k].getName()+".\n")
                    Delete.append(UnBus.getQueue()[k].getName())
                    if len(UnBus.getQueue()[k].getPath()) == 1:
                            ObliteratePersonne(UnBus.getQueue()[k])
                    else:
                        #   Telling person their next destination
                        del(UnBus.getQueue()[k].getPath()[0])
                        #   Adding to arrêt waiting list
                        PersonneJoinQueue(UnBus.getQueue()[k])
                    z = True
    k = 0
    while k < len(UnBus.getQueue()):
        j=0
        while j < len(Delete):
            if Delete[j] == UnBus.getQueue()[k].getName():
                del(UnBus.getQueue()[k])
            j+=1
        k+=1
    return z

def PersonneLeaveQueue(UnePersonne):
    for UnArret in Arrets:
        if UnArret.getID() == UnePersonne.getPath()[0][1][0]:
            for i in range(len(UnArret.getQueue())):
                if UnArret.getQueue()[i].getName() == UnePersonne.getName():
                    del(UnArret.getQueue()[i])
                    return

def PersonneJoinQueue(UnePersonne):
    for UnArret in Arrets:
        if UnePersonne.getPath()[0][1][0] == UnArret.getID():
            UnArret.Queue.append(UnePersonne)
            return

def PersonneGetIn(UnBus,time):
    i = 0
    Delete = []
    z = False
    # Only if bus is not full
    if UnBus.getMaxCharge() > len(UnBus.getQueue()):
        for Personne in Personnes:
            # Only if bus can bring people to its destination
            for j in range(len(UnBus.getArrets())):
                if UnBus.getArrets()[j].getID() == Personne.getPath()[0][1][1]:
                    # Only if they are at the same arrêt
                    if int(Personne.getPath()[0][0]) <= time and Personne.getPath()[0][1][0] == UnBus.getPosition()[0][0]:
                        for UnArret in Arrets:
                            for k in range(len(UnArret.getQueue())):
                                if UnArret.getQueue()[k].getName() == Personne.getName():
                                    # For as long as the bus can take people
                                    if UnBus.getEfficiency() > i:
                                        # As many as the bus can
                                        UnBus.setQueue(Personne)
                                        Personne.isMoving = True
                                        logs.write("Le bus "+UnBus.getArrets()[0].getID()+UnBus.getArrets()[1].getID()+" fait monter "+Personne.getName()+".\n")
                                        logs.write("Capacité du bus : "+str(len(UnBus.getQueue()))+"/"+str(UnBus.getMaxCharge())+"\n")
                                        Delete.append(Personne)
                                        z = True
                                        if len(UnBus.getQueue())+1 <= UnBus.MaxCharge :
                                            UnBus.OnTheRoad = True
                                        else:
                                            UnBus.OnTheRoad = False
                                        i += 1
            # If the personne can't get in, we make sure they at least have one bus that can do the path
            # To make sure he's not forever stuck
            if not Personne.isMoving:
                TrajetPossible = False
                for Bus in MyBus:
                    for j in range(len(Bus.getArrets())):
                        for k in range(len(Bus.getArrets())):
                            #  Only if the path is possible using one bus
                            if Bus.getArrets()[k].getID() == Personne.getPath()[0][1][1] and Bus.getArrets()[j].getID() == Personne.getPath()[0][1][0]:
                                TrajetPossible = True
                # If not, searching for another path
                if not TrajetPossible:
                    # We search an alternative path
                    if PersonneFindPath(Personne):
                        # Only if the bus can do the path
                        for j in range(len(UnBus.getArrets())):
                            if UnBus.getArrets()[j].getID() == Personne.getPath()[0][1][1]:
                                # Only if they are at the same arrêt
                                if int(Personne.getPath()[0][0]) <= time and Personne.getPath()[0][1][0] == \
                                        UnBus.getPosition()[0][0]:
                                    for UnArret in Arrets:
                                        for k in range(len(UnArret.getQueue())):
                                            if UnArret.getQueue()[k].getName() == Personne.getName():
                                                # Only if bus has still time
                                                if UnBus.getEfficiency() > i:
                                                    # As many people that can get in, in a second
                                                    UnBus.setQueue(Personne)
                                                    Personne.isMoving = True
                                                    logs.write(
                                                        "Le bus " + UnBus.getArrets()[0].getID() + UnBus.getArrets()[
                                                            1].getID() + " fait monter " + Personne.getName() + ".\n")
                                                    logs.write(
                                                        "Capacité du bus : " + str(len(UnBus.getQueue())) + "/" + str(
                                                            UnBus.getMaxCharge()) + "\n")
                                                    Delete.append(Personne)
                                                    z = True
                                                    if len(UnBus.getQueue()) + 1 <= UnBus.MaxCharge:
                                                        UnBus.OnTheRoad = True
                                                    else:
                                                        UnBus.OnTheRoad = False
                                                    i += 1
    # We remove person that got in from the waiting list
    for j in range(len(Delete)):
        PersonneLeaveQueue(Delete[j])
    return z

def BusStart():
    # Iniatializing persons
    InitializePersonnes()
    # Starting all bus
    for UnBus in MyBus:
        # Only if path is valid
        if len(UnBus.getArrets()) > 1:
            Arret1 = UnBus.getArrets()[0].getID()
            Arret2 = UnBus.getArrets()[1].getID()
            UnBus.setPosition(Arret1 + Arret2, 0, 0)

def BusAvance(time):
    DestinationFound = False
    FoundRoute = False
    # Progress bus
    for UnBus in MyBus:
        SauteProg = False
        logs.write("\n")
        # Looking if bus is not at an arrêt
        if UnBus.getPosition()[1] >= 100:
            # If at the end of the path, goes reverse
            # Looking for start of latest route taken
            for UnArret in range(len(UnBus.getArrets())):
                if not DestinationFound:
                    if UnBus.getPosition()[0][0] == UnBus.getArrets()[UnArret].getID():
                        if UnBus.getPosition()[0][1] == UnBus.getArrets()[UnArret + 1].getID():
                            # Found path
                            # If end of path, reverse it
                            if UnArret + 2 == len(UnBus.getArrets()):
                                UnBus.Arrets = list(reversed(UnBus.getArrets()))
                                UnBus.setPosition(UnBus.getArrets()[0].getID() + UnBus.getArrets()[1].getID(), 0, 0)
                                logs.write("Trajet :" + str(UnBus.getPosition()[0]) + " Avancée :" + str(int(UnBus.getPosition()[1])) + "%\n")
                                DestinationFound = True
                            else:
                                # Next arrêt
                                UnBus.setPosition(UnBus.getArrets()[UnArret + 1].getID() + UnBus.getArrets()[UnArret + 2].getID(),0, 0)
                                logs.write("Trajet :" + str(UnBus.getPosition()[0]) + " Avancée :" + str(int(UnBus.getPosition()[1])) + "%\n")
                                DestinationFound = True
        else:
            # Before progress, looking if people needs to get in or out
            if UnBus.getPosition()[1] == 0:
                # Making people get out
                if not PersonneGetOut(UnBus):
                    UnBus.OnTheRoad = False
                else:
                    SauteProg = True
                # Looking if not full
                if UnBus.getMaxCharge() > len(UnBus.getQueue()) :
                    # Next arrêt
                    for UnArret in Arrets:
                        if UnArret.getID() == UnBus.getPosition()[0][0]:
                            # Looking if queue is empty
                            if len(UnArret.getQueue()) > 0:
                                # Getting people in
                                if not PersonneGetIn(UnBus,time):
                                    UnBus.OnTheRoad = False
                                else:
                                    SauteProg = True
            if not SauteProg:
                if not UnBus.OnTheRoad:
                    for UneRoute in Routes:
                        # Searching for current route
                        if UneRoute.getPath() == UnBus.getPosition()[0] or ''.join(reversed(UneRoute.getPath())) == UnBus.getPosition()[0]:
                            UnBus.getProgress(UneRoute.getDistance())
                            logs.write("Trajet :" + str(UnBus.getPosition()[0]) + " Avancée :" + str(int(UnBus.getPosition()[1])) + "%\n")
                            FoundRoute = True







#   Getting information
dataLine = []
for line in Lines:
    dataLine.append(line.split(" "))
Personnes = []

#   Start of universe
logs = open("logs.txt", "w")
logs.close()
logs = open("logs.txt", "a")
time = 1
InitializeBus()
FindMissingRoutes()
BusStart()
#   Universe's life duration is 100000s or when everyone is dead (they made it home safely)
while time < 100000 and len(Personnes) > 0:
    logs.write("\n\n\nUnivers à la seconde ")
    logs.write(str(time) + "\n")
    BusAvance(time)
    # A second has passed
    time += 1
logs.close()