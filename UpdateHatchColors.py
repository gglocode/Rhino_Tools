import rhinoscriptsyntax as rs
import os
import re
from getLayerList import getLayers

def ToList(str):
    return list(map(lambda x: int(x), str[1:-1].split(",")))
def cleanLayerList(layers):
    return list(filter(lambda x: not rs.IsLayerReference(x), layers))
    

file_name = r"\\file-1\cadd\2017\2017032.00\3-Production\Images and Graphics\ColorStandard\colors.csv"
file = open(file_name, 'r')
lines = file.readlines()
file.close()

del lines[0]

layerDict = {}

for line in lines:
    line = line.strip()
    line_data = line.split("|")
    prefix = "A-HATCH-"
    if line_data[0] not in ["BOH", "PARKING", "AMENITY"]:
        layerDict[prefix+line_data[0]] = {"LayerColor" : line_data[2],
                                              "LayerPrintColor" : line_data[2]}
        if line_data[0] == "RESIDENTIAL":
            line_data[0] = "RES"
            
        layerDict[prefix+line_data[0]+"_LOBBY"] = {"LayerColor" : line_data[1],
                                              "LayerPrintColor" : line_data[1]}
        layerDict[prefix+line_data[0]+"_BOH"] = {"LayerColor" : line_data[3],
                                              "LayerPrintColor" : line_data[3]}
    else:
        layerDict[prefix+line_data[0]] = {"LayerColor" : line_data[1],
                                          "LayerPrintColor" : line_data[1]}
                                          
rs.EnableRedraw(False)

layers = cleanLayerList(rs.LayerNames())

#
#print(layers)
#print(layerDict)

for layer in layers:
    for key, val  in layerDict.items():
        if layer+"::"+key in rs.LayerChildren(layer):
            
            rs.LayerColor(layer+"::"+key, rs.coercecolor(ToList(val["LayerColor"])))
            rs.LayerPrintColor(layer+"::"+key, rs.coercecolor(ToList(val["LayerPrintColor"])))



rs.EnableRedraw(True)
