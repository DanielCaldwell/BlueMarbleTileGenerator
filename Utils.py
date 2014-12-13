import urllib
import os.path
from vipsCC import *


__author__ = 'Daniel Caldwell'
__license__ = 'MIT'
__copyright__ = 'Daniel Caldwell'

def downloadFile( url, localFile ):
    if (os.path.isfile(localFile)):
        print "File (%s) is already downloaded " % (localFile)
    else :
        print "Downloading file (%s) to local file (%s)" % (url, localFile)
        testfile=urllib.URLopener()
        testfile.retrieve(url, localFile)



# convert to vips
def convertPngToVips(filepath):
    if (os.path.isfile(filepath + ".v")):
        print "File (%s) is already converted " % (filepath)
    else :
        print "Converting file (%s) to vips" % (filepath)
        file = VImage.VImage(filepath)
        file.write(filepath + ".v")

