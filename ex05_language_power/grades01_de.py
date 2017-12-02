#! /usr/bin/env python
"""
Schueler haben Noten. Eine Schulklasse hat Schueler.

Mit diesen sieben Worten kann man in einer Sekunde einiges Mitteilen. Jeder
weiss sofort, wovon die Rede ist. Python ist eine sehr vorteilhafte Programmier-
sprache, weil sie kurzen und leicht leserlichen Code ermoeglicht. Man kann sich
dei Versprachlichung von Denkkonzepten zunutze machen. Wenn man die obigen
sieben Worte in die Sprache Python uebersetzt, dann hat man sofort sinnvolle
Klassendefinitionen (hier jetzt "Klassen" im Kontext objektorientierter
Programmierung). Weiter kann man vorgehen, indem man die Wuensche "was soll ein
Objekt der Klasse alles koennen" als Funktionsdefinitionen erstmal einfach
hinschreibt und spaeter fuer die Implementierung im Detail sorgt.
"""
import numpy as np

#--- Klassendefinitionen

class Schueler(object):
    
    def __init__(self,name):
        self.name=name
        self.mathenoten=[]
        self.deutschnoten=[]
    
    def berechne_eigenen_schnitt(self,fach):
        """Berechnung der Durchschnittsnote fuer ein bestimmtes Fach"""
        raise NotImplementedError('Ich will diese Funktion irgendwann haben, mach es aber spaeter.')


class Schulklasse(object):
    
    def __init__(self,name):
        self.name=name
        self.schueler_liste=[]
        self.anzahl=0
    
    def aktualisiere_anzahl(self):
        self.anzahl=len(self.schueler_liste)
    
    def berechne_schnitt(self,fach,i):
        """Berechnung der Durchschnittsnote einer bestimmten Klassenarbeit""" 
        S=0.
        if fach=='mathe':
            for schueler in self.schueler_liste:
                S=S+schueler.mathenoten[i]
        elif fach=='deutsch':
            for schueler in self.schueler_liste:
                S=S+schueler.deutschnoten[i]
        else:
            raise ValueError('unbekkanntes Fach: "{}"'.format(fach))
        return S/float(self.anzahl)

    def berechne_alle_durchschnittsnoten(self,fach,anzahl_tests):
        """Berechnung des Klassendurchschnitts ueber alle Klassenarbeiten eines Faches""" 
        S=0.
        if fach=='mathe':
            for schueler in self.schueler_liste:
                S+=np.sum(schueler.mathenoten)
        elif fach=='deutsch':
            for schueler in self.schueler_liste:
                S+=np.sum(schueler.deutschnoten)
        else:
            raise ValueError('unbekkanntes Fach: "{}"'.format(fach))
        return S/float(self.anzahl)/float(anzahl_tests)


#--- Hauptteil des Programms

Otto=Schueler('Otto')
Otto.mathenoten=[2,1,3,1,2]
Otto.deutschnoten=[3,2,2,3,3]

Anna=Schueler('Anna')
Anna.mathenoten=[1,2,3,2,1]
Anna.deutschnoten=[1,1,2,1,1]

Leila=Schueler('Leila')
Leila.mathenoten=[1,2,3,4,5]
Leila.deutschnoten=[6,5,4,3,2]

Frank=Schueler('Frank')
Frank.mathenoten=[1.5, 2, 2.5, 1, 1.5]
Frank.deutschnoten=[2, 2.25, 2.5, 2.75, 1.75]

Tobi=Schueler('Tobi')
Tobi.mathenoten=[2,2,3,2,2]
Tobi.deutschnoten=[3,3,2,3,3]

a9=Schulklasse('9a') # Ein Variablenname darf nicht mit einer Ziffer beginnen, das ist eine Syntaxregel
a9.schueler_liste=[Otto,Anna,Leila,Frank,Tobi]
a9.aktualisiere_anzahl()
mathe_avg1=a9.berechne_schnitt('mathe',0)
mathe_avg5=a9.berechne_schnitt('mathe',4)
total_deutsch_avg=a9.berechne_alle_durchschnittsnoten('deutsch',5)

print 'Schnitt der ersten Mathearbeit: ',mathe_avg1
print 'Schnitt der fuenften Mathearbeit: ',mathe_avg5
print 'Gesamtschnitt ueber alle Deutscharbeiten: ',total_deutsch_avg

print 'Schnitte aller Mathearbeiten: ',[a9.berechne_schnitt('mathe',i) for i in range(5)]
print 'Schnitte aller Deutscharbeiten: ',[a9.berechne_schnitt('deutsch',i) for i in range(5)]

