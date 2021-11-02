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
# Remove Plane, to allow for multiple runs
if bpy.context.scene.objects.get("Plane"):
    bpy.data.objects['Plane'].select_set(True)
    bpy.ops.object.delete()
    
######################################
# Set a few render/output influences #
bpy.context.scene.render.resolution_x = 1536
bpy.context.scene.render.resolution_y = 1536
bpy.context.scene.render.fps = 30
bpy.context.scene.render.filepath = "//../output/temp_grid_" + now.strftime('%m%d%y_%H%M')
bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
bpy.context.scene.render.ffmpeg.format = 'MPEG4'

######################################
#########
# WORLD #
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0.02, 0.03, 0.07, 1)
#########
#########################
# EEVEE RENDER SETTINGS #
bpy.context.scene.eevee.taa_render_samples = 64
# Ambient Occlusions
bpy.context.scene.eevee.use_gtao = True
bpy.context.scene.eevee.gtao_distance = 10
# Bloom
bpy.context.scene.eevee.use_bloom = True
# Subsurface Scattering
bpy.context.scene.eevee.sss_jitter_threshold = 0.5
# Screen Space Reflections
bpy.context.scene.eevee.use_ssr = True
bpy.context.scene.eevee.use_ssr_refraction = True
# Volumetrics
bpy.context.scene.eevee.use_volumetric_lights = True
bpy.context.scene.eevee.volumetric_end = 150
bpy.context.scene.eevee.use_volumetric_shadows = True
# Hair
bpy.context.scene.render.hair_type = 'STRIP'
bpy.context.scene.render.hair_subdiv = 1



#########################################################################
# create a few CONSTANTS, for subtle uniqueness at the foundation level #
#
# wildcard should have a 50% chance of multiplier influence
WILDCARD = random.randint(1, 2)
# PLANESIZE applies to size of plane created
PLANESIZE = WILDCARD * 16
#print build parameters
print("Using CONSTANTS: " + "WILDCARD = " + str(WILDCARD) + ", PLANESIZE = " + str(PLANESIZE) )
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
    #thePlane=bpy.context.active_object

    #subdivide the plane
    bpy.ops.mesh.subdivide()
    bpy.ops.mesh.subdivide(number_cuts=numberofcuts)

    #set some scene tweaks
    bpy.context.scene.tool_settings.use_proportional_edit = True
    bpy.context.scene.tool_settings.use_proportional_connected = True
    bpy.context.scene.tool_settings.proportional_edit_falloff = 'RANDOM'

    #print("Build count = " + str(buildcountparameter))
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
        print("Using rangeofy: " + str(rangeofy) )
        
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
        print("outlyer vertices choosen from " + str(100 - outlyerVerts) + "% of eligable range")
        
        # Modify the BMesh, can do anything here...
        for v in bm.verts:
            ##print(v.co.x, v.co.y, v.co.z)
            if v.co.y > rangeofy or v.co.y < -rangeofy:
                if random.randint(0, 100) > outlyerVerts:
                    v.select = True
                    v.co.z += random.random()

        # Show the updates in the viewport
        # and recalculate n-gon tessellation.
        bmesh.update_edit_mesh(me, True)

        #specific range for y
        min = -.05
        max = .3

        #generate a random floating point number for y
        fy = min + (max-min)*random.random()

        #specific range for z
        min = 0.123
        max = 1.234
        #generate a random floating point number for X
        fz = min + (max-min)*random.random()

        #print(fz)

        bpy.ops.transform.translate(value=(0, fy, fz), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=True, proportional_edit_falloff='RANDOM', proportional_size=random.randint(2, 4), use_proportional_connected=True, use_proportional_projected=False)
        # Show the updates in the viewport (and recalculate n-gon tessellation)
        bmesh.update_edit_mesh(me, True)

    #################################################################################
    # END def editModeVertZ():                                                      #
    #################################################################################
    
    # Call the function three times. Because seperate random numbers are created each time which gives it a slightly different outcome everytime 3 fold.
    editModeVertZ()
    editModeVertZ()
    editModeVertZ()

    return buildcountparameter
# END mountainGenerator()                                                                        #
##################################################################################################
##################################################################################################
##################################################################################################
randomrange = random.randint(3, 12)

for x in range(randomrange):
    #update the build count returned from the iteration of the mountainGenerator() function
    buildcount = mountainGenerator(buildcount)



###############
### NEXT UP ###
###############

# disable edit mode
bpy.ops.object.editmode_toggle()

# position default camera on the ground
#camx = int(-1 * (PLANESIZE / WILDCARD))
camx = 0
camz = WILDCARD * 0.420
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(camx, 0, camz), rotation=(1.5708, 0, -1.5708), scale=(1, 1, 1))

obj_camera = bpy.data.objects["Camera"]
obj_camera.data.lens = random.randint(12, 70)




# X, Y, and Z location to set
obj_camera.location = (camx, 0.0, camz)
# Set the keyframe with that location, and which frame.
obj_camera.keyframe_insert(data_path="location", frame=0)




# Select the plane again (plane of mountains)
mountains=bpy.data.objects['Plane']

# Add mirror modifier
mirrorMountains = mountains.modifiers.new("mountainMirror", "MIRROR")
# Move to y axis (beginning camera location)
mountains.location[0]=(buildcount - (PLANESIZE/2) )
print(PLANESIZE)
# Add array modifier
arrayOfMountains = mountains.modifiers.new("mountainArray", "ARRAY")
mountainArrayCount = random.randint(3, 7)
arrayOfMountains.count = mountainArrayCount
# Add wireframe modifier
wireframedMountains = mountains.modifiers.new("mountainArray", "WIREFRAME")
wireframedMountains.use_replace = False
wireframeThickness = 0.0007 + (0.002-0.0007)*random.random()
wireframedMountains.thickness = wireframeThickness
wireframedMountains.material_offset = random.randint(2, 4)


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
randr = 0.0007 + (0.007-0.0007)*random.random()
randg = 0.0007 + (0.007-0.0007)*random.random()
randb = 0.0007 + (0.007-0.0007)*random.random()
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (randr, randg, randb, 1)
randmetalic = ( (random.randint(4, 8)) * 0.111)
mountainBaseMat.node_tree.nodes["Principled BSDF"].inputs[4].default_value = randmetalic


###################
# Add glow material
mountainGlowMat= bpy.data.materials.new(name = "Mountain Glow")
mountains.data.materials.append(mountainGlowMat)

mountainGlowMat.use_nodes = True
nodes = mountainGlowMat.node_tree.nodes

material_output = nodes.get("Material Output")
node_emission = nodes.new(type="ShaderNodeEmission")

randr = 0.1 + (0.9-0.1)*random.random()
randg = 0.1 + (0.9-0.1)*random.random()
randb = 0.1 + (0.9-0.1)*random.random()
node_emission.inputs[0].default_value = (randr, randg, randb, 1) # color
#node_emission.inputs[0].default_value = ( 0.1, 0.5, 0.8, 0.9) # color
randstrength = random.randint(50, 250)
node_emission.inputs[1].default_value = randstrength # strength
#node_emission.inputs[1].default_value = 1.234 # strength

links = mountainGlowMat.node_tree.links
new_link = links.new(node_emission.outputs[0], material_output.inputs[0])




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


bpy.context.scene.render.image_settings.file_format = 'JPEG'
bpy.context.scene.render.image_settings.quality = 80

bpy.ops.render.render('INVOKE_DEFAULT', animation=False, write_still=True)

##Render the default render (same as F12 only better)
#bpy.ops.render.render('INVOKE_DEFAULT', animation=True, write_still=True)