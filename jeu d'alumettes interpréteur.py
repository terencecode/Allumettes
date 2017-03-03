# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 19:44:19 2015

@author: Marie
"""

#########################################################################
# Import des modules
import random

#########################################################################
# Définition des constantes

HUMAIN = -1
MACHINE = 1
LIMITE = 3
MULTIJOUEUR = 10
SOLO = 11
MIN = -1
MAX = 1

#########################################################################
# Définition des fonctions
victoire = 0

def coups(liste1, liste2, nb):
    ''' Cette fonction récupère le nombre d'allumettes à enlever 
    par l'ordinateur lorsque la fonction minMax renvoie 100 (victoire)
    '''                                                                                                                                                                                
    if max(liste1) == 100 :
        coup_gagnant = liste2[liste1.index(100)]
        return coup_gagnant
    elif max(liste1) == -100 :
        return random.randint(1,min(nb,3))

def Op(liste, player):
    ''' Cette fonction élague les noeuds qui ne modifieront pas la
    valeur renvoyée par la fonction minMax afin de gagner du temps
    et des ressources'''
    
    if len(liste)==0:
        return True
    if player==MIN:
        if min(liste) == -100:
            return False
        else :
            return True
    if player==MAX:
        if max(liste) == 100:
            return False
        else:
            return True

def minMax(n, joueur):
    ''' fonction récurrente qui explore l'arbre des possibilités 
    et renvoie une valeur +100 (gagné pr Max) ou -100 (perdu pr Max)
    paramètres : 
    n le nombre d'allumettes
    joueur le joueur
    '''
    global victoire
    resultats = []
    coup_joue = []
    if n == 0 :
        if joueur == MIN :
            return -100
        elif joueur == MAX :
            return +100
    else :
        #min(a,b) : renvoie la valeur min entre a et b
        for i in range (1,min(n+1,4)) : 
        #Pourquoi min(n+1,4) ? : 
        #dernière valeur exclue de la range, 
        
        #donc 4 pour i=1 ou 2 ou 3
        #et (n+1) si n<=3 pr ne pas obtenir de valeurs négatives dans l'arbre. 
            if Op(resultats, joueur) is True :
                resultats.append(minMax(n-i, -joueur))
                coup_joue.append(i)
        victoire = coups(resultats, coup_joue, n)
        if joueur == MIN :
            return min(resultats)
        elif joueur == MAX :
            return max(resultats)

def afficher(n):
    '''Affiche le nombre d'allumettes
    '''
    print (n * "| ")
    
def enlever1(joueur, n):
    '''Renvoie le nombre d'allumettes a retirer par le joueur dans le jeu en multijoueur
    '''
    enleve = int(input(getStringJoueur(joueur) + " combien d'allumettes voulez-vous enlever ? "))
    if (enleve < 1 or enleve > min(n, LIMITE)) : 
        enleve = int(input(getStringJoueur(joueur) + " vous devez enlever entre 1 et " + min(n, LIMITE) + " allumettes. Combien voulez-vous en enlever?"))
    return enleve

def enlever2(joueur, n):
    '''Renvoie le nombre d'allumettes a enlever par les joueurs dans le jeu contre la machine
    '''
    global victoire
    if joueur == HUMAIN: 
        return enlever1(joueur, n)
    if joueur == MACHINE:
        if n  <= 25 :
            minMax(n, joueur)
            _coup = victoire
            print ("l'Ordinateur enlève ", _coup, " allumette(s).")
            return _coup
        else :
            _coup = random.randint(1,min(n,3))
            print ("l'Ordinateur enlève ", _coup, " allumette(s).")
            return _coup

def choixAleatoireJoueur():
    '''définit le joueur au pif
    '''
    _joueur = random.choice([HUMAIN, MACHINE])
    return _joueur

def getStringJoueur(joueur):
    '''Renvoie une String en fonction du joueur passé en paramètre:
    joueur1, joueur2 ou ordinateur
    '''
    if joueur == HUMAIN:
        return "joueur 1 "
    else :
        if jeu == SOLO :
            return "joueur 2 "
        else : 
            return "Ordinateur "
 
 
    
#########################################################################
# Début du programme principal (main)
    
jeu = int(input("jeu multijoueur : tapez 1 jeu, contre la machine : tapez 2 : "))

    
# choisir nombre d'allumettes
nb_Alu = int(input("Avec combien d'allumettes joue-t-on ? "))

#définition du joueur qui commence
joueur_de_la_partie = choixAleatoireJoueur()

#jouer

while (nb_Alu > 0):
    afficher(nb_Alu)
    if jeu == 1:
        nb_Alu = nb_Alu - enlever1(joueur_de_la_partie, nb_Alu)
    elif jeu == 2:
        nb_Alu = nb_Alu - enlever2(joueur_de_la_partie, nb_Alu)
    joueur_de_la_partie = joueur_de_la_partie * -1
    print (nb_Alu)
    
print ("fin du jeu")
print (getStringJoueur(joueur), " gagne la partie")
