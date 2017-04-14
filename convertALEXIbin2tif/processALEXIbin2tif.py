#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:18:16 2017

@author: mschull
"""
import numpy as np
from osgeo import osr,gdal
import os
import shutil
import argparse

def writeArray2Tiff(data,res,UL,inProjection,outfile,outFormat):

    xres = res[0]
    yres = res[1]

    ysize = data.shape[0]
    xsize = data.shape[1]

    ulx = UL[0] #- (xres / 2.)
    uly = UL[1]# - (yres / 2.)
    driver = gdal.GetDriverByName('GTiff')
    ds = driver.Create(outfile, xsize, ysize, 1, outFormat)
    #ds = driver.Create(outfile, xsize, ysize, 1, gdal.GDT_Int16)
    
    srs = osr.SpatialReference()
    
    if isinstance(inProjection, basestring):        
        srs.ImportFromProj4(inProjection)
    else:
        srs.ImportFromEPSG(inProjection)
        
    ds.SetProjection(srs.ExportToWkt())
    
    gt = [ulx, xres, 0, uly, 0, -yres ]
    ds.SetGeoTransform(gt)
    
    ds.GetRasterBand(1).WriteArray(data)
    #ds = None
    ds.FlushCache()  
    
def convertBin2tif(inFile,inUL,shape,res):
    inProj4 = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
    outFormat = gdal.GDT_Float32
    read_data = np.fromfile(inFile, dtype=np.float32)
    dataset = np.flipud(read_data.reshape([shape[0],shape[1]]))
    outTif = inFile[:-4]+".tif"
    writeArray2Tiff(dataset,res,inUL,inProj4,outTif,outFormat) 
    
ALEXIshape = [3750,3750]
ALEXIres = [0.004,0.004]
#ALEXIfolder = '/Users/mschull/umdGD/data/VIIRS_GLOBAL_PROCESS/tiles/T063/' 
#ALEXIfolder = os.getcwd()   
#files2convert = glob.glob(os.path.join(ALEXIfolder,'FINAL_EDAY*.dat'))
files2convert = []
for dirpath, dirnames, filenames in os.walk("."):
    for filename in [f for f in filenames if (f.startswith("FINAL_EDAY") & f.endswith(".dat"))]:
        files2convert.append(os.path.join(dirpath, filename))

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("remove", type=float, help="remove old files")
    args = parser.parse_args()
    remove = args.remove

    for inFile in files2convert:
        # get UL lat/lon
        tile = int(inFile.split(os.sep)[-1].split('_')[-1][1:4])
        row = tile/24
        col = tile-(row*24)
        ULlat= (75.-(row)*15.)
        ULlon=(-180.+(col-1.)*15.)      
        inUL = [ULlon,ULlat]   
        convertBin2tif(inFile,inUL,ALEXIshape,ALEXIres)
        if remove==1:
            os.remove(inFile)


if __name__ == "__main__":
    main()
