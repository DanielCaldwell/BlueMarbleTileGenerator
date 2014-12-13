#!/usr/bin/env python

from BlueMarbleUtils import BlueMarbleUrls
from BlueMarbleUtils import cutTiles
from BlueMarbleUtils import mergeToZoomLevel

from Utils import downloadFile
from Utils import convertPngToVips

__author__ = 'Daniel Caldwell'
__license__ = 'MIT'
__copyright__ = 'Daniel Caldwell'

urls =  BlueMarbleUrls(9, True, True)


# download the blue marble images
downloadFile( urls.A1(), "A1.png")
downloadFile( urls.A2(), "A2.png")
downloadFile( urls.B1(), "B1.png")
downloadFile( urls.B2(), "B2.png")
downloadFile( urls.C1(), "C1.png")
downloadFile( urls.C2(), "C2.png")
downloadFile( urls.D1(), "D1.png")
downloadFile( urls.D2(), "D2.png")


# convert to vips for faster processing
convertPngToVips("A1.png")
convertPngToVips("A2.png")
convertPngToVips("B1.png")
convertPngToVips("B2.png")
convertPngToVips("C1.png")
convertPngToVips("C2.png")
convertPngToVips("D1.png")
convertPngToVips("D2.png")


# cut the tiles at the maximum resolution (zoom level 8) and store them in sub directory
cutTiles("A1.png.v", "bm", 8, "A", "1" )
cutTiles("B1.png.v", "bm", 8, "B", "1" )
cutTiles("C1.png.v", "bm", 8, "C", "1" )
cutTiles("D1.png.v", "bm", 8, "D", "1" )
cutTiles("A2.png.v", "bm", 8, "A", "2" )
cutTiles("B2.png.v", "bm", 8, "B", "2" )
cutTiles("C2.png.v", "bm", 8, "C", "2" )
cutTiles("D2.png.v", "bm", 8, "D", "2" )


# combine the chopped up tiles in sub directory into higher scale zoom levels
# 8 -> 7, 7 -> 6, 6 -> 5, ... -> 0
mergeToZoomLevel("bm", "8", "7" )
mergeToZoomLevel("bm", "7", "6" )
mergeToZoomLevel("bm", "6", "5" )
mergeToZoomLevel("bm", "5", "4" )
mergeToZoomLevel("bm", "4", "3" )
mergeToZoomLevel("bm", "3", "2" )
mergeToZoomLevel("bm", "2", "1" )
mergeToZoomLevel("bm", "1", "0" )


