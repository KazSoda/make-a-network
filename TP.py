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
        self.Parcours = Parcours  # Liste d'arrêts, tableau d'arrêts
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
#   Bus
MonBus = []
MonBus.append(bus("Double", 10, 1, 30, ("B", "A", "C", "E", "C", "A")))
MonBus.append(bus("Double", 10, 1, 30, ("D", "C", "E", "C")))
MonBus.append(bus("Double", 10, 1, 30, ("B", "E", "D")))
MonBus.append(bus("Fast", 2, 1, 10, ("A", "C")))

#   Arrets
Arrets = []
Arrets.append(arret("A", [("B", 10), ("C", 4)]))
Arrets.append(arret("B", [("A", 10), ("B", 0)]))
Arrets.append(arret("C", [("A", 4), ("D", 12), ("E", 4)]))
Arrets.append(arret("D", [("C", 12), ("D", 0)]))
Arrets.append(arret("E", [("C", 4), ("E", 0)]))

#   Routes
Routes = []
Routes.append(route(("A", "B"), 10))
Routes.append(route(("A", "C"), 4))
Routes.append(route(("C", "D"), 12))
Routes.append(route(("C", "E"), 4))

#   Lire fichier de données
fichier = open('file.txt', "r")
lesLignes = fichier.readlines()
fichier.close()


# def CréeRoute(Départ, Arrivée, AccessiblesA, AccessiblesB):
#     if len(AccessiblesA)==0 and len(AccessiblesB)==0:
#         AccessiblesA.append([])
#         AccessiblesB.append([])
#     # On cherche les arrêts atteignables depuis le départ ou l'arrivée
#     for UnArret in Arrets:
#         # On récupère les arrêts atteignables depuis le départ
#         if UnArret.getID() == Départ:
#             AccessiblesA[0]=AccessiblesA[0]+UnArret.getArretsProches()
#         if UnArret.getID() == Arrivée:
#             # On récupère les arrêts atteignables depuis l'arrivée
#             AccessiblesB[0]=AccessiblesB[0]+UnArret.getArretsProches()
#     # On regarde s'il existe un arrêt en commun
#     print(AccessiblesA)
#     for i in range(len(AccessiblesA[0])):
#         for j in range(len(AccessiblesB[0])):
#             if AccessiblesA[0][i][0] == AccessiblesB[0][j][0]:
#                 # On crée la route intermédiaire (exemple Arrêt C en commun de A et B alors on créé AB qui vaut AC + AB)
#                 Routes.append(route((Départ,Arrivée),10))
#                 # TODO : On cherche et renvoie la route intermédiaire
#                 for UneRoute in Routes:
#                     if Routes[len(Routes)-1].getTrajet() == UneRoute.getTrajet():
#                          return UneRoute
#     # Si on arrive ici, c'est que l'on a pas trouvé la route.
#     # On teste alors de trouver une route intermédiaire de niveau plus bas
#     AccessiblesA[0] = AccessiblesA[0] + AccessiblesB[0]
#     ChercherRoute(Départ, Arrivée, AccessiblesA[0])

#  TODO: Placer dans Bus des objets arrêts, pas des id !!
def InitialisePersonnes():
    #   Traitement des données trouvées
    for i in range(len(dataLigne)):
        #   Traitement du nombre de personnes cooncernées
        for j in range(int(dataLigne[i][0])):
            #   TODO: Supprimer le \n qui traine à dataLigne[i][5]
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
                    logs.write("Le bus "+UnBus.getParcours()[0]+UnBus.getParcours()[1]+" fait descendre "+UnBus.getFile()[k].getNom()+".\n")
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
            for j in range(len(UnBus.getParcours())):
                if len(Personne.getParcours()) > 0 :
                    if UnBus.getParcours()[j] == Personne.getParcours()[0][1][1]:
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
                                            logs.write("Le bus "+UnBus.getParcours()[0]+UnBus.getParcours()[1]+" fait monter "+Personne.getNom()+".\n")
                                            logs.write("Capacité du bus : "+str(len(UnBus.getFile()))+"/"+str(UnBus.getChargeMaximale())+"\n")
                                            PersonnesSuppr.append(Personne)
                                            z = True
                                            if len(UnBus.getFile())+1 <= UnBus.ChargeMaximale :
                                                UnBus.Alarret = True
                                            else:
                                                UnBus.Alarret = False
                                            i += 1
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
        if len(UnBus.getParcours()) > 1:
            Arret1 = UnBus.getParcours()[0]
            Arret2 = UnBus.getParcours()[1]
            UnBus.setPosition(Arret1 + Arret2, 0, 0)
            # On vérifie que la route existe
            for UneRoute in Routes:
                if UneRoute.getTrajet() == str(Arret1 + Arret2) or ''.join(reversed(UneRoute.getTrajet())) == str(Arret1 + Arret2):
                    RouteExiste = True
            if RouteExiste == False:
                # Si la route n'existe pas, on cherche une voie intermédiaire
                AccessiblesA = []
                AccessiblesB = []
                # CréeRoute(Arret1,Arret2,AccessiblesA,AccessiblesB)
        else:
            # Gestion d'erreur sur le bus (A REVOIR !!!)
            print(
                "Erreur. Le nombre d'arrêts pour le bus n'est pas valide. Un bus doit avoir au-moins deux arrêts pour circuler.\n")


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
            for UnArret in range(len(UnBus.getParcours())):
                if not DestinationTrouvée:
                    if UnBus.getPosition()[0][0] == UnBus.getParcours()[UnArret]:
                        if UnBus.getPosition()[0][1] == UnBus.getParcours()[UnArret + 1]:
                            # On a trouvé le trajet actuel, on lit le prochain arrêt
                            # Si l'arrêt en cours est le dernier, on fait le parcours inverse
                            if UnArret + 2 == len(UnBus.getParcours()):
                                UnBus.Parcours = ''.join(reversed(UnBus.getParcours()))
                                UnBus.setPosition(UnBus.getParcours()[0] + UnBus.getParcours()[1], 0, 0)
                                logs.write("Trajet :" + str(UnBus.getPosition()[0]) + " Avancée :" + str(int(UnBus.getPosition()[1])) + "%\n")
                                DestinationTrouvée = True
                            else:
                                # On lit l'arrêt suivant
                                UnBus.setPosition(UnBus.getParcours()[UnArret + 1] + UnBus.getParcours()[UnArret + 2],0, 0)
                                logs.write("Trajet :" + str(UnBus.getPosition()[0]) + " Avancée :" + str(
                                int(UnBus.getPosition()[1])) + "%\n")
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
                            # if RouteTrouvée==False:
                            # CréeRoute(UnBus.getPosition()[0][0],UnBus.getPosition()[0][1])

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
BusDémarre()
#   La durée de vie de l'univers est de 10000 S
while temps < 100000:
    logs.write("\n\n\nUnivers à la seconde ")
    logs.write(str(temps) + "\n")
    BusAvance(temps)
    # Une unité de temps est passée
    temps += 1
logs.close()