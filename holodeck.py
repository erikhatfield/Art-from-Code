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

#RENDER SAMPLE COUNT
bpy.context.scene.cycles.samples = 32
cyclesRenderSamples=bpy.data.objects['CYCLES_RENDER_SAMPLES']
cyclesRenderSamples.data.body=str(bpy.context.scene.cycles.samples)


#LIGHT PATHS (MAX BOUNCES)
bpy.context.scene.cycles.max_bounces = 8
maxBounces=bpy.data.objects['MAX_BOUNCES']
maxBounces.data.body=str(bpy.context.scene.cycles.max_bounces)

#LIGHT PATHS (diffuse, glossy, transparency, transmission, volume)
bpy.context.scene.cycles.diffuse_bounces = 8
bpy.context.scene.cycles.glossy_bounces = 1
bpy.context.scene.cycles.transparent_max_bounces = 8
bpy.context.scene.cycles.transmission_bounces = 8
bpy.context.scene.cycles.volume_bounces = 8

lightPathsCollective=bpy.data.objects['LIGHT_PATHS_COLLECTIVE']
lightPathsCollective.data.body="      ++      diffuse_bounces:    "+str(bpy.context.scene.cycles.diffuse_bounces)+"\n      ++      glossy_bounces:    "+str(bpy.context.scene.cycles.glossy_bounces)+"\n      ++      transparent_max_bounces:    "+str(bpy.context.scene.cycles.transparent_max_bounces)+"\n      ++      transmission_bounces:    "+str(bpy.context.scene.cycles.transmission_bounces)+"\n      ++      volume_bounces:    "+str(bpy.context.scene.cycles.volume_bounces)

#OTHER RENDER SETTINGS FOR DYNAMIC DISPLAY
otherRenderInfo=bpy.data.objects['OTHER_RENDER_INFO']
#ambient occulusion
bpy.context.scene.world.light_settings.use_ambient_occlusion = False
otherRenderInfo.data.body="ambient_occlusion: "+str(bpy.context.scene.world.light_settings.use_ambient_occlusion)+"\n"
#render tiles
bpy.context.scene.render.tile_x = 96
bpy.context.scene.render.tile_y = 96
otherRenderInfo.data.body+="render.tile_x: "+str(bpy.context.scene.render.tile_x)+"  render.tile_y: "+str(bpy.context.scene.render.tile_y)+"\n"
#caustics_reflective & caustics_refractive
bpy.context.scene.cycles.caustics_reflective = False
bpy.context.scene.cycles.caustics_refractive = True
otherRenderInfo.data.body+="caustics_reflective: "+str(bpy.context.scene.cycles.caustics_reflective)+"\n"
otherRenderInfo.data.body+="caustics_refractive: "+str(bpy.context.scene.cycles.caustics_refractive)+"\n"
#sampling > adaptive sampling
bpy.context.scene.cycles.use_adaptive_sampling = False
otherRenderInfo.data.body+="adaptive_sampling: "+str(bpy.context.scene.cycles.use_adaptive_sampling)+"\n"

#######################################################
#######################################################

##Render the default render (same as F12)
bpy.context.scene.render.filepath = "/Users/magichat/Desktop/HOLODECK_blendrndr/out_" + now.strftime('%m%d%y_%H%M')+".jpg"
bpy.context.scene.render.image_settings.file_format = 'JPEG'
bpy.context.scene.render.image_settings.quality = 80


    
bpy.ops.render.render('INVOKE_DEFAULT', animation=False, write_still=True)
#PRINT OUT OR ECHO IN IMAGE: bpy.context.scene.world.light_settings.use_ambient_occlusion = False

