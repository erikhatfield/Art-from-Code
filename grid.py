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
bpy.context.scene.render.filepath = "./output/grid_" + now.strftime('%m%d%y_%H%M') + "-"
bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
bpy.context.scene.render.ffmpeg.format = 'MPEG4'

######################################

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
camx = int(-1 * (PLANESIZE / 2))
camz = WILDCARD * 0.420
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(camx, 0, camz), rotation=(1.5708, 0, -1.5708), scale=(1, 1, 1))

obj_camera = bpy.data.objects["Camera"]
obj_camera.data.lens = random.randint(12, 70)




# X, Y, and Z location to set
obj_camera.location = (camx, 0.0, camz)
# Set the keyframe with that location, and which frame.
obj_camera.keyframe_insert(data_path="location", frame=1)
#bpy.ops.action.interpolation_type(type='LINEAR')


obj_camera.location = ((buildcount/ 2), 0.0, camz)
# setting it for frame 250
obj_camera.keyframe_insert(data_path="location", frame=250)


# Set keyframe curve to linear
#First save the default type:
##keyInterp = bpy.context.user_preferences.edit.keyframe_new_interpolation_type
#Then change it to what you want:
#bpy.context.user_preferences.edit.keyframe_new_interpolation_type ='LINEAR'
#Then change it back again after you’re done with:
###bpy.context.user_preferences.edit.keyframe_new_interpolation_type = keyInterp

    
##Render the default render (same as F12 only better)
bpy.ops.render.render('INVOKE_DEFAULT', animation=True, write_still=True)