#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
PHOTOMETRYDEMO - model.py

the data model

Created on Tue Sep 23 12:09:45 2014
@author: rafik
"""

import numpy as np
import math

class Model(object):
    
    def __init__(self):
        pass
    



class Selection(object):

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
        
    def _update(self):
        r=5
        self.canv.coords(self.p_a, self.x1-r, self.y1-r, self.x1+r, self.y1+r)
        self.canv.coords(self.p_b, self.x2-r, self.y2-r, self.x2+r, self.y2+r)
        self.canv.coords(self.rect, self.x1, self.y1, self.x2, self.y2)
        
    # inherit and overwrite
    def update(self):
        self._update()
       


#
class Mask(Selection):
    def __init__(self, canv, nr):
        Selection.__init__(self, canv, nr)
        self.type = "mask"

        self.lines = []
        dx = -self.x1+self.x2
        nlines = 10
        for i in range(1,nlines+1):
            x = i*dx/(nlines+1)
            l = self.canv.create_line(self.x1+x, self.y1, self.x1+x, self.y2, tags='rect_%i' % self.nr)
            #print self.x1+x, self.y1, self.x1+x, self.y2
            self.lines.append(l)
        

    def update(self):
        self._update()

        dx = -self.x1+self.x2
        
        for i in range(len(self.lines)):
            x = (i+1)*dx/(len(self.lines)+1)
            self.canv.coords(self.lines[i], self.x1+x, self.y1, self.x1+x, self.y2)
        


#
# used to select an region of interesst (inside selected)
class ROI(Selection):
    def __init__(self, canv, nr):
        print "init roi"
        Selection.__init__(self, canv, nr)
        self.type = "roi"

        self.lines = []
        dd = 5
        sx = int(self.canv.cget('width'))
        sy = int(self.canv.cget('height'))
        
        #print sx, sy        
        
        for xx in range(0,sx):
            #print xx, xx%dd, xx%dd==True
            if xx%dd == 0:
                minx = np.min([self.x1, self.x2])
                maxx = np.max([self.x1, self.x2])
                miny = np.min([self.y1, self.y2])
                maxy = np.max([self.y1, self.y2])

                if xx<minx or xx>maxx:
                    l1 = self.canv.create_line(xx, 0, xx, sy//2, tags='roi_%i' % self.nr)
                    l2 = self.canv.create_line(xx, sy//2, xx, sy, tags='roi_%i' % self.nr)
                else:
                    l1 = self.canv.create_line(xx, 0, xx, miny, tags='roi_%i' % self.nr)
                    l2 = self.canv.create_line(xx, maxy, xx, sy, tags='roi_%i' % self.nr)

                self.lines.append((l1,l2))
        

    def update(self):
        self._update()

        sx = int(self.canv.cget('width'))
        sy = int(self.canv.cget('height'))

        minx = np.min([self.x1, self.x2])
        maxx = np.max([self.x1, self.x2])
        miny = np.min([self.y1, self.y2])
        maxy = np.max([self.y1, self.y2])
        
        for l1, l2 in self.lines:
#            x = (i+1)*dx/(len(self.lines)+1)
#            self.canv.coords(self.lines[i], self.x1+x, self.y1, self.x1+x, self.y2)

            ax1,ay1,ax2,ay2 = self.canv.coords(l1)
            bx1,by1,bx2,by2 = self.canv.coords(l2)
            
            xx = ax1
            
            if xx<minx or xx>maxx:
                self.canv.coords(l1, xx, 0, xx, sy//2)
                self.canv.coords(l2, xx, sy//2, xx, sy)
            else:
                self.canv.coords(l1, xx, 0, xx, miny)
                self.canv.coords(l2, xx, maxy, xx, sy)




class Ellipse(object):
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
        
        
        

    def _poly_oval(self, steps=8):
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
