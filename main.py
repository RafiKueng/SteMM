#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
PHOTOMETRYDEMO - main.py

Handles the ui (View in MVC)


Created on Tue Sep 23 12:09:45 2014
@author: rafik
"""

import math
import numpy as np


import Tkinter
import Tkinter as tk
import tkFileDialog

import model
from model import Ellipse, Mask, ROI

import controller


glob = dict()



class StatusBar(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.label.pack(fill=tk.X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()
        


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle






        

class PhotoMetryGUI(Tkinter.Tk):

    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        
        self.el = None
        self.roi = None
        self.masks = []

    def initialize(self):
        
        self.grid()

        #tool bar
        self.toolbar = tk.Frame(self)

        b = tk.Button(self.toolbar, text="open fits", width=6, command=self.openFits)
        b.pack(side=tk.LEFT, padx=2, pady=2)

        b = tk.Button(self.toolbar, text="ellipse", width=6, command=self.createEllipse)
        b.pack(side=tk.LEFT, padx=2, pady=2)

        b = tk.Button(self.toolbar, text="mask", width=6, command=self.createMask)
        b.pack(side=tk.LEFT, padx=2, pady=2)

        b = tk.Button(self.toolbar, text="roi", width=6, command=self.createROI)
        b.pack(side=tk.LEFT, padx=2, pady=2)

        self.toolbar.pack(side=tk.TOP, fill=tk.X)



        self.canv = tk.Canvas(self, width=800, height=800, bg="#aaa")
        self.canv.pack()
        
        #self.canv.create_rectangle((1,1,499,50), fill='blue', tags='bluerect')
        #self.canv.create_rectangle((1,1,50,499), fill='red' , tags='redrect')
        
        self.canv.bind("<Button-1>", self.onCanvClick)
        self.canv.bind("<B1-Motion>", self.onMouseMove)

        #


        # status bar
        self.status = StatusBar(self)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        self.resizable(True,True)
        self.update()
        self.geometry(self.geometry())       



    def openFits(self):
        options = {}
        options['defaultextension'] = '.fits'
        options['filetypes'] = [('fits files', '.fits'),('all files', '.*')]
#        options['initialdir'] = 'C:\\'
#        options['initialfile'] = 'myfile.txt'
        options['parent'] = self
        options['title'] = 'select fits file to open...'
        tkFileDialog.askopenfilename(**options)

    def createEllipse(self):
        #print "onNewClick"
        #self.status.clear()
        if not self.el:
            self.el = Ellipse(self.canv)

    def createMask(self):
        #self.status.set("createMask")
        
        n=len(self.masks)
        self.masks.append(Mask(self.canv, n))

    def createROI(self):
        #self.status.set("createMask")
        if not self.roi:
            n=len(self.masks)
            roi = ROI(self.canv, n)
            self.roi = roi
            self.masks.append(roi)


    def onCanvClick(self, evt):
        self.status.set("onCanvClick")
        item = self.canv.find_closest(evt.x, evt.y)[0]
        tags = self.canv.gettags(item)
        print 'tags1:', tags
        
        try:
            self.selected = False
            if tags[0] == 'poly':
                #item=self.canv.find_below(item)
                #tags = self.canv.gettags(item)
                self.selected = ('ely', 'c')
                return
                
            print 'tags2:', tags
            if tags[0].startswith('p'):
                pnt = tags[0][1]
                #self.el.transform(pnt, evt.x, evt.y)
                print 'sel',pnt
                self.selected = ('ely', pnt)
                return
                
            if tags[0].startswith('rect'):
                _, nr = tags[0].split('_') # "rect_12" for 12th mask
                self.selected = ('rect', int(nr), 'cp') # cp center point
                return

            if tags[0].startswith('rc'): # rectangle corner
                _, nr, tp = tags[0].split('_') # "rc_12_ul" for 12th mask UpperLeft
                self.selected = ('rect', int(nr), tp)
                return
                
                
        except:
            pass

    def onMouseMove(self, evt):
        #print 'mm'
        if self.selected:
            if self.selected[0] == 'ely':
                self.el.transform(self.selected[1], evt.x, evt.y)
            elif self.selected[0] == 'rect':
                self.masks[self.selected[1]].transform(self.selected[2], evt.x, evt.y)

#        self.entryVariable = Tkinter.StringVar()
#        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
#        self.entry.grid(column=0,row=0,sticky='EW')
#        self.entry.bind("<Return>", self.OnPressEnter)
#        self.entryVariable.set(u"Enter text here.")
#
#        button = Tkinter.Button(self,text=u"Click me !",
#                                command=self.OnButtonClick)
#        button.grid(column=1,row=0)
#
#        self.labelVariable = Tkinter.StringVar()
#        label = Tkinter.Label(self,textvariable=self.labelVariable,
#                              anchor="w",fg="white",bg="blue")
#        label.grid(column=0,row=1,columnspan=2,sticky='EW')
#        self.labelVariable.set(u"Hello !")
#
#        self.grid_columnconfigure(0,weight=1)
#        self.resizable(True,False)
#        self.update()
#        self.geometry(self.geometry())       
#        self.entry.focus_set()
#        self.entry.selection_range(0, Tkinter.END)
#
#    def OnButtonClick(self):
#        self.labelVariable.set( self.entryVariable.get()+" (You clicked the button)" )
#        self.entry.focus_set()
#        self.entry.selection_range(0, Tkinter.END)
#
#    def OnPressEnter(self,event):
#        self.labelVariable.set( self.entryVariable.get()+" (You pressed ENTER)" )
#        self.entry.focus_set()
#        self.entry.selection_range(0, Tkinter.END)




if __name__ == "__main__":
    app = PhotoMetryGUI(None)
    app.title('PhotoMetryDemo')
    app.mainloop()