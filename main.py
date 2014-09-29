#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
PHOTOMETRYDEMO - main.py

starts up the app with corresponding gui


Created on Tue Sep 23 12:09:45 2014
@author: rafik
"""


from model import Model
from controller import Controller
from view_tk import View


if __name__ == "__main__":
    M = Model()
    C = Controller(M)
    #app = PhotoMetryGUI(None, M, C)
    V = View(M, C)
    C.setView(V)

    V.start()