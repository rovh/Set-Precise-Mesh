# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

name = "(Set Precise Mesh)"
bl_info = {
    "name" : "Set Precise Mesh /CAD",
    "author" : "Rovh",
    "description" : "This addon allows you to set exact values for the mesh",
    "blender" : (2, 83, 0),
    "version" : (1,2,3),
    "location" : "View3D > Sidebar in Edit Mode > Item Tab, View Tab and Edit Tab",
    "warning" : "",
    "wiki_url": "https://github.com/rovh/Set-Precise-Mesh",
    "category" : "Mesh",
    "tracker_url": "https://github.com/rovh/Set-Precise-Mesh/issues",
    # "new_info": "https://github.com/rovh/Set-Precise-Mesh",
}


import bpy

from .SetAngle import *
from .SetLength import *
from .Set_Mesh_Position import *
from .Presets import *
from .Presets_Object import *
from .Set_Cursor_To_Normal import *
from .Draw import *
from .SetArea import *


from bpy import types
from bpy.props import (
        FloatProperty,
        BoolProperty,
        PointerProperty,
        EnumProperty,
        StringProperty,
        IntProperty,
        )


"""Pop up menus"""
class Dialog_Warning_Operator   (bpy.types.Operator):
    bl_idname = "object.dialog_warning_operator"
    bl_label = "Warning Panel Operator"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event): 
        bool_warning = bpy.data.scenes[bpy.context.scene.name_full].bool_warning
        settings = bpy.context.preferences.addons[__name__].preferences
        bool_warning_global = settings.bool_warning_global

        if bool_warning_global == 1:
            if bool_warning == 1:
                # return context.window_manager.invoke_props_dialog(self)
                return context.window_manager.invoke_popup(self, width=700)
                # return context.window_manager.invoke_popup(self)
                # return context.window_manager.invoke_props_popup(self, event)
                # return context.window_manager.invoke_confirm(self, event)
            else:
                return {'FINISHED'}
        else:
            return {'FINISHED'}


    def draw(self, context):
        layout = self.layout
        layout.label(text='Warning' , icon="ERROR")

        if bpy.context.object.scale != Vector((1.0, 1.0, 1.0)):
            
            layout.label(text='Your object scale is not by default. Please, apply "Scale"')
            layout.label(text='Shortcut: Objetc Mode > Ctrl A > Apply "Scale"')

        elif bpy.context.object.delta_scale != Vector((1.0, 1.0, 1.0)):

            layout.label(text='Your object delta transform scale is not by default. Please, change it')
            layout.label(text='How to do it: Properties Editor > Object Properties > Transform > Delta Transform >')
            layout.label(text='> You need to set values: All Scales = 1')

        layout.prop(context.scene, "bool_warning", text="Show Warning Panel next time (Warning: Panel will show up in new Blender file even if you disable it)")
        layout.label(text="If you need to disable it globally (so that it does not show up in new Blender file), you need to go to Set Precise Mesh Preferences")
        layout.label(text="Warning Panel appears if object scale or delta scale is not by default")
        layout.label(text='You can find more info about this warning in README.md on Github page or in files')

class Dialog_Warning_Operator_2 (bpy.types.Operator):
    bl_idname = "object.dialog_warning_operator_2"
    bl_label = "Warning Panel Operator"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event): 

        # return context.window_manager.invoke_props_dialog(self)
        return context.window_manager.invoke_popup(self, width=320)
        # return context.window_manager.invoke_popup(self)
        # return context.window_manager.invoke_props_popup(self, event)
        # return context.window_manager.invoke_confirm(self, event)

    def draw(self, context):
        layout = self.layout
        lay = layout.label(text='Warning' , icon="ERROR")

        row = layout.row()
        row.label(icon = "SNAP_PERPENDICULAR")
        row.label(text = " = True ")
        row.scale_x = 0.1
        
        lay = layout.label(text = "Your angle projection is perpendicular to the matrix (plane)")
        # lay = layout.label(text = "Your rotation can be not correct")
        lay = layout.label(text = "Please, move one of the selected vertices")

class Dialog_Warning_Operator_3 (bpy.types.Operator):
    bl_idname = "object.dialog_warning_operator_3"
    bl_label = "Warning Panel Operator"

    warnin: StringProperty()

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event): 

        # return context.window_manager.invoke_props_dialog(self)
        return context.window_manager.invoke_popup(self, width=400)
        # return context.window_manager.invoke_popup(self)
        # return context.window_manager.invoke_props_popup(self, event)
        # return context.window_manager.invoke_confirm(self, event)

    def draw(self, context):
        layout = self.layout
        lay = layout.label(text= "Warning" , icon="ERROR")

        row = layout.row()
        row.label(icon = "DRIVER_ROTATIONAL_DIFFERENCE")
        row.label(text = " = 0 ")
        row.scale_x = 0.1
        
        lay = layout.label(text = "Angle between your cursor or custom object is zero")
        lay = layout.label(text = "Your rotation can be not correct")
        lay = layout.label(text = "Please, change (cursor/custom object) location or change selected vertices")

class Dialog_Warning_Operator_4 (bpy.types.Operator):
    bl_idname = "object.dialog_warning_operator_4"
    bl_label = "Warning Panel Operator"

    warnin: StringProperty()

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event): 

    #     # return context.window_manager.invoke_props_dialog(self)
        return context.window_manager.invoke_popup(self, width=200)
    #     # return context.window_manager.invoke_popup(self)
    #     # return context.window_manager.invoke_props_popup(self, event)
    #     # return context.window_manager.invoke_confirm(self, event)

    def draw(self, context):
        layout = self.layout
        lay = layout.label(text= "Warning" , icon="ERROR")

        # row = layout.row()
        # row.label(text = " = 0 ")
        # row.scale_x = 0.1
        
        lay = layout.label(text = "You length/distance will be zero")

class Angle_Simulation_SetPreciseMesh (bpy.types.Operator):
   
    bl_idname = "wm.header_angle_simulation_setprecisemesh"
    bl_label = "Header Menu"
    bl_description = '\nYou need to select two vertexes to use "Angle Simulation"\n\n\
    To make it convenient to use this menu You can assign shortcut \n \
    ( For example Ctrl + Alt + Middle Mouse )\n \
    How to do it: > right-click on this button > Assign Shortcut'
  
    
    def invoke(self, context, event): 

        x = event.mouse_x
        y = event.mouse_y 

        move_x = -15
        move_y = 5
        
        bpy.context.window.cursor_warp(x + move_x, y + move_y)

        # inv = context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self, width=600, height=500)
        # return context.window_manager.invoke_popup(self)
        inv = context.window_manager.invoke_popup(self, width = 190)
        # return context.window_manager.invoke_props_popup(self, event)
        # return context.window_manager.popmenu_begin__internal()
        # return context.window_manager.invoke_confirm(self, event)

        bpy.context.window.cursor_warp(x, y)

        return inv


    def execute(self, context):
        return {'FINISHED'}
        # return {"INTERFACE"}


    def draw(self, context):
        layout=self.layout

        w_m = context.window_manager.setprecisemesh

        row = layout.row(align=0)
        col_left = row.column(align=0)
        col_right = row.column(align=0)
        
        # col_left.scale_y = 0.8
        # col_right.scale_x = 5.0


        # For Matrix
        sub_col = col_left.column(align = 0)
        sub_col.scale_y = 1.9
        sub_col.label(icon='WORLD_DATA')

        # For Cursor
        sub_col = col_left.column(align = 0)
        sub_col.scale_y = 2.7
        sub_col.label(icon='PIVOT_CURSOR')
        

        # For Object
        sub_col = col_left.column(align = 0)
        sub_col.scale_y = 1.65
        sub_col.label(icon='OBJECT_DATA')  

        # Make space if
        # prog = context.window_manager.setprecisemesh.projection_type

        # if prog == "custom_object_location" or  prog == "custom_object_matrix":
        #     sub_col = col_left.column(align = 0)
        #     sub_col.scale_y = 0.9
        #     sub_col.label(icon='BLANK1')         
        
        # col_left.prop(w_m, "projection_type", expand = 1)

        # Matrix menu
        sub_col = col_right.column(align = 1)
        sub_col.prop_enum( w_m, "projection_type", "local_matrix")
        sub_col.prop_enum( w_m, "projection_type", "global_matrix")

        # space
        sub_col = col_right.column(align = 0)
        sub_col.scale_y = 0.15
        sub_col = sub_col.label(text = "")

        # Cursor menu
        sub_col = col_right.column(align = 1)
        sub_col.prop_enum( w_m, "projection_type", "cursor_location")
        sub_col.prop_enum( w_m, "projection_type", "cursor_matrix")

        # space
        # sub_col = col_right.column(align = 0)
        # sub_col.scale_y = 0.15
        # sub_col = sub_col.label(text = "")

        # # Cursor menu
        # sub_col = col_right.column(align = 1)
        # sub_col.prop_enum( w_m, "projection_type", "normal_matrix")
        # sub_col.prop_enum( w_m, "projection_type", "cursor_matrix")

        # space
        sub_col = col_right.column(align = 0)
        sub_col.scale_y = 0.15
        sub_col = sub_col.label(text = "")

        # Object menu
        sub_col = col_right.column(align = 1)
        sub_col.prop_enum( w_m, "projection_type", "custom_object_location")
        
        sub_col.prop_enum( w_m, "projection_type", "custom_object_matrix")

        # Make space object selection box
        prog = context.window_manager.setprecisemesh.projection_type
        if prog == "custom_object_location" or  prog == "custom_object_matrix":
            sub_col.prop(context.scene, "my_property", text = "")

        # sub_col.prop(context.scene, "my_property", text = "")

class Length_Simulation_SetPreciseMesh (bpy.types.Operator):
   
    bl_idname = "wm.header_length_simulation_setprecisemesh"
    bl_label = "Header Menu"
    bl_description = '\nYou need to select one vertex to use "Length / Distance Simulation"\n\n\
    To make it convenient to use this menu You can assign shortcut \n \
    ( For example Ctrl + Alt + Middle Mouse )\n \
    How to do it: > right-click on this button > Assign Shortcut'
  
    
    def invoke(self, context, event): 

        x = event.mouse_x
        y = event.mouse_y 

        move_x = -15
        move_y = 5
        
        bpy.context.window.cursor_warp(x + move_x, y + move_y)
        
        # return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self, width=600, height=500)
        # return context.window_manager.invoke_popup(self)
        inv = context.window_manager.invoke_popup(self, width = 190)
        # return context.window_manager.invoke_props_popup(self, event)
        # return context.window_manager.popmenu_begin__internal()
        # return context.window_manager.invoke_confirm(self, event)

        bpy.context.window.cursor_warp(x, y)


        return inv


    def execute(self, context):
        return {'FINISHED'}
        # return {"INTERFACE"}


    def draw(self, context):
        layout=self.layout

        w_m = context.window_manager.setprecisemesh

        row = layout.row(align=0)
        col_left = row.column(align=0)
        col_right = row.column(align=0)
        
        # col_left.scale_y = 0.8
        # col_right.scale_x = 5.0


        # For Matrix
        sub_col = col_left.column(align = 0)
        sub_col.scale_y = 1.9
        sub_col.label(icon='WORLD_DATA')

        # For Cursor
        sub_col = col_left.column(align = 0)
        sub_col.scale_y = 2.7
        sub_col.label(icon='PIVOT_CURSOR')
        

        # For Object
        sub_col = col_left.column(align = 0)
        sub_col.scale_y = 1.65
        sub_col.label(icon='OBJECT_DATA')  

        # Make space if
        # prog = context.window_manager.setprecisemesh.projection_type

        # if prog == "custom_object_location" or  prog == "custom_object_matrix":
        #     sub_col = col_left.column(align = 0)
        #     sub_col.scale_y = 0.9
        #     sub_col.label(icon='BLANK1')         
        
        # col_left.prop(w_m, "projection_type", expand = 1)

        # Matrix menu
        sub_col = col_right.column(align = 1)
        sub_col.prop_enum( w_m, "projection_type_2", "local_matrix")
        sub_col.prop_enum( w_m, "projection_type_2", "global_matrix")

        # space
        sub_col = col_right.column(align = 0)
        sub_col.scale_y = 0.15
        sub_col = sub_col.label(text = "")

        # Cursor menu
        sub_col = col_right.column(align = 1)
        sub_col.prop_enum( w_m, "projection_type_2", "cursor_location")
        sub_col.prop_enum( w_m, "projection_type_2", "cursor_matrix")

        # space
        # sub_col = col_right.column(align = 0)
        # sub_col.scale_y = 0.15
        # sub_col = sub_col.label(text = "")

        # # Cursor menu
        # sub_col = col_right.column(align = 1)
        # sub_col.prop_enum( w_m, "projection_type", "normal_matrix")
        # sub_col.prop_enum( w_m, "projection_type", "cursor_matrix")

        # space
        sub_col = col_right.column(align = 0)
        sub_col.scale_y = 0.15
        sub_col = sub_col.label(text = "")

        # Object menu
        sub_col = col_right.column(align = 1)
        sub_col.prop_enum( w_m, "projection_type_2", "custom_object_location")
        
        sub_col.prop_enum( w_m, "projection_type_2", "custom_object_matrix")

        # Make space object selection box
        prog = context.window_manager.setprecisemesh.projection_type_2
        if prog == "custom_object_location" or  prog == "custom_object_matrix":
            sub_col.prop(context.scene, "my_property_2", text = "")

        # sub_col.prop(context.scene, "my_property_2", text = "")

def   header_draw   (self, context):
    layout = self.layout

    try:
        object_mode = bpy.context.active_object.mode
    except AttributeError:
        pass
    except UnboundLocalError:
        pass
    else:
        if object_mode in {'EDIT'}:
            
            row = layout.row(align=1)

            sub = row.row(align = 0)
            sub.scale_x = 1.5
            # sub = sub.operator("mesh.set_cursor", text="", icon = "ORIENTATION_CURSOR")
            sub = sub.operator("mesh.set_cursor_to_normal_pop_up", text="", icon = "ORIENTATION_CURSOR")
            

            # sub = row.row(align = 1)
            # sub.scale_x = 0.6
            # split = sub.split(align = 1, factor = 0.5)
            # split.operator("wm.header_angle_simulation_setprecisemesh", text="Angle Simulation", icon = "MOD_SIMPLIFY")
            # split.operator("wm.header_length_simulation_setprecisemesh", text="Distance Simulation", icon = "CON_TRACKTO")
 
def   draw_VIEW3D_MT_transform(self, context):
    layout = self.layout

    layout.separator()

    layout.operator("mesh.set_mesh_position_pop_up", text="Set Mesh Position")

# draw_buttons(self, context, layout)

class Popup_Menu_SetPreciseMesh_Operator (bpy.types.Operator):
    bl_idname = "wm.menu_setprecisemesh_operator"
    bl_label = "Pop-up Menu | All " + name
    bl_description = "To make it convenient to use the pop-up menu You can assign shortcut \n \
         ( For exaple Ctrl + Alt + Wheel Down )\n \
        How to do it: > right-click on this button > Assign Shortcut"
        
    def execute(self, context):

        # context.window_manager.invoke_popup(self, width = 200)
        return {'FINISHED'}

    def invoke(self, context, event):
        x = event.mouse_x
        y = event.mouse_y 

        move_x = 0
        move_y = 60

        bpy.context.window.cursor_warp(x + move_x, y + move_y)
        # context.window_manager.invoke_popup(self, width = 200)
        # return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self, width=600, height=500)
        # return context.window_manager.invoke_popup(self)
        inv = context.window_manager.invoke_popup(self, width = 200)
        
        bpy.context.window.cursor_warp(x, y)

        return inv

        # return {"INTERFACE"}

        # if self.return == {"CANCELLED"}:
            # context.window_manager.invoke_popup(self, width = 200)
        # return

        # return context.window_manager.invoke_props_popup(self, event)
        # return context.window_manager.invoke_confirm(self, event)
    def draw(self, context):
        bpy.types.VIEW3D_PT_edit_mesh_set_precise_mesh1.draw_angle(self, context)
        bpy.types.VIEW3D_PT_edit_mesh_set_precise_mesh1.draw_length(self, context)
        bpy.types.VIEW3D_PT_edit_mesh_set_precise_mesh1.draw_area(self, context)

class Popup_Menu_SetPreciseMesh_SetAngle (bpy.types.Operator):
    bl_idname = "wm.menu_setprecisemesh_setangle"
    bl_label = "Pop-up Menu | Set Angle   " + name 
    bl_description = "To make it convenient to use the pop-up menu You can assign shortcut \n \
         ( For exaple Ctrl + Alt + Wheel Down )\n \
        How to do it: > right-click on this button > Assign Shortcut"
        
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        x = event.mouse_x
        y = event.mouse_y 

        move_x = 0
        move_y = 10

        bpy.context.window.cursor_warp(x + move_x, y + move_y)
        # context.window_manager.invoke_popup(self, width = 200)
        # return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self, width=600, height=500)
        # return context.window_manager.invoke_popup(self)
        inv = context.window_manager.invoke_popup(self, width = 200)
        
        bpy.context.window.cursor_warp(x, y)

        return inv

    def draw(self, context):

        bpy.types.VIEW3D_PT_edit_mesh_set_precise_mesh1.draw_angle(self, context)
        
        # layout = self.layout

        # scene = context.scene
        # sc = scene
        # ob = context.object

        # w_m = context.window_manager.setprecisemesh

        # # Get values
        # bool_panel_arrow = bpy.data.scenes[bpy.context.scene.name_full].bool_panel_arrow
        # bool_panel_arrow2 = bpy.data.scenes[bpy.context.scene.name_full].bool_panel_arrow2

        # script_input = bpy.data.scenes[bpy.context.scene.name_full].script_input
        # script_input_2 = bpy.data.scenes[bpy.context.scene.name_full].script_input_2

        # col = layout.column(align=True)

        # split = col.split(factor=0.65, align=True)
        # split.scale_y =1.2      

        # # split.operator("mesh.change_angle_copy", icon="DRIVER_ROTATIONAL_DIFFERENCE")

        # # split = split.split(factor=0.8, align=True)

        # # split.operator("mesh.change_angle_plus", icon="ADD", text = "")

        # split_left = col.split(factor=0.55, align=True)
        # split_left.scale_y = 1.2
        
        # split_left.operator("mesh.change_angle", icon="DRIVER_ROTATIONAL_DIFFERENCE").Clear_angle_globally = 0

        # split_center = split_left.split(factor=0.43, align=True)

        # split_center.operator("mesh.change_angle", icon="ADD", text = "").Clear_angle_globally = 1
        #     # 
        # split_right = split_center.split(factor=0.8, align=True)

        # split_right.operator("mesh.change_angle", icon="REMOVE", text = "").Clear_angle_globally = -1
        

        # # split = split.split(factor=1, align=True)

        # if sc.bool_panel_arrow:
        #     split_right.prop(sc, "bool_panel_arrow", text="", icon='DOWNARROW_HLT')
        # else:
        #     split_right.prop(sc, "bool_panel_arrow", text="", icon='RIGHTARROW')

        # if sc.bool_panel_arrow:
            
        #     box = col.column(align=True).box().column()

        #     col_top = box.column(align = True)

        #     row = col_top.row(align = True)
        #     row.prop(w_m, "angle")

        #     row = row.row(align = False)
        #     row.scale_x = 1.2
        #     row.prop(sc, "script_input", text = "", icon = "FILE_SCRIPT")


        #     if script_input:
        #         col_top.prop(w_m, "data_block", text = "")


        #     split = col_top.split(factor = 0.835, align = 0)
        #     split.prop(w_m, "anglebool" )
        #     split.operator("wm.header_angle_simulation_setprecisemesh", text=" Angle Simulation", icon = "MOD_SIMPLIFY")

class Popup_Menu_SetPreciseMesh_SetLength (bpy.types.Operator):
    bl_idname = "wm.menu_setprecisemesh_setlength"
    bl_label = "Pop-up Menu | Set Length " + name
    bl_description = "To make it convenient to use the pop-up menu You can assign shortcut \n \
         ( For exaple Ctrl + Alt + Wheel Up )\n \
        How to do it: > right-click on this button > Assign Shortcut"
        
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        x = event.mouse_x
        y = event.mouse_y 

        move_x = 0
        move_y = 10

        bpy.context.window.cursor_warp(x + move_x, y + move_y)
        # context.window_manager.invoke_popup(self, width = 200)
        # return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self, width=600, height=500)
        # return context.window_manager.invoke_popup(self)
        inv = context.window_manager.invoke_popup(self, width = 200)
        
        bpy.context.window.cursor_warp(x, y)

        return inv

    def draw(self, context):

        bpy.types.VIEW3D_PT_edit_mesh_set_precise_mesh1.draw_length(self, context)

        # layout = self.layout

        # scene = context.scene
        # sc = scene
        # ob = context.object

        # w_m = context.window_manager.setprecisemesh

        # # Get values
        # bool_panel_arrow = bpy.data.scenes[bpy.context.scene.name_full].bool_panel_arrow
        # bool_panel_arrow2 = bpy.data.scenes[bpy.context.scene.name_full].bool_panel_arrow2

        # script_input = bpy.data.scenes[bpy.context.scene.name_full].script_input
        # script_input_2 = bpy.data.scenes[bpy.context.scene.name_full].script_input_2
        
        # col = layout.column(align= True )
        
        # split_left = col.split(factor=0.55, align=True)
        # split_left.scale_y = 1.2
        
        # split_left.operator("mesh.change_length",icon="DRIVER_DISTANCE").plus_length = 0

        # split_center = split_left.split(factor=0.43, align=True)

        # split_center.operator("mesh.change_length",icon="ADD", text = "").plus_length = 1
        
        # split_right = split_center.split(factor=0.8, align=True)

        # split_right.operator("mesh.change_length", icon="REMOVE", text = "").plus_length = -1

        # # split_right = split_center.split(factor=0.9, align=True)

        # if sc.bool_panel_arrow2:
        #     split_right.prop(sc, "bool_panel_arrow2", text="", icon='DOWNARROW_HLT')
        # else:
        #     split_right.prop(sc, "bool_panel_arrow2", text="", icon='RIGHTARROW')

        # if sc.bool_panel_arrow2:            
        #     box = col.column(align=True).box().column()            
        #     col_top = box.column(align=True)


        #     # col_top.prop(w_m, "length") 

        #     row = col_top.row(align = True)
        #     row.prop(w_m, "length")

        #     row = row.row(align = False)
        #     row.scale_x = 1.2
        #     row.prop(sc, "script_input_2", text = "", icon = "FILE_SCRIPT")


        #     if script_input_2:   
        #         col_top.prop(w_m, "data_block_2", text = "") 

           
        #     split = col_top.split(factor = 0.835, align = 0)
        #     split.prop(w_m, "lengthbool")
        #     split.operator("wm.header_length_simulation_setprecisemesh", text=" Distance Simulation", icon = "CON_TRACKTO")

class Popup_Menu_SetPreciseMesh_SetArea (bpy.types.Operator):
    bl_idname = "wm.menu_setprecisemesh_setarea"
    bl_label = "Pop-up Menu | Set Area " + name
    bl_description = "To make it convenient to use the pop-up menu You can assign shortcut \n \
         ( For exaple Ctrl + Alt + Wheel Up )\n \
        How to do it: > right-click on this button > Assign Shortcut"
        
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        x = event.mouse_x
        y = event.mouse_y 

        move_x = 0
        move_y = 10

        bpy.context.window.cursor_warp(x + move_x, y + move_y)
        # context.window_manager.invoke_popup(self, width = 200)
        # return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self, width=600, height=500)
        # return context.window_manager.invoke_popup(self)
        inv = context.window_manager.invoke_popup(self, width = 200)
        
        bpy.context.window.cursor_warp(x, y)

        return inv

    def draw(self, context):

        bpy.types.VIEW3D_PT_edit_mesh_set_precise_mesh1.draw_area(self, context)

"""Operators"""

class Browser_Link (bpy.types.Operator):
    """Tooltip"""
    bl_idname = "wm.setprecisemesh_link"
    bl_label = "Change version " + name
    bl_description = "Link" 
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.wm.url_open(url = "https://github.com/rovh/Set-Precise-Mesh/releases")
        return {"FINISHED"}

# items = [('one', 'Any', "", 'PRESET', 1), ('two', 'PropertyGroup', "", 'PRESET', 2), ('three', 'type', "", 'PRESET', 3)]

# class ChooseItemOperator(bpy.types.Operator):
#     bl_idname = "example.choose_item"
#     bl_label = "Choose item"
#     bl_options = {'INTERNAL'}
#     bl_property = "enum"

#     def get_enum_options(self, context):
#         global items
#         return items

#     enum: EnumProperty(items=get_enum_options, name="Items")
#     node_tree: StringProperty()
#     node: StringProperty()

#     def execute(self, context):
#         tree = bpy.data.node_groups[self.node_tree]
#         node = tree.nodes[self.node]
#         node.item_set = True
#         node.set_item(self.enum)
#         return {"FINISHED"}

#     def invoke(self, context, event):
#         context.window_manager.invoke_search_popup(self)
#         return {"FINISHED"}

        

# class NewItemOperator(bpy.types.Operator):
#     bl_idname = "example.new_item"
#     bl_label = "New Item"
#     bl_options = {'INTERNAL'}

#     node_tree: StringProperty()
#     node: StringProperty()

#     def execute(self, context):
#         global items
#         tree = bpy.data.node_groups[self.node_tree]
#         node = tree.nodes[self.node]
#         node.item_set = True
#         newitem = ('four', 'type', "", 'PRESET', 4)
#         items.append(newitem)
#         node.set_item(newitem)
#         return {'FINISHED'}

# class ClearItemOperator(bpy.types.Operator):
#     bl_idname = "example.clear_item"
#     bl_label = "Clear Item"
#     bl_options = {'INTERNAL'}

#     node_tree: StringProperty()
#     node: StringProperty()

#     def execute(self, context):
#         tree = bpy.data.node_groups[self.node_tree]
#         node = tree.nodes[self.node]
#         node.item_set = False
#         return {'FINISHED'}

"""Main Panel"""
class SetPresiceMesh_Panel (bpy.types.Panel):
    bl_label = "Set Presice Mesh"
    bl_idname = "VIEW3D_PT_edit_mesh_set_precise_mesh"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"
    bl_context = "mesh_edit"
    bl_options = {'DEFAULT_CLOSED'}
    bl_label = "Set Precise Mesh / CAD"

    # def draw(self, context):   
    # 
    def draw(self, context):
        
        self.draw_angle(context)
        self.draw_length(context)
        self.draw_area(context)

    def draw_angle(self, context):

        layout = self.layout

        scene = context.scene
        sc = scene
        ob = context.object

        w_m = context.window_manager.setprecisemesh

        # Get values
        bool_panel_arrow = bpy.data.scenes[bpy.context.scene.name_full].bool_panel_arrow
        bool_panel_arrow2 = bpy.data.scenes[bpy.context.scene.name_full].bool_panel_arrow2

        script_input = bpy.data.scenes[bpy.context.scene.name_full].script_input
        script_input_2 = bpy.data.scenes[bpy.context.scene.name_full].script_input_2
    
    
        col = layout.column(align=True)

        split = col.split(factor=0.65, align=True)
        split.scale_y =1.2      

        # split.operator("mesh.change_angle_copy", icon="DRIVER_ROTATIONAL_DIFFERENCE")

        # split = split.split(factor=0.8, align=True)

        # split.operator("mesh.change_angle_plus", icon="ADD", text = "")

        split_left = col.split(factor=0.55, align=True)
        split_left.scale_y = 1.2
        
        split_left.operator("mesh.change_angle", icon="DRIVER_ROTATIONAL_DIFFERENCE", text = "Set Angle").Clear_angle_globally = 0

        split_center = split_left.split(factor=0.43, align=True)

        split_center.operator("mesh.change_angle", icon="ADD", text = "").Clear_angle_globally = 1
            # 
        split_right = split_center.split(factor=0.8, align=True)

        split_right.operator("mesh.change_angle", icon="REMOVE", text = "").Clear_angle_globally = -1
        

        # split = split.split(factor=1, align=True)

        if sc.bool_panel_arrow:
            split_right.prop(sc, "bool_panel_arrow", text="", icon='DOWNARROW_HLT')
        else:
            split_right.prop(sc, "bool_panel_arrow", text="", icon='RIGHTARROW')

        if sc.bool_panel_arrow:
            
            box = col.column(align=True).box().column()

            col_top = box.column(align = True)

            row = col_top.row(align = True)
            row.prop(w_m, "angle", text = "")

            sub_row = row.row(align = 1)
            sub_row.label(icon="BLANK1")
            sub_row.scale_x = 0.1
            
            sub_row = row.row(align = 1)
            sub_row.operator("mesh.change_angle",icon="EYEDROPPER", text = "").eyedropper = True
            sub_row.scale_x = 1.3

            row = row.row(align = False)
            row.scale_x = 1.2
            row.prop(sc, "script_input", text = "", icon = "FILE_SCRIPT")


            if script_input:
                col_top.prop(w_m, "data_block", text = "")


            # split = col_top.split(factor = 0.835, align = 0)
            split = col_top.row(align = 0)

            split.prop(w_m, "anglebool" )
            row = split.row(align = 0)
            row.operator("wm.header_angle_simulation_setprecisemesh", text=" Angle Simulation", icon = "MOD_SIMPLIFY")
            row.scale_x = 0.14

        #  sub = row.row(align = 1)
        # sub.scale_x = 0.6
        # split = sub.split(align = 1, factor = 0.5)

    def draw_length(self, context):
        layout = self.layout

        scene = context.scene
        sc = scene
        ob = context.object

        w_m = context.window_manager.setprecisemesh

        # Get values
        bool_panel_arrow = bpy.data.scenes[bpy.context.scene.name_full].bool_panel_arrow
        bool_panel_arrow2 = bpy.data.scenes[bpy.context.scene.name_full].bool_panel_arrow2

        script_input = bpy.data.scenes[bpy.context.scene.name_full].script_input
        script_input_2 = bpy.data.scenes[bpy.context.scene.name_full].script_input_2

        col = layout.column(align= True )
        
        split_left = col.split(factor=0.55, align=True)
        split_left.scale_y = 1.2
        
        split_left.operator("mesh.change_length",icon="DRIVER_DISTANCE", text = "Set Length / Distance").plus_length = 0

        split_center = split_left.split(factor=0.43, align=True)

        split_center.operator("mesh.change_length",icon="ADD", text = "").plus_length = 1
            # 
        split_right = split_center.split(factor=0.8, align=True)

        split_right.operator("mesh.change_length", icon="REMOVE", text = "").plus_length = -1

        # split_right = split_center.split(factor=0.9, align=True)

        if sc.bool_panel_arrow2:
            split_right.prop(sc, "bool_panel_arrow2", text="", icon='DOWNARROW_HLT')
        else:
            split_right.prop(sc, "bool_panel_arrow2", text="", icon='RIGHTARROW')

        if sc.bool_panel_arrow2:            
            box = col.column(align=True).box().column()            
            col_top = box.column(align=True)


            # col_top.prop(w_m, "length") 

            row = col_top.row(align = True)
            row.prop(w_m, "length", text = "")

            sub_row = row.row(align = 1)
            sub_row.label(icon="BLANK1")
            sub_row.scale_x = 0.1
            
            sub_row = row.row(align = 1)
            sub_row.operator("mesh.change_length",icon="EYEDROPPER", text = "").eyedropper = True
            sub_row.scale_x = 1.3
            # sub_row.scale_x = .13
            # sub_row.ui_units_x = 1.3
            


            row = row.row(align = False)
            row.scale_x = 1.2
            row.prop(sc, "script_input_2", text = "", icon = "FILE_SCRIPT")

            if script_input_2:   
                col_top.prop(w_m, "data_block_2", text = "") 



            space = col_top.row(align = 1)
            space.label(icon="BLANK1")
            space.scale_y = 0.1



            row = col_top.row(align = 1)

            row_left = row.row(align = 0)
            row_left.prop(w_m, "lengthbool")
            row_left.scale_x = 1.2



            depress = bpy.context.window_manager.setprecisemesh.draw_length_line
            row_center = row.row(align = 0)
            row_center.operator("view3d.modal_operator_setprecisemesh_draw_length", text="", icon = "RESTRICT_VIEW_OFF", depress=depress)
            row_center.scale_x = 1.3



            row_right = row.row(align = 0)
            row_right.operator("wm.header_length_simulation_setprecisemesh", text=" Distance Simulation", icon = "CON_TRACKTO")
            row_right.scale_x = 0.14

    


                 
            # row = col_top.row(align=1)
            # row.scale_y = 0.25
            # row.label(text = "")


            # row_main = col_top.row(align=1)

            # row_main.scale_y = 0.76

            # row = row_main.row(align=1)

            # row.alignment = "CENTER"

            # if w_m.anglebool:
            #     row.prop(w_m, "anglebool", icon = "CHECKMARK" , icon_only = 1)
            #     row.scale_x = 1
            #     row.scale_y = 1.2
            # else:
            #     # row.label(icon = "CHECKBOX_DEHLT")
            #     row.prop(w_m, "anglebool", icon = "BLANK1" , icon_only = 1)
            #     row.scale_x = 0.78
            #     row.scale_y = 1

            # row = row_main.row(align=1)
            # row.scale_x = 0.9
            # row.alignment = "LEFT"
            # row.prop(w_m, "anglebool", emboss=0)




            # col_top.prop(self, "projection_type")
            # col_top.prop(ob, "angleinput")
            # row = layout.row(align=True)

            # sub = row.row()
            # sub.ui_units_x = 5
            # sub.prop_with_popover(
            #     self,
            #     "projection_type",
            #     text="",
            #     panel="VIEW3D_PT_Set_Precise_Mesh",
            # )         
                    
    

            # row = col_top.row(align=1)
            # row.scale_y = 0.25
            # row.label(text = "")

            # row_main = col_top.row(align=1)
            # row_main.scale_y = 0.76

            # row = row_main.row(align=1)


            # if w_m.lengthbool:

            #     row.prop(w_m, "lengthbool", icon = "CHECKMARK" , icon_only = 1)
            #     row.scale_x = 0.76
            #     row.scale_y = 1

            #     row = row_main.row(align=1)
            #     row.scale_x = 1
            #     row.alignment = "LEFT"
            #     row.prop(w_m, "lengthbool", emboss=0)

            # else:
            #     row.prop(w_m, "lengthbool", icon = "BLANK1" , icon_only = 1)
            #     row.scale_x = 0.76
            #     row.scale_y = 1

            #     row = row_main.row(align=1)
            #     row.scale_x = 0.9
            #     row.alignment = "LEFT"
            #     row.prop(w_m, "lengthbool", emboss=0)



            

            # row = row_main.row(align=1)
            # row.scale_x = 0.1
            # row.label(text = "")


        
            # col_top.prop(ob, "lengthinput")
            # col_top.operator(bpy.ops.ui.eyedropper_id.idname())
            # col_top.operator(bpy.ops.wm.url_open(url = "https://github.com/rovh/Set-Precise-Mesh"))

    def draw_area(self, context):
        
        layout = self.layout

        scene = context.scene
        sc = scene
        ob = context.object

        w_m = context.window_manager.setprecisemesh

        # Get values
        bool_panel_arrow = bpy.data.scenes[bpy.context.scene.name_full].bool_panel_arrow
        bool_panel_arrow2 = bpy.data.scenes[bpy.context.scene.name_full].bool_panel_arrow2
        bool_panel_arrow3 = bpy.data.scenes[bpy.context.scene.name_full].bool_panel_arrow3

        script_input = bpy.data.scenes[bpy.context.scene.name_full].script_input
        script_input_2 = bpy.data.scenes[bpy.context.scene.name_full].script_input_2
        script_input_3 = bpy.data.scenes[bpy.context.scene.name_full].script_input_3

        col = layout.column(align= True )
        
        split_left = col.split(factor=0.55, align=True)
        split_left.scale_y = 1.2
        
        split_left.operator("mesh.change_area",icon="FULLSCREEN_ENTER", text = "Set Area").plus_area = 0

        split_center = split_left.split(factor=0.43, align=True)

        split_center.operator("mesh.change_area",icon="ADD", text = "").plus_area = 1
            
        split_right = split_center.split(factor=0.8, align=True)

        split_right.operator("mesh.change_area", icon="REMOVE", text = "").plus_area = -1



        if sc.bool_panel_arrow3:
            split_right.prop(sc, "bool_panel_arrow3", text="", icon='DOWNARROW_HLT')
        else:
            split_right.prop(sc, "bool_panel_arrow3", text="", icon='RIGHTARROW')

        if sc.bool_panel_arrow3:            
            box = col.column(align=True).box().column()            
            col_top = box.column(align=0)


            # col_top.prop(w_m, "length") 

            row = col_top.row(align = True)
            row.prop(w_m, "area", text = "")

            sub_row = row.row(align = 1)
            sub_row.label(icon="BLANK1")
            sub_row.scale_x = 0.1
            
            sub_row = row.row(align = 1)
            sub_row.operator("mesh.change_area",icon="EYEDROPPER", text = "").eyedropper = True
            sub_row.scale_x = 1.3
            # sub_row.scale_x = .13
            # sub_row.ui_units_x = 1.3


            row = row.row(align = False)
            row.scale_x = 1.2
            row.prop(sc, "script_input_3", text = "", icon = "FILE_SCRIPT")

            if script_input_3:   
                col_top.prop(w_m, "data_block_3", text = "") 


            space = col_top.row(align = 1)
            space.label(icon="BLANK1")
            space.scale_y = 0.2

            row_right = col_top.row(align = 0)
            row_right.scale_y = .9
            row_right.prop_enum( w_m, "scale_point", "madian_point")
            row_right.prop_enum( w_m, "scale_point", "auto_point")
            row_right.prop_enum( w_m, "scale_point", "cursor_point")
            # row_right_sub = row_right.row(align = 1)
            # row_right_sub.prop_enum( w_m, "scale_point", "madian_point")
            # row_right_sub.alignment = "RIGHT"
            # row_right_sub = row_right.row(align = 1)
            # row_right_sub.prop_enum( w_m, "scale_point", "cursor_point")
            # row_right_sub.alignment = "RIGHT"
            # row_right.alignment = "RIGHT"
            # row_right.prop("wm.header_length_simulation_setprecisemesh", text=" Distance Simulation", icon = "CON_TRACKTO")
            # row_right.operator("wm.header_length_simulation_setprecisemesh", text=" Distance Simulation", icon = "CON_TRACKTO")
            # row_right.scale_x = 0.14


"""Preferences Panel and Props"""
class SetPreciseMesh_Preferences (bpy.types.AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    direction_of_length: BoolProperty(
            name="bool",
            description="Change direction",
            default=False,
            )

    direction_of_angle: BoolProperty(
            name="bool",
            description="Change direction",
            default=False,
            )

    bool_warning_global: BoolProperty(
            name="bool",
            description="Globally",
            default=True,
            )
    
    round_precision: IntProperty(
        default = 2,
        name="Round",
        description="Round",
    )
    
    
    # location_in_UI_1: BoolProperty(
    #         name="location_in_UI",
    #         description="location_in_UI",
    #         default=True,
    #         )
    # location_in_UI_2: BoolProperty(
    #         name="location_in_UI",
    #         description="location_in_UI",
    #         default=True,
    #         )
    # location_in_UI_3: BoolProperty(
    #         name="location_in_UI",
    #         description="location_in_UI",
    #         default=True,
    #         )


    def draw(self, context):

        layout = self.layout

        box = layout.box()
        box.label(icon="PREFERENCES", text = "Preferences")
        row = box.row()
        col = row.column(align = False)


        row = col.row(align = True)
        row.label(icon = "ARROW_LEFTRIGHT" )
        row.prop(self, "direction_of_length", text='Invert / Reverse "Set Length" direction')
        
        row = col.row(align = True)
        row.alignment = 'LEFT'
        # row.label(icon = "TRACKER")
        # row.label(text = '"Draw Length" precision =')
        row.label(icon = "TRACKER", text = '"Draw Length" precision =')

        row_2 = row.row(align = True)
        row_2.prop(self, "round_precision", text='', emboss = True)
        row_2.alignment = 'LEFT'
        # row_2.prop(self, "round_precision", text='"Draw Length" precision  =', emboss = True)
        # row_2.prop(self, "round_precision", text='', emboss = False)
        row_2.scale_x = .28



        row = col.row(align = False)
        row.operator("wm.menu_setprecisemesh_setangle" ,icon="DRIVER_ROTATIONAL_DIFFERENCE", text="Pop-up Menu (Hover cursor on it for more information)")
        row.operator("wm.menu_setprecisemesh_setlength",icon="DRIVER_DISTANCE", text="Pop-up Menu (Hover cursor on it for more information)")
        row.operator("wm.menu_setprecisemesh_setarea"  ,icon="FULLSCREEN_ENTER", text="Pop-up Menu (Hover cursor on it for more information)")

        row = col.row()
        row.label(text = "")
        row.scale_y = 0.1

        col.operator("wm.menu_setprecisemesh_operator",icon="WINDOW", text="Pop-up Menu (Hover cursor on it for more information)")


        # split = col.split(align = 1 , factor = 0.5)
        # row = col.row(align = 1)
        # row.prop(self, "location_in_UI_1", text = "1", icon = "BLANK1")
        # row.prop(self, "location_in_UI_2", text = "2", icon = "BLANK1")
        # row.prop(self, "location_in_UI_3", text = "3", icon = "BLANK1")

        col.prop(self, "bool_warning_global", text='Show Warning Panel in Blender (Global)')

        col.label(icon="INFO", text = "If you don't like this version you can download the previous version or download the next version if it exists:")
        
        col.operator("wm.setprecisemesh_link",icon="RECOVER_LAST", text="Change version")

"""Props"""
class SetPreciseMesh_Props (bpy.types.PropertyGroup):
    """
    Fake module like class
    bpy.context.window_manager.setprecisemesh
    """
    angle: bpy.props.FloatProperty(
        name="Angle",
        description="Angle",
        min=-360.0, max=360.0,
        default=0.0,
        step = 100.0,
        unit="ROTATION",
        precision = 6,
    )
    anglebool: bpy.props.BoolProperty(
        name="Change adjacent edge",
        description="Change the length of the opposite edge OR Change the length of the adjacent edge",
        default=False,
    )
    angleinput: bpy.props.BoolProperty(
        name="Input Mode",
        description="",
        default=False,
    )

    length: bpy.props.FloatProperty(
        name="Length",
        description="Length of the edge",
        default=1.0,
        step = 100.0,
        unit='LENGTH',
        precision = 6,
    )
    lengthbool: bpy.props.BoolProperty(
        name="Use two directions",
        description='Change length in two directions OR in the direction of the active vertex',
        default=False,
    )
    lengthinput: bpy.props.BoolProperty(
        name="Input Mode",
        description='User Mode',
        default=False,
    )


    area: bpy.props.FloatProperty(
        name="Area",
        description="Area of the face",
        default=1.0,
        step = 100.0,
        unit='LENGTH',
        precision = 6,
    )
    scale_point: bpy.props.EnumProperty(
        name = "Scale point",
        default = "auto_point",
        description = "",
        items=(
            ("madian_point"   , "Median Point" , "" , "PIVOT_MEDIAN" , 0),
            ("cursor_point"   , "3D Cursor"    , "" , "PIVOT_CURSOR" , 1),
            ("auto_point"     , "Calculate"    , "" , "EDITMODE_HLT" , 2),
        ))



    data_block: bpy.props.StringProperty(
        name = "Number input",
        description="\n u = Angle\
                     \n unit = Angle" ,
    )
    data_block_2: bpy.props.StringProperty(
        name = "Number input",
        description="\n u = Length\
                     \n unit = Length" ,
    )
    data_block_3: bpy.props.StringProperty(
        name = "Number input",
        description="\n u = Area\
                     \n unit = Area",
    )


    description_projection_type = [
        #description_0
        "Local Matrix. It uses the matrix of the editing object and projects the selected vertices onto it" ,

        #description_1
        "Global Matrix. It uses the matrix of the world and projects the selected vertices onto it",

        #description_2
        "Custon Object Location. It uses the location of the specified object to simulate an angle",

        #description_3
        "Custon Object Matrix. It uses the matrix of the specified object\
        \nand projects the selected vertices onto it",

        #description_4
        'Cursor Location. It uses the location of the 3d cursor to simulate an angle\
        \n To make it more convinient to use 3d cursor in the cursor settings You can enable\
        \n "Surface Project" and "Orintation: Geometry" ',

        #description_5
        'Cursor Matrix. It uses the matrix of the 3d cursor\
        \n To make it more convinient to use 3d cursor You can use\
        \n "Set Cursor to normal face" which you can find next to "Angle Simulation"\
        \n Also in the cursor settings You can enable\
        \n "Surface Project" and "Orintation: Geometry" (Warning: Use it very carefully for "Cursor Matrix")',
    ]
    projection_type: bpy.props.EnumProperty(
        name="Angle Simulation",
        items=(
            ("local_matrix"   , "Local Matrix  (Object)" , description_projection_type[0]  , "GRID"              , 0),
            ("global_matrix"  , "Global Matrix (World)"  , description_projection_type[1]  , "VIEW_PERSPECTIVE"  , 1),
            (None),
            ("custom_object_location"  , "Custom Object Location" , description_projection_type[2] , "EMPTY_ARROWS", 2),
            ("custom_object_matrix"    , "Custom Object Matrix"   , description_projection_type[3] , "GRID"        , 3),
            (None),
            ("cursor_location", "Cursor Location", description_projection_type[4] , "EMPTY_ARROWS", 4),
            ("cursor_matrix"  , "Cursor Matrix"  , description_projection_type[5] , "GRID"        , 5),
            (None),
            ("normal_matrix"  , "Normal Matrix"  , description_projection_type[5] , "GRID"        , 6),

        ),
        description="Angle Simulation",
        default='global_matrix'
    )
    description_projection_type_2 = [
        #description_0
        "Local Matrix. It uses the matrix of the editing object and projects the selected vertex onto it" ,

        #description_1
        "Global Matrix. It uses the matrix of the world and projects the selected vertex onto it",

        #description_2
        "Custon Object Location. It uses the location of the specified object to simulate the distance",

        #description_3
        "Custon Object Matrix. It uses the matrix of the specified object\
        \nand projects the selected vertex onto it",

        #description_4
        'Cursor Location. It uses the location of the 3d cursor to simulate the distance\
        \n To make it more convinient to use 3d cursor in the cursor settings You can enable\
        \n "Surface Project" and "Orintation: Geometry" ',

        #description_5
        'Cursor Matrix. It uses the matrix of the 3d cursor and projects the selected vertex onto it\
        \n To make it more convinient to use 3d cursor You can use\
        \n "Set Cursor to normal face" which you can find next to "Angle Simulation"\
        \n Also in the cursor settings You can enable\
        \n "Surface Project" and "Orintation: Geometry" (Warning: Use it very carefully for "Cursor Matrix")',
    ]
    projection_type_2: bpy.props.EnumProperty(
        name="Length\Distance Simulation",
        items=(
            ("local_matrix"   , "Local Matrix  (Object)" , description_projection_type_2[0]  , "GRID"              , 0),
            ("global_matrix"  , "Global Matrix (World)"  , description_projection_type_2[1]  , "VIEW_PERSPECTIVE"  , 1),
            (None),
            ("custom_object_location"  , "Custom Object Location" , description_projection_type_2[2] , "EMPTY_ARROWS", 2),
            ("custom_object_matrix"    , "Custom Object Matrix"   , description_projection_type_2[3] , "GRID"        , 3),
            (None),
            ("cursor_location", "Cursor Location", description_projection_type_2[4] , "EMPTY_ARROWS", 4),
            ("cursor_matrix"  , "Cursor Matrix"  , description_projection_type_2[5] , "GRID"        , 5),
            (None),
            ("normal_matrix"  , "Normal Matrix"  , description_projection_type_2[5] , "GRID"        , 6),
        ),
        description="Length\Distance Simulation",
        default='global_matrix'
    )
    position_origin: bpy.props.BoolProperty(
        name="Set Origin Location",
        description='Set Origin location of the active mesh',
        default = False,
    )
    position_origin_clear_matrix: bpy.props.BoolProperty(
        name="Clear Rotation",
        description="Apply the object's rotation transformation to its data",
        default = False,
    )
    position_location: bpy.props.BoolProperty(
        name="Move Location",
        description=" Only Move object \
        \n(Set the mesh position not in accordance with the normal of the selected part of the mesh)",
        default = False,
    )

    length_display_number:         bpy.props.FloatProperty      (options = {"SKIP_SAVE"})
    length_display_stop:           bpy.props.BoolProperty       (options = {"SKIP_SAVE"})
    draw_length_line:              bpy.props.BoolProperty       ()
    length_display_coordinate_1:   bpy.props.FloatVectorProperty(options = {"SKIP_SAVE"})
    length_display_coordinate_2:   bpy.props.FloatVectorProperty(options = {"SKIP_SAVE"})

    x: bpy.props.BoolProperty(default = 1, name = "Use X axis", description = "Move the object along the X axis")
    y: bpy.props.BoolProperty(default = 1, name = "Use Y axis", description = "Move the object along the Y axis")
    z: bpy.props.BoolProperty(default = 1, name = "Use Z axis", description = "Move the object along the Z axis")

    seconds: bpy.props.IntProperty()

"""Duplications of the Main panel"""
class Dupli (SetPresiceMesh_Panel):
    bl_label = "Set Presice Mesh1"
    bl_idname = "VIEW3D_PT_edit_mesh_set_precise_mesh1"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "View"
    bl_label = "Set Precise Mesh /CAD"

    # bl_order = 1
class Dupli2 (SetPresiceMesh_Panel):
    bl_label = "Set Presice Mesh2"
    bl_idname = "VIEW3D_PT_edit_mesh_set_precise_mesh2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"
    bl_label = "Set Precise Mesh /CAD"
    # bl_order = 1
class Dupli3 (SetPresiceMesh_Panel):
    bl_label = "Set Presice Mesh2"
    bl_idname = "VIEW3D_PT_edit_mesh_set_precise_mesh3"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Edit"
    bl_label = "Set Precise Mesh /CAD"
    # bl_order = 1


"""Classes registration"""
blender_classes = [

    Dupli,
    Dupli2,
    Dupli3,
    # SetPresiceMesh_Panel,

    SetAngle,

    SetLength,

    SetArea,

    Dialog_Warning_Operator,
    Dialog_Warning_Operator_2,
    Dialog_Warning_Operator_3,
    Dialog_Warning_Operator_4,


    SetPreciseMesh_Props,
    SetPreciseMesh_Preferences,

    Popup_Menu_SetPreciseMesh_Operator,
    Popup_Menu_SetPreciseMesh_SetAngle,
    Popup_Menu_SetPreciseMesh_SetLength,
    Popup_Menu_SetPreciseMesh_SetArea,

    Angle_Simulation_SetPreciseMesh,
    Length_Simulation_SetPreciseMesh,


    Set_Cursor_To_Normal,
    Pop_Up_Set_Cursor_To_Normal,

    Browser_Link,

    Pop_Up_Set_Mesh_Position,
    Set_Mesh_Position,

    ModalDrawOperator_Set_Precise_Mesh_Length,

    # ChooseItemOperator,
    # NewItemOperator,
    # ClearItemOperator,
]

"""Classes of Presets"""
classes = (
    #"""Presets for Scene""",
    PRESETS_OT_Length_actions,
    PRESETS_OT_Length_clearList,
    PRESETS_OT_Length_actions_add,
    PRESETS_OT_Length_actions_refresh,
    PRESETS_OT_Length_Rename,
    PRESETS_OT_Length_actions_import,
    PRESETS_OT_Length_Change_unit,
    # PRESETS_OT_removeDuplicates,


    PRESETS_OT_Angle_actions,
    PRESETS_OT_Angle_actions_add,
    PRESETS_OT_Angle_actions_refresh,
    PRESETS_OT_Angle_actions_import,
    PRESETS_OT_Angle_Rename,
    PRESETS_OT_Angle_clearList,


    PRESETS_OT_Area_actions,
    PRESETS_OT_Area_actions_add,
    PRESETS_OT_Area_actions_refresh,
    PRESETS_OT_Area_actions_import,
    PRESETS_OT_Area_Rename,
    PRESETS_OT_Area_Change_unit,
    PRESETS_OT_Area_clearList,


    PRESETS_FOR_PRESETS_ANGLE_MT_DisplayPresets,
    PRESETS_FOR_PRESETS_ANGLE_OT_AddPreset,
    PRESETS_FOR_PRESETS_ANGLE_OT_Rename,
    PRESETS_FOR_PRESETS_ANGLE_OT_Refresh,

    PRESETS_FOR_PRESETS_LENGTH_MT_DisplayPresets,
    PRESETS_FOR_PRESETS_LENGTH_OT_AddPreset,
    PRESETS_FOR_PRESETS_LENGTH_OT_Rename,
    PRESETS_FOR_PRESETS_LENGTH_OT_Refresh,

    PRESETS_FOR_PRESETS_AREA_MT_DisplayPresets,
    PRESETS_FOR_PRESETS_AREA_OT_AddPreset,
    PRESETS_FOR_PRESETS_AREA_OT_Rename,
    PRESETS_FOR_PRESETS_AREA_OT_Refresh,


    PRESETS_FOR_PRESETS_PT_panel,


    # PRESETS_UL_items_Area,
    # PRESETS_PT_presets_List_Area,
    

    PRESETS_UL_items_Angle,
    PRESETS_PT_presets_List_Angle,


    PRESETS_UL_items_Length,
    PRESETS_PT_presets_List_Length,


    # """Presets for Object""",

    PRESETS_OT_Angle_Object_actions,
    PRESETS_OT_Angle_Object_actions_add,
    PRESETS_OT_Angle_Object_actions_refresh,
    PRESETS_OT_Angle_Object_actions_import,
    PRESETS_OT_Angle_Object_Rename,
    PRESETS_OT_Angle_Object_clearList,

    PRESETS_UL_items_Angle_Object,
    PRESETS_PT_presets_List_Angle_Object,


    PRESETS_OT_Length_Object_actions,
    PRESETS_OT_Length_Object_actions_add,
    PRESETS_OT_Length_Object_actions_refresh,
    PRESETS_OT_Length_Object_actions_import,
    PRESETS_OT_Length_Object_Rename,
    PRESETS_OT_Length_Object_clearList,

    PRESETS_UL_items_Length_Object,
    PRESETS_PT_presets_List_Length_Object,


    #====================================
    PRESETS_presets_angle_Collection,
    PRESETS_presets_length_Collection,
    PRESETS_presets_area_Collection,
    #====================================
) 

# kc = bpy.context.window_manager.keyconfigs.addon

def register():

    # if kc:
    #     km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
    #     kmi = km.keymap_items.new('mesh.change_length', 'LEFTMOUSE', 'CLICK', shift=True)
        # Could pass settings to operator properties here
        # kmi.properties.mode = (False, True, False)

    # bpy.app.handlers.depsgraph_update_post.append(my_handler)
    # bpy.app.handlers.on_scene_update_pre.append(my_handler)

    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)
    # pynput.register()

    bpy.types.WindowManager.setprecisemesh = PointerProperty(type=SetPreciseMesh_Props)
    bpy.types.VIEW3D_HT_tool_header.append(header_draw)
    bpy.types.VIEW3D_MT_transform.append(draw_VIEW3D_MT_transform)

    bpy.types.Scene.my_property = PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.my_property_2 = PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.object_position = PointerProperty(type=bpy.types.Object)

    bpy.types.Scene.bool_panel_arrow = bpy.props.BoolProperty(
        name="bool_panel_arrow",
        description="",
        default=True,
    )
    bpy.types.Scene.bool_panel_arrow2 = bpy.props.BoolProperty(
        name="bool_panel_arrow2",
        description="",
        default=True,
    )
    bpy.types.Scene.bool_panel_arrow3 = bpy.props.BoolProperty(
        name="bool_panel_arrow3",
        description="",
        default=True,
    )
    bpy.types.Scene.script_input = bpy.props.BoolProperty(
            name="Advanced input",
            description="",
            default=False,
    )
    bpy.types.Scene.script_input_2 = bpy.props.BoolProperty(
            name="Advanced input",
            description="",
            default=False,
    )
    bpy.types.Scene.script_input_3 = bpy.props.BoolProperty(
            name="Advanced input",
            description="",
            default=False,
    )
    bpy.types.Scene.bool_warning = bpy.props.BoolProperty(
        name="Show this warning panel next time",
        description="Warning Panel will appear if object scale or delta scale is not correct \n You can also enable it or disable in \n Property Editor > Scene Properties > Custom Properties",
        default=1,
        options = {"SKIP_SAVE"}
    )
    bpy.types.Scene.remember_length = bpy.props.FloatProperty(
        name="remember_length",
        description="",
        # default=,
    )

    """Register Presets"""
    from  bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    """Presets for Scene"""
    bpy.types.Scene.presets_angle = CollectionProperty(type=PRESETS_presets_angle_Collection)
    bpy.types.Scene.presets_angle_index = IntProperty()
    bpy.types.Scene.presets_angle_save = IntProperty()


    bpy.types.Scene.presets_length = CollectionProperty(type=PRESETS_presets_length_Collection)
    bpy.types.Scene.presets_length_index = IntProperty()
    bpy.types.Scene.presets_length_save = IntProperty()

    
    bpy.types.Scene.presets_length = CollectionProperty(type=PRESETS_presets_angle_Collection)
    bpy.types.Scene.presets_length_index = IntProperty()
    bpy.types.Scene.presets_length_save = IntProperty()


    """Presets for Objetcs"""
    bpy.types.Object.presets_angle = CollectionProperty(type=PRESETS_presets_angle_Collection)
    bpy.types.Object.presets_angle_index = IntProperty()

    bpy.types.Object.presets_length = CollectionProperty(type=PRESETS_presets_length_Collection)
    bpy.types.Object.presets_length_index = IntProperty()

def unregister():

    # kc = bpy.context.window_manager.keyconfigs.addon
    # if kc:
    #     km = kc.keymaps["3D View"]
    #     for kmi in km.keymap_items:
    #         if kmi.idname == 'mesh.change_length':
    #             km.keymap_items.remove(kmi)
    #             break

    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)

    del bpy.types.WindowManager.setprecisemesh

    del bpy.types.Scene.bool_panel_arrow
    del bpy.types.Scene.bool_panel_arrow2
    del bpy.types.Scene.bool_panel_arrow3
    del bpy.types.Scene.script_input
    del bpy.types.Scene.script_input_2
    del bpy.types.Scene.script_input_3
    del bpy.types.Scene.bool_warning
    del bpy.types.Scene.remember_length

    del bpy.types.Scene.my_property
    bpy.types.VIEW3D_HT_tool_header.remove(header_draw)
    bpy.types.VIEW3D_MT_transform.remove(draw_VIEW3D_MT_transform)


    """Unregister Presets"""
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)

    """Presets for Scene"""
    del bpy.types.Scene.presets_angle
    del bpy.types.Scene.presets_angle_index

    del bpy.types.Scene.presets_length
    del bpy.types.Scene.presets_length_index

    """Presets for Object"""
    del bpy.types.Object.presets_angle
    del bpy.types.Object.presets_angle_index

    del bpy.types.Object.presets_length
    del bpy.types.Object.presets_length_index


if __name__ == "__main__":
    register()
