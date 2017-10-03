import rhinoscriptsyntax as rs
import rhinoscript.userinterface
import rhinoscript.geometry

__commandname__ = "TEST"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):


	rs.EnableRedraw(False)

	defaultName = ''
	areaObj = rs.GetObject("Select Object:", filter=65536, preselect=True)
	areaName = rs.ObjectName(areaObj)

	if not areaName:
	    defaultName = rs.ObjectLayer(areaObj).split("-")[-1].replace("_", " ")
	    print("default", defaultName)
	    areaName = rs.GetString("Enter name of area to be displayed", defaultName, ["RETAIL", "RESIDENTIAL", "AMENITY", "BOH", "LOBBY"])
	else:
	    areaName = areaName.upper()
	#areaName = areaName.replace(" ", "\n")

	nameOffset = 20 
	nameTextSize = 50
	areaTextSize = 40
	scale = rs.GetReal("Scale for text (.5 for towers)", 1)

	nameOffset = nameOffset*scale
	nameTextSize = nameTextSize*scale
	areaTextSize = areaTextSize*scale

	areaObjExp = rs.ExplodeHatch(areaObj)
	try:
	    area = rs.Area(areaObjExp)
	except:
	    print("Object not a solid hatch")
	    rs.DeleteObject(areaObjExp)
	    

	area = area*(rs.UnitScale(9))**2

	area = int(area)
	area = "{:,} SF".format(area)

	areaCenter = rs.SurfaceAreaCentroid(areaObjExp)[0]
	rs.DeleteObject(areaObjExp)

	areaCenter = rs.PointAdd(areaCenter, (0,((nameOffset+areaTextSize)/-2),0))
	nameCenter = rs.PointAdd(areaCenter, (0,nameOffset+nameTextSize,0))
	print(nameCenter, areaCenter)

	areaText = rs.AddText(area, areaCenter, areaTextSize, justification=2)
	nameText = rs.AddText(areaName, nameCenter, nameTextSize, justification=2)
	textBounds = rs.BoundingBox(areaText)
	textBoundary = rs.AddPolyline(textBounds[0:5])

	nameTextHeight = rs.Distance(rs.BoundingBox(nameText)[2],rs.BoundingBox(nameText)[1])
	print("AreaNameHeight", nameTextHeight) 

	textBorder = rs.OffsetCurve(textBoundary, (0,0,0), 5*scale,style=1)

	rs.DeleteObject(textBoundary)

	rs.ObjectName(nameText, "Name Text")
	rs.ObjectName(areaText, "Area Text")
	rs.ObjectName(textBorder, "Text Border")

	parent = rs.ParentLayer(rs.ObjectLayer(areaObj))

	rs.ObjectLayer(nameText, parent+"::A-ANNO-NOTE")
	rs.ObjectLayer(areaText, parent+"::A-ANNO-NOTE")
	rs.ObjectLayer(textBorder, parent+"::A-ANNO-NOTE")


	areasGroup = rs.AddGroup()
	rs.AddObjectsToGroup([areaText, nameText, textBorder], areasGroup)

	rs.SelectObjects(rs.ObjectsByGroup(areasGroup))

	rs.EnableRedraw(True)
RunCommand(True)