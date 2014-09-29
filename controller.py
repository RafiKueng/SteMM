#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
PHOTOMETRYDEMO - controller.py

basically the interface to galfit and fits files


Created on Tue Sep 23 12:09:45 2014
@author: rafik
"""

import time
import subprocess



templates = {

'header' : '''
================================================================================
# IMAGE and GALFIT CONTROL PARAMETERS
A) {A:<20}  # Input data image (FITS file)
B) {B:<20}  # Output data image block
C) {C:<20}  # Sigma image name (made from data if blank or "none") 
D) {D:<20}  # Input PSF image and (optional) diffusion kernel
E) {E:<20}  # PSF fine sampling factor relative to data 
F) {F:<20}  # Bad pixel mask (FITS image or ASCII coord list)
G) {G:<20}  # File with parameter constraints (ASCII file) 
H) {H:<20}  # Image region to fit (xmin xmax ymin ymax)
I) {I:<20}  # Size of the convolution box (x y)
J) {J:<20}  # Magnitude photometric zeropoint 
K) {K:<20}  # Plate scale (dx dy)   [arcsec per pixel]
O) {O:<20}  # Display type (regular, curses, both)
P) {P:<20}  # Options: 0=normal run; 1,2=make model/imgblock & quit
''',

'sersic' : '''

# Sersic function
 0) sersic               # Object type
 1) {p1:<16} {p1t} # position x, y        [pixel]
 3) {p3:<18} {p3t} # total magnitude    
 4) {p4:<18} {p4t} # R_e              [Pixels]
 5) {p5:<18} {p5t} # Sersic exponent (deVauc=4, expdisk=1)  
 9) {p9:<18} {p9t} # axis ratio (b/a)   
10) {p10:<18} {p10t} # position angle (PA)  [Degrees: Up=0, Left=90]
 Z) {pZ:<20} #  Skip this model in output image?  (yes=1, no=0)
''',

'sky' : '''

# sky
 0) sky
 1) {p1:<18} {p1t} # sky background       [ADU counts]
 2) {p2:<18} {p2t} # dsky/dx (sky gradient in x) 
 3) {p3:<18} {p3t} # dsky/dy (sky gradient in y) 
 Z) {pZ:<20} #  Skip this model in output image?  (yes=1, no=0)
''',
}

ParamsAvail = {  # dont list the Z
    'sersic':   ['1','3','4','5','9','10'],
    'sky':      ['1','2','3']
}

#defaults = {
#'header': {
#    'A': 'gal.fits',
#    'B': 'imgblock.fits',
#    'C': 'none',
#    'D': 'psf.fits',
#    'E': '1',
#    'F': 'none',
#    'G': 'none',
#    'H': '1 93 1 93',
#    'I': '100 100',
#    'J': '26.563',
#    'K': '0.038 0.038',
#    'O': 'regular',
#    'P': '0',
#    },
#    
#'sersic': {
#    'p1': '',
#    'p1t': '1',
#    'p2': '',
#    'p2t': '1',
#    'p3': '',
#    'p3t': '1',
#    'p4': '',
#    'p4t': '1',
#    'p5': '',
#    'p5t': '1',
#    'p9': '',
#    'p9t': '1',
#    'p10': '',
#    'p10t': '1',
#    'pZ': '0',
#    },
#}


class Controller(object):
    def __init__(self, model, view=None):
        self.model = model
        self.view = view
        self.prefix = '_' # prefix for paths for generated files
        self.configfn = None # filename of config file .galfit / .feedme ...
        
    def setView(self, V):
        self.view = V
        
        
    def galfit(self):
        print 'create config file'
        self.view.msg('create config file')
        self.createConfigFile()
        print 'config file done'
        self.view.msg('running galfit')

#        process = sp.Popen('./galfit '+self.model.name+'.galfit', shell=True, stdout=sp.PIPE)
#        process.wait()
#        print process.returncode

#        cmd = ['./galfit', self.model.name+'.galfit']
#        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
#        for line in p.stdout:
#            print line
#        p.wait()
#        print p.returncode

        rc = subprocess.call('./galfit '+self.configfn, shell=True)         
        self.view.msg('done')        
        return "success"

        
    def createConfigFile(self):
        fn = self.prefix + self.model.name + '.galfit'
        
        #create header
        params = {}
        for c in 'ABCDEFGHIJKOP':
            params[c] = self.getParam(c)
        head = templates['header'].format(**params)

        # create all object entries
        objstxt = ''
        for obj in ['sersic', 'sky']: #TODO make this more dynamic
            oparams = {}
            for c in ParamsAvail[obj]:
                print obj, c
                p, a = self.getObjParams(obj, c)
                oparams['p%s'%c] = p
                oparams['p%st'%c] = a
            oparams['pZ'] = 0
            print oparams
            objtxt = templates[obj].format(**oparams)
            objstxt += objtxt
        
        txt = head + objstxt
        
        with open(fn, 'w') as f:
            f.write(txt)
            
        self.configfn = fn
        return fn
            

    
    def getParam(self, p):
        
        if p=="A":
            return self.model.filename
        
        elif p=='B':
            #return self.view.askOutfileName()
            return self.prefix + 'out.fits'
            
        elif p=='C':
            return 'none'
            
        elif p=='D':
            if not self.model.psf:
                self.model.createPSF(pfx=self.prefix)
            return self.prefix+self.model.psf.getFileName()

        elif p=='E':
            return '1'

        elif p=='F':
            maskfn = self.model.getMaskFilename(pfx=self.prefix)
            return maskfn
            
        elif p=='G':
            return self.generateContraintsFile(self.prefix)
            
        elif p=='H':
            xmin, ymin, xmax, ymax = self.model.getRegionCoords()
            return '%.1f %.1f %.1f %.1f' % (xmin, xmax, ymin, ymax)
            
        elif p=='I':
            if not self.model.psf:
                self.model.createPSF(pfx=self.prefix)
            return '%.1f %.1f' % self.model.psf.getBoxSize()
            
        elif p=='J':
            return self.model.getPhotometricZeropoint()
            
        elif p=='K':
            return '%.5f %.5f' % self.model.getPlateScale()
            
        elif p=='O':
            return 'regular'
            
        elif p=='P':
            return 0
            
            
    def getObjParams(self, typ, p):
        if typ == 'sersic':
            
            if p=='1':
                return ("%i %i" % self.model.ellipse.getCoords(), '1 1')
            
            elif p=='3':
                #TODO
                return (12, 1)
                
            elif p=='4':
                return (self.model.ellipse.getRe(), 1)
                
            elif p=='5':
                return (4, 1)
                
            elif p=='9':
                return (self.model.ellipse.getAxisRatio(), 1)
                
            elif p=='10':
                return (self.model.ellipse.getPositionAngle(), 1)
                
                
        elif typ == 'sky':

            if p=='1':
                #TODO
                return (1.3, '1')
            
            elif p=='2':
                #TODO
                return (0, 1)
                
            elif p=='3':
                return (0, 1)
                
            
            
        
        
        
    def generateContraintsFile(self, pfx=''):
        filename = pfx + 'constr.txt'
        #TODO

        txt = '''
# Component/    parameter   constraint	Comment
# operation	(see below)   range
1               n           3.5 to 6    # sersic index 
'''
        
        with open(filename, 'w') as f:
            f.write(txt)

        return filename
    



def sendToGalfit():
    pass


def openFitsFile(filename):
    pass
    
    
def printdata():
    print model.masks
    
# testing
if __name__ == "__main__":
    pass