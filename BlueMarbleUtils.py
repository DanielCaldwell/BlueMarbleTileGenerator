import  math
import os.path
from vipsCC import *
from PIL import Image

__author__ = 'Daniel Caldwell'
__license__ = 'MIT'
__copyright__ = 'Daniel Caldwell'

class BlueMarbleUrls:

    s_base_url = 'ftp://neoftp.sci.gsfc.nasa.gov/bluemarble/bmng/world_500m/'

    def __init__(self, month, has_topo, has_bathy ):
        self.m_has_topo = has_topo
        self.m_has_bathy = has_bathy
        self.m_month = month

    def GenerateUrl(self, Quadrant ):
        url = self.s_base_url
        url += 'world.'

        if ( self.m_has_topo):
            url += 'topo.'

        if ( self.m_has_bathy ):
            url += 'bathy.'

        url += '2004'

        url += '%(month)02d' % { 'month': self.m_month}

        url += '.3x21600x21600.'

        url += Quadrant

        url += '.png'

        return url


    def A1(self):
        return self.GenerateUrl('A1')

    def A2(self):
        return self.GenerateUrl('A2')

    def B1(self):
        return self.GenerateUrl('B1')

    def B2(self):
        return self.GenerateUrl('B2')

    def C1(self):
        return self.GenerateUrl('C1')

    def C2(self):
        return self.GenerateUrl('C2')

    def D1(self):
        return self.GenerateUrl('D1')

    def D2(self):
        return self.GenerateUrl('D2')



def HorizontalQuadrantToOrigin( HorizontalQuadrant):
    if ( HorizontalQuadrant == "A" ):
        return -180
    if ( HorizontalQuadrant == "B"):
        return -90
    if ( HorizontalQuadrant == "C"):
        return 0
    if ( HorizontalQuadrant == "D"):
        return 90

def VerticalQuadrantToOrigin( VerticalQuadrant ):
    if ( VerticalQuadrant == "1"):
        return 0
    else:
        return -90


# Calculate the pixels given the lon lat values
def CalculatePixel( lon, lat, HorizontalQuadrant, VerticalQuadrant, height=21600, width=21600):

    # get the origins and shift them to 0-180 for vertical and 0-360 for horizontal
    horizontalOrigin = HorizontalQuadrantToOrigin(HorizontalQuadrant) + 180
    verticalOrigin = VerticalQuadrantToOrigin(VerticalQuadrant) + 90

    targetLon = lon + 180
    targetLat = lat + 90

    # subtract the origin to get where it would be in that tile
    targetLon = targetLon - horizontalOrigin
    targetLat = targetLat - verticalOrigin

    # print "Adjusted Lon/Lat = ( %s, %s )" % (targetLon, targetLat)

    # cross multiply and divide
    x = (21600 * targetLon ) / 90

    # change lat scale from (-90 to 90) to (0 - 180)
    y = 21600 - (21600 * targetLat ) / 90

    # print "Calculated Pixel for ( %s, %s ) == ( %s, %s )" % (lon, lat, x, y)

    x = int(x)
    y = int(y)

    # print "Image Pixel for ( %s, %s ) == ( %s, %s )" % (lon, lat, x, y)

    return (x, y)





def CalculateDegreesForTile( xTile, yTile, zoomLevel ):

    # number of tiles vertical or horizontal, not total for the whole zoom level.

    numberOfTiles = 2.0 ** zoomLevel
    # lon_deg = xTile / n * 360.0 - 180.0
    # lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * yTile / n)))
    # lat_deg = math.degrees(lat_rad)

    minLat = math.degrees( math.atan( math.sinh( math.pi * ( 1 - 2 * (yTile + 1)  / numberOfTiles ))) )
    maxLat = math.degrees( math.atan( math.sinh( math.pi * ( 1 - 2 * yTile  / numberOfTiles ))) )

    # to calculate the degrees, we find where the tile is long the x axis from 0 -> nNumberOfTiles
    # as a percentage. (0.5 from 0 - 256 would be 128)
    # multiply that by 360 to get where it would be on a world between 0 and 360
    # subtract 180 as our degree coordinates are between -180 and 180
    minLon = (xTile / numberOfTiles) * 360.0 - 180.0
    maxLon = (xTile + 1) / numberOfTiles * 360.0 - 180.0

    return (minLat, minLon, maxLat, maxLon)



def LongitudeWithinQuadrant( HorizontalQuadrant, lon ):
    if ( lon >= -180 and lon <= -90 and HorizontalQuadrant == "A"  ):
        return True
    if ( lon >= -90 and lon <= 0 and HorizontalQuadrant == "B"):
        return True
    if ( lon >= 0 and lon <= 90 and HorizontalQuadrant == "C" ):
        return True
    if ( lon >= 90 and lon <= 180 and HorizontalQuadrant == "D" ):
        return True
    return False



def LatitudeWithinQuadrant( VerticalQuadrant, lat ):
    if ( lat <= 90 and lat >= 0 and VerticalQuadrant == "1" ):
        return True
    if ( lat <= 0 and lat >= -90 and VerticalQuadrant == "2" ):
        return True
    return False



def IsWithinTile( HorizontalQuadrant, VerticalQuadrant,  lon, lat ):

    if ( LongitudeWithinQuadrant ( HorizontalQuadrant, lon ) and
         LatitudeWithinQuadrant ( VerticalQuadrant, lat )):
        return True
    else:
        return False





def cutTiles(filePath, destinationDirectory, zoomLevel, HorizontalQuadrant, VerticalQuadrant ):
    if( HorizontalQuadrant != "A" and HorizontalQuadrant != "B" and HorizontalQuadrant != "C" and HorizontalQuadrant != "D"):
        print ("invalid hemisphere")
        return

    if ( VerticalQuadrant != "1" and VerticalQuadrant != "2"):
        print ("invalid horizontal quadrant")
        return

    currentImage = VImage.VImage(filePath)

    # 64 is the number of tiles at 90 degrees
    # for zoomLevel in range (5,10):

    tileCount = 2 ** zoomLevel
    verticalTileCount = tileCount
    horizontalTileCount = tileCount

    for verticalTileIndex in range( 0, verticalTileCount):
        for horizontalTileIndex in range (0, horizontalTileCount ):

            # latitude is vertical and longitude is horizontal... :p
            minLat, minLon, maxLat, maxLon = CalculateDegreesForTile(horizontalTileIndex, verticalTileIndex, zoomLevel )

            if not ( IsWithinTile( HorizontalQuadrant, VerticalQuadrant, minLon, minLat ) and \
                    IsWithinTile(HorizontalQuadrant, VerticalQuadrant, maxLon, maxLat ) ) :
                # print "Tile ( %s, %s ) from ( %s, %s ) to ( %s, %s ) is not within Quadrant ( %s, %s )" % (horizontalTileIndex, verticalTileIndex, minLon, minLat, maxLon, maxLat, HorizontalQuadrant, VerticalQuadrant)
                continue

            print "Calculated Lon, Lat for Tile (%s, %s) = (%s, %s) to (%s, %s)" % (horizontalTileIndex, verticalTileIndex, minLon, minLat, maxLon, maxLat )

            minPixelX, minPixelY = CalculatePixel( minLon, minLat, HorizontalQuadrant, VerticalQuadrant )
            maxPixelX, maxPixelY = CalculatePixel( maxLon, maxLat, HorizontalQuadrant, VerticalQuadrant )

            print "Calculated Pixel Bounds for Tile ( %s, %s ) = ( %s, %s ) to ( %s, %s )" % (horizontalTileIndex, verticalTileIndex, minPixelX, minPixelY, maxPixelX, maxPixelY)

            realTileX = horizontalTileIndex
            realTileY = verticalTileIndex
            if ( HorizontalQuadrant == "A"):
                # do nothing, the coordinates are already in tile A1
                i=0
            elif ( HorizontalQuadrant == "B"):
                realTileX += (horizontalTileCount * 1)
            elif ( HorizontalQuadrant == "C"):
                realTileX += (horizontalTileCount * 2)
            elif ( HorizontalQuadrant == "D"):
                realTileX += (horizontalTileCount * 3)

            if ( VerticalQuadrant == "1"):
                # do nothing, the coordinates are already in tile A1
                i=0
            elif( VerticalQuadrant == "2"):
                realTileY += (verticalTileCount * 1)

            # print "    Extracting Image for tile (%s, %s) from area (%s, %s) - (%s, %s)" % (realTileX, realTileY, minPixelX, minPixelY, maxPixelX, maxPixelY )
            # print "    Extracted Tile Will be: ( %s, %s )" % ( maxPixelX - minPixelX, maxPixelY - minPixelY)


            # extract the sub image
            height =  minPixelY - maxPixelY
            width = maxPixelX - minPixelX

            print "Extracting Image at ( %s, %s ) with dimensions ( %s, %s ) " % (minPixelX, maxPixelY, width, height)

            # use min x and max y as coordinate system is inverted...
            extractedImage = currentImage.extract_area(minPixelX, maxPixelY, width, height )

            print "Extracted Image Size: ( %s, %s )" % ( extractedImage.Xsize(), extractedImage.Ysize() )

            scaleHeight = 256.0 / height
            scaleWidth = 256.0 / width

            print "Scaling Image for tile by (%s, %s)" % (scaleWidth, scaleHeight)

            # scale to web mercator's 256x256
            scaledImage = extractedImage.resize_linear( 256, 256 )

            print "Saving tile as tile ( %s, %s )" % (horizontalTileIndex, verticalTileIndex)

            newDirPath = "./%s/%s/%s" % ( destinationDirectory, zoomLevel, horizontalTileIndex)

            if not os.path.exists(newDirPath):
                os.makedirs(newDirPath)

            newFilePath = "%s/%s.png" % (newDirPath, verticalTileIndex)

            scaledImage.write(newFilePath)

            print ""




def mergeToZoomLevel(tileCacheRootDirectory, sourceZoomLevel, targetZoomLevel ):

    sourceDirectory = tileCacheRootDirectory + "/" + str(sourceZoomLevel)

    if not (os.path.exists(sourceDirectory)):
        print "Source Directory : %s doesn't exist" % ( sourceDirectory )
        return

    if not (int(sourceZoomLevel) > int(targetZoomLevel)):
        print "Target Zoom Level: %s , must be less than Source Zoom Level: %s " % sourceZoomLevel, targetZoomLevel

    sourceTileEdgeCount = 2 ** int(sourceZoomLevel);
    targetTileEdgeCount = 2 ** int(targetZoomLevel)

    # number of photos to merge to get to the lower zoom level
    # distance of 1 = 2 x 2 = 4
    # distance of 2 = 4 x 4 = 16
    # distance of 3 = 8 x 8 = 64
    # distance of n = 2^n
    mergeCountEdge = 2 ** (int(sourceZoomLevel) - int(targetZoomLevel))
    mergeCountTotal = mergeCountEdge * mergeCountEdge

    for targetTileIndexX in range ( 0, targetTileEdgeCount ):
        for targetTileIndexY in range(0, targetTileEdgeCount ):

            print "Creating Image for Tile ( %s, %s, %s )" % (targetZoomLevel, targetTileIndexX, targetTileIndexY)

            sourceStartTileX = mergeCountEdge * targetTileIndexX
            sourceStartTileY = mergeCountEdge * targetTileIndexY

            sourceEndTileX = sourceStartTileX + mergeCountEdge
            sourceEndTileY = sourceStartTileY + mergeCountEdge

            newImage = Image.new("RGB", (mergeCountEdge * 256, mergeCountEdge * 256))

            xCount = 0
            yCount = 0

            for sourceTileIndexX in range ( sourceStartTileX, sourceEndTileX ):
                for sourceTileIndexY in range ( sourceStartTileY, sourceEndTileY ):


                    imagePath = sourceDirectory + "/" + str(sourceTileIndexX) + "/" + str(sourceTileIndexY) + ".png"
                    currentSourceImage = Image.open(imagePath)

                    currentPixelX = xCount * 256
                    currentPixelY = yCount * 256

                    newImage.paste( currentSourceImage, (currentPixelX, currentPixelY) )

                    yCount = yCount + 1
                xCount = xCount + 1
                yCount = 0

            newImage = newImage.resize( (256, 256), Image.BICUBIC )

            targetFileDirectory = tileCacheRootDirectory + "/" + str(targetZoomLevel) + "/" + str(targetTileIndexX)

            if not ( os.path.exists(targetFileDirectory)):
                os.makedirs( targetFileDirectory )

            targetFilePath = "./" + targetFileDirectory + "/" + str(targetTileIndexY) + ".png"

            try :
                # newImage.save( "test.png", "png" )
                newImage.save( targetFilePath, "png" )
            except IOError as err:
                print(str(err))

