import bpy
import bmesh
import random

# Remove Cube, because.
original_cube = bpy.context.scene.objects.get("Cube")
if bpy.context.scene.objects.get("Cube"):
    bpy.data.objects['Cube'].select_set(True)
    bpy.ops.object.delete()

############################################################
# create a few variables, for subtle uniqueness every time #
#
# wildcard should have a 50% chance of multiplier influence
wildcard = random.randint(1, 2)
# planesize applies to size of plane created
planesize = wildcard * 16
# number of cuts of the plane's subdivision op
numberofcuts = planesize + (planesize / 2)
# range of y is the size (in y) of the effected area on the (y) sides of the plane
rangeofy = (planesize / random.randint((planesize/4), ((planesize/4)+wildcard)))
############################################################

#add a plane and enter edit mode
bpy.ops.mesh.primitive_plane_add(size=planesize, enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
#thePlane=bpy.context.active_object

#subdivide the plane
bpy.ops.mesh.subdivide()
bpy.ops.mesh.subdivide(number_cuts=numberofcuts)

#set some scene tweaks
bpy.context.scene.tool_settings.use_proportional_edit = True
bpy.context.scene.tool_settings.use_proportional_connected = True
bpy.context.scene.tool_settings.proportional_edit_falloff = 'RANDOM'


#################################################################################
# This function assumes it is called when there is a mesh object in edit-mode   #
# NOTE2SELF: Python Function Syntax doesn't use brackets- relies on indentation #
#################################################################################
def editModeVertZ():
    # Get the active mesh (in edit mode)
    obj = bpy.context.edit_object
    me = obj.data

    # Get a BMesh representation
    bm = bmesh.from_edit_mesh(me)
    bm.faces.active = None
    bpy.ops.mesh.select_all(action='DESELECT')

    # Modify the BMesh, can do anything here...
    for v in bm.verts:
        ##print(v.co.x, v.co.y, v.co.z)
        if v.co.y > rangeofy or v.co.y < -rangeofy:
            if random.randint(0, 100) > 97:
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

#################################################################################
# END def editModeVertZ():                                                      #
#################################################################################

# Call the function three times. Because seperate random numbers are created each time which gives it a slightly different outcome everytime 3 fold.
editModeVertZ()
editModeVertZ()
editModeVertZ()
