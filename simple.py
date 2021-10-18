import bpy

# Remove Cube, because.
original_cube = bpy.context.scene.objects.get("Cube")
if bpy.context.scene.objects.get("Cube"):
    bpy.data.objects['Cube'].select_set(True)
    bpy.ops.object.delete()

bpy.ops.mesh.primitive_cube_add(size=3, enter_editmode=False, align='WORLD', location=(0, 2, 0), scale=(2, 3, 1))
w00t=bpy.context.active_object

# Move object down 1 on the z axis 
w00t.location[2]=-1

################################
# TAB triggers auto-completion #
# works better in console      #
################################

# MODIFIERS
# MOD BASIC (subsurface)
mod_w00t = w00t.modifiers.new("w00tMOD", "SUBSURF")
mod_w00t.levels = 2

# MOD displace
mod_displace = w00t.modifiers.new("jaggedCrystal", "DISPLACE")

magic_texture = bpy.data.textures.new("magicTexture", "MAGIC")
magic_texture.noise_depth = 2
magic_texture.turbulence = 2.3

mod_displace.texture = magic_texture

#bpy.context.object.modifiers["jaggedCrystal"].strength = 3.9
mod_displace.strength = 22.22
mod_displace.mid_level = 0.667

# MATERIAL
w00t_mat = bpy.data.materials.new(name = "w00tMat")
w00t.data.materials.append(w00t_mat)

w00t_mat.use_nodes = True
nodes = w00t_mat.node_tree.nodes

material_output = nodes.get("Material Output")
node_emission = nodes.new(type="ShaderNodeEmission")

node_emission.inputs[0].default_value = ( 0.1, 0.5, 0.8, 0.9) # color
node_emission.inputs[1].default_value = 12.34 # strength

links = w00t_mat.node_tree.links
new_link = links.new(node_emission.outputs[0], material_output.inputs[0])


# layout view and render settings
#bpy.context.space_data.shading.type = 'RENDERED'
bpy.context.scene.eevee.use_bloom = True



# Camera
# Active Render Camera
#obj_camera = bpy.context.scene.camera
# Object named "Camera"
obj_camera = bpy.data.objects["Camera"]

#bpy.ops.outliner.item_activate(extend=False, deselect_all=True)
#bpy.context.space_data.lock_camera = True

obj_camera.location[0] = 45.0
obj_camera.location[1] = -42.0
obj_camera.location[2] = 30.0
obj_camera.rotation_euler[0] = 1.1
obj_camera.rotation_euler[1] = 0
obj_camera.rotation_euler[2] = 0.8
