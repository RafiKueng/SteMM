# ipython interactive demo
# coding: utf-8
import PIL
import Tkinter as tk
import pyfits as pf
import numpy as np
import ImageTk as itk

fits = pf.open('test.fits')
scidata = fits[0].data
uimg = np.clip(scidata, 0, 255).astype(np.uint8)
pilimg = PIL.Image.fromarray(uimg)
root = tk.Tk()
root.grid()
canv = tk.Canvas(root, width=800, height=800, bg='yellow')
canv.pack()
canv.grid()
piimg = itk.PhotoImage(pilimg)
h = piimg.height()
w = piimg.width()
canv.create_image(h//2,w//2,image=piimg)
label = tk.Label(root, image=piimg)
label.grid()
root.mainloop()