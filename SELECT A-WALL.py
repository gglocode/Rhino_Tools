import rhinoscriptsyntax as rs
import re

def main():
    rs.EnableRedraw(enable=False)
    
    walls = []
    parentFolder = rs.CurrentLayer()
    if re.search("::", parentFolder):
        parentFolder = parentFolder.rsplit("::", 1)[0]
    try:
        walls = rs.ObjectsByLayer(parentFolder + "::A-WALL")
    except ValueError:
        print("No Wall Sublayers in this Layer")
    try:
        walls.extend(rs.ObjectsByLayer(parentFolder + "::A-AREA-BOUNDARY"))
    except ValueError:
        pass
    
    if not walls:
        print("No walls on this floor.")
        return None
    
    curves = []
    
    for wall in walls:
        if rs.IsCurve(wall):
            curves.append(wall)
    rs.SelectObjects(curves)
    
    rs.EnableRedraw(enable=True)
    
    
if __name__=="__main__":
    main()