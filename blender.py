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
        # create collection of class instances if it doesnt exist
        if bpy.context.scene.collection.children.get("LCD_collective"):
            self.collective = bpy.context.scene.collection.children.get("LCD_collective")
        else:
            # create new collection for LCD instance
            self.collective = bpy.data.collections.new("LCD_collective")
            # Add collection to scene collection
            bpy.context.scene.collection.children.link(self.collective)
        # create plane mesh for display
        bpy.ops.mesh.primitive_plane_add()
        # Name it
        self.name = "LCD" + str(LiquidCrystalDisplay.count)
        bpy.context.active_object.name = self.name
        # create reference to the obj
        self.backLitPlane = bpy.data.objects["LCD" + str(LiquidCrystalDisplay.count)]
        # save obj to collection
        # Loop through all collections self.backLitPlane is linked to
        for allcoll in self.backLitPlane.users_collection:
            # Unlink the object
            allcoll.objects.unlink(self.backLitPlane)
        # and link to self.collective collection
        self.collective.objects.link(self.backLitPlane)
        ###
        # rotate object to face X axis, scale z for 4/3 ratio
        self.backLitPlane.rotation_euler[1] = 1.5708
        self.backLitPlane.scale = [0.75,1.0,0.0]
        # apply all transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        # apply (and create if none) default LCD material
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
            mat.metallic = 0.667
            mat.roughness = 0
        # Assign it to self
        if self.backLitPlane.data.materials:
            # assign to 1st material slot
            self.backLitPlane.data.materials[0] = mat
        else:
            # no slots
            self.backLitPlane.data.materials.append(mat)
        # add text to LCD screen
        font_curve = bpy.data.curves.new(type="FONT", name="FontCurve"+str(LiquidCrystalDisplay.count))
        font_curve.body = "LCD instance " + str(LiquidCrystalDisplay.count) + " \n "
        ### ^^^ use 'instancevarname.textObj.data.body = "w00000"' as reference to body/main text input
        self.textObj = bpy.data.objects.new(name="mainTextLCD"+str(LiquidCrystalDisplay.count), object_data=font_curve)
        self.collective.objects.link(self.textObj)
        # add text parent as backLitPlane
        self.textObj.parent = self.backLitPlane
        ###
        self.textObj.scale = [0.1,0.1,0.1]
        # move slightly on x axis to put on top of backlight
        self.textObj.location = [0.001,0,0]
        # apply rotation transforms
        #######self.textObj.transform_apply(location=False, rotation=False, scale=True)
        # rotate text for to match it's parent/backLitPlane
        self.textObj.rotation_euler[0] = 1.5708
        self.textObj.rotation_euler[2] = 1.5708
        # apply (and create if none) default TEXT material
        mat = bpy.data.materials.get("defaultTextLCD")
        if mat is None:
            # create default back light material
            mat = bpy.data.materials.new(name="defaultTextLCD")
            mat.use_nodes = True
            mat.use_backface_culling = True
            matColor = (0.5, 1, 1, 1)
            mat.node_tree.nodes.get("Principled BSDF").inputs[0].default_value = matColor # base color
            mat.node_tree.nodes.get("Principled BSDF").inputs[7].default_value = 0 # roughness
            mat.node_tree.nodes.get("Principled BSDF").inputs[17].default_value = matColor # emission color
            mat.node_tree.nodes.get("Principled BSDF").inputs[18].default_value = 4.0 # emission strength
            # set viewport display settings
            mat.diffuse_color = matColor
            mat.metallic = 0
            mat.roughness = 0
        # Assign it to self
        if self.textObj.data.materials:
            # assign to 1st material slot
            self.textObj.data.materials[0] = mat
        else:
            # no slots
            self.textObj.data.materials.append(mat)

# create some instances of class LiquidCrystalDisplay
lcd1 = LiquidCrystalDisplay()
lcd2 = LiquidCrystalDisplay()

lcd2.textObj.data.body = str(lcd2.textObj.data.body) + "w00000\n"