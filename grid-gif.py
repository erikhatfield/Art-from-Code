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

# Animation timeline
scene_frame_start = 25
scene_frame_end = 1000
scene_frame_step = 25
bpy.context.scene.frame_start = scene_frame_start
bpy.context.scene.frame_end = scene_frame_end
bpy.context.scene.frame_step = scene_frame_step

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
bpy.context.scene.render.resolution_x = 720
bpy.context.scene.render.resolution_y = 480

bpy.context.scene.render.filepath = "//../output/temp_gif/"

bpy.context.scene.render.image_settings.file_format = 'JPEG'
bpy.context.scene.render.image_settings.quality = 86
bpy.ops.render.render('INVOKE_DEFAULT', animation=True, write_still=True)

##########################################################
##########################################################

frame_calc_delay = (scene_frame_end / scene_frame_step) * 59
print('exiting in '+str(frame_calc_delay)+' seconds.')
time.sleep(int(frame_calc_delay))
bpy.ops.wm.quit_blender()
