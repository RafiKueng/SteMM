#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
PHOTOMETRYDEMO - main.py

Handles the ui (View in MVC)


Created on Tue Sep 23 12:09:45 2014
@author: rafik
"""

import Tkinter
import Tkinter as tk

import model
import controller






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
        
        
        

class PhotoMetryGUI(Tkinter.Tk):

    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        
        #tool bar
        self.toolbar = tk.Frame(self)

        b = tk.Button(self.toolbar, text="new", width=6, command=self.onNewClick)
        b.pack(side=tk.LEFT, padx=2, pady=2)

        b = tk.Button(self.toolbar, text="open", width=6, command=self.onOpenClick)
        b.pack(side=tk.LEFT, padx=2, pady=2)

        self.toolbar.pack(side=tk.TOP, fill=tk.X)



        self.canv = tk.Canvas(self, width=500, height=500, bg="yellow")
        self.canv.pack()
        
        self.canv.create_rectangle((1,1,499,50), fill='blue')
        self.canv.create_rectangle((1,1,50,499), fill='red')

        #self.grid()


        # status bar
        self.status = StatusBar(self)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        self.resizable(True,True)
        self.update()
        self.geometry(self.geometry())       


    def onNewClick(self):
        print "onNewClick"
        self.status.clear()
    def onOpenClick(self):
        self.status.set("onOpenClick")



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