#   PROJET MAN (Make A Network)
#   Objectif : Optimiser les déplacements d'un bus pour transporter des personnes

from turtle import *
import turtle
#   Objet : un bus
#   Possède :
#       - une charge maximale // Capacité maximum de personnes transportables à un instant t
#       - une rapidité de chargement/déchargement // En unité de temps (S) par personne (les chargements/déchargements se faisant en parallèle
#       - une vitesse de déplacement // Nombre d'unité de mesure (M) en unité de temps (S)
#       - un parcours // Des arrêts à faire en boucle "indéfiniment"
class bus:
    def __init__(self, Type, ChargeMaximale, Rapidité, Vitesse, Parcours):
        self.Type = Type#Type de transport, str
        self.ChargeMaximale = ChargeMaximale#Charge maximale de personne, int
        self.Rapidité = Rapidité#Rapidité de charge en S/Personne, int
        self.Vitesse = Vitesse#Vitesse en M/S, int
        self.Parcours = Parcours#Liste d'arrêts, tableau d'arrêts
        self.Position = []#Position actuelle du bus par rapport à son trajet (exemple : 80% du trajet AB avec 0.x distance parcourue) => ("AB",x,80)

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

    def setPosition(self,pos,pourcentage,avancee):
        self.Position.clear()
        self.Position.append(pos)
        self.Position.append(pourcentage)
        self.Position.append(avancee)

    def getPourcentage(self,Distance):
        return (self.getPosition()[2]*100)/Distance
    def getAvancée(self,Distance):
        self.Position[2]=self.getPosition()[2]+Distance/self.Vitesse
        self.Position[1]=(self.getPourcentage(Distance)/Distance)
        return None

#   Objet : un arrêt
#   Possède :
#       - des routes // (Minimum 1) reliant cet arrêt
#       - une file d'attente // Ordonnée des personnes (premier arrivé, premier choisi)
class arret:
    def __init__(self, ID, Routes):
        self.ID = ID#Lettre de l'arrêt
        self.Routes = Routes#Route(s) reliant cet arrêt, tableau de routes
        self.File =  []#File d'attente (ordonnée) des personnes, tableau de personnes

    def getID(self):
        return self.ID
    
    def getRoutes(self):
        return self.Routes

    def getFile(self):
        return self.File
    
#   Objet : une route
#   Possède :
#       - deux arrêts
#       - une distance (de trajet) en unité de mesure (M)
class route:
    def __init__(self, Arrets, Distance):
        self.Arrets = Arrets#Arrêts, arret
        self.Distance = Distance#Distance en (M), int

    def getArrets(self):
        return self.Arrets

    def getDistance(self):
        return self.Distance

    def getTrajet(self):
        return (self.Arrets[0]+self.Arrets[1])

#   Objet : une personne
#   Possède :
#       - un trajet aller // Heure et arrêt de départ, Heure et arrêt d'arrivée
#       - un trajet retour // Heure et arrêt de départ, Heure et arrêt d'arrivée
#       - un nom // Identité
class personne:
    def __init__(self, Aller, Retour, Nom):
        self.Aller = Aller#Trajet aller (heure départ, arrêt départ, arrêt arrivée), tableau de str
        self.Retour = Retour#Trajet retour (heure départ, arrêt départ, arrêt arrivée), tableau de str
        self.Nom = Nom#Nom, str

    def getAller(self):
        return self.Aller

    def getRetour(self):
        return self.Retour

    def getNom(self):
        return self.Nom
    
#   Données fixes
#   Bus
Bus = []
Bus.append(bus("Double",10,1,30,("B","A","C","E","C","A")))
Bus.append(bus("Double",10,1,30,("D","C","E","C")))
Bus.append(bus("Double",10,1,30,("B","E","D")))
Bus.append(bus("Fast",2,1,10,("A","C")))

#   Arrets
Arrets = []
Arrets.append(arret("A","12"))
Arrets.append(arret("B","1"))
Arrets.append(arret("C","234"))
Arrets.append(arret("D","3"))
Arrets.append(arret("E","4"))

#   Routes
Routes = []
Routes.append(route(("A","B"),10))
Routes.append(route(("A","C"),4))
Routes.append(route(("C","D"),12))
Routes.append(route(("C","E"),4))

#   Lire fichier de données
fichier = open('file.txt', "r")
lesLignes = fichier.readlines()
fichier.close()


def BusDémarre():
    logs.write("Démarrage des bus.\n")
    #On démarre tous les bus
    for UnBus in Bus:
        #On ne traite que si le bus a un parcours valide
        if len(UnBus.getParcours()) > 1:
            Arret1 = UnBus.getParcours()[0]
            Arret2 = UnBus.getParcours()[1]
            UnBus.setPosition(Arret1+Arret2,0,0)
            logs.write("Départ du bus (trajet de départ/pourcentage):\n")
            logs.write(UnBus.getPosition()[0]+"\n")
            logs.write(str(UnBus.getPosition()[1])+"\n")
        else :
            #Gestion d'erreur sur le bus (A REVOIR !!!)
            print("Erreur. Le nombre d'arrêts pour le bus n'est pas valide. Un bus doit avoir au-moins deux arrêts pour circuler.\n")
            
def BusAvance():
    logs.write("Avancée des bus\n")
    #Destination trouvée (pour éviter que la boucle se répète sur un même arrêt)
    DestinationTrouvée = False
    RouteTrouvée = False
    #On avance tous les bus
    for UnBus in Bus:
        #On vérifie si le bus n'est pas à un arrêt
        if UnBus.getPosition()[1] >= 100 :
            #TO DO : On compte les personnes à décharger

            #On part en direction du prochain arrêt (uniquement lorsque les gens sont descendus !!)
            #On vérifie si l'on est pas en fin de parcours, si c'est le cas on fait tout dans le sens inverse !
            #On cherche le départ de la dernière étape en date
            for UnArret in range(len(UnBus.getParcours())):
                if DestinationTrouvée == False:
                    if UnBus.getPosition()[0][0]==UnBus.getParcours()[UnArret]:
                        if UnBus.getPosition()[0][1]==UnBus.getParcours()[UnArret+1]:
                        #On a trouvé le trajet actuel, on lit le prochain arrêt
                        #Si l'arrêt en cours est le dernier, on fait le parcours inverse
                            if UnArret+2 == len(UnBus.getParcours()):
                                UnBus.Parcours = ''.join(reversed(UnBus.getParcours()))
                                UnBus.setPosition(UnBus.getParcours()[0]+UnBus.getParcours()[1],0,0)
                                logs.write("Trajet :" + str(UnBus.getPosition()[0]) + " Avancée :" + str(int(UnBus.getPosition()[1])) + "%\n")
                                DestinationTrouvée = True
                            else:
                                #On lit l'arrêt suivant
                                UnBus.setPosition(UnBus.getParcours()[UnArret+1]+UnBus.getParcours()[UnArret+2],0,0)
                                logs.write("Trajet :" + str(UnBus.getPosition()[0]) + " Avancée :" + str(int(UnBus.getPosition()[1])) + "%\n")
                                DestinationTrouvée = True
        else:
            for UneRoute in Routes:
                #On cherche la route actuelle
                if UneRoute.getTrajet() == UnBus.getPosition()[0] or ''.join(reversed(UneRoute.getTrajet())) == UnBus.getPosition()[0]:
                    UnBus.getAvancée(UneRoute.getDistance())
                    logs.write("Trajet :"+str(UnBus.getPosition()[0])+" Avancée :"+str(int(UnBus.getPosition()[1]))+"%\n")
                    RouteTrouvée=True
            # Si aucune route trouvée, cela signifie qu'il faut trouver une route intermédiaire !
            if RouteTrouvée==False:
                for UneRoute in Routes:
                #On récupère les arrêts de départ et d'arrivée du trajet
                    Départ = UnBus.getPosition()[0][0]
                    Arrivée = UnBus.getPosition()[0][1]




#   Traitement par ligne
dataLigne = []
for ligne in lesLignes:
    dataLigne.append(ligne.split(" "))

#   Traitement des données trouvées
Personnes = []
for i in range(len(dataLigne)):
    #   Traitement du nombre de personnes cooncernées
    for j in range(len(dataLigne[i][0])):
        Personnes.append(personne([dataLigne[i][2],dataLigne[i][3]],[dataLigne[i][4],dataLigne[i][5]],dataLigne[i][1]))
   

#   Initialisation de l'univers
logs = open("logs.txt", "w")
logs.close()
logs = open("logs.txt", "a")
temps = 1
BusDémarre()
#   La durée de vie de l'univers est de 10000 S
while temps < 100000:
    logs.write("\n\n\nUnivers à la seconde ")
    logs.write(str(temps)+"\n")
    BusAvance()
    # Une unité de temps est passée
    temps+=1
logs.close()
