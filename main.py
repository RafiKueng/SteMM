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

import model
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





class Mask(object):

    def __init__(self, canv, nr):
        self.canv = canv
        self.x1, self.y1, self.x2, self.y2 = (30,60,100,120)
        self.nr = nr
        
        tg = 'rect_%i' % nr
        tg2 = 'rc_%i_' % nr
        self.rect = canv.create_rectangle(self.x1, self.y1, self.x2, self.y2, tags=tg)
        self.p_a  = canv.create_circle(self.x1,self.y1,5, fill='black', tags=tg2+'ul')
        self.p_b  = canv.create_circle(self.x2,self.y2,5, fill='black', tags=tg2+'lr')
        
    def transform(self, pnt, x, y):
        
        if pnt=="cp":
            xo = (self.x1+self.x2) // 2
            yo = (self.y1+self.y2) // 2
            dx = self.x2 - xo
            dy = self.y2 - yo

            self.x1 = x-dx
            self.y1 = y-dy
            self.x2 = x+dx
            self.y2 = y+dy
        elif pnt=="ul":
            self.x1 = x
            self.y1 = y
        elif pnt=='lr':
            self.x2 = x
            self.y2 = y
            
        
        self.update()
        
    def update(self):
        r=5
        self.canv.coords(self.p_a, self.x1-r, self.y1-r, self.x1+r, self.y1+r)
        self.canv.coords(self.p_b, self.x2-r, self.y2-r, self.x2+r, self.y2+r)
        self.canv.coords(self.rect, self.x1, self.y1, self.x2, self.y2)
       



class Ellypse(object):
    def __init__(self, canv):
        self.canv = canv
        self.xc = 300
        self.yc = 300
        self.a  = 100
        self.b  = 50
        self.r  = np.pi / 4
        
        pnts = self._poly_oval()
        xa, ya, xb, yb = self._getHandlePoints()
        
        self.poly = canv.create_polygon(pnts, fill='', outline='#fff', width=2, smooth=1, tags='poly')
        self.p_a  = canv.create_circle(xa,ya,5, fill='black', tags='pa')
        self.p_b  = canv.create_circle(xb,yb,5, fill='black', tags='pb')
        self.p_c  = canv.create_circle(self.xc,self.yc,5, fill='black', tags='pc')


    def _getHandlePoints(self):
        xa = self.xc + self.a*np.cos(self.r)
        ya = self.yc - self.a*np.sin(self.r)

        xb = self.xc + self.b*np.cos(self.r+np.pi/2)
        yb = self.yc - self.b*np.sin(self.r+np.pi/2)
        
        return (xa,ya,xb,yb)        
        
    def update(self):
        pnts = self._poly_oval()
        xa, ya, xb, yb = self._getHandlePoints()
        xc, yc = (self.xc, self.yc)
        r = 5

        self.canv.delete(self.poly)
        self.canv.coords(self.p_a, xa-r, ya-r, xa+r, ya+r)
        self.canv.coords(self.p_b, xb-r, yb-r, xb+r, yb+r)
        self.canv.coords(self.p_c, xc-r, yc-r, xc+r, yc+r)
        self.poly = self.canv.create_polygon(pnts, fill='', outline='#fff', width=2, smooth=1, tags='poly')
        
                
        
    def transform(self, pnt, xp=0, yp=0):
        
        if pnt=='c':
            self.xc=xp
            self.yc=yp
            self.update()
            return

        xc = self.xc
        yc = self.yc
        a  = self.a
        b  = self.b
        
        dx = xc - xp
        dy = yc - yp
        
        ab = np.sqrt(dx*dx+dy*dy)
        wab = np.arctan2(dx,dy)
        
        if pnt=='a':
            a = ab
            r = wab + np.pi/2
            if a<b: return
        else:
            b = ab
            r = wab
            if b>a:return
            
        

        self.a  = a
        self.b  = b
        self.r  = r
        
        self.update()
        return
    
    def move(self, xc=0, yc=0):
        pass

        

#    def poly_oval2(x0,y0, x1,y1, r=0, steps=20):
#        """return an oval as coordinates suitable for create_polygon"""
#
#        # x0,y0,x1,y1 are as create_oval
#    
#        # rotation is in degrees anti-clockwise, convert to radians
#        #rotation = r * math.pi / 180.0
#        rotation = r
#    
#        # major and minor axes
#        a = (x1 - x0) / 2.0
#        b = (y1 - y0) / 2.0
#    
#        # center
#        xc = x0 + a
#        yc = y0 + b
#    
#        point_list = []
#    
#        # create the oval as a list of points
#        for i in range(steps):
#    
#            # Calculate the angle for this step
#            # 360 degrees == 2 pi radians
#            theta = (math.pi * 2) * (float(i) / steps)
#    
#            x1 = a * math.cos(theta)
#            y1 = b * math.sin(theta)
#    
#            # rotate x, y
#            x = (x1 * math.cos(rotation)) + (y1 * math.sin(rotation))
#            y = (y1 * math.cos(rotation)) - (x1 * math.sin(rotation))
#    
#            point_list.append(round(x + xc))
#            point_list.append(round(y + yc))
#    
#        return point_list
        
        
        

    def _poly_oval(self, steps=20):
        """return an oval as coordinates suitable for create_polygon"""
        xc = self.xc
        yc = self.yc
        a = self.a
        b = self.b
        r = self.r
        
        point_list = []
    
        # create the oval as a list of points
        for i in range(steps):
    
            # Calculate the angle for this step
            # 360 degrees == 2 pi radians
            theta = (math.pi * 2) * (float(i) / steps)
    
            x1 = a * math.cos(theta)
            y1 = b * math.sin(theta)
    
            # rotate x, y
            x = (x1 * math.cos(r)) + (y1 * math.sin(r))
            y = (y1 * math.cos(r)) - (x1 * math.sin(r))
    
            point_list.append(round(x + xc))
            point_list.append(round(y + yc))
    
        return point_list

        

class PhotoMetryGUI(Tkinter.Tk):

    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        
        self.masks = []

    def initialize(self):
        
        self.grid()

        #tool bar
        self.toolbar = tk.Frame(self)

        b = tk.Button(self.toolbar, text="new", width=6, command=self.onNewClick)
        b.pack(side=tk.LEFT, padx=2, pady=2)

        b = tk.Button(self.toolbar, text="open", width=6, command=self.onOpenClick)
        b.pack(side=tk.LEFT, padx=2, pady=2)

        self.toolbar.pack(side=tk.TOP, fill=tk.X)



        self.canv = tk.Canvas(self, width=500, height=500, bg="yellow")
        self.canv.pack()
        
        self.canv.create_rectangle((1,1,499,50), fill='blue', tags='bluerect')
        self.canv.create_rectangle((1,1,50,499), fill='red' , tags='redrect')
        
        self.canv.bind("<Button-1>", self.onCanvClick)
        self.canv.bind("<B1-Motion>", self.onMouseMove)

        #


        # status bar
        self.status = StatusBar(self)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        self.resizable(True,True)
        self.update()
        self.geometry(self.geometry())       


    def onNewClick(self):
        print "onNewClick"
        #self.status.clear()
        
        self.el = Ellypse(self.canv)

    def onOpenClick(self):
        self.status.set("onOpenClick")
        
        n=len(self.masks)
        self.masks.append(Mask(self.canv, n))

    def onCanvClick(self, evt):
        self.status.set("onCanvClick")
        item = self.canv.find_closest(evt.x, evt.y)[0]
        tags = self.canv.gettags(item)
        print 'tags1:', tags
        
        try:
            self.selected = False
            if tags[0] == 'poly':
                item=self.canv.find_below(item)
                tags = self.canv.gettags(item)
                
            print 'tags2:', tags
            if tags[0].startswith('p'):
                pnt = tags[0][1]
                #self.el.transform(pnt, evt.x, evt.y)
                print 'sel',pnt
                self.selected = ('ely', pnt)
                
            if tags[0].startswith('rect'):
                _, nr = tags[0].split('_') # "rect_12" for 12th mask
                self.selected = ('rect', int(nr), 'cp') # cp center point

            if tags[0].startswith('rc'): # rectangle corner
                _, nr, tp = tags[0].split('_') # "rc_12_ul" for 12th mask UpperLeft
                self.selected = ('rect', int(nr), tp)
                
                
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