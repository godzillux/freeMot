#!/usr/bin/python
#-*- encoding:utf-8 -*-

import random
import sys

"""
permet de generer des fichiers de mot de passe.
"""

xchar = 'AZERTYUIOPQSDFGHJKLMWXCVBNazertyuiopqsdfghjklmwxcvbn1234567890 ,;:!/.'

taille=int(sys.argv[1])
if not taille:
    print("le premier argument doit etre la taille du mot de passe")
    sys.exit(2)

print('taille du fichier en octet %d' % (len(xchar)**taille))

def p(r, l):
    char = list(xchar)
    random.shuffle(char)
    for a in char:
        if(l==1):
            sys.stdout.write(r+a)
        else:
            p(r+a, l-1)
    if(l==1):
        sys.stdout.flush()
p('', taille)

