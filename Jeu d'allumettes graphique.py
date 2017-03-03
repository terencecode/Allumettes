# -*- coding: utf-8 -*-
#########################################################################
# Import des modules

from tkinter import *
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
défaut = 20
OptionAlu = défaut
TourHUMAIN = 0
TourMULTI = 0
joueur = 0
numerojoueur = 1

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
            
def choixAleatoireJoueur():
    '''définit le joueur au pif
    '''
    _joueur = random.choice([HUMAIN, MACHINE])
    return _joueur

def Intermédiaire(n, joueur):
    global victoire
    if n > 26 :
        victoire = random.randint(1,3)
    else :
        minMax(n,joueur)

###############################################################################
# Interface graphique : Fenêtres

###############################################################################
# Menu

def Menu():
    '''Cette fonction est la fenêtre de jeu principale'''
    #Choix Aléatoire Joueur pour la partie Solo avant toute partie
    global joueur
    joueur=choixAleatoireJoueur()
    
    #Defaut Alumettes
    global OptionAlu
    OptionAlu = défaut
    
    #Tour pc
    if joueur == 1 :
        Intermédiaire(OptionAlu,MACHINE)
        OptionAlu=OptionAlu-victoire
    
    #fenetre
    global fenetre
    fenetre=Tk()
    image_solo= PhotoImage(file='bouton_jeu_en_solo.gif')
    image_multijoueurs= PhotoImage(file='bouton_multijoueurs.gif')
    image_option= PhotoImage(file='bouton_options.gif')
    fenetre['bg']='white'
    fenetre.title("Menu prinicipal - Jeu d'allumettes ")
    fenetre.geometry("800x505")
    fenetre.iconbitmap('iconejeu.ico')

    # Ajout de Boutons
    Button(fenetre, image=image_multijoueurs, relief=FLAT, command=fenetre_de_jeu_multi,bg='#FFFFFF').pack(side=TOP, padx=100, pady=52)
    Button(fenetre, image=image_solo, relief=FLAT, command=fenetre_de_jeu_solo,bg='#FFFFFF').pack(side=TOP, padx=100, pady=45)
    Button(fenetre, image=image_option, relief=FLAT, command=Option,bg='#FFFFFF').pack(side=TOP, padx=100, pady=52)
    
    #Copyright
    Canevas=Canvas(fenetre)
    Canevas.pack()
    Label(Canevas,text='Copyright Marie.P, William.T, Leonard.NC',height=1,width=180,bg='#FFC89B',anchor=SE).pack(side=BOTTOM)

    fenetre.mainloop()
    
###############################################################################
# Jeu multi joueurs

def fenetre_de_jeu_multi():
    '''Cette fonction est fenêtre du jeu multi-joueurs'''
    global JeuM
    xx=21
    yy=143.5
    fenetre.withdraw()
    JeuM=Toplevel()
    JeuM['bg']='white'
    JeuM.title("Multijoueurs - Jeu d'allumettes ")
    JeuM.geometry("1035x419")
    JeuM.iconbitmap('iconejeu.ico')
    
    retour_menu= PhotoImage(file='retour_menu.gif')
    abandonner= PhotoImage(file='url2.gif')
    alumette= PhotoImage(file='url.gif')
    
    #Bouton abandonner
    Button(JeuM, image=abandonner, relief=FLAT, command=AbandonnerM,bg='#FFFFFF').grid(row=0,column=0,padx=20,sticky=W)
    
    #Bouton menu
    Button(JeuM, image=retour_menu, relief=FLAT, command=RetourAuMenuM,bg='#FFFFFF').grid(row=0, column=1,padx=2,sticky=W)
    
    #Maitre du canevas
    frame=Frame(JeuM)
    frame.grid(row=1,column=0,padx=20,pady=20,rowspan=3,columnspan=3,sticky=W)
    
    #Canevas d'affichage allumettes
    canvas=Canvas(frame,bg='#FFFFFF',scrollregion=(0,0,192000,192000))
    
    #Scrollbar du canevas
    hbar=Scrollbar(frame,orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=canvas.xview)
    
    #Configuration du Canevas
    canvas.config(width=700,height=287)
    canvas.config(xscrollcommand=hbar.set)
    canvas.pack(side=LEFT,expand=True,fill=BOTH)
    
        #Affichage des alumettes
    for i in range (OptionAlu):
        canvas.create_image(xx,yy, image=alumette)
        xx=xx+30
    
    # nombre d'allumettes à retirer 
    global valeur_retirerM
    valeur_retirerM=Entry(JeuM, textvariable=IntVar())
    valeur_retirerM.bind("<Return>",retirermulti)
    valeur_retirerM.grid(row=1, column=4,padx=10, pady=10)
    
    #Alumettes restantes
    Restantes=Label(JeuM, text='Il reste ' + str(OptionAlu) + ' Alumettes', fg='#000000', bg='#FFFFFF')
    Restantes.grid(row=0,column=2,padx=20,pady=10)    
    
    #Consignes de jeu 
    Indication=Label(JeuM, text='Entrez un chiffre entre 1 et 3 pour jouer', fg='#000000', bg='#FFFFFF')
    Indication.grid(row= 1, column=4,padx=20, pady=20,rowspan=2)
    
    #Indication du joueur qui doit jouer
    Tour=Label(JeuM, text="C'est au tour du joueur " + str(numerojoueur) + " de joueur", fg='#000000', bg='#FFFFFF')
    Tour.grid(row= 3, column=4,padx=20, pady=20,rowspan=2)
    
    #Copyright
    Canevas=Canvas(JeuM)
    Canevas.grid(row=4,column=0,columnspan=6)
    Label(Canevas,text='Copyright Marie.P, William.T, Leonard.NC',height=1,width=147,bg='#FFC89B',anchor=SE).pack(side=BOTTOM)
        
    #Test du vainqueur
    if OptionAlu == 1 :
        JeuM.withdraw()
        FinPartie(2)
    elif OptionAlu == 0 :
        JeuM.withdraw()
        FinPartie(1)
    else :
        JeuM.mainloop()
    
###############################################################################
# Jeu contr l'ordinateur

def fenetre_de_jeu_solo():
    '''Cette fonction est la fenêtre de jeu contre l'ordinateur'''
    global Jeu
    global OptionAlu
    xx=21
    yy=143.5
    fenetre.withdraw()
    Jeu=Toplevel()
    Jeu['bg']='white'
    Jeu.title("Solo - Jeu d'allumettes ")
    Jeu.geometry("1035x419")
    Jeu.iconbitmap('iconejeu.ico')
    
    retour_menu= PhotoImage(file='retour_menu.gif')
    abandonner= PhotoImage(file='url2.gif')
    alumette= PhotoImage(file='url.gif')
      
    
    #Bouton abandonner
    Button(Jeu, image=abandonner, relief=FLAT, command=Abandonner,bg='#FFFFFF').grid(row=0,column=0,padx=20,sticky=W)
        
    #Bouton menu
    Button(Jeu, image=retour_menu, relief=FLAT, command=RetourAuMenu,bg='#FFFFFF').grid(row=0, column=1,padx=2,sticky=W)
    
    #Maitre du canevas
    frame=Frame(Jeu)
    frame.grid(row=1,column=0,padx=20,pady=20,rowspan=3,columnspan=3,sticky=W)
    
    #Canevas d'affichage allumettes
    canvas=Canvas(frame,bg='#FFFFFF',scrollregion=(0,0,192000,192000))
    
    #Scrollbar du canevas
    hbar=Scrollbar(frame,orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=canvas.xview)
    
    #Configuration du Canevas et son scrollbar
    canvas.config(width=700,height=287)
    canvas.config(xscrollcommand=hbar.set)
    canvas.pack(side=LEFT,expand=True,fill=BOTH)
    
    #Affichage des alumettes
    for i in range (OptionAlu):
        canvas.create_image(xx,yy, image=alumette)
        xx=xx+30
    
    # nombre d'allumettes à retirer par l'humain
    global valeur_retirer
    valeur_retirer=Entry(Jeu,textvariable=IntVar())
    valeur_retirer.bind("<Return>",retirersolo)
    valeur_retirer.grid(row=1, column=4,padx=10, pady=10)

    #Alumettes restantes
    Restantes=Label(Jeu, text='Il reste ' + str(OptionAlu) + ' Alumettes', fg='#000000', bg='#FFFFFF')
    Restantes.grid(row=0,column=2,padx=40,pady=10)    
    
    #Consignes de jeu 
    Indication=Label(Jeu, text='Entrez un chiffre entre 1 et 3 pour jouer', fg='#000000', bg='#FFFFFF')
    Indication.grid(row= 1, column=4,padx=20, pady=20,rowspan=2)
    
    #Coup joué par l'odinateur
    CoupOrdi=Label(Jeu, text="Le joeur 2 a retiré " + str(victoire) + " allumettes", fg='#000000', bg='#FFFFFF')
    CoupOrdi.grid(row= 3, column=4,padx=20, pady=20,rowspan=2)

    #Copyright
    Canevas=Canvas(Jeu)
    Canevas.grid(row=4,column=0,columnspan=6)
    Label(Canevas,text='Copyright Marie.P, William.T, Leonard.NC',height=1,width=147,bg='#FFC89B',anchor=SE).pack(side=BOTTOM)

        #Test du vainqueur
    if OptionAlu < 0 :
        Jeu.withdraw()
        FinPartie(2)
    elif OptionAlu == 0:
        Jeu.withdraw()
        FinPartie(1)         
    else :
        Jeu.mainloop()
    
###############################################################################
# Menu Option
    
def Option():
    '''fenêtre Option qui permet de choisir le nombre d'alluemettes et peut être
    dans le futur les paramètres des effets sonores'''
    fenetre.withdraw()
    global MenuOp
    MenuOp = Toplevel()
    MenuOp['bg']='white'
    MenuOp.title("Options - Jeu d'allumettes ")
    MenuOp.geometry("705x280")
    MenuOp.iconbitmap('iconejeu.ico')
    RetourAuMenuP = PhotoImage(file='flèche retour.png')
    #Case à cocher musique 
    boutonmusique = Checkbutton(MenuOp, text="Musique : ",bg='#FFFFFF')
    #Placement
    boutonmusique.grid(row =0, column =0, sticky=SW,padx=10,pady=10)
    value1 = DoubleVar()
    barremusique = Scale(MenuOp, variable=value1, orient=HORIZONTAL,length=500,bg='#FFFFFF')
    barremusique.grid(row =0, column =1,padx=10,pady=10)
    
    boutonson = Checkbutton(MenuOp, text="Son : ",bg='#FFFFFF')
    boutonson.grid(row =1, column =0, sticky=SW,padx=10,pady=10)
    value2 = DoubleVar()
    son = Scale(MenuOp, variable=value2, orient=HORIZONTAL,length=500,bg='#FFFFFF')
    son.grid(row =1, column= 1,padx=20,pady=10)
    
    textallumettes = Label(MenuOp, text="Nombre d'allumettes : ",bg='#FFFFFF')
    textallumettes.grid(row =2, column =0, sticky=SW,padx=10,pady=10)
    value3 = IntVar(value=20)
    global barreallumettes
    barreallumettes = Scale(MenuOp, variable=value3, orient=HORIZONTAL,from_=0,to=1000,length=500,bg='#FFFFFF')
    barreallumettes.grid(row =2, column= 1,columnspan=3,padx=10,pady=10)
    
    Button(MenuOp,image=RetourAuMenuP,command=RetourAuMenuO,relief=FLAT).grid(row=3,column=0,padx=50,pady=10)
    Button(MenuOp,text='Valider',command=ChangeAlu,relief=GROOVE,bg='#FFFFFF').grid(row=3,column=1,padx=50,pady=10)
    
    #Copyright
    Canevas=Canvas(MenuOp)
    Canevas.grid(row=4,column=0,columnspan=6)
    Label(Canevas,text='Copyright Marie.P, William.T, Leonard.NC',height=1,width=100,bg='#FFC89B',anchor=SE).pack(side=BOTTOM)
    
    MenuOp.mainloop()
    
###############################################################################
# Fenêtre de fin de partie
    
def FinPartie(joueur=2):
    global fen_fin
    joueurgagnant = str(getStringJoueur(joueur))
    #création de la fenêtre :
    fen_fin = Toplevel()
    fen_fin.title("Jeu des Allumettes")
    fen_fin.geometry("650x400")
    fen_fin.iconbitmap("iconejeu.ico")
    fen_fin["bg"] = ("beige")
    # bouton qui ferme la fenêtre :
    ferme = Button(fen_fin,text="Retour au menu",command=RetourAuMenuF,bg="beige",relief=GROOVE)
    ferme.pack(side=BOTTOM)
    # Message au gagnant :
    message= Label(fen_fin, text = joueurgagnant + " , vous avez gagné ! Bravo !", fg = "Black", bg = "beige", font= ("Gill Sans Ultra Bold", 22))
    message.pack()
    #image de fond :
    artifice = PhotoImage(file = "artifice.gif")
    lab = Label(fen_fin, image = artifice)
    lab.image = artifice
    lab.pack()
    fen_fin.mainloop()
    
def getStringJoueur(joueur):
    '''Renvoie une String en fonction du joueur passé en paramètre:
    joueur1, joueur2 ou ordinateur
    '''
    if joueur == 1:
        return "joueur 1 "
    if joueur == 2 :
            return "joueur 2 "
    

###############################################################################
# Commandes Liées aux fenêtres


def ChangeAlu():
    global OptionAlu
    OptionAlu=int(barreallumettes.get())
    
def Abandonner():
    Jeu.withdraw()
    FinPartie()
    
def AbandonnerM():
    JeuM.withdraw()
    FinPartie(joueur)
    
def RetourAuMenuF():
    fen_fin.withdraw()
    fenetre.deiconify()

def RetourAuMenu():
    Jeu.withdraw()
    fenetre.deiconify()
    
def RetourAuMenuM():
    JeuM.withdraw()
    fenetre.deiconify()
    
def RetourAuMenuO():
    MenuOp.destroy()
    fenetre.deiconify()    
    
def retirersolo(event):
    global OptionAlu
    global TourHUMAIN
    TourHUMAIN=int(valeur_retirer.get())
    if 0 < TourHUMAIN <= min(OptionAlu,3) :
        Jeu.withdraw()
        OptionAlu=OptionAlu-TourHUMAIN
        Intermédiaire(OptionAlu,MACHINE)
        OptionAlu=OptionAlu-victoire
        TourHUMAIN=0
        fenetre_de_jeu_solo()

def retirermulti(event):
    global OptionAlu
    global TourMULTI
    global numerojoueur
    TourMULTI=int(valeur_retirerM.get())
    if 0  < TourMULTI <= min(OptionAlu,3) :
        JeuM.withdraw()
        OptionAlu=OptionAlu-TourMULTI
        
        if numerojoueur == 1 :
            numerojoueur = 2
        elif numerojoueur == 2 :
            numerojoueur = 1
        TourMULTI = 0
        fenetre_de_jeu_multi()
        
###############################################################################
# PROGRAMME PRINCIPAL
        
Menu()