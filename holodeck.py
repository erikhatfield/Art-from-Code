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

new_line = "\n"
testboxtextbox_text=bpy.data.objects['TestBoxTextBox']
testboxtextbox_text.data.body = new_line + "" + new_line + ">>> help(string) # on Python 3" + new_line + "...." + new_line + "DATA" + new_line + "    ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'" + new_line + "    ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'" + new_line + "    ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'" + new_line + "    digits = '0123456789'" + new_line + "    hexdigits = '0123456789abcdefABCDEF'" + new_line + "    octdigits = '01234567'" + new_line + "    printable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'" + new_line + "    punctuation = '!#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'" + new_line + "    whitespace = ' \t\n\r\x0b\x0c'"


## ANIMATION? perhaps program still image first then animation...
isAnim = False
##"""
##
##BEGIN RENDER SETTINGS OUTPUTS (CYCLES)
##
##"""

#this will only work with the CYCLES rendering engine selected - if cycles

#######################################################
def setRenderSettings(isAnim):
    cycleFactor=1
    if (isAnim):
        cycleFactor=2

    bpy.context.scene.cycles.samples = 96 / cycleFactor

    bpy.context.scene.cycles.max_bounces = 24 / cycleFactor #16
    bpy.context.scene.cycles.diffuse_bounces = 12 / cycleFactor #8
    bpy.context.scene.cycles.glossy_bounces = 12 / cycleFactor #8
    bpy.context.scene.cycles.transparent_max_bounces = 18 / cycleFactor #12
    bpy.context.scene.cycles.transmission_bounces = 24 / cycleFactor #16
    bpy.context.scene.cycles.volume_bounces = 24 / cycleFactor #16

    bpy.context.scene.world.light_settings.use_ambient_occlusion = False
    bpy.context.scene.cycles.caustics_reflective = False
    bpy.context.scene.cycles.caustics_refractive = True
    bpy.context.scene.cycles.use_adaptive_sampling = False

    bpy.context.scene.cycles.sample_clamp_indirect = 0 #default is 1
    bpy.context.scene.cycles.light_sampling_threshold = 0 #default is 0.01

    ##blender 3.0 no longer has tile x,y's
    ##bpy.context.scene.render.tile_x = 512
    ##bpy.context.scene.render.tile_y = 512



#still image vs animation output settings

if (isAnim):
    #anim settings
    setRenderSettings(True)

    bpy.context.scene.render.resolution_x = 1280
    bpy.context.scene.render.resolution_y = 1280

    bpy.context.scene.render.filepath = "//../holodeck-outs/holodeck-anim_" + now.strftime('%m%d%y_%H%M')+".mp4"
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
else:
    #Regular Still Image
    setRenderSettings(False)
    #bpy.context.scene.render.resolution_x = 1920
    #bpy.context.scene.render.resolution_y = 1080

    bpy.context.scene.render.resolution_x = 2560
    bpy.context.scene.render.resolution_y = 2560

    bpy.context.scene.render.filepath = "//../holodeck-outs/holodeck___" + now.strftime('%m%d%y-%H%M')+".jpg"
    bpy.context.scene.render.image_settings.file_format = 'JPEG'
    bpy.context.scene.render.image_settings.quality = 88


#RENDER SAMPLE COUNT
cyclesRenderSamples=bpy.data.objects['CYCLES_RENDER_SAMPLES']
cyclesRenderSamples.data.body=str(bpy.context.scene.cycles.samples)


#LIGHT PATHS (MAX BOUNCES)
maxBounces=bpy.data.objects['MAX_BOUNCES']
maxBounces.data.body=str(bpy.context.scene.cycles.max_bounces)

#LIGHT PATHS (diffuse, glossy, transparency, transmission, volume)

lightPathsCollective=bpy.data.objects['LIGHT_PATHS_COLLECTIVE']
lightPathsCollective.data.body="      ++      diffuse_bounces:    "+str(bpy.context.scene.cycles.diffuse_bounces)+"\n      ++      glossy_bounces:    "+str(bpy.context.scene.cycles.glossy_bounces)+"\n      ++      transparent_max_bounces:    "+str(bpy.context.scene.cycles.transparent_max_bounces)+"\n      ++      transmission_bounces:    "+str(bpy.context.scene.cycles.transmission_bounces)+"\n      ++      volume_bounces:    "+str(bpy.context.scene.cycles.volume_bounces)

#OTHER RENDER SETTINGS FOR DYNAMIC DISPLAY
otherRenderInfo=bpy.data.objects['OTHER_RENDER_INFO']
#ambient occulusion
otherRenderInfo.data.body="ambient_occlusion: "+str(bpy.context.scene.world.light_settings.use_ambient_occlusion)+"\n"
##render tiles ## blender 3.0 no longer has tiles lke this
##otherRenderInfo.data.body+="render.tile_x: "+str(bpy.context.scene.render.tile_x)+"  render.tile_y: "+str(bpy.context.scene.render.tile_y)+"\n"
#caustics_reflective & caustics_refractive
otherRenderInfo.data.body+="caustics_reflective: "+str(bpy.context.scene.cycles.caustics_reflective)+"\n"
otherRenderInfo.data.body+="caustics_refractive: "+str(bpy.context.scene.cycles.caustics_refractive)+"\n"
#sampling > adaptive sampling
otherRenderInfo.data.body+="adaptive_sampling: "+str(bpy.context.scene.cycles.use_adaptive_sampling)+"\n"

#######################################################

if (isAnim):
    #anim settings
    ##Render the default render (same as F12 only better)
    bpy.ops.render.render('INVOKE_DEFAULT', animation=True, write_still=True)
else:
    #Regular Still Image
    ##Render the default render (same as F12 only better)
    bpy.ops.render.render('INVOKE_DEFAULT', animation=False, write_still=True)
