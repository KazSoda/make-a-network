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

    def getType(self):
        return Type

    def getChargeMaximale(self):
        return ChargeMaximale

    def getRapidité(self):
        return Rapidité

    def getVitesse(self):
        return Vitesse

    def getParcours(self):
        return Parcours
    
#   Objet : un arrêt
#   Possède :
#       - des routes // (Minimum 1) reliant cet arrêt
#       - une file d'attente // Ordonnée des personnes (premier arrivé, premier choisi)
class arret:
    def __init__(self, Routes, File):
        self.Routes = Routes#Route(s) reliant cet arrêt, tableau de routes
        self.File =  File#File d'attente (ordonnée) des personnes, tableau de personnes

    def getRoutes(self):
        return Routes

    def getFile(self):
        return File
    
#   Objet : une route
#   Possède :
#       - deux arrêts
#       - une distance (de trajet) en unité de mesure (M)
class route:
    def __init__(self, Arrets, Distance):
        self.Arrets = Arrets#Arrêts, arret
        self.Distance = Distance#Distance en (M), int

    def getArrets(self):
        return Arrets

    def getDistance(self):
        return Distance

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
    
#   Données fixes
#   Bus
Bus1 = bus("Double",10,1,30,("B","A","C","E","C","A"))
Bus2 = bus("Double",10,1,30,("D","C","E","C"))
Bus3 = bus("Double",10,1,30,("B","E","D"))
Bus4 = bus("Fast",2,1,10,("A","C"))

#   Arrets
Arrets = []
Arrets.append(arret("12",[]))
Arrets.append(arret("1",[]))
Arrets.append(arret("234",[]))
Arrets.append(arret("3",[]))
Arrets.append(arret("4",[]))

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


# Test : Tracer les routes avec Turtle
speed(0)
turtle.setup(500,500)
hideturtle()
penup()
# On place le premier arrêt
goto(-150,-150)
dot()
NomsArrets=[]
# On cherche à tracer les routes
for route in Routes:
    # On récupère le premier caractère comme arrêt 1
    print("0")
    


#   Initialisation de l'univers
#temps = 0
#   La durée de vie de l'univers est de 10000 S
#while temps < 100000:
    
    # Une unité de temps est passée
#    temps+=temps
