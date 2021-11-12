import bpy
import bmesh
import random
import datetime
# Record time stamp
now = datetime.datetime.now()

# Remove Cube, because.
if bpy.context.scene.objects.get("Cube"):
    bpy.data.objects['Cube'].select_set(True)
    bpy.ops.object.delete()
# Remove Camera, will recreate.
if bpy.context.scene.objects.get("Camera"):
    bpy.data.objects['Camera'].select_set(True)
    bpy.ops.object.delete()
# Remove MountainPlane, to allow for multiple runs
if bpy.context.scene.objects.get("MountainPlane"):
    bpy.data.objects['MountainPlane'].select_set(True)
    bpy.ops.object.delete()
# Remove Default Light
if bpy.context.scene.objects.get("Light"):
    bpy.data.objects['Light'].select_set(True)
    bpy.ops.object.delete()

#########
# WORLD #
randr = 0.0007 + (0.04-0.0007)*random.random()
randg = 0.0007 + (0.04-0.0007)*random.random()
randb = 0.0007 + (0.04-0.0007)*random.random()
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (randr, randg, randb, 1)
#########
#########################
# EEVEE RENDER SETTINGS #
bpy.context.scene.eevee.taa_render_samples = 64
# Ambient Occlusions
bpy.context.scene.eevee.use_gtao = True
bpy.context.scene.eevee.gtao_distance = 50
# Bloom
bpy.context.scene.eevee.use_bloom = True
# Subsurface Scattering
bpy.context.scene.eevee.sss_jitter_threshold = 0.8
# Screen Space Reflections
bpy.context.scene.eevee.use_ssr = True
bpy.context.scene.eevee.use_ssr_refraction = True
# Volumetrics
bpy.context.scene.eevee.use_volumetric_lights = True
bpy.context.scene.eevee.volumetric_end = 150
bpy.context.scene.eevee.use_volumetric_shadows = True
# Hair
bpy.context.scene.render.hair_type = 'STRAND'
bpy.context.scene.render.hair_subdiv = 1



#########################################################################
# create a few CONSTANTS, for subtle uniqueness at the foundation level #
#
# wildcard should have a 50% chance of multiplier influence
WILDCARD = random.randint(1, 2)
# PLANESIZE applies to size of plane created
PLANESIZE = WILDCARD * 16
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
    numberofcuts = (( PLANESIZE + (PLANESIZE / WILDCARD) ) / wildcard)
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
        rangeofy = (PLANESIZE / random.randint((PLANESIZE/(WILDCARD*4)), ((PLANESIZE/4)+WILDCARD)))
        # so, that is, a range of y that is i.e. 16/ divided by a int in the range of 2,4 through 5,6
        #%#print("Using rangeofy: " + str(rangeofy) )
        
        # Get the active mesh (in edit mode)
        obj = bpy.context.edit_object
        me = obj.data

        # Get a BMesh representation
        bm = bmesh.from_edit_mesh(me)
        bm.faces.active = None
        bpy.ops.mesh.select_all(action='DESELECT')

        # Generate a random interger between 93-99
        # Lower numbers represent more vertices selected (93% represents 7% selected) 
        outlyerVerts = random.randint(93, 99)
        #%#print("outlyer vertices choosen from " + str(100 - outlyerVerts) + "% of eligable range")
        
        # Modify the BMesh, can do anything here...
        for v in bm.verts:
            ##print(v.co.x, v.co.y, v.co.z)
            if v.co.y > rangeofy or v.co.y < -rangeofy:
                if random.randint(0, 100) > outlyerVerts:
                    v.select = True
                    v.co.z += random.random()
            
            ###if v.co.x == 0:
            ###    print(v.co.x, v.co.y, v.co.z)

        # Show the updates in the viewport
        # and recalculate n-gon tessellation.
        bmesh.update_edit_mesh(me, True)

        #specific range for x
        min = -0.01
        max = 0.01
        #generate a random floating point number for x
        fx = min + (max-min)*random.random()
        
        #specific range for y
        min = -0.28
        max = 0.28
        #generate a random floating point number for y
        fy = min + (max-min)*random.random()

        #specific range for z
        min = 0.111
        max = 1.111
        #generate a random floating point number for X
        fz = min + (max-min)*random.random()

        #print(fz)

        bpy.ops.transform.translate(value=(fx, fy, fz), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=True, proportional_edit_falloff='RANDOM', proportional_size=random.randint(2, 4), use_proportional_connected=True, use_proportional_projected=False)
        # Show the updates in the viewport (and recalculate n-gon tessellation)
        bmesh.update_edit_mesh(me, True)

    #################################################################################
    # END def editModeVertZ():                                                      #
    #################################################################################
    
    # Call the function 2-4 times. Because seperate random numbers are created each time which gives it a slightly different outcome everytime 3 fold.
    randomrange = random.randint(2, 4)
    for x in range(randomrange):
        editModeVertZ()

    return buildcountparameter
# END mountainGenerator()                                                                        #
##################################################################################################
##################################################################################################
##################################################################################################
randomrange = random.randint(4, 20)

for x in range(randomrange):
    #update the build count returned from the iteration of the mountainGenerator() function
    buildcount = mountainGenerator(buildcount)



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
mountainArrayCount = random.randint(3, 7)
arrayOfMountains.count = mountainArrayCount
# Add wireframe modifier
wireframedMountains = mountains.modifiers.new("wireframeArray", "WIREFRAME")
wireframedMountains.use_replace = False
wireframeThickness = 0.0009 + (0.02-0.0009)*random.random()
wireframedMountains.thickness = wireframeThickness
wireframedMountains.material_offset = random.randint(0, 7) #0 creates a moonlit scene :)

# Apply wireframeArray modifier here for a different material application
bpy.ops.object.modifier_apply(modifier="mountainMirror")
bpy.ops.object.modifier_apply(modifier="mountainArray")
#bpy.ops.object.modifier_apply(modifier="wireframeArray")



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
#generate three random r,g,b values near 0
randr = 0.0007 + (0.07-0.0007)*random.random()
randg = 0.0007 + (0.07-0.0007)*random.random()
randb = 0.0007 + (0.07-0.0007)*random.random()
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (randr, randg, randb, 1)
randmetalic = ( (random.randint(5, 8)) * 0.111)
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[4].default_value = randmetalic
####################################################
# randomize a bunch of values within principled BSDF
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[5].default_value = ((random.randint(2, 8)) * 0.111) #specular
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[6].default_value = ((random.randint(1, 9)) * 0.111) #specular tint
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.007 + (1.0-0.007)*random.random() #roughness
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[8].default_value = ((random.randint(0, 5)) * 0.111) #anisotropic
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[9].default_value = ((random.randint(0, 9)) * 0.111) #anisotropic rotation
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
#magic texture color output TO emission color input (17)
mountainBaseMat.node_tree.links.new(magicTextureNode.outputs[0], mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[17])
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0.00004 + (0.0003-0.00004)*random.random() #emission strength

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
node_emission.inputs[0].default_value = (randr, randg, randb, 1) # color
#node_emission.inputs[0].default_value = ( 0.1, 0.5, 0.8, 0.9) # color
randstrength = random.randint(4, 108)
node_emission.inputs[1].default_value = randstrength # strength

links = mountainGlowMat.node_tree.links
new_link = links.new(node_emission.outputs[0], material_output.inputs[0])
###################
# Apply wireframeArray modifier earlier for a different material look
#bpy.ops.object.modifier_apply(modifier="mountainMirror")
#bpy.ops.object.modifier_apply(modifier="mountainArray")
bpy.ops.object.modifier_apply(modifier="wireframeArray")

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
camz = WILDCARD * 0.420
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(camx, 0, camz), rotation=(1.5708, 0, -1.5708), scale=(1, 1, 1))

obj_camera = bpy.data.objects["Camera"]
obj_camera.data.lens = random.randint(18, 135)

# X, Y, and Z location to set
obj_camera.location = (camx, 0.0, camz)
# Set the keyframe with that location, and which frame.
obj_camera.keyframe_insert(data_path="location", frame=0)


# need solution for linear interpolation curve so the camera y movement is steady
#bpy.ops.action.interpolation_type(type='LINEAR')

#camx_end = ( ((buildcount/2) * mountainArrayCount) + (PLANESIZE*WILDCARD))
camx_end = (2 * ((buildcount*2) - PLANESIZE) )
obj_camera.location = (camx_end, 0.0, camz)
# setting it for frame 250
obj_camera.keyframe_insert(data_path="location", frame=250)

# Set keyframe curve to linear
#First save the default type:
##keyInterp = bpy.context.user_preferences.edit.keyframe_new_interpolation_type
#Then change it to what you want:
#bpy.context.user_preferences.edit.keyframe_new_interpolation_type ='LINEAR'
#Then change it back again after you’re done with:
###bpy.context.user_preferences.edit.keyframe_new_interpolation_type = keyInterp

#Finish with camera obj (DESELECT)
#obj_camera.select_all(action='DESELECT')
bpy.ops.object.select_all(action='DESELECT')
###############################################################





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
bpy.context.scene.render.resolution_x = 1600
bpy.context.scene.render.resolution_y = 1200
#bpy.context.scene.render.resolution_x = 400
#bpy.context.scene.render.resolution_y = 300

bpy.context.scene.render.fps = 30
bpy.context.scene.render.filepath = "//../output/temp_grid_" + now.strftime('%m%d%y_%H%M') + "-out"

# if isANIM logic needed for easy switch between image and animation (mp4)
# for now these are controlled at the end of the script - near the f12 command
#bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
#bpy.context.scene.render.ffmpeg.format = 'MPEG4'                                          
                                                       
bpy.context.scene.render.image_settings.file_format = 'JPEG'
bpy.context.scene.render.image_settings.quality = 80
##Render the default render (same as F12 only better)
bpy.ops.render.render('INVOKE_DEFAULT', animation=False, write_still=True)


#bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
#bpy.context.scene.render.ffmpeg.format = 'MPEG4'
##Render the default render (same as fan-F12 only better)
#bpy.ops.render.render('INVOKE_DEFAULT', animation=True, write_still=True)

##########################################################
##########################################################

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
bpy.ops.object.editmode_toggle()

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

    # Modify the BMesh, can do anything here...
    for v in bm.verts:
        #print(v.co)
        if v.co.x == 0:
            print(v.co)
            v.select = True

    # Show the updates in the viewport
    # and recalculate n-gon tessellation.
    bmesh.update_edit_mesh(me, True)
    #########################################################

#########################################################
# END def calcBasePlate():                              #
#########################################################

#calcBasePlate()


# disable edit mode
bpy.ops.object.editmode_toggle()

#######################################################################################

#######################################################################################



###########################IDEADROP:
##################the ability to save settings. when u really like the artwork produced
#################and therefore, the ability to load settings too
###################or maybe just the recording of settings integrated into the artwork?