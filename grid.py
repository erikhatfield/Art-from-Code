import bpy
import bmesh
import random

# Remove Cube, because.
original_cube = bpy.context.scene.objects.get("Cube")
if bpy.context.scene.objects.get("Cube"):
    bpy.data.objects['Cube'].select_set(True)
    bpy.ops.object.delete()

#add a plane
bpy.ops.mesh.primitive_plane_add(size=16, enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

#thePlane=bpy.context.active_object

bpy.ops.mesh.subdivide()
bpy.ops.mesh.subdivide(number_cuts=25)

bpy.context.scene.tool_settings.use_proportional_edit = True
bpy.context.scene.tool_settings.use_proportional_connected = True
bpy.context.scene.tool_settings.proportional_edit_falloff = 'RANDOM'



# This example assumes we have a mesh object in edit-mode

# Get the active mesh
obj = bpy.context.edit_object
me = obj.data

# Get a BMesh representation
bm = bmesh.from_edit_mesh(me)

bm.faces.active = None

bpy.ops.mesh.select_all(action='DESELECT')

# Modify the BMesh, can do anything here...
for v in bm.verts:
    ##print(v.co.x, v.co.y, v.co.z)

    if v.co.y > 5 or v.co.y < -5:
        if random.randint(0, 100) > 96:
            v.select = True
            #v.co.z += 1.0



# Show the updates in the viewport
# and recalculate n-gon tessellation.
bmesh.update_edit_mesh(me, True)


#specific range for x
min = .4
max = .5

#generate a random floating point number for X
fx = min + (max-min)*random.random()
fx = fx * -1

#specific range for y
min = -.1
max = .2

#generate a random floating point number for y
fy = min + (max-min)*random.random()

#specific range for z
min = 0.8
max = 1.4
#generate a random floating point number for X
fz = min + (max-min)*random.random()

print(fz)

bpy.ops.transform.translate(value=(fx, fy, fz), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=True, proportional_edit_falloff='RANDOM', proportional_size=1, use_proportional_connected=True, use_proportional_projected=False)







bpy.ops.mesh.select_all(action='DESELECT')

# Modify the BMesh, can do anything here...
for v in bm.verts:
    ##print(v.co.x, v.co.y, v.co.z)

    if v.co.y > 5 or v.co.y < -5:
        if random.randint(0, 100) > 96:
            v.select = True
            #v.co.z += 1.0


#RUN AGAIN... need python function stuff sir
# Show the updates in the viewport
# and recalculate n-gon tessellation.
bmesh.update_edit_mesh(me, True)


#specific range for x
min = -0.4
max = .5

#generate a random floating point number for X
fx = min + (max-min)*random.random()
#fx = fx * -1

#specific range for y
min = -.1
max = .2

#generate a random floating point number for y
fy = min + (max-min)*random.random()

#specific range for z
min = 0.8
max = 1.4
#generate a random floating point number for X
fz = min + (max-min)*random.random()

print(fz)

bpy.ops.transform.translate(value=(fx, fy, fz), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=True, proportional_edit_falloff='RANDOM', proportional_size=1, use_proportional_connected=True, use_proportional_projected=False)
