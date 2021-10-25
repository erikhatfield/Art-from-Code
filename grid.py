import bpy
import bmesh

# Remove Cube, because.
original_cube = bpy.context.scene.objects.get("Cube")
if bpy.context.scene.objects.get("Cube"):
    bpy.data.objects['Cube'].select_set(True)
    bpy.ops.object.delete()

#add a plane
bpy.ops.mesh.primitive_plane_add(size=16, enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

thePlane=bpy.context.active_object

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

# Modify the BMesh, can do anything here...
for v in bm.verts:
    v.co.x += 1.0
    ##### select a few verts how tho


# Show the updates in the viewport
# and recalculate n-gon tessellation.
bmesh.update_edit_mesh(me, True)


bpy.ops.transform.translate(value=(0, 0, 2.77777), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=True, proportional_edit_falloff='RANDOM', proportional_size=1, use_proportional_connected=True, use_proportional_projected=False)
