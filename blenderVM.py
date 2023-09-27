import dearpygui.dearpygui as dpg
import os
from tinydb import TinyDB, Query

link_bridge = r"https://noorllpori.github.io/bvmlinkbridge.github.io/"

# APPDATA 
env_appdata = ""
for key, value in os.environ.items():
    if key == 'APPDATA':
        env_appdata = value
bl_funcpath = env_appdata+"\Blender Foundation\Blender"

data = TinyDB('data.json')
vers = data.table('vers')
setting = data.table('setting')
vcmd = data.table('vcmd')

Data = Query()

dpg.create_context()

def _log(sender, app_data, user_data):
    print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")

def _changeCmdDefault(sender, app_data, user_data):
    if app_data != "[ Add New ++ ]":
        blv = int(sender[3:6])
        print(blv)
        vcmd.update({'default': '0'}, Data.blv == blv)
        vcmd.update({'default': '1'}, (Data.blv == blv) & (Data.cmd == app_data))
    else:
        blv = sender[3:6]
        result = vcmd.search((Data.default == "1") & (Data.blv == int(blv)))  
        cmd = result[0]['cmd']
        dpg.configure_item('cmd'+blv, default_value=cmd)
        dpg.configure_item("cmd_setting", show=True)
        print("cmd_setting/show")
    pass

def _start(sender, app_data, user_data):
    print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")
    result1 = vers.search(Data.blv == int(sender[1:]) )
    path = result1[0]['path']
    cmd = r"cd/ && "+path[0:2]+r" && cd "+path+r" && blender " + dpg.get_value(item='cmd'+sender[1:])
    print(cmd)
    os.system(cmd)
    pass

def _hsv_to_rgb(h, s, v):
    if s == 0.0: return (v, v, v)
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
    if i == 0: return (255*v, 255*t, 255*p)
    if i == 1: return (255*q, 255*v, 255*p)
    if i == 2: return (255*p, 255*v, 255*t)
    if i == 3: return (255*p, 255*q, 255*v)
    if i == 4: return (255*t, 255*p, 255*v)
    if i == 5: return (255*v, 255*p, 255*q)

#样式
with dpg.theme(tag="red"):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, _hsv_to_rgb(0.02, 0.7, 0.3))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, _hsv_to_rgb(0.02, 0.8, 0.5))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, _hsv_to_rgb(0.02, 0.75, 0.4))

with dpg.theme(tag="blue"):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, _hsv_to_rgb(4/7.0, 0.2, 0.3))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, _hsv_to_rgb(4/7.0, 0.3, 0.5))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, _hsv_to_rgb(4/7.0, 0.4, 0.4))
        #dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 18)
        #dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 8)

with dpg.theme(tag="grey"):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, _hsv_to_rgb(0, 0.01, 0.4))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, _hsv_to_rgb(0, 0.01, 0.6))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, _hsv_to_rgb(0, 0.01, 0.5))
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding,16, 3)

with dpg.theme(tag="org"):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, _hsv_to_rgb(0.1, 0.6, 0.4))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, _hsv_to_rgb(0.1, 0.8, 0.6))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, _hsv_to_rgb(0.1, 0.7, 0.5))
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 20)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding,16, 8)


#字体注册
def bindFont(font,size):
    with dpg.font_registry():
        with dpg.font(font, size) as font1:
            # add the default font range
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)

            # helper to add range of characters
            #    Options:
            #        mvFontRangeHint_Japanese
            #        mvFontRangeHint_Korean
            #        mvFontRangeHint_Chinese_Full
            #        mvFontRangeHint_Chinese_Simplified_Common
            #        mvFontRangeHint_Cyrillic
            #        mvFontRangeHint_Thai
            #        mvFontRangeHint_Vietnamese
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
            # add specific range of glyphs
            dpg.add_font_range(0x3100, 0x3ff0)
            # add specific glyphs
            dpg.add_font_chars([0x3105, 0x3107, 0x3108])
            # remap や to %
            dpg.add_char_remap(0x3084, 0x0025)
    dpg.bind_font(font1)

font = "FZMWFont.ttf"
bindFont(font,18)

def _fontsize(sender, app_data, user_data):
    bindFont(font,app_data)

def changeAppdatapath(sender, app_data, user_data):
    setting.update({'info': app_data}, Data.name == "APPDATA" )

def autogetapppath(sender, app_data, user_data):
    dpg.configure_item("apppath", default_value=env_appdata)
    setting.update({'info': env_appdata}, Data.name == "APPDATA" )

#全局设置面板
with dpg.window(label="GlobalSetting", pos=(48,32), width=520, height=280, modal=True, show=False, tag="global_setting", no_title_bar=True):
    dpg.add_button(label="关闭", width=75, callback=lambda: dpg.configure_item("global_setting", show=False))
    dpg.bind_item_theme(dpg.last_item(), "red")
    result1 = setting.search(Data.name == 'APPDATA')  
    path = result1[0]['info']
    with dpg.group(horizontal=True):
        dpg.add_input_text(callback = changeAppdatapath, label="系统数据目录", width=300, default_value = path, tag="apppath" )
        dpg.add_button(label="自动获取", width=82, callback=autogetapppath)
    pass

#cmd整体修改
with dpg.window(label="CmdSetting", pos=(160,32), width=240, height=400, modal=True, show=False, tag="cmd_setting", no_title_bar=True):
    dpg.add_button(label="关闭", width=75, callback=lambda: dpg.configure_item("cmd_setting", show=False))
    dpg.bind_item_theme(dpg.last_item(), "red")
    dpg.add_input_text(callback=_log, label="default")
    pass

def blenderSetting(sender, app_data, user_data):
    blv = int(user_data[1:4])
    vn = user_data[0:1]
    dpg.configure_item("bl_setting_vnum", default_value = str(blv)[0:1]+"."+str(blv)[1:3] ) 
    result = vers.search((Data.vn == vn) & (Data.blv == blv))  
    path = result[0]['path']
    dpg.configure_item("bl_setting_path", default_value = path )
    dpg.configure_item("bl_setting_path", user_data = vn+str(blv) )

    dpg.configure_item("bl_setting", show=True )
    pass

def changeAppdatapath(sender, app_data, user_data):
    blv = int(user_data[1:4])
    vn = user_data[0:1]
    vers.update({'path': app_data},(Data.vn == vn) & (Data.blv == blv))

#单个版本修改
with dpg.window(label="blenderSetting", pos=(56,48), width=500, height=320, modal=True, show=False, tag="bl_setting", no_title_bar=True):
    dpg.add_button(label="关闭", width=75, callback=lambda: dpg.configure_item("bl_setting", show=False))
    dpg.bind_item_theme(dpg.last_item(), "red")
    with dpg.group(horizontal=True):
        dpg.add_text("版本: ", color=(200, 200, 200))
        dpg.add_text("xxx", color=(255, 255, 255),wrap=500, tag="bl_setting_vnum" )
    dpg.add_input_text(callback=changeAppdatapath, label="路径", tag="bl_setting_path", user_data = "xx")
    pass


with dpg.window(label="Tutorial", tag="Primary Window") as window:
    # When creating items within the scope of the context
    # manager, they are automatically "parented" by the
    # container created in the initial call. So, "window"
    # will be the parent for all of these items.

    with dpg.group(horizontal=True):
        dpg.add_button(label="全局设置", callback=lambda: dpg.configure_item("global_setting", show=True))
        dpg.add_button(label="预设管理", callback=lambda: dpg.configure_item("", show=True))

    dpg.add_separator()
    dpg.add_separator()

    with dpg.group(horizontal=False):

        result = vers.search(Data.blv > 100)
        for rs in result:
            blv = rs['blv']
            vn = rs['vn']
            with dpg.group(horizontal=True):
                blv = str(blv)
                vname = blv[0:1]+"."+blv[1:3]
                vtag = vn+blv

                dpg.add_button(label="打开操作面板", callback=blenderSetting, user_data = vn+blv )
                dpg.bind_item_theme(dpg.last_item(), "blue")

                dpg.add_text("v "+vname, color=(255, 255, 255))

                result = vcmd.search(Data.blv == int(blv))
                default_cmd = ""
                cmds = ["[ Add New ++ ]"]
                for rs in result:
                    blv = rs['blv']
                    cmd = rs['cmd']
                    if rs['default'] == str(1):
                        default_cmd = cmd
                    cmds.append(cmd)
                
                dpg.add_combo(( "泉此方", "嘉然" ), label="", default_value="泉此方", callback=_log, width=94)
                dpg.add_combo(cmds, label="", default_value=default_cmd, tag='cmd'+str(blv), callback=_changeCmdDefault, width=172)

                dpg.add_button(label="启动 "+vname, tag=vtag, callback=_start)
                dpg.bind_item_theme(dpg.last_item(), "org")

            dpg.add_separator()
            pass

        dpg.add_button(label="Add", tag="add", callback=_log)
        dpg.bind_item_theme(dpg.last_item(), "grey")
        dpg.add_separator()


    with dpg.group(horizontal=True):
        dpg.add_text("字体尺寸: ", color=(200, 200, 200))
        slider_int = dpg.add_slider_int(label="", width=120, min_value=7, max_value=36, default_value=20, callback=_fontsize)
        #slider_float = dpg.add_slider_float(label="", width=100)

# If you want to add an item to an existing container, you
# can specify it by passing the container's tag as the
# "parent" parameter.
button2 = dpg.add_button(label="更换图片", parent=window)



with dpg.theme() as global_theme:

    with dpg.theme_component(dpg.mvAll):
        pass
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 1, category=dpg.mvThemeCat_Core)

    with dpg.theme_component(dpg.mvInputInt):
        pass

dpg.bind_theme(global_theme)


dpg.create_viewport(title=' Blender VManager ~ ', width=650, height=500)
dpg.set_primary_window("Primary Window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()