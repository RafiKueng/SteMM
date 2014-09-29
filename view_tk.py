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


import Tkinter as tk
import tkFileDialog

import PIL
import pyfits as pf     # sudo apt-get install python-pyfits
import numpy as np
import ImageTk as itk   # sudo apt-get install python-pil.imagetk


#import model
from model import Model, Ellipse, Mask, ROI


from controller import Controller






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






        

class PhotoMetryGUI(tk.Tk):

    def __init__(self,parent, model, controller):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        
        self.el = None
        self.roi = None
        self.masks = []
        
        self.C = controller
        self.data = model   #TODO replace self.data with self.model
        self.model = model
        self.data.masks = self.masks

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

        b = tk.Button(self.toolbar, text="RUN", width=6, command=self.runGalfit)
        b.pack(side=tk.RIGHT, padx=2, pady=2)


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

        filename = tkFileDialog.askopenfilename(**options)
        
#        self.bg_img = openFitsFile(filename)

        
        fits = pf.open(filename)
        scidata = fits[0].data
        uimg = np.clip(scidata, 0, 255).astype(np.uint8)
        self.pilimg = PIL.Image.fromarray(uimg)
        sx, sy = self.pilimg.size
        
        f = 2.0  #hardcoded scaling
        self.bg_scale = f
        self.model.scale = f
        self.canv.scale = f
        self.model.shape = (sx, sy)

        self.pilimg = self.pilimg.resize((int(sx*f),int(sy*f)), PIL.Image.ANTIALIAS)
        self.piimg = itk.PhotoImage(self.pilimg)
        h = self.piimg.height()
        w = self.piimg.width()
        self.bg = self.canv.create_image(h//2,w//2,image=self.piimg)
        
        self.data.bg = {
            'scidata': scidata,
            'mapped' : uimg,
            'pil'    : self.pilimg,
            'pi'     : self.piimg,
            'tk'     : self.bg,
        }
        
        self.model.name = '.'.join(filename.split('/')[-1].split('.')[0:-1])
        self.model.filename = filename.split('/')[-1]
        self.model.filepath = filename
        
        

    def createEllipse(self):
        #print "onNewClick"
        #self.status.clear()
        if not self.el:
            self.el = Ellipse(self.canv)
            self.data.ellipse = self.el

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
            self.data.roi = self.roi
            
            
    def runGalfit(self):
        self.status.set("... runing galfit ... please wait ...")
        ec = self.C.galfit()
        self.status.set("Done [%s]" % ec)


    def onCanvClick(self, evt):
        self.status.set("onCanvClick")
        try:
            item = self.canv.find_closest(evt.x, evt.y)[0]
        except:
            return
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



    def askOutfileName(self):
        options = {}
        options['defaultextension'] = '.fits'
        options['filetypes'] = [('fits files', '.fits'),('all files', '.*')]
#        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'imgblock.fits'
        options['parent'] = self
        options['title'] = 'select output fits file to save...'

        filename = tkFileDialog.asksaveasfilename(**options)
        
    def msg(self, s):
        self.status.set(s)




class View(PhotoMetryGUI):
    
    def __init__(self, model=None, controller=None):
        PhotoMetryGUI.__init__(self, None, model, controller)
    
    def start(self):
        self.title('PhotoMetryDemo')
        self.mainloop()        


#if __name__ == "__main__":
#    M = Model()
#    C = Controller(M)
#    app = PhotoMetryGUI(None, M, C)
#    C.setView(app)
