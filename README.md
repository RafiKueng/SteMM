# SteMM - StellarMassMaps

Basically a frontend for galfit and SExtractor with database access to CHFTL cutout service.
More things (tools, database access) will be added by need or demand.

This is a test appilcation. The final product will possibly be included in SpaghettiLens using a web frontend and running serverside.


## Install

You need the following:

* PIL    (should be installed; `sudo apt-get install python-pil`)
* ImageTk (`sudo apt-get install python-pil.imagetk`)
* pyfits (`sudo apt-get install python-pyfits`)
* numpy / scipy / matplotlib (`sudo apt-get install python-numpy python-scipy python-matplotlib`)

or in one line:

* `sudo apt-get install python-pil python-pil.imagetk python-pyfits python-numpy python-scipy python-matplotlib`

or using pip:

* pip install pil pyfits numpy scipy matplotlib

## Usage
run `python main.py`

(currently, there's only a basic TkInter GUI available)