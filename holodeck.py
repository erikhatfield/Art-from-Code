import bpy
import datetime
utcnow = datetime.datetime.utcnow()
now = datetime.datetime.now()


t4dw=bpy.data.objects['Text4DayofWeek']
t4dw.data.body = now.strftime('%A')
t4d=bpy.data.objects['Text4Date']
t4d.data.body = now.strftime('%B %d, %Y')


t4t=bpy.data.objects['Text4Time']
t4t.data.body = now.strftime('%H:%M')

#calculate time difference from utcnow (only works for western timezones lol)
##if utc-month > local-month OR utc-day is > local-day
##then add 24 to utc-hour
##
utcHourCalc = utcnow.strftime('%H')
##time-dif = utc-hour - local-hour
if (utcnow.strftime('%m') > now.strftime('%m')) or (utcnow.strftime('%d') > now.strftime('%d')):
  ##if utc-month > local-month OR utc-day is > local-day
  ##then add 24 hour to utc calc
  str(int(utcHourCalc) + int(24))

#int(str(x) + str(y))
###elif localtime greater... for eastern timezones... (not implementing yet)
###else:
##else what

timeZDifference = int(utcHourCalc) - int(now.strftime('%H'))
timeZDifferenceStr = "[-"+ str(timeZDifference) + "00]"
t4dtz=bpy.data.objects['Text4Date+Time+Zone']
t4dtz.data.body = now.strftime('%m%d%y @%H:%M ') + timeZDifferenceStr




##"""
##
##BEGIN RENDER SETTINGS OUTPUTS (CYCLES)
##
##"""

#this will only work with the CYCLES rendering engine selected - if cycles
#output settings
useTheseSettings = True
if (useTheseSettings):
    #RENDER SAMPLE COUNT
    bpy.context.scene.cycles.samples = 128

    #LIGHT PATHS (MAX BOUNCES)
    bpy.context.scene.cycles.max_bounces = 32

    #LIGHT PATHS (diffuse, glossy, transparency, transmission, volume)
    bpy.context.scene.cycles.diffuse_bounces = 30
    bpy.context.scene.cycles.glossy_bounces = 30
    bpy.context.scene.cycles.transparent_max_bounces = 31
    bpy.context.scene.cycles.transmission_bounces = 32
    bpy.context.scene.cycles.volume_bounces = 32

    #OTHER RENDER SETTINGS FOR DYNAMIC DISPLAY
    #ambient occulusion
    bpy.context.scene.world.light_settings.use_ambient_occlusion = False
    #render tiles
    bpy.context.scene.render.tile_x = 96
    bpy.context.scene.render.tile_y = 96
    #caustics_reflective & caustics_refractive
    bpy.context.scene.cycles.caustics_reflective = True
    bpy.context.scene.cycles.caustics_refractive = True
    #sampling > adaptive sampling
    bpy.context.scene.cycles.use_adaptive_sampling = False


#######################################################
#######################################################
cyclesRenderSamples=bpy.data.objects['CYCLES_RENDER_SAMPLES']
cyclesRenderSamples.data.body=str(bpy.context.scene.cycles.samples)
maxBounces=bpy.data.objects['MAX_BOUNCES']
maxBounces.data.body=str(bpy.context.scene.cycles.max_bounces)
lightPathsCollective=bpy.data.objects['LIGHT_PATHS_COLLECTIVE']
lightPathsCollective.data.body="      ++      diffuse_bounces:    "+str(bpy.context.scene.cycles.diffuse_bounces)+"\n      ++      glossy_bounces:    "+str(bpy.context.scene.cycles.glossy_bounces)+"\n      ++      transparent_max_bounces:    "+str(bpy.context.scene.cycles.transparent_max_bounces)+"\n      ++      transmission_bounces:    "+str(bpy.context.scene.cycles.transmission_bounces)+"\n      ++      volume_bounces:    "+str(bpy.context.scene.cycles.volume_bounces)
otherRenderInfo=bpy.data.objects['OTHER_RENDER_INFO']
otherRenderInfo.data.body="ambient_occlusion: "+str(bpy.context.scene.world.light_settings.use_ambient_occlusion)+"\n"
otherRenderInfo.data.body+="render.tile_x: "+str(bpy.context.scene.render.tile_x)+"  render.tile_y: "+str(bpy.context.scene.render.tile_y)+"\n"
otherRenderInfo.data.body+="render.tile_x: "+str(bpy.context.scene.render.tile_x)+"  render.tile_y: "+str(bpy.context.scene.render.tile_y)+"\n"
otherRenderInfo.data.body+="caustics_reflective: "+str(bpy.context.scene.cycles.caustics_reflective)+"\n"
otherRenderInfo.data.body+="caustics_refractive: "+str(bpy.context.scene.cycles.caustics_refractive)+"\n"
otherRenderInfo.data.body+="adaptive_sampling: "+str(bpy.context.scene.cycles.use_adaptive_sampling)+"\n"
#######################################################
#######################################################

#output settings
isAnim = False
if (isAnim):
    #anim settings
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080

    #bpy.context.scene.render.filepath = "Desktop/outs-lost-found/holodeck_anim_" + now.strftime('%m%d%y-%H%M')+".mp4"
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'

    ##Render the default render (same as F12 only better)
    bpy.ops.render.render('INVOKE_DEFAULT', animation=True, write_still=True)
else:
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    #bpy.context.scene.render.resolution_x = 3840
    #bpy.context.scene.render.resolution_y = 2160

    #bpy.context.scene.render.filepath = "Desktop/outs-lost-found/holodeck_" + now.strftime('%m%d%y-%H%M')+".jpg"
    ###JPG
    ###bpy.context.scene.render.filepath = "//holodeck-outs/holodeck_" + now.strftime('%m%d%y-%H%M')+".jpg"
    ###bpy.context.scene.render.image_settings.file_format = 'JPEG'
    ###bpy.context.scene.render.image_settings.quality = 86
    ##PNG
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = "//holodeck-outs/holodeck_" + now.strftime('%m%d%y-%H%M')+".png"
    
    ##Render the default render (same as F12 only better)
    bpy.ops.render.render('INVOKE_DEFAULT', animation=False, write_still=True)

#stairs 3d model
#seats 3d model
#half circle of stairs and seats 3d model

##py for generating extrusion to holo core (from bottom view of 3d object)
