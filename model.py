#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
PHOTOMETRYDEMO - model.py

the data model

Created on Tue Sep 23 12:09:45 2014
@author: rafik
"""

import numpy as np
import scipy as sp
import scipy.ndimage.interpolation
import math
import pyfits


class Model(object):
    
    def __init__(self):
        self.name = None
        self.masks = []
        self.roi = None
        self.ellipse = None
        self.shape = None
        self.scale = -1
        self.psf = None
        
        
    def getRegionCoords(self):
        return self.roi.getRegionCoords()
        
    def getMaskFilename(self):
        filename = 'bla.fits'
        sx, sy = self.shape
        
        renderedmask = np.ones((sx, sy), dtype=np.int)
        for mask in self.masks:
            if mask.type == 'mask':
                pixels = mask.getCoveredPixels()
                for px, py in pixels:
                    renderedmask[px, py] = 0

        hdu = pyfits.PrimaryHDU(np.rot90(renderedmask))
        hdu.writeto(filename)
        #renderedmask = sp.ndimage.interpolation.zoom(mask, 1./self.scale)
        #TODO implement saving as fits
        return filename

    def createPSF(self):
        #TODO
        self.psf = PSF()
        
    def getPhotometricZeropoint(self):
        #TODO
        return 0.0
            
    def getPlateScale(self):
        #TODO
        return (0.001, 0.001)
        
    



class Selection(object):

    def __init__(self, canv, nr, color):
        self.canv = canv
        s = self.canv.scale
        print 'scale', s
        self.x1, self.y1, self.x2, self.y2 = np.array([30,60,100,120])
        self.nr = nr
        self.color = color
        self.type = None
        
        
        tg = 'rect_%i' % nr
        tg2 = 'rc_%i_' % nr
        self.rect = canv.create_rectangle(self.x1*s, self.y1*s, self.x2*s, self.y2*s, tags=tg, outline=self.color)
        self.p_a  = canv.create_circle(self.x1*s,self.y1*s,5, fill=self.color, tags=tg2+'ul')
        self.p_b  = canv.create_circle(self.x2*s,self.y2*s,5, fill=self.color, tags=tg2+'lr')
        
    def transform(self, pnt, x, y):
        
        s = self.canv.scale        
        x /= s
        y /= s
        
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
        s = self.canv.scale
        self.canv.coords(self.p_a, self.x1*s-r, self.y1*s-r, self.x1*s+r, self.y1*s+r)
        self.canv.coords(self.p_b, self.x2*s-r, self.y2*s-r, self.x2*s+r, self.y2*s+r)
        self.canv.coords(self.rect, self.x1*s, self.y1*s, self.x2*s, self.y2*s)
        
    # inherit and overwrite
    def update(self):
        self._update()
       


#
class Mask(Selection):
    def __init__(self, canv, nr):
        Selection.__init__(self, canv, nr, color='yellow')
        self.type = "mask"
        s = self.canv.scale
        self.lines = []
        dx = -self.x1+self.x2
        dx *= s
        nlines = 10
        for i in range(1,nlines+1):
            x = i*dx/(nlines+1)
            l = self.canv.create_line(self.x1*s+x, self.y1*s, self.x1*s+x, self.y2*s, tags='rect_%i' % self.nr, fill=self.color)
            #print self.x1+x, self.y1, self.x1+x, self.y2
            self.lines.append(l)
        

    def update(self):
        self._update()
        s = self.canv.scale

        dx = -self.x1+self.x2
        
        for i in range(len(self.lines)):
            x = (i+1)*dx/(len(self.lines)+1)*s
            self.canv.coords(self.lines[i], self.x1*s+x, self.y1*s, self.x1*s+x, self.y2*s)
            
            
    def getCoveredPixels(self):
        px = []
        minx = int(np.floor(np.min([self.x1, self.x2])))
        maxx = int(np.floor(np.max([self.x1, self.x2])))
        miny = int(np.floor(np.min([self.y1, self.y2])))
        maxy = int(np.floor(np.max([self.y1, self.y2])))
        for x in range(minx, maxx+1):
            for y in range(miny, maxy+1):
                px.append((x,y))
        return px
        


#
# used to select an region of interesst (inside selected)
class ROI(Selection):
    def __init__(self, canv, nr):
        print "init roi"
        Selection.__init__(self, canv, nr, color='green')
        self.type = "roi"

        s = self.canv.scale

        self.lines = []
        dd = 5
        sx = int(self.canv.cget('width'))
        sy = int(self.canv.cget('height'))
        
        #print sx, sy        
        
        for xx in range(0,sx):
            #print xx, xx%dd, xx%dd==True
            if xx%dd == 0:
                minx = np.min([self.x1, self.x2])*s
                maxx = np.max([self.x1, self.x2])*s
                miny = np.min([self.y1, self.y2])*s
                maxy = np.max([self.y1, self.y2])*s

                if xx<minx or xx>maxx:
                    l1 = self.canv.create_line(xx, 0, xx, sy//2, tags='roi_%i' % self.nr, fill=self.color)
                    l2 = self.canv.create_line(xx, sy//2, xx, sy, tags='roi_%i' % self.nr, fill=self.color)
                else:
                    l1 = self.canv.create_line(xx, 0, xx, miny, tags='roi_%i' % self.nr, fill=self.color)
                    l2 = self.canv.create_line(xx, maxy, xx, sy, tags='roi_%i' % self.nr, fill=self.color)

                self.lines.append((l1,l2))
        

    def update(self):
        self._update()
        
        s = self.canv.scale

        sx = int(self.canv.cget('width'))
        sy = int(self.canv.cget('height'))

        minx = np.min([self.x1, self.x2])*s
        maxx = np.max([self.x1, self.x2])*s
        miny = np.min([self.y1, self.y2])*s
        maxy = np.max([self.y1, self.y2])*s
        
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
                
                
    def getRegionCoords(self):
        minx = np.min([self.x1, self.x2])
        maxx = np.max([self.x1, self.x2])
        miny = np.min([self.y1, self.y2])
        maxy = np.max([self.y1, self.y2])        
        return (minx, miny, maxx, maxy)




class Ellipse(object):
    def __init__(self, canv):
        self.canv = canv
        self.xc = 300
        self.yc = 300
        self.a  = 100
        self.b  = 50
        self.r  = np.pi / 4

        s = self.canv.scale
        
        pnts = self._poly_oval()
        xa, ya, xb, yb = self._getHandlePoints()
        
        self.poly = canv.create_polygon(pnts, fill='', outline='#fff', width=2, smooth=1, tags='poly')
        self.p_a  = canv.create_circle(xa,ya,5, fill='red', tags='pa')
        self.p_b  = canv.create_circle(xb,yb,5, fill='red', tags='pb')
        self.p_c  = canv.create_circle(self.xc*s,self.yc*s,5, fill='red', tags='pc')
        
    def getCoords(self):
        return (self.xc, self.yc)
        
    # R_e (half light radius)
    def getRe(self):
        return np.sqrt(self.a * self.b)

    def getAxisRatio(self):
        return 1.0 * self.b / self.a
        
    def getPositionAngle(self):
        # should be in deg
        # is messured from upwards y axis, internal saved from horizontal x axis (+90)
        return self.r / np.pi * 180 + 90
        
        
    def _getHandlePoints(self):
        s = self.canv.scale
        
        xa = self.xc + self.a*np.cos(self.r)
        ya = self.yc - self.a*np.sin(self.r)

        xb = self.xc + self.b*np.cos(self.r+np.pi/2)
        yb = self.yc - self.b*np.sin(self.r+np.pi/2)
        
        return (xa*s,ya*s,xb*s,yb*s)        
        
    def update(self):
        print (self.xc, self.yc, self.a, self.b, self.r)
        s = self.canv.scale
        pnts = self._poly_oval()
        xa, ya, xb, yb = self._getHandlePoints()
        xc, yc = (self.xc*s, self.yc*s)
        r = 5

        self.canv.delete(self.poly)
        self.canv.coords(self.p_a, xa-r, ya-r, xa+r, ya+r)
        self.canv.coords(self.p_b, xb-r, yb-r, xb+r, yb+r)
        self.canv.coords(self.p_c, xc-r, yc-r, xc+r, yc+r)
        self.poly = self.canv.create_polygon(pnts, fill='', outline='#fff', width=2, smooth=1, tags='poly')
        
                
        
    def transform(self, pnt, xp=0, yp=0):
        s = self.canv.scale
        xp /= s
        yp /= s
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
        
        
        

    def _poly_oval(self, steps=16):
        """return an oval as coordinates suitable for create_polygon"""
        s = self.canv.scale
        
        xc = self.xc * s
        yc = self.yc * s
        a = self.a * s
        b = self.b * s
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



class PSF(object):
    def __init__(self):
        #TODO
        pass
    
    def getBoxSize(self):
        #TODO
        return (100, 100)
        
    def getFileName(self):
        #TODO
        return 'psf.fits'