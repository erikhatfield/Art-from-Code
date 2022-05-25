print("  ______  _______  ______ _______   ")
print(" /      \|       \|      \       \  ")
print("|  ▓▓▓▓▓▓\ ▓▓▓▓▓▓▓\\▓▓▓▓▓▓ ▓▓▓▓▓▓▓\ ")
print("| ▓▓ __\▓▓ ▓▓__| ▓▓ | ▓▓ | ▓▓  | ▓▓ ")
print("| ▓▓|    \ ▓▓    ▓▓ | ▓▓ | ▓▓  | ▓▓ ")
print("| ▓▓ \▓▓▓▓ ▓▓▓▓▓▓▓\ | ▓▓ | ▓▓  | ▓▓ ")
print("| ▓▓__| ▓▓ ▓▓  | ▓▓_| ▓▓_| ▓▓__/ ▓▓ ")
print(" \▓▓    ▓▓ ▓▓  | ▓▓   ▓▓ \ ▓▓    ▓▓ ")
print("  \▓▓▓▓▓▓ \▓▓   \▓▓\▓▓▓▓▓▓\▓▓▓▓▓▓▓  ")
print("                                    ")
print("GRID.PY a blender render art program")
print("\n\n\n")
import bpy
import bmesh
import random
import datetime
import time
import math
import sys
import os
argv = sys.argv #pass in parameters/arguements from the command line
argv = argv[argv.index("--") + 1:]  # get all args after "--"
# argv example command: % blender /the/path/file.blend -P /the/path/of/script.py -- smurf berries
LCD0_MSG = "G R I D \n"
# Record time stamps
now = datetime.datetime.now()
print("NOW-> datetime.now(): " + str(now) + "\n\n");
LCD0_MSG = LCD0_MSG + "\n" + str(now) + "\n"
initial_timestamp = time.time()
LCD0_MSG = LCD0_MSG + "\n" + "initial_timestamp = " + str(initial_timestamp) + "\n"
print("\n"+LCD0_MSG+"\n")
# time stamp used for output graphics file and text file
renderedFilepathTimeStamp = now.strftime('%m%d%y_%H%M')
# implement a render settings file out/in method
renderedSettingsFilepath = "./output/temp_settings_txt/grid_settings_" + renderedFilepathTimeStamp + ".txt"
outTxtFile = open(renderedSettingsFilepath,'w')  #write, read or append the file 'w', 'r' or 'a' respectively
# Set some manual parameters:
minimalModeEnabled = False
# Remove all objects
# ^^^ useful for multiple runs of this script
# except for spaceship (for now)
for o in bpy.context.scene.objects:
    if o.name == 'Spaceship':
        o.select_set(False)
    else:
        o.select_set(True)

# Call the operator only once (best-practice practice?)
bpy.ops.object.delete()

#########
# WORLD #
randr = round(0.0002 + (0.07-0.0002)*random.random(), 4)
randg = round(0.0002 + (0.07-0.0002)*random.random(), 4)
randb = round(0.0002 + (0.07-0.0002)*random.random(), 4)
# Note2self: add background gradient to sky. first step: identify node_tree levels as seen in GUI
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (randr, randg, randb, 1)
# Also add the color to the viewport world
bpy.context.scene.world.color = (randr, randg, randb)
##%%##%%##%%##%%##%%##%%# # # # # # # # # # # # # # # # #
####WRITE##TO##TEXTFILE##worldRGB//world background color
outTxtFile.write("wrgb:" + str(randr) +"," + str(randg) + "," + str(randb) + "\n")
#########
#########################
# EEVEE RENDER SETTINGS #
bpy.context.scene.eevee.taa_render_samples = 64
# Ambient Occlusions
bpy.context.scene.eevee.use_gtao = True
bpy.context.scene.eevee.gtao_distance = 1500
bpy.context.scene.eevee.gtao_quality = 0.86

# Bloom
bpy.context.scene.eevee.use_bloom = True
# Subsurface Scattering
bpy.context.scene.eevee.sss_jitter_threshold = 0.8
# Screen Space Reflections
bpy.context.scene.eevee.use_ssr = True
bpy.context.scene.eevee.use_ssr_refraction = True
# Volumetrics
bpy.context.scene.eevee.use_volumetric_lights = True
bpy.context.scene.eevee.volumetric_end = 1500
bpy.context.scene.eevee.use_volumetric_shadows = True
# Hair
bpy.context.scene.render.hair_type = 'STRAND'
bpy.context.scene.render.hair_subdiv = 2
# Animation timeline
bpy.context.scene.frame_end = 1000

#########################################################################
# create a few CONSTANTS, for subtle uniqueness at the foundation level #
#
# wildcard should have a 50% chance of multiplier influence
WILDCARD = random.randint(1, 2)
# PLANESIZE applies to size of plane created
PLANESIZE = WILDCARD * 48
#print build parameters
print( "Using CONSTANTS: " + "WILDCARD = " + str(WILDCARD) + ", PLANESIZE = " + str(PLANESIZE) )
#########################################################################

##################################################################################################
##################################################################################################
##################################################################################################
# build count variable keeps track of iterations of mountainGenerator function                   #
buildcount = 0
# BEGIN mountainGenerator()                                                                      #
def mountainGenerator(buildcountparameter):
    ############################################################
    # create a few variables, for subtle uniqueness every time #
    wildcard = random.randint(1, 3)
    # number of cuts of the plane's subdivision op
    numberofcuts = int(( PLANESIZE + (PLANESIZE / WILDCARD) ) / wildcard)
    ############################################################

    #print build parameters
    print("Build parameters of mountainGenerator(" + str(buildcountparameter) + ") are " +
    "wildcard: " + str(wildcard) + ", "
    "numberofcuts: " + str(numberofcuts)
    )

    #add a plane and enter edit mode (use build count on the x axis)
    bpy.ops.mesh.primitive_plane_add(size=PLANESIZE, enter_editmode=True, align='WORLD', location=(buildcountparameter, 0, 0), scale=(1, 1, 1))
    bpy.context.selected_objects[0].name = "MountainPlane"

    #subdivide the plane
    bpy.ops.mesh.subdivide()
    bpy.ops.mesh.subdivide(number_cuts=numberofcuts)

    #set some scene tweaks
    bpy.context.scene.tool_settings.use_proportional_edit = True
    bpy.context.scene.tool_settings.use_proportional_connected = True
    bpy.context.scene.tool_settings.proportional_edit_falloff = 'RANDOM'

    #%#print("Build count = " + str(buildcountparameter))
    #increment buildcount by PLANESIZE
    buildcountparameter = buildcountparameter + PLANESIZE

    #################################################################################
    # This function assumes it is called when there is a mesh object in edit-mode   #
    # NOTE2SELF: Python Function Syntax doesn't use brackets- relies on indentation #
    #################################################################################
    def editModeVertZ():
        #######################################################
        # create a rangeofy, for subtle uniqueness every time #
        # range of y is the size (in y) of the effected area on the (y) sides of the plane
        rangeofy = (PLANESIZE / random.randint((PLANESIZE/(WILDCARD*(PLANESIZE/4))), ((PLANESIZE/4)+WILDCARD)))
        # create a different range of y for the R side
        rangeofyR = (PLANESIZE / random.randint((PLANESIZE/(WILDCARD*(PLANESIZE/4))), ((PLANESIZE/4)+WILDCARD)))
        # so, that is, a range of y that is i.e. 16/ divided by an int in the range of 2,4 through 5,6
        #%#print("Using rangeofy: " + str(rangeofy) )

        # Get the active mesh (in edit mode)
        obj = bpy.context.edit_object
        me = obj.data

        # Modify the BMesh for each side of y
        def modifyBMesh(sideBool):
            # Get a BMesh representation
            bm = bmesh.from_edit_mesh(me)
            bm.faces.active = None
            bpy.ops.mesh.select_all(action='DESELECT')

            # Generate a random interger between 93-99
            # Lower numbers represent more vertices selected (93% represents 7% selected)
            outlyerVerts = random.randint(93, 99)
            #%#print("outlyer vertices choosen from " + str(100 - outlyerVerts) + "% of eligable range")
            for v in bm.verts:
                ###print(v.co.x, v.co.y, v.co.z)
                #if v.co.y > rangeofyR or v.co.y < -rangeofy:
                if sideBool == True and v.co.y > rangeofyR:
                    if random.randint(0, 100) > outlyerVerts:
                        v.select = True
                        v.co.z += random.random()
                elif sideBool == False and v.co.y < -rangeofy:
                    if random.randint(0, 100) > outlyerVerts:
                        v.select = True
                        v.co.z += random.random()
                ###    print(v.co.x, v.co.y, v.co.z)

            # Show the updates in the viewport
            # and recalculate n-gon tessellation.
            ###bmesh.update_edit_mesh(me, True)
            bmesh.update_edit_mesh(me, loop_triangles=True)

            #specific range for x
            min = -0.07
            max = 0.07
            #generate a random floating point number for x
            fx = min + (max-min)*random.random()

            #specific range for y
            min = -0.28
            max = 0.28
            #generate a random floating point number for y
            fy = min + (max-min)*random.random()

            #specific range for z
            min = 0.011
            max = 1.667
            #generate a random floating point number for Z
            fz = min + (max-min)*random.random()

            if fz >= 1.234:
                fz = fz*fz

            bpy.ops.transform.translate(value=(fx, fy, fz), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=True, proportional_edit_falloff='RANDOM', proportional_size=random.randint(2, 4), use_proportional_connected=True, use_proportional_projected=False)
            # Show the updates in the viewport (and recalculate n-gon tessellation)
            ###bmesh.update_edit_mesh(me, True) #blender 2.9
            bmesh.update_edit_mesh(me, loop_triangles=True)
        modifyBMesh(True)
        modifyBMesh(False)

    #################################################################################
    # END def editModeVertZ():                                                      #
    #################################################################################

    if minimalModeEnabled == True:
        randomrange = 1
    else:
        # Call the function 2-4 times. Because seperate random numbers are created each time which gives it a slightly different outcome everytime 3 fold.
        randomrange = random.randint(2, 5) #increasing this range can create heavy blend files
        print("editModeVertZ() instances: " + str(randomrange))

    for x in range(randomrange):
        editModeVertZ()

    return buildcountparameter
# END mountainGenerator()                                                                        #
##################################################################################################
##################################################################################################
##################################################################################################
################################################################
def printCharacterLine(numberOf,character):
    for c in range(numberOf):
        print(character, end ="")
    print("")
################################################################
if minimalModeEnabled == True:
    randomrange = 2
else:
    randomrange = random.randint(2, 22) #upper bounds of this range can generate heavy files (1GB) when combined with applied modifiers
    print("mountainGenerator() instances: " + str(randomrange))

for x in range(randomrange):
    #update the build count returned from the iteration of the mountainGenerator() function
    print("")
    printCharacterLine(x, "#^^#")
    print("mountainGenerator instance: " + str(x)+ "/" + str(randomrange-1))
    buildcount = mountainGenerator(buildcount)

#########################################################
# calculate and add base plate before exiting edit mode #
#########################################################
def calcBasePlate():
    #########################################################
    #
    # Get the active mesh (in edit mode)
    obj = bpy.context.edit_object
    me = obj.data

    # Get a BMesh representation
    bm = bmesh.from_edit_mesh(me)
    bm.faces.active = None
    bpy.ops.mesh.select_all(action='DESELECT')

    #initial value 0
    highestX = 0
    highestY = 0
    lowestX = 0
    lowestY = 0

    for v in bm.verts:
        #print("x: " + str(v.co.x) + ", y: " + str(v.co.y) + ", z: "  + str(v.co.z))
        if v.co.z == 0:
            if v.co.x >= highestX:
                highestX = v.co.x
            if v.co.y >= highestY:
                highestY = v.co.y

            if v.co.x <= lowestX:
                lowestX = v.co.x
            if v.co.y <= lowestY:
                lowestY = v.co.y

    basePlateZindex=-12
    bm.verts.new((highestX, highestY, basePlateZindex))
    bm.verts.new((highestX, lowestY, basePlateZindex))
    bm.verts.new((lowestX, highestY, basePlateZindex))
    bm.verts.new((lowestX, lowestY, basePlateZindex))

    for v in bm.verts:
        #print("x: " + str(v.co.x) + ", y: " + str(v.co.y) + ", z: "  + str(v.co.z))
        if v.co.z == basePlateZindex:
            v.select = True

        if v.co.z == 0:
            if v.co.x == highestX or v.co.x == lowestX:
                v.select = True
            if v.co.y == highestY or v.co.y == lowestY:
                v.select = True

    # with select verts (corners) create a convex hull; a base plate
    bpy.ops.mesh.convex_hull()

    bmesh.update_edit_mesh(me, loop_triangles=True)
    #########################################################

#########################################################
# END def calcBasePlate():                              #
#########################################################

calcBasePlate()

# disable edit mode
bpy.ops.object.editmode_toggle()

########################
# ADD MODIFIERS to mountain plane

# Select the plane again (plane of mountains)
mountains=bpy.data.objects['MountainPlane']

# Add mirror modifier
mirrorMountains = mountains.modifiers.new("mountainMirror", "MIRROR")
# Move to y axis (beginning camera location)
mountains.location[0]=(buildcount - (PLANESIZE/2) )

# Add array modifier
arrayOfMountains = mountains.modifiers.new("mountainArray", "ARRAY")
mountainArrayCount = random.randint(5, 6)
arrayOfMountains.count = mountainArrayCount
# Add wireframe modifier
wireframedMountains = mountains.modifiers.new("wireframeArray", "WIREFRAME")
wireframedMountains.use_replace = False
wireframeThickness = round((0.002 + (0.022-0.002)*random.random()), 7)#limit to 7 digit decimal prescesion 
wireframedMountains.thickness = wireframeThickness
materialOffsetInt = random.randint(0, 7) #0 creates a moonlit scene :)
wireframedMountains.material_offset = materialOffsetInt
##%%##%%##%%##%%##%%##%%# # # # # # # # # # # # # # # # # # # #
####WRITE##TO##TEXTFILE##wireframe thickness and material offset
outTxtFile.write("wThick:" + str(wireframeThickness) + "\n")
outTxtFile.write("mOffset:" + str(materialOffsetInt) + "\n")

# Apply wireframeArray modifier here for a different material application
#bpy.ops.object.modifier_apply(modifier="mountainMirror")
#bpy.ops.object.modifier_apply(modifier="mountainArray")

# Add materials to mountains
###################
# Add base material

mountainBaseMat = bpy.data.materials.new(name="Mountain Base")

# Assign it to object
if mountains.data.materials:
    # assign to 1st material slot
    mountains.data.materials[0] = mountainBaseMat
else:
    # no slots
    mountains.data.materials.append(mountainBaseMat)

mountainBaseMat.use_nodes = True
####################################################
#generate three random r,g,b floating points
randr = 0.000007 + (0.09-0.000007)*random.random()
randg = 0.000007 + (0.09-0.000007)*random.random()
randb = 0.000007 + (0.09-0.000007)*random.random()
####################################################
# randomize a bunch of values within principled BSDF
#mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (randr, randg, randb, 1)
#Use random floats on subsurface color, the base color recieves input from magic texture
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[1].default_value = 0.007 + (1.0-0.007)*random.random() #subsurface
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[3].default_value = (randr, randg, randb, 1)
bpy.context.object.active_material.diffuse_color = (randr, randg, randb, 1) # set material zcolor of viewport + workbench => same as subsurface
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[4].default_value = ((random.randint(5, 8)) * 0.111)
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[5].default_value = ((random.randint(2, 8)) * 0.111) #specular
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[6].default_value = ((random.randint(1, 9)) * 0.111) #specular tint
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.007 + (1.0-0.007)*random.random() #roughness
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[8].default_value = ((random.randint(0, 5)) * 0.111) #anisotropic
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[9].default_value = ((random.randint(2, 9)) * 0.111) #anisotropic rotation
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[10].default_value = ((random.randint(0, 5)) * 0.111) #sheen
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[11].default_value = ((random.randint(4, 7)) * 0.111) #sheen tint
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[12].default_value = ((random.randint(0, 8)) * 0.111) #clearcoat
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[13].default_value = 0.007 + (0.07-0.007)*random.random()  #cleatcoat roughness
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[14].default_value = 1.007 + (1.777-1.007)*random.random() #IOR
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[15].default_value = 0.0007 + (0.07-0.0007)*random.random() #transmission
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[16].default_value = 0.007 + (1.0-0.007)*random.random() #transmission roughness
####################################################

# add magic texture as base color to principled BSDF base color input
# ref: https://docs.blender.org/api/current/bpy.types.html
######################################################################################
magicTextureNode = mountainBaseMat.node_tree.nodes.new(type="ShaderNodeTexMagic")
magicTextureNode.turbulence_depth = random.randint(0, 3)
magicTextureNode.inputs[1].default_value = ( 0.007 + (0.420-0.007)*random.random() ) #scale
magicTextureNode.inputs[2].default_value = ( 0.1 + (11.11-0.1)*random.random() ) #distortion
######################################################################################
#magic texture color output TO base color input
mountainBaseMat.node_tree.links.new(magicTextureNode.outputs[0], mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[0])
#magic texture fac output TO subsurface radius input
mountainBaseMat.node_tree.links.new(magicTextureNode.outputs[1], mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[2])
#magic texture color output TO emission color input (17)
mountainBaseMat.node_tree.links.new(magicTextureNode.outputs[0], mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[17])
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0.00004 + (0.0005-0.00004)*random.random() #emission strength

#magic texture Fac output TO normal (20) or clearcoat normal (21) or tangent (22)
mountainBaseMat.node_tree.links.new(magicTextureNode.outputs[1], mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[20])
mountainBaseMat.node_tree.links.new(magicTextureNode.outputs[1], mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[21])
mountainBaseMat.node_tree.links.new(magicTextureNode.outputs[1], mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[22])

###################

###################
# Add glow material
mountainGlowMat= bpy.data.materials.new(name = "Mountain Glow")
mountains.data.materials.append(mountainGlowMat)

mountainGlowMat.use_nodes = True
nodes = mountainGlowMat.node_tree.nodes

material_output = nodes.get("Material Output")
node_emission = nodes.new(type="ShaderNodeEmission")

randr = 0.09 + (0.9-0.09)*random.random()
randg = 0.09 + (0.9-0.09)*random.random()
randb = 0.09 + (0.9-0.09)*random.random()
if WILDCARD == 2:
    randg = 1.0 - randr
node_emission.inputs[0].default_value = (randr, randg, randb, 1) # color
#node_emission.inputs[0].default_value = ( 0.1, 0.5, 0.8, 0.9) # color
randstrength = 0.5 + (27.777-0.5)*random.random()
node_emission.inputs[1].default_value = randstrength # strength

links = mountainGlowMat.node_tree.links
new_link = links.new(node_emission.outputs[0], material_output.inputs[0])
###################
# Apply wireframeArray modifier earlier for a different material look
####bpy.ops.object.modifier_apply(modifier="mountainMirror")
####bpy.ops.object.modifier_apply(modifier="mountainArray")
#bpy.ops.object.modifier_apply(modifier="wireframeArray")
###################
######################################
#scale Y and Z of entire mountainPlane
#calc an zScaleFac that is only near the ground in outlying cases
outlyerVerts = random.randint(86, 99)
if random.randint(0, 100) > outlyerVerts:
    zScaleFac = (( 0.1 + (0.67-0.1)*random.random() ) * WILDCARD)
    bpy.context.object.scale[2] =  max(zScaleFac, 1)
else:
    zScaleFac = min(4,((( 0.67 + (3.67-0.67)*random.random() ) + (1/WILDCARD) + WILDCARD)))
    bpy.context.object.scale[2] = zScaleFac
#calc an yScaleFac is large and effects z scale in outlying cases
outlyerVerts = random.randint(95, 99)
if random.randint(0, 100) > outlyerVerts:
    yScaleFac = 32
    zScaleFac = zScaleFac*3.22
    bpy.context.object.scale[2] = zScaleFac
else:
    yScaleFac = (random.randint(1, 7) + (WILDCARD*WILDCARD))
bpy.context.object.scale[1] = yScaleFac
######################################
###############################################################
#    ______   ______  __       __ ________ _______   ______
#   /      \ /      \|  \     /  \        \       \ /      \
#  |  ▓▓▓▓▓▓\  ▓▓▓▓▓▓\ ▓▓\   /  ▓▓ ▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓\  ▓▓▓▓▓▓\
#  | ▓▓   \▓▓ ▓▓__| ▓▓ ▓▓▓\ /  ▓▓▓ ▓▓__   | ▓▓__| ▓▓ ▓▓__| ▓▓
#  | ▓▓     | ▓▓    ▓▓ ▓▓▓▓\  ▓▓▓▓ ▓▓  \  | ▓▓    ▓▓ ▓▓    ▓▓
#  | ▓▓   __| ▓▓▓▓▓▓▓▓ ▓▓\▓▓ ▓▓ ▓▓ ▓▓▓▓▓  | ▓▓▓▓▓▓▓\ ▓▓▓▓▓▓▓▓
#  | ▓▓__/  \ ▓▓  | ▓▓ ▓▓ \▓▓▓| ▓▓ ▓▓_____| ▓▓  | ▓▓ ▓▓  | ▓▓
#   \▓▓    ▓▓ ▓▓  | ▓▓ ▓▓  \▓ | ▓▓ ▓▓     \ ▓▓  | ▓▓ ▓▓  | ▓▓
#    \▓▓▓▓▓▓ \▓▓   \▓▓\▓▓      \▓▓\▓▓▓▓▓▓▓▓\▓▓   \▓▓\▓▓   \▓▓
#
# CAMERA TWEEKS
########## ASCII ART GEN: texteditor.com/multiline-text-art/

# position default camera on the ground
#camx = int(-1 * (PLANESIZE / WILDCARD))
camx = 0
#camz is altitude of ship
camz = zScaleFac
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(camx, 0, camz), rotation=(1.5708, 0, -1.5708), scale=(1, 1, 1))
bpy.ops.object.transforms_to_deltas(mode='ALL')

obj_camera = bpy.data.objects["Camera"]
#lensangle = random.randint(18, 135)
lensangle = random.randint(32, 85) #35 min zoom for spaceship cockpit for now
obj_camera.data.lens = lensangle
bpy.context.object.data.clip_start = 0.2 # default is .01
obj_camera.data.clip_end = 15000

# if exists- attach spaceship to camera
if bpy.context.scene.objects.get("Spaceship"):
    bpy.data.objects['Spaceship'].parent = bpy.data.objects["Camera"]
    bpy.data.objects['Spaceship'].track_axis = 'POS_X'
    bpy.data.objects['Spaceship'].up_axis = 'Z'
    bpy.data.objects['Spaceship'].rotation_euler[0] = -1.5708
    bpy.data.objects['Spaceship'].rotation_euler[1] = 1.5708
    bpy.data.objects['Spaceship'].rotation_euler[2] = 0

    spaceshipPOVX = ((0.15 + (0.25-0.15)*random.random()) *-1)
    spaceshipPOVZ = 0.009 + (0.02-0.009)*random.random()
    bpy.data.objects['Spaceship'].location[1] = spaceshipPOVZ # y is actually z...
    bpy.data.objects['Spaceship'].location[2] = spaceshipPOVX # z is actually x...

# need solution for linear interpolation curve so the camera y movement is steady
#bpy.ops.action.interpolation_type(type='LINEAR')
# Create F-Curve
action = bpy.data.actions.new("cube_linear")
action.fcurves.new("location", action_group="location")
action.fcurves[0].keyframe_points.insert(0, 0)
action.fcurves[0].keyframe_points.insert(1000, 1000)
action.fcurves[0].extrapolation = 'LINEAR'

obj_camera.animation_data_create()
obj_camera.animation_data.action=action

# X, Y, and Z location to set
obj_camera.location = (camx, 0.0, camz)
# Set the keyframe with that location, and which frame.
obj_camera.keyframe_insert(data_path="location", frame=0)

#camx_end = ( ((buildcount/2) * mountainArrayCount) + (PLANESIZE*WILDCARD))
camx_end = (2 * ((buildcount*2) - PLANESIZE) )
obj_camera.location = (camx_end, 0.0, camz)
# setting it for frame 250
obj_camera.keyframe_insert(data_path="location", frame=1000)

#Finish with camera obj (DESELECT)
#obj_camera.select_all(action='DESELECT')
bpy.ops.object.select_all(action='DESELECT')
###############################################################

#######################################################################################

#######################################################################################
#Example on how to select a certain object in the scene and make it the active object #
#ob = bpy.context.scene.objects["MountainPlane"]         # Get the object
#bpy.ops.object.select_all(action='DESELECT')            # Deselect all objects
#bpy.context.view_layer.objects.active = ob              # Make the MountainPlane the active object
#ob.select_set(True)
#######################################################################################
mountains = bpy.context.scene.objects.get("MountainPlane")      # Get the object
bpy.context.view_layer.objects.active = mountains               # Make it the the active object
#######################################################################################

#######################################################
# bigBangTheory and birthOfAStar()                    #
# create a sphere, assign relation to parent (camera) #
#######################################################
def bigBangTheory():
    # MATERIAL
    star_mat = bpy.data.materials.new(name = "starGlow")
    #bpy.context.object.data.materials.append(star_mat)

    star_mat.use_nodes = True
    #nodes = w00t_mat.node_tree.nodes
    material_output = star_mat.node_tree.nodes.get("Material Output")
    node_emission = star_mat.node_tree.nodes.new(type="ShaderNodeEmission")

    node_emission.inputs[0].default_value = ( 0.8, 0.8, 0.8, 1.0) # color
    node_emission.inputs[1].default_value = ( 12.345 + (123.45-12.345)*random.random() ) # strength
    #node_emission.inputs[1].default_value = 45.1 # strength
    #links = w00t_mat.node_tree.links
    #new_link = links.new(node_emission.outputs[0], material_output.inputs[0])
    star_mat.node_tree.links.new(node_emission.outputs[0], material_output.inputs[0])

    def birthOfAStar(star_material_arg):
        # add star with random size floating point (near zero)
        bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1.0, 1.0, 1.0))
        this_star=bpy.context.active_object

        # name it Star
        #bpy.context.selected_objects[0].name = "Star"
        bpy.context.object.name = "Star"

        #make the star's parent relation that of the camera
        #this_star.parent = obj_camera
        bpy.context.object.parent = bpy.data.objects["Camera"]
        bpy.context.object.track_axis = 'POS_X'
        bpy.context.object.up_axis = 'Z'

        # for some reason, the X is the -Z
        bpy.context.object.location[2]= ( (random.randint(512, 1024)) * -2 ) #distance from camera
        # and Z is Y
        bpy.context.object.location[1]= random.randint(4, (480 - lensangle*2)) #vertical
        # and Y is X
        starrangey = 0.1 + (1280.0-0.1)*random.random() #horizontal

        if random.randint(1, 2) == 1:
            starrangey = starrangey * -1 # both sides of center line

        bpy.context.object.location[0]= starrangey

        specialBoundaries = random.randint(9989, 9999)
        if random.randint(0, 10000) > specialBoundaries:
            starscale = 10.1 + (45.1-10.1)*random.random()
        else:
            starscale = 0.004 + (0.5-0.004)*random.random()

        bpy.context.object.scale[0]= starscale
        bpy.context.object.scale[1]= starscale
        bpy.context.object.scale[2]= starscale

        # APPLY MATERIAL
        bpy.context.object.data.materials.append(star_material_arg)

    if minimalModeEnabled == True:
        numberofstars = 1
    else:
        numberofstars = random.randint(200, 1200)

    for x in range(numberofstars):
        birthOfAStar(star_mat)

    # Join all stars into one object
    for o in bpy.context.scene.objects:
        if o.name.startswith("Star"):
            o.select_set(True)
        else:
            o.select_set(False)
    bpy.ops.object.join()

bigBangTheory()

def cockpitLCD():
    #add a plane and enter edit mode (use build count on the x axis)
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

    bpy.context.selected_objects[0].name = "LCD_CUBE"
    bpy.context.object.parent = bpy.data.objects["Spaceship"]

    # scale object to fit center console
    bpy.context.object.scale[0]= (0.05     * 0.1)
    bpy.context.object.scale[1]= 0.1
    bpy.context.object.scale[2]= 0.1
    # tilt display
    bpy.context.object.rotation_euler[1] = 00.32

    bpy.context.scene.tool_settings.use_proportional_edit = False
    #bpy.context.object.data.use_mirror_y = True
    bpy.context.object.location[0] = 0.67
    #bpy.context.object.location[1] = 0
    bpy.context.object.location[2] = -0.125

    bpy.ops.object.editmode_toggle()

    # MATERIAL
    lcd_mat = bpy.data.materials.new(name = "LCD1")
    bpy.context.object.data.materials.append(lcd_mat)

    lcd_mat.use_nodes = True
    nodes = lcd_mat.node_tree.nodes

    material_output = nodes.get("Material Output")
    node_emission = nodes.new(type="ShaderNodeEmission")

    node_emission.inputs[0].default_value = ( 0.0, 0.004, 0.027, 1.0) # color
    node_emission.inputs[1].default_value = 2 # strength

    # update viewport display (aka workbench render)
    lcd_mat.diffuse_color = (0, 0, 0.259, 1)
    lcd_mat.roughness = 0

    links = lcd_mat.node_tree.links
    new_link = links.new(node_emission.outputs[0], material_output.inputs[0])
    #add text block
    bpy.ops.object.text_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.context.selected_objects[0].name = "LCD_TEXT"
    bpy.context.object.parent = bpy.data.objects["LCD_CUBE"]

    bpy.context.object.rotation_euler[0] = 1.5708
    #bpy.context.object.rotation_euler[1] = 0.32
    bpy.context.object.rotation_euler[2] = -1.5708

    #place text flat with screen surface
    bpy.context.object.location[0] = -0.51  #X coord
    # move to left side of LCD
    bpy.context.object.location[1] = 0.42  #Y coord
    # move to top of screen a little bit
    bpy.context.object.location[2] = 0.08 #Z coord

    bpy.context.object.scale[0] = 0.039
    bpy.context.object.scale[1] = 0.039
    bpy.context.object.scale[2] = 0.039

    # LCDTEXT TEXT TEXT MATERIAL
    lcd_mat = bpy.data.materials.new(name = "LCD1TEXT")
    bpy.context.object.data.materials.append(lcd_mat)

    lcd_mat.use_nodes = True
    nodes = lcd_mat.node_tree.nodes

    material_output = nodes.get("Material Output")
    node_emission = nodes.new(type="ShaderNodeEmission")

    node_emission.inputs[0].default_value = ( 0.0, 0.9, 1.0, 1.0) # color
    node_emission.inputs[1].default_value = 22 # strength

    # update viewport display (aka workbench render)
    lcd_mat.diffuse_color = (0, 0.667, 0.667, 1)
    lcd_mat.metallic = 1 #SAME AS #bpy.context.object.active_material.metallic = 1
    lcd_mat.roughness = 0.667

    links = lcd_mat.node_tree.links
    new_link = links.new(node_emission.outputs[0], material_output.inputs[0])

    second_timestamp = time.time()
    run_time = int(round(second_timestamp - initial_timestamp))
    LCD_MESSAGE_OUT = LCD0_MSG + "\nrun_time (before rendering time) is " + str(run_time) + " seconds."

    t4dw=bpy.data.objects['LCD_TEXT']
    t4dw.data.body = LCD_MESSAGE_OUT

cockpitLCD()

##########################################################

###############################
####CLOSE##SETTINGS##TEXTFILE##
outTxtFile.close()#############
###############################

##########################################################
#   _______  ________ __    __ _______  ________ _______
#  |       \|        \  \  |  \       \|        \       \
#  | ▓▓▓▓▓▓▓\ ▓▓▓▓▓▓▓▓ ▓▓\ | ▓▓ ▓▓▓▓▓▓▓\ ▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓\
#  | ▓▓__| ▓▓ ▓▓__   | ▓▓▓\| ▓▓ ▓▓  | ▓▓ ▓▓__   | ▓▓__| ▓▓
#  | ▓▓    ▓▓ ▓▓  \  | ▓▓▓▓\ ▓▓ ▓▓  | ▓▓ ▓▓  \  | ▓▓    ▓▓
#  | ▓▓▓▓▓▓▓\ ▓▓▓▓▓  | ▓▓\▓▓ ▓▓ ▓▓  | ▓▓ ▓▓▓▓▓  | ▓▓▓▓▓▓▓\
#  | ▓▓  | ▓▓ ▓▓_____| ▓▓ \▓▓▓▓ ▓▓__/ ▓▓ ▓▓_____| ▓▓  | ▓▓
#  | ▓▓  | ▓▓ ▓▓     \ ▓▓  \▓▓▓ ▓▓    ▓▓ ▓▓     \ ▓▓  | ▓▓
#   \▓▓   \▓▓\▓▓▓▓▓▓▓▓\▓▓   \▓▓\▓▓▓▓▓▓▓ \▓▓▓▓▓▓▓▓\▓▓   \▓▓
#
# Set a few render/output influences #
###bpy.context.scene.render.resolution_x = 1920
###bpy.context.scene.render.resolution_y = 1080
## for mbp16 retina display: 3584x2240, 4096x2560@144
##bpy.context.scene.render.resolution_x = 3584
##bpy.context.scene.render.resolution_y = 2240
bpy.context.scene.render.resolution_x = 4096
bpy.context.scene.render.resolution_y = 2560

bpy.context.scene.render.fps = 30
renderedFilepath = "//../output/temp_grid_" + renderedFilepathTimeStamp + "-out"
bpy.context.scene.render.filepath = renderedFilepath

# if animation, render mp4
isANIM = False

if isANIM == True:
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
    ##Render the default render (same as fan-F12 only better)
    bpy.ops.render.render('INVOKE_DEFAULT', animation=True, write_still=True)
else:
    bpy.context.scene.render.image_settings.file_format = 'JPEG'
    bpy.context.scene.render.image_settings.quality = 86
    ##Render the default render (same as F12 only better)
    bpy.ops.render.render('INVOKE_DEFAULT', animation=False, write_still=True)

##########################################################
##########################################################
# print out run time of this py
second_timestamp = time.time()
run_time = int(round(second_timestamp - initial_timestamp))
print('COMPLETED. run_time (before rendering time) is ' + str(run_time) + " seconds.")

# CONSIDER performing garbage collection
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
####bpy.ops.wm.open_mainfile(filepath=bpy.data.filepath)

try:
    argv[0]
    if argv[0] == "automated":
        print('AUTOMATED_MODE active: exiting in 259 seconds.')
        # Need dynamic delay here, in some rare cases 259 is not enough delay to finish render
        time.sleep(259)
        #sys.exit(0)
        bpy.ops.wm.quit_blender()
except IndexError:
    print('no parameters entered [[exeception handled]]')
# FIN
