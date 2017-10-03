import rhinoscriptsyntax as rs
import re
import sys
import getLayerList

def HEXtoRGB(h):
    return(tuple(int(h[i:i+2], 16) for i in (0, 2 ,4)))

colorDict = {
             "AMENITY" : (255, 213, 212),
             "BOH" : HEXtoRGB('616161'),
             "OUTDRAMEN" : (150,200,100),
             "CORE" : (183,207,225),
             "CORRIDOR" : (200,200,200),
             "LIVEWORK" : (158,222,255),
             "RES_LOBBY" : (248, 230, 211),
             "HOTEL" : (220,165,120),
             "OFFICE_LOBBY" : HEXtoRGB('bf93bd'),
             "PARKING" : (180,180,180),
             "RESIDENTIAL" : (212, 155, 106),
             "RETAIL" : (241, 172, 150),
             "RETAIL_LOBBY" :(242, 152, 121),
             "RETAIL_BOH" :(216, 184, 173),
             "RES_AMENITY" : (244, 224, 220),
             "ROOFDECK" : (134, 201, 138),
             "GREENSPACE" : (134, 201, 138)
             
             }
print(rs.coercecolor)

def changeColors(childLayers):
    print(childLayers)
    for childLayer in childLayers: 
            for name, color in colorDict.items():
                color = rs.coercecolor(color)
                if re.search('HATCH-'+name+'$', childLayer):
                    print(childLayer)
                    rs.LayerPrintColor(childLayer,color)
                    rs.LayerColor(childLayer, color)
                    layer_c = rs.LayerColor(childLayer)
                    layer_m = rs.LayerMaterialIndex(childLayer)
                    if layer_m == -1:
                        layer_m = rs.AddMaterialToLayer(childLayer)
                    rs.MaterialColor(layer_m, layer_c)

def main():
    rs.EnableRedraw(enable=False)
    allLayers = rs.LayerNames()
    showList = sorted(getLayerList.getLayers(exclude=[".3dm", "Make2D"]))
    showList.append("Select All")
    boxList = [(x,False) for x in showList]
    
    selectedLayer = rs.CheckListBox(boxList, message="Layer To Activate")
    
    
    if selectedLayer == "Select All":
        layers = sorted(list(set(topList)))
    elif selectedLayer:
        layers = [L[0] for L in selectedLayer if L[1]==True]
    else:
        return(None)
    print(layers)
    if isinstance(layers, str):        
        changeColors(rs.LayerChildren(layers))
    else:
        for layer in layers:
            changeColors(rs.LayerChildren(layer))
    rs.EnableRedraw(enable=True)


if __name__=="__main__":
    main()