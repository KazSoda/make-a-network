#   PROJET MAN (Make A Network)
#   Objectif : Optimiser les déplacements d'un bus pour transporter des personnes

#   Objet : un bus
#   Possède :
#       - une charge maximale // Capacité maximum de personnes transportables à un instant t
#       - une rapidité de chargement/déchargement // En unité de temps (S) par personne (les chargements/déchargements se faisant en parallèle
#       - une vitesse de déplacement // Nombre d'unité de mesure (M) en unité de temps (S)
#       - un parcours // Des arrêts à faire en boucle "indéfiniment"
class bus:
    def __init__(self, Type, ChargeMaximale, Rapidité, Vitesse, Parcours):
        self.Type = Type  # Type de transport, str
        self.ChargeMaximale = ChargeMaximale  # Charge maximale de personne, int
        self.Rapidité = Rapidité  # Rapidité de charge en S/Personne, int
        self.Vitesse = Vitesse  # Vitesse en M/S, int
        self.Parcours = Parcours  # Liste d'arrêts, tableau d'arrêts TODO : Temporaire, à terme, assimiler dès la création du bus en lecture de fichier
        self.Arrets = [] # Liste d'arrêts desservis
        self.Position = []  # Position actuelle du bus par rapport à son trajet (exemple : 80% du trajet AB avec 0.x distance parcourue) => ("AB",x,80)
        self.File = []  # File d'attente (ordonnée) des personnes, tableau de personnes
        self.Alarret = False # Savoir si le bus est à l'arrêt ou en mouvement

    def getType(self):
        return self.Type

    def getChargeMaximale(self):
        return self.ChargeMaximale

    def getRapidité(self):
        return self.Rapidité

    def getVitesse(self):
        return self.Vitesse

    def getParcours(self):
        return self.Parcours

    def getArrets(self):
        return self.Arrets

    def getPosition(self):
        return self.Position

    def setFile(self, Personne):
        self.File.append(Personne)

    def getFile(self):
        return self.File

    def getAlarret(self):
        return self.Alarret

    def setPosition(self, pos, pourcentage, avancee):
        self.Position.clear()
        self.Position.append(pos)
        self.Position.append(pourcentage)
        self.Position.append(avancee)

    def getPourcentage(self, Distance):
        return (self.getPosition()[2] * 100) / Distance

    def getAvancée(self, Distance):
        self.Position[2] = self.getPosition()[2] + Distance / self.Vitesse
        self.Position[1] = (self.getPourcentage(Distance) / Distance)
        return None


#   Objet : un arrêt
#   Possède :
#       - des routes // (Minimum 1) reliant cet arrêt
#       - une file d'attente // Ordonnée des personnes (premier arrivé, premier choisi)
class arret:
    def __init__(self, ID, ArretsProches):
        self.ID = ID  # Lettre de l'arrêt
        self.ArretsProches = ArretsProches  # Arrêt(s) joignables à cet arrêt
        self.File = [] # Personnes faisant la queue

    def getID(self):
        return self.ID

    def getArretsProches(self):
        return self.ArretsProches

    def getFile(self):
        return self.File



#   Objet : une route
#   Possède :
#       - deux arrêts
#       - une distance (de trajet) en unité de mesure (M)
class route:
    def __init__(self, Arrets, Distance):
        self.Arrets = Arrets  # Arrêts, arret
        self.Distance = Distance  # Distance en (M), int

    def getArrets(self):
        return self.Arrets

    def getDistance(self):
        return self.Distance

    def getTrajet(self):
        return (self.Arrets[0] + self.Arrets[1])


#   Objet : une personne
#   Possède :
#       - un trajet aller // Heure et arrêt de départ, Heure et arrêt d'arrivée
#       - un trajet retour // Heure et arrêt de départ, Heure et arrêt d'arrivée
#       - un nom // Identité
class personne:
    def __init__(self, Parcours, Nom):
        self.Parcours = Parcours  # Trajet aller (heure départ, arrêt départ, arrêt arrivée), Trajet retour (heure départ, arrêt départ, arrêt arrivée)
        self.Nom = Nom  # Nom, str
        self.isMoving = False # Savoir si une personne est dans le bus ou non

    def getParcours(self):
        return self.Parcours

    def getNom(self):
        return self.Nom

    def getPosition(self):
        return self.isMoving


#   Données fixes
#   Arrets
Arrets = []
Arrets.append(arret("A", [("B", 10), ("C", 4)]))
Arrets.append(arret("B", [("A", 10), ("B", 0)]))
Arrets.append(arret("C", [("A", 4), ("D", 12), ("E", 4)]))
Arrets.append(arret("D", [("C", 12), ("D", 0)]))
Arrets.append(arret("E", [("C", 4), ("E", 0)]))


#   Bus
MonBus = []
MonBus.append(bus("Double", 10, 1, 30, ("B", "A", "C", "E", "C", "A")))
MonBus.append(bus("Double", 10, 1, 30, ("D", "C", "E", "C")))
MonBus.append(bus("Double", 10, 1, 30, ("B", "E", "D")))
MonBus.append(bus("Fast", 2, 1, 10, ("A", "C")))

#   Routes
Routes = []
Routes.append(route(("A", "B"), 10))
Routes.append(route(("A", "C"), 4))
Routes.append(route(("C", "D"), 12))
Routes.append(route(("C", "E"), 4))

p = 1
res = 0
#   Calcul du nombre de routes possibles
for o in range(len(Arrets)):
    for u in range(len(Arrets)-p):
        res+=1
    p+=1

def TrouveRoutesManquantes():
    #   On essaye de faire en sorte que chaque arrêt soit atteignable depuis un autre, à l'aide de parcours de plusieurs routes
    while len(Routes) < res:
         for Arret1 in Arrets:
             for Arret2 in Arrets:
                 doesExist = False
                 if Arret1.getID() != Arret2.getID():
                     for i in range(len(Routes)):
                         if (Arret1.getID(),Arret2.getID()) == Routes[i].getArrets() or (Arret2.getID(),Arret1.getID()) == Routes[i].getArrets():
                            doesExist = True
                     if not doesExist:
                         # Calcul de la route
                         for h in range(len(Arret1.getArretsProches())):
                             for s in range(len(Arret2.getArretsProches())):
                                 if Arret1.getArretsProches()[h][0] == Arret2.getArretsProches()[s][0]:
                                    RouteExisteDeja = False
                                    Distance=0
                                    #  On créé la route intermédiaire
                                    for Route1 in Routes:
                                        if Route1.getArrets() == (Arret1.getID(),Arret1.getArretsProches()[h][0]) or Route1.getArrets() == (Arret1.getArretsProches()[h][0],Arret1.getID()):
                                            Distance+=Route1.getDistance()
                                    for Route2 in Routes:
                                        if Route2.getArrets() == (Arret2.getArretsProches()[s][0],Arret2.getID()) or Route2.getArrets() == (Arret2.getID(),Arret2.getArretsProches()[s][0]):
                                            Distance+=Route2.getDistance()
                                    RouteTemp = route((Arret1.getID(),Arret2.getID()),Distance)
                                    for Route3 in Routes:
                                        if Route3.getArrets() == RouteTemp.getArrets() or Route3.getArrets() == reversed(RouteTemp.getArrets()):
                                            RouteExisteDeja = True
                                    if not RouteExisteDeja:
                                        Routes.append(RouteTemp)
                                        # On rajoute aux arrêts les nouvelles destinations atteignables
                                        Arret1.getArretsProches().append((Arret2.getID(),Distance))
                                        Arret2.getArretsProches().append((Arret1.getID(),Distance))





#   Lire fichier de données
fichier = open('file.txt', "r")
lesLignes = fichier.readlines()
fichier.close()

def getArretById(ID):
    for Arret in Arrets:
        if Arret.getID() == ID:
            return Arret
    return False

def InitialiseBus():
    for UnBus in MonBus:
        for i in range(len(UnBus.getParcours())):
            for Arret in Arrets:
                # Si on trouve l'arrêt, on l'assimile au bus
                if Arret.getID() == UnBus.getParcours()[i]:
                    UnBus.Arrets.append(Arret)

        # On détruit le "parcours" du Bus qui ne sert plus à rien maintenant qu'on a les arrêts
        UnBus.Parcours = None

def InitialisePersonnes():
    #   Traitement des données trouvées
    for i in range(len(dataLigne)):
        #   Traitement du nombre de personnes cooncernées
        for j in range(int(dataLigne[i][0])):
            Personnes.append(personne([[dataLigne[i][2], dataLigne[i][3]], [dataLigne[i][4], dataLigne[i][5][0]+dataLigne[i][5][1]]], dataLigne[i][1]+str(j+1)))
    # On place chaque personne à son arrêt
    for Arret in Arrets:
        for Personne in Personnes:
            if Arret.getID() == Personne.getParcours()[0][1][0]:
                Arret.File.append(Personne)

def AssassinerPersonne(UnePersonne):
    for i in range(len(Personnes)):
        if Personnes[i].getNom() == UnePersonne.getNom():
            del(Personnes[i])
            return

def PassagerTrouveCorrespondance(UnePersonne):
    #   Dans le cas où une personne ne trouve pas de bus pour l'emmener à destination, c'est qu'il doit prendre une correspondance.
    #   On cherche alors les bus qui pourraient assurer ce trajet intermédiaire
    for Bus in MonBus:
        for i in range(len(Bus.getArrets())):
            if UnePersonne.getParcours()[0][1][0] == Bus.getArrets()[i].getID():
                

def PassagersDescend(UnBus):
    UnBus.Alarret = True
    l = 0
    z = False
    ASupprimer = []
    if len(UnBus.getFile()) > 0:
        for k in range(len(UnBus.getFile())):
            # On cherche ceux qui doivent descendre
            if UnBus.getFile()[k].getParcours()[0][1][1] == UnBus.getPosition()[0][0]:
                # On fait descendre ceux qui doivent descendre (dans la limite de vitesse de déchargement)
                if l < UnBus.Rapidité:
                    # On fait descendre la personne
                    l += 1
                    # Si quelqu'un descend, on indique que le bus est à l'arrêt
                    UnBus.Alarret = True
                    UnBus.getFile()[k].isMoving=False
                    logs.write("Le bus "+UnBus.getArrets()[0].getID()+UnBus.getArrets()[1].getID()+" fait descendre "+UnBus.getFile()[k].getNom()+".\n")
                    ASupprimer.append(UnBus.getFile()[k].getNom())
                    if len(UnBus.getFile()[k].getParcours()) == 1:
                            AssassinerPersonne(UnBus.getFile()[k])
                    else:
                        #   On redirige le passager vers sa prochaine destination
                        del(UnBus.getFile()[k].getParcours()[0])
                        #   On l'ajoute à la liste d'attente de l'arrêt
                        PassagerRejointFileArret(UnBus.getFile()[k])
                    z = True
    k = 0
    j = 0
    while k < len(UnBus.getFile()):
        j=0
        while j < len(ASupprimer):
            if ASupprimer[j] == UnBus.getFile()[k].getNom():
                del(UnBus.getFile()[k])
            j+=1
        k+=1
    return z

def PassagerQuitteFileArret(UnePersonne):
    for UnArret in Arrets:
        if UnArret.getID() == UnePersonne.getParcours()[0][1][0]:
            for i in range(len(UnArret.getFile())):
                if UnArret.getFile()[i].getNom() == UnePersonne.getNom():
                    del(UnArret.getFile()[i])
                    return

def PassagerRejointFileArret(UnePersonne):
    for UnArret in Arrets:
        if UnePersonne.getParcours()[0][1][0] == UnArret.getID():
            UnArret.File.append(UnePersonne)
            return

def PassagersMonte(UnBus,temps):
    i = 0
    PersonnesSuppr = []
    z = False
    # On ne fait monter que si le bus n'est pas plein
    if UnBus.getChargeMaximale() > len(UnBus.getFile()):
        for Personne in Personnes:
            # On ne fait monter que si le bus fait le trajet nécessaire pour la personne
            for j in range(len(UnBus.getArrets())):
                if UnBus.getArrets()[j].getID() == Personne.getParcours()[0][1][1]:
                    # On ne les fait monter que s'ils sont au même arrêt que le bus
                    if int(Personne.getParcours()[0][0]) <= temps and Personne.getParcours()[0][1][0] == UnBus.getPosition()[0][0]:
                        for UnArret in Arrets:
                            for k in range(len(UnArret.getFile())):
                                if UnArret.getFile()[k].getNom() == Personne.getNom():
                                    # On ne fait monter autant que ce que le bus peut prendre par seconde
                                    if UnBus.getRapidité() > i:
                                        # On fait monter le nombre de personnes qu'on peut en une seconde :
                                        UnBus.setFile(Personne)
                                        Personne.isMoving = True
                                        logs.write("Le bus "+UnBus.getArrets()[0].getID()+UnBus.getArrets()[1].getID()+" fait monter "+Personne.getNom()+".\n")
                                        logs.write("Capacité du bus : "+str(len(UnBus.getFile()))+"/"+str(UnBus.getChargeMaximale())+"\n")
                                        PersonnesSuppr.append(Personne)
                                        z = True
                                        if len(UnBus.getFile())+1 <= UnBus.ChargeMaximale :
                                            UnBus.Alarret = True
                                        else:
                                            UnBus.Alarret = False
                                        i += 1
            # Si la personne ne peut pas monter, on regarde si son trajet est réalisable par au-moins l'un des bus
            # Pour s'assurer qu'il ne soit pas bloqué éternellement à l'arrêt
            if not Personne.isMoving:
                TrajetPossible = False
                for Bus in MonBus:
                    for k in range(len(Bus.getArrets())):
                        if Bus.getArrets()[k].getID() == Personne.getParcours()[1]:
                            TrajetPossible = True
                # Si aucun bus ne peut assurer le trajet, alors on cherche une correspondance
                if not TrajetPossible:
                    PassagerTrouveCorrespondance(Personne)

    # On retire les personnes montées de la liste d'attente
    for j in range(len(PersonnesSuppr)):
        PassagerQuitteFileArret(PersonnesSuppr[j])
    return z

def BusDémarre():
    # On initialise les personnes
    InitialisePersonnes()
    # On démarre tous les bus
    for UnBus in MonBus:
        RouteExiste = False
        # On ne traite que si le bus a un parcours valide
        if len(UnBus.getArrets()) > 1:
            Arret1 = UnBus.getArrets()[0].getID()
            Arret2 = UnBus.getArrets()[1].getID()
            UnBus.setPosition(Arret1 + Arret2, 0, 0)
            # On vérifie que la route existe
            for UneRoute in Routes:
                if UneRoute.getTrajet() == str(Arret1 + Arret2) or ''.join(reversed(UneRoute.getTrajet())) == str(Arret1 + Arret2):
                    RouteExiste = True
        else:
            # Gestion d'erreur sur le bus (A REVOIR !!!)
            print("Erreur. Le nombre d'arrêts pour le bus n'est pas valide. Un bus doit avoir au-moins deux arrêts pour circuler.\n")


def BusAvance(temps):
    # Destination trouvée (pour éviter que la boucle se répète sur un même arrêt)
    DestinationTrouvée = False
    RouteTrouvée = False
    BusPeutRedémarrer = False
    # On avance tous les bus
    for UnBus in MonBus:
        SauteProg = False
        logs.write("\n")
        # On vérifie si le bus n'est pas à un arrêt
        if UnBus.getPosition()[1] >= 100:
            # On vérifie si l'on est pas en fin de parcours, si c'est le cas on fait tout dans le sens inverse !
            # On cherche le départ de la dernière étape en date
            for UnArret in range(len(UnBus.getArrets())):
                if not DestinationTrouvée:
                    if UnBus.getPosition()[0][0] == UnBus.getArrets()[UnArret].getID():
                        if UnBus.getPosition()[0][1] == UnBus.getArrets()[UnArret + 1].getID():
                            # On a trouvé le trajet actuel, on lit le prochain arrêt
                            # Si l'arrêt en cours est le dernier, on fait le parcours inverse
                            if UnArret + 2 == len(UnBus.getArrets()):
                                UnBus.Arrets = list(reversed(UnBus.getArrets()))
                                UnBus.setPosition(UnBus.getArrets()[0].getID() + UnBus.getArrets()[1].getID(), 0, 0)
                                logs.write("Trajet :" + str(UnBus.getPosition()[0]) + " Avancée :" + str(int(UnBus.getPosition()[1])) + "%\n")
                                DestinationTrouvée = True
                            else:
                                # On lit l'arrêt suivant
                                UnBus.setPosition(UnBus.getArrets()[UnArret + 1].getID() + UnBus.getArrets()[UnArret + 2].getID(),0, 0)
                                logs.write("Trajet :" + str(UnBus.getPosition()[0]) + " Avancée :" + str(int(UnBus.getPosition()[1])) + "%\n")
                                DestinationTrouvée = True
        else:
            # Avant d'avancer, on regarde si l'on est à un arrêt, et si oui, combien de place il reste et de personnes à prendre
            if UnBus.getPosition()[1] == 0:
                # On fait descendre des personnes
                if not PassagersDescend(UnBus):
                    UnBus.Alarret = False
                else:
                    SauteProg = True
                # On vérifie si on a encore de la place
                if UnBus.getChargeMaximale() > len(UnBus.getFile()) :
                    # On cherche l'arrêt courant
                    for UnArret in Arrets:
                        if UnArret.getID() == UnBus.getPosition()[0][0]:
                            # On regarde si la file est vide
                            if len(UnArret.getFile()) > 0:
                                # On récupère des personnes
                                if not PassagersMonte(UnBus,temps):
                                    UnBus.Alarret = False
                                else:
                                    SauteProg = True
            if not SauteProg:
                if not UnBus.Alarret:
                    for UneRoute in Routes:
                        # On cherche la route actuelle
                        if UneRoute.getTrajet() == UnBus.getPosition()[0] or ''.join(reversed(UneRoute.getTrajet())) == UnBus.getPosition()[0]:
                            UnBus.getAvancée(UneRoute.getDistance())
                            logs.write("Trajet :" + str(UnBus.getPosition()[0]) + " Avancée :" + str(int(UnBus.getPosition()[1])) + "%\n")
                            RouteTrouvée = True
                            # Si aucune route trouvée, cela signifie qu'il faut trouver une route intermédiaire !








#   Traitement par ligne
dataLigne = []
for ligne in lesLignes:
    dataLigne.append(ligne.split(" "))
Personnes = []

#   Initialisation de l'univers
logs = open("logs.txt", "w")
logs.close()
logs = open("logs.txt", "a")
temps = 1
InitialiseBus()
TrouveRoutesManquantes()
BusDémarre()
#   La durée de vie de l'univers est de 10000 S
while temps < 100000:
    logs.write("\n\n\nUnivers à la seconde ")
    logs.write(str(temps) + "\n")
    BusAvance(temps)
    # Une unité de temps est passée
    temps += 1
logs.close()