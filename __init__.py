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

bl_info = {
    "name" : "Set Presice Mesh /CAD",
    "author" : "Rovh",
    "description" : "This addon allows you to set exact values for the mesh",
    "blender" : (2, 82, 0),
    "version" : (1,1,3),
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
from .Operators import *
from .UI import *


from bpy import types
from bpy.props import (
        FloatProperty,
        BoolProperty,
        PointerProperty,
        EnumProperty,
        StringProperty,
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
    bl_description = "To make it convenient to use this menu You can assign shortcut \n \
         ( For example Ctrl + Alt + Middle Mouse )\n \
        How to do it: > right-click on this button > Assign Shortcut"
  
    
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
    bl_description = "To make it convenient to use this menu You can assign shortcut \n \
         ( For example Ctrl + Alt + Middle Mouse )\n \
        How to do it: > right-click on this button > Assign Shortcut"
  
    
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
    object_mode = bpy.context.active_object.mode

    if object_mode in {'EDIT'}:
        
        row = layout.row(align=1)

        sub = row.row(align = 0)
        sub.scale_x = 1.5
        sub = sub.operator("mesh.set_cursor", text="", icon = "ORIENTATION_CURSOR")
        
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
    bl_label = "Pop-up Menu"
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
        bpy.types.VIEW3D_PT_edit_mesh_set_precise_mesh1.draw(self, context)

class Popup_Menu_SetPreciseMesh_SetAngle (bpy.types.Operator):
    bl_idname = "wm.menu_setprecisemesh_setangle"
    bl_label = "Pop-up Menu Set Angle"
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
        
        split_left.operator("mesh.change_angle_copy", icon="DRIVER_ROTATIONAL_DIFFERENCE")

        split_center = split_left.split(factor=0.43, align=True)

        split_center.operator("mesh.change_angle_plus", icon="ADD", text = "")
            # 
        split_right = split_center.split(factor=0.8, align=True)

        split_right.operator("mesh.change_angle_minus", icon="REMOVE", text = "")
        

        # split = split.split(factor=1, align=True)

        if sc.bool_panel_arrow:
            split_right.prop(sc, "bool_panel_arrow", text="", icon='DOWNARROW_HLT')
        else:
            split_right.prop(sc, "bool_panel_arrow", text="", icon='RIGHTARROW')

        if sc.bool_panel_arrow:
            
            box = col.column(align=True).box().column()

            col_top = box.column(align = True)

            row = col_top.row(align = True)
            row.prop(w_m, "angle")

            row = row.row(align = False)
            row.scale_x = 1.2
            row.prop(sc, "script_input", text = "", icon = "FILE_SCRIPT")


            if script_input:
                col_top.prop(w_m, "data_block", text = "")


            split = col_top.split(factor = 0.835, align = 0)
            split.prop(w_m, "anglebool" )
            split.operator("wm.header_angle_simulation_setprecisemesh", text=" Angle Simulation", icon = "MOD_SIMPLIFY")

class Popup_Menu_SetPreciseMesh_SetLength (bpy.types.Operator):
    bl_idname = "wm.menu_setprecisemesh_setlength"
    bl_label = "Pop-up Menu Set Length"
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
        
        split_left.operator("mesh.change_length_copy",icon="DRIVER_DISTANCE")

        split_center = split_left.split(factor=0.43, align=True)

        split_center.operator("mesh.change_length_plus",icon="ADD", text = "")
            # 
        split_right = split_center.split(factor=0.8, align=True)

        split_right.operator("mesh.change_length_minus", icon="REMOVE", text = "")

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
            row.prop(w_m, "length")

            row = row.row(align = False)
            row.scale_x = 1.2
            row.prop(sc, "script_input_2", text = "", icon = "FILE_SCRIPT")


            if script_input_2:   
                col_top.prop(w_m, "data_block_2", text = "") 

           
            split = col_top.split(factor = 0.835, align = 0)
            split.prop(w_m, "lengthbool")
            split.operator("wm.header_length_simulation_setprecisemesh", text=" Distance Simulation", icon = "CON_TRACKTO")

"""Operators"""
class Set_Cursor_To_Normal (bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.set_cursor"
    bl_label = "Set the Cursor to the normal"
    bl_description = "Set the cursor location to the selected vertex/edge/face and set the cursor direction along its normal\
        \nYou can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bpy.context.object.update_from_editmode()
        bmesh.update_edit_mesh(me, True)

        
        #Create lists
        # face_ind = []
        # edge_ind = []
        # vec_ind  = []

        # face_list = []
        # edge_list = []
        # vec_list  = []


        selected_verts = [verts for verts in bm.verts if verts.select]
        selected_edges = [edge for edge in bm.edges if edge.select]
        selected_faces = [face for face in bm.faces if face.select]

        wm = bpy.context.active_object.matrix_world.copy()
        wm_inverted = wm.inverted()

        # print("\n")        


        """Maybe it will be need"""
        # if len(selected_verts) != 0 and len(selected_edges) == 0 and len(selected_faces) == 0:
        #     print(bm.select_history)
        #     for v in bm.select_history:
        #         if v.select:
        #             # vec_list.append(bm.verts[v.index].co)
        #             vec_list.append(v)
        #             vec_ind.append(v.index)

        # if len(selected_verts) != 0 and len(selected_edges) != 0 and len(selected_faces) == 0:

        #     for e in bm.select_history:
        #         if e.select:
        #             # edge_list.append(bm.edges[e.index])
        #             edge_list.append(e)
        #             edge_ind.append(e.index)

        # if len(selected_verts) != 0 and len(selected_edges) != 0 and len(selected_faces) != 0:

        #     for f in bm.select_history:
        #         if f.select:
        #             # face_list.append(bm.faces[f.index])
        #             face_list.append(f)
        #             # try:
        #             #     # list_2 = list(set(selected_faces) & set(lst2))
        #             #     # if bm.faces[f.index] == selected_faces[:]:
        #             #     face_list.append(selected_faces[f.index])
        #             # except IndexError:
        #             #     pass
        #             # else:
        #             #     face_list.append(selected_faces[f.index])
        #             face_ind.append(f.index)
    



        # for geom in bm.select_history:
        #     if isinstance(geom, bmesh.types.BMFace):
        #         print(geom.index, "geom.index")
        
        # print(f.select)
        # print(len(vec_ind))
        # print(len(edge_ind))
        # print(len(face_ind))

        # print(selected_faces, "selected_faces")
        # print(selected_edges, "selected_edges")
        # print(selected_verts, "selected_verts")

        # print(vec_list,  "vec_list")
        # print(edge_list, "edge_list")
        # print(face_list, "face_list")

        # print(vec_ind,  "vec_ind")
        # print(edge_ind, "edge_ind")
        # print(face_ind, "face_ind")

        if len(selected_verts) == 0 and len(selected_edges) == 0 and len(selected_faces) == 0:

            text = "You need to select one vertex/edge/face"
            war = "ERROR"
            self.report({war}, text)
            return{"FINISHED"}

        if len(selected_verts) != 0 and len(selected_edges) == 0 and len(selected_faces) == 0:

            if len(selected_verts) > 1:
                text = "You need to select only one vertex"
                war = "ERROR"
                self.report({war}, text)
                return{"FINISHED"}

            
            bpy.context.scene.cursor.location = wm @ selected_verts[0].co

            normal = selected_verts[0].normal @ wm_inverted

            obj_camera = bpy.data.scenes[bpy.context.scene.name_full].cursor       
            direction = normal
            # point the cameras '-Z' and use its 'Y' as up
            rot_quat = direction.to_track_quat('-Z', 'Y')
            obj_camera.rotation_euler = rot_quat.to_euler()
            rot_quat =  rot_quat.to_euler()

        if len(selected_verts) != 0 and len(selected_edges) != 0 and len(selected_faces) == 0:

            if len(selected_edges) > 1:
                text = "You need to select only one edge"
                war = "ERROR"
                self.report({war}, text)
                return{"FINISHED"}

            
            edge_verts = selected_edges[0].verts

            location_of_edge = ((wm @ edge_verts[0].co) + (wm @ edge_verts[1].co)) /2
            bpy.context.scene.cursor.location = location_of_edge

            faces_of_edge = selected_edges[0].link_faces

            normals_of_the_faces = []

            # normal_from_face = 

            for f in range(0, len(faces_of_edge)):
                # print(faces_of_edge[f])
                normals_of_the_faces.append(faces_of_edge[f].normal @ wm_inverted) 


            normal_from_face = ((normals_of_the_faces[0]) + (normals_of_the_faces[1])) /2
            normal_from_face = (normal_from_face) + (location_of_edge) 
            normal_projection_from_face = mathutils.geometry.intersect_point_line(normal_from_face, (wm @ edge_verts[0].co), (wm @ edge_verts[1].co))
            normal_projection_from_face = normal_projection_from_face[0]
            # normal_from_face = normal_projection_from_face
            normal_from_face = (normal_from_face - normal_projection_from_face)
            normal = normal_from_face



            # print(normals_of_the_faces[0])


            # normal = ((edge_verts[0].normal) + (edge_verts[1].normal))
            # normal = (location_of_edge) + normal
            # normal_projection = mathutils.geometry.intersect_point_line(normal, (wm @ edge_verts[0].co), (wm @ edge_verts[1].co))
            # normal_projection = normal_projection[0]
            # normal = (normal - normal_projection)

            # normal = normal_from_face + normal

            

            obj_camera = bpy.data.scenes[bpy.context.scene.name_full].cursor       
            direction = normal
            # point the cameras '-Z' and use its 'Y' as up
            rot_quat = direction.to_track_quat('-Z', 'Y')
            obj_camera.rotation_euler = rot_quat.to_euler()
            rot_quat =  rot_quat.to_euler()

        if len(selected_verts) != 0 and len(selected_edges) != 0 and len(selected_faces) != 0:

            if len(selected_faces) > 1:
                text = "You need to select only one face"
                war = "ERROR"
                self.report({war}, text)
                return{"FINISHED"}


            my_location = wm @ selected_faces[0].calc_center_median()
            normalgl = selected_faces[0].normal @ wm_inverted

                        
            bpy.context.scene.cursor.location = my_location

            # Set cursor direction
            obj_camera = bpy.data.scenes[bpy.context.scene.name_full].cursor       
            direction = normalgl
            # point the cameras '-Z' and use its 'Y' as up
            rot_quat = direction.to_track_quat('-Z', 'Y')
            obj_camera.rotation_euler = rot_quat.to_euler()
            rot_quat =  rot_quat.to_euler()

        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bpy.context.object.update_from_editmode()
        bmesh.update_edit_mesh(me, True)


        return {'FINISHED'}

class Browser_Link (bpy.types.Operator):
    """Tooltip"""
    bl_idname = "wm.setprecisemesh_link"
    bl_label = "Change version"
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

    def draw(self, context):

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
        
        split_left.operator("mesh.change_angle_copy", icon="DRIVER_ROTATIONAL_DIFFERENCE")

        split_center = split_left.split(factor=0.43, align=True)

        split_center.operator("mesh.change_angle_plus", icon="ADD", text = "")
            # 
        split_right = split_center.split(factor=0.8, align=True)

        split_right.operator("mesh.change_angle_minus", icon="REMOVE", text = "")
        

        # split = split.split(factor=1, align=True)

        if sc.bool_panel_arrow:
            split_right.prop(sc, "bool_panel_arrow", text="", icon='DOWNARROW_HLT')
        else:
            split_right.prop(sc, "bool_panel_arrow", text="", icon='RIGHTARROW')

        if sc.bool_panel_arrow:
            
            box = col.column(align=True).box().column()

            col_top = box.column(align = True)

            row = col_top.row(align = True)
            row.prop(w_m, "angle")

            row = row.row(align = False)
            row.scale_x = 1.2
            row.prop(sc, "script_input", text = "", icon = "FILE_SCRIPT")


            if script_input:
                col_top.prop(w_m, "data_block", text = "")


            split = col_top.split(factor = 0.835, align = 0)
            split.prop(w_m, "anglebool" )
            split.operator("wm.header_angle_simulation_setprecisemesh", text=" Angle Simulation", icon = "MOD_SIMPLIFY")


        #  sub = row.row(align = 1)
        # sub.scale_x = 0.6
        # split = sub.split(align = 1, factor = 0.5)


        col = layout.column(align= True )
        
        split_left = col.split(factor=0.55, align=True)
        split_left.scale_y = 1.2
        
        split_left.operator("mesh.change_length_copy",icon="DRIVER_DISTANCE")

        split_center = split_left.split(factor=0.43, align=True)

        split_center.operator("mesh.change_length_plus",icon="ADD", text = "")
            # 
        split_right = split_center.split(factor=0.8, align=True)

        split_right.operator("mesh.change_length_minus", icon="REMOVE", text = "")

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
            row.prop(w_m, "length")

            row = row.row(align = False)
            row.scale_x = 1.2
            row.prop(sc, "script_input_2", text = "", icon = "FILE_SCRIPT")


            if script_input_2:   
                col_top.prop(w_m, "data_block_2", text = "") 

           
            split = col_top.split(factor = 0.835, align = 0)
            split.prop(w_m, "lengthbool")
            split.operator("wm.header_length_simulation_setprecisemesh", text=" Distance Simulation", icon = "CON_TRACKTO")


                 
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
        col.prop(self, "direction_of_length", text='Invert "Set Length" direction')
        
        row = col.row(align = False)
        row.operator("wm.menu_setprecisemesh_setangle",icon="DRIVER_ROTATIONAL_DIFFERENCE", text="Pop-up Menu (Hover cursor on it for more information)")
        row.operator("wm.menu_setprecisemesh_setlength",icon="DRIVER_DISTANCE", text="Pop-up Menu (Hover cursor on it for more information)")

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
    data_block: bpy.props.StringProperty(
        name = "Number input",
        description = "" ,
    )
    data_block_2: bpy.props.StringProperty(
        name = "Number input",
        description = "",
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
        default = True,
    )
    position_origin_clear_matrix: bpy.props.BoolProperty(
        name="Clear Rotation",
        description="Apply the object's rotation transformation to its data",
        default = False,
    )

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
    SetAngle_Copy,
    SetAngle_Plus,
    SetAngle_Minus,


    SetLength,
    SetLength_Copy,
    SetLength_Plus,
    SetLength_Minus,


    Dialog_Warning_Operator,
    Dialog_Warning_Operator_2,
    Dialog_Warning_Operator_3,
    Dialog_Warning_Operator_4,


    SetPreciseMesh_Props,
    SetPreciseMesh_Preferences,
    Popup_Menu_SetPreciseMesh_Operator,
    Popup_Menu_SetPreciseMesh_SetAngle,
    Popup_Menu_SetPreciseMesh_SetLength,
    Angle_Simulation_SetPreciseMesh,
    Length_Simulation_SetPreciseMesh,


    Set_Cursor_To_Normal,
    Browser_Link,

    Pop_Up_Set_Mesh_Position,
    Set_Mesh_Position_Global,
    Set_Mesh_Position_Local,
    Set_Mesh_Position_Cursor,
    Set_Mesh_Position_Object,
    Set_Mesh_Position,

    
    # ChooseItemOperator,
    # NewItemOperator,
    # ClearItemOperator,

]

classes = (
    CUSTOM_OT_actions,
    CUSTOM_OT_clearList,
    CUSTOM_OT_removeDuplicates,
    # CUSTOM_OT_selectItems,
    CUSTOM_UL_items,
    CUSTOM_PT_objectList,
    CUSTOM_objectCollection,
)


def register():
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


    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # Custom scene properties
    bpy.types.Scene.custom = CollectionProperty(type=CUSTOM_objectCollection)
    bpy.types.Scene.custom_index = IntProperty()


def unregister():
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)

    del bpy.types.WindowManager.setprecisemesh

    del bpy.types.Scene.bool_panel_arrow
    del bpy.types.Scene.bool_panel_arrow2
    del bpy.types.Scene.script_input
    del bpy.types.Scene.script_input_2
    del bpy.types.Scene.bool_warning
    del bpy.types.Scene.remember_length

    del bpy.types.Scene.my_property
    bpy.types.VIEW3D_HT_tool_header.remove(header_draw)
    bpy.types.VIEW3D_MT_transform.remove(draw_VIEW3D_MT_transform)

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.custom
    del bpy.types.Scene.custom_index


if __name__ == "__main__":
    register()
