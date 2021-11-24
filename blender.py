# A Blender Python blog entry about Blender and Python
import bpy
import mathutils
import math

# using python to operate Blender has several key objectives
# 0 # document what I learn without having to document anything
# 1 # evaluate operating system security from an all-resources-used prospective
# 2 # reenforce OOP principles and practices
# 3 # create art 

######################################################
######################################################

# instructions for use
# 0 # navigate to your project directory with your terminal command line:
# % # cd /path/to/my/art-from-code-git-rep/or-something/
# 1 # open a fresh blender with console and exec the blender.py program
# % # blender -P blender.py

######################################################
######################################################
# Remove everything to start:
def sceneClean():
    for o in bpy.context.scene.objects:
        if o.name == 'Unicorn':
            o.select_set(False)
        else:
            o.select_set(True)
    # Call the operator only once (best-practice practice?)
    bpy.ops.object.delete()
sceneClean()
######################################################
######################################################

# Add a camera and angle it twds the -X axis 
# [[ 1.5708 == 90˚ ]]

def createCamera1():
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(10, 0, 1), rotation=(1.5708, 0, 1.5708), scale=(1, 1, 1))

def createCamera2():
    scn = bpy.context.scene
    # create the camera
    camster = bpy.data.cameras.new("CamsterData")
    camster.lens = 28
    # apply it to an object and add it the scn you just caused ;P
    obj_camera = bpy.data.objects.new("Camster", camster)
    obj_camera.location = (10, 0, 1)
    obj_camera.rotation_euler = (1.5708, 0, 1.5708)
    scn.collection.objects.link(obj_camera)

createCamera2()

######################################################
######################################################

# define a class for LCDs (Liquid Crystal Display)
class LiquidCrystalDisplay:
    count = 0
    def __init__(self): # constructor method
        LiquidCrystalDisplay.count += 1
        print('LiquidCrystalDisplay Class Constructor invoked. Instance count = ' + str(LiquidCrystalDisplay.count))
        # create plane mesh for display
        bpy.ops.mesh.primitive_plane_add()
        # Name it
        self.name = "LCD" + str(LiquidCrystalDisplay.count)
        bpy.context.active_object.name = self.name
        # create reference to the obj
        self.lcdPlane = bpy.data.objects["LCD" + str(LiquidCrystalDisplay.count)]
        # rotate object to face X axis, scale z for 4/3 ratio
        self.lcdPlane.rotation_euler[1] = 1.5708
        self.lcdPlane.scale = [0.75,1.0,0.0]
        # apply all transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        # apply (and create if none) default LCD material
        #ob = bpy.context.active_object
        # Get material
        mat = bpy.data.materials.get("defaultBackLightLCD")
        if mat is None:
            # create default back light material
            mat = bpy.data.materials.new(name="defaultBackLightLCD")
            mat.use_nodes = True
            mat.use_backface_culling = True
            matColor = (0.0, 0.001, 0.007, 1.0)
            mat.node_tree.nodes.get("Principled BSDF").inputs[0].default_value = matColor # base color
            mat.node_tree.nodes.get("Principled BSDF").inputs[7].default_value = 0 # roughness
            mat.node_tree.nodes.get("Principled BSDF").inputs[17].default_value = matColor # emission color
            mat.node_tree.nodes.get("Principled BSDF").inputs[18].default_value = 4.0 # emission strength
            # set viewport display settings
            mat.diffuse_color = matColor
            mat.metallic = 1
            mat.roughness = 0
        # Assign it to self
        if bpy.context.active_object.data.materials:
            # assign to 1st material slot
            bpy.context.active_object.data.materials[0] = mat
        else:
            # no slots
            bpy.context.active_object.data.materials.append(mat)

# create some instances of class LiquidCrystalDisplay
lcd1 = LiquidCrystalDisplay()
lcd2 = LiquidCrystalDisplay()

