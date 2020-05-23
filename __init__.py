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
    "version" : (1,1,1),
    "location" : "View3D > Sidebar in Edit Mode > Item Tab and View Tab",
    "warning" : "",
    "wiki_url": "https://github.com/rovh/Set-Precise-Mesh",
    "category" : "Mesh",
    "tracker_url": "https://github.com/rovh/Set-Precise-Mesh/issues",
    # "new_info": "https://github.com/rovh/Set-Precise-Mesh",
}


import bpy

from .SetAngle import *
from .SetLength import *

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
        # layout.label(text='https://github.com/rovh/Set-Precise-Mesh')

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

class Header_SetPreciseMesh (bpy.types.Operator):
   
    bl_idname = "wm.header_setprecisemesh_operator"
    bl_label = "Header Menu"
    bl_description = "To make it convenient to use the this menu You can assign shortcut \n \
         ( For exaple Ctrl + Alt + Wheel Up )\n \
        How to do it: > right-click on this button > Assign Shortcut"
  
    
    def invoke(self, context, event): 
        
        # return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self, width=600, height=500)
        # return context.window_manager.invoke_popup(self)
        return context.window_manager.invoke_popup(self, width = 190)
        # return context.window_manager.invoke_props_popup(self, event)
        # return context.window_manager.popmenu_begin__internal()
        # return context.window_manager.invoke_confirm(self, event)

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
        sub_col = col_right.column(align = 0)
        sub_col.scale_y = 0.15
        sub_col = sub_col.label(text = "")

        # Cursor menu
        sub_col = col_right.column(align = 1)
        sub_col.prop_enum( w_m, "projection_type", "normal_matrix")
        # sub_col.prop_enum( w_m, "projection_type", "cursor_matrix")

        # space
        sub_col = col_right.column(align = 0)
        sub_col.scale_y = 0.15
        sub_col = sub_col.label(text = "")

        # Object menu
        sub_col = col_right.column(align = 1)
        sub_col.prop_enum( w_m, "projection_type", "custom_object_location")
        # sub_col.prop_enum( w_m, "projection_type", "custom_object_matrix")
        # Make space object selection box
        # prog = context.window_manager.setprecisemesh.projection_type
        # if prog == "custom_object_location" or  prog == "custom_object_matrix":
        #     sub_col.prop(context.scene, "my_property", text = "")
        sub_col.prop(context.scene, "my_property", text = "")

def   header_draw(self, context):
    layout = self.layout
    object_mode = bpy.context.active_object.mode

    if object_mode in {'EDIT'}:
        
        row = layout.row(align=0)
        sub = row.row()

        # row.ui_units_x = 4.5
        sub.scale_x = 1.2
        sub = sub.operator("mesh.set_cursor", text="", icon = "ORIENTATION_CURSOR")
        
        sub = row.row()
        sub.operator("wm.header_setprecisemesh_operator", text="Angle Simulation", icon = "MOD_SIMPLIFY")
        # sub.scale_x = 0.5
        # row.ui_units_x = 100

class Popup_Menu_SetPreciseMesh_Operator (bpy.types.Operator):
    bl_idname = "wm.menu_setprecisemesh_operator"
    bl_label = "Pop-up Menu"
    bl_description = "To make it convenient to use the pop-up menu You can assign shortcut \n \
         ( For exaple Ctrl + Alt + Wheel Down )\n \
        How to do it: > right-click on this button > Assign Shortcut"
        
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event): 
        
        # return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self, width=600, height=500)
        # return context.window_manager.invoke_popup(self)
        return context.window_manager.invoke_popup(self, width = 200)
        # if self.return == {"CANCELLED"}:
            # context.window_manager.invoke_popup(self, width = 200)

        # return  

        # return context.window_manager.invoke_props_popup(self, event)
        # return context.window_manager.invoke_confirm(self, event)
    def draw(self, context):
        bpy.types.VIEW3D_PT_edit_mesh_set_precise_mesh1.draw(self, context)
    # def draw(self, context):
    #     layout = self.layout

    #     scene = context.scene
    #     sc = scene
    #     ob = context.object

    #     w_m = context.window_manager.setprecisemesh

    #     # Get values
    #     bool_panel_arrow = bpy.data.scenes[bpy.context.scene.name_full].bool_panel_arrow
    #     bool_panel_arrow2 = bpy.data.scenes[bpy.context.scene.name_full].bool_panel_arrow2

    #     col = layout.column(align=True)
        
    #     split = col.split(factor=0.85, align=True)
    #     split.scale_y =1.2      

    #     split.operator("mesh.change_angle", icon="DRIVER_ROTATIONAL_DIFFERENCE")

        
    
    #     if sc.bool_panel_arrow:
    #         split.prop(sc, "bool_panel_arrow", text="", icon='DOWNARROW_HLT')
    #     else:
    #         split.prop(sc, "bool_panel_arrow", text="", icon='RIGHTARROW')

    #     if sc.bool_panel_arrow:
            
    #         box = col.column(align=True).box().column()
    #         col_top = box.column(align=True)
            
    #         col_top.prop(w_m, "angle")
    #         col_top.prop(w_m, "anglebool" )
    #         # col_top.prop(ob, "angleinput")         
                    
    #     col = layout.column(align=False)
    #     col = layout.column(align=True)

        
    #     split = col.split(factor=0.85, align=True)
    #     split.scale_y =1.2
        
    #     split.operator("mesh.change_length",icon="DRIVER_DISTANCE")
        
    
    #     if sc.bool_panel_arrow2:
    #         split.prop(sc, "bool_panel_arrow2", text="", icon='DOWNARROW_HLT')
    #     else:
    #         split.prop(sc, "bool_panel_arrow2", text="", icon='RIGHTARROW')

    #     if sc.bool_panel_arrow2:            
    #         box = col.column(align=True).box().column()            
    #         col_top = box.column(align=True)
    #         col_top.prop(w_m, "length")            
    #         col_top.prop(w_m, "lengthbool") 
                       
            # col_top.prop(ob, "lengthinput")

"""Operators"""
class Set_Cursor_To_Normal (bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.set_cursor"
    bl_label = "Set Cursor to normal face"
    bl_description = "You can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        bpy.context.object.update_from_editmode()
        bmesh.update_edit_mesh(me, True, True)
        bpy.context.scene.update_tag()
        bpy.context.view_layer.update()

    
        # obj = bpy.context.object
        # text = "You need to select from 1 to 4 vertices"
        # war = "ERROR"
        # self.report({war}, text)


        
        #Create lists
        vec = []
        ind = []

        #Append to lists                                                            
        for g in bm.select_history:
            # if len(vec)<3:
                vec.append(bm.verts[g.index].co)
                # ind.append(g.index)

        selected_faces = [face for face in bm.faces if face.select]
        try:
            my_location = selected_faces[0].calc_center_median()
        except IndexError:
            text = "You need to select all vertices of the face"
            war = "ERROR"
            self.report({war}, text)

            return {"FINISHED"}

        
        matrix_location = bpy.context.active_object.matrix_world @ my_location
        bpy.context.scene.cursor.location = matrix_location

        g = len(vec)
        # print(g)
        for k in range (0, g):
            vec[k] = bpy.context.active_object.matrix_world  @ vec[k] # 1 selected

        normallistgl = vec
        normalgl = mathutils.geometry.normal(normallistgl)

        # Set cursor direction
        obj_camera = bpy.data.scenes[bpy.context.scene.name_full].cursor       
        direction = normalgl
        # point the cameras '-Z' and use its 'Y' as up
        rot_quat = direction.to_track_quat('-Z', 'Y')
        obj_camera.rotation_euler = rot_quat.to_euler()
        rot_quat =  rot_quat.to_euler()

        

        # print(normalgl," Normal was calculated")

        return {'FINISHED'}

class Browser_Link (bpy.types.Operator):
    """Tooltip"""
    bl_idname = "wm.setprecisemesh_link"
    bl_label = "Change version"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.wm.url_open(url = "https://github.com/rovh/Set-Precise-Mesh/releases")
        return {"FINISHED"}

items = [('one', 'Any', "", 'PRESET', 1), ('two', 'PropertyGroup', "", 'PRESET', 2), ('three', 'type', "", 'PRESET', 3)]

class ChooseItemOperator(bpy.types.Operator):
    bl_idname = "example.choose_item"
    bl_label = "Choose item"
    bl_options = {'INTERNAL'}
    bl_property = "enum"

    def get_enum_options(self, context):
        global items
        return items

    enum: EnumProperty(items=get_enum_options, name="Items")
    node_tree: StringProperty()
    node: StringProperty()

    def execute(self, context):
        tree = bpy.data.node_groups[self.node_tree]
        node = tree.nodes[self.node]
        node.item_set = True
        node.set_item(self.enum)
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"FINISHED"}

class NewItemOperator(bpy.types.Operator):
    bl_idname = "example.new_item"
    bl_label = "New Item"
    bl_options = {'INTERNAL'}

    node_tree: StringProperty()
    node: StringProperty()

    def execute(self, context):
        global items
        tree = bpy.data.node_groups[self.node_tree]
        node = tree.nodes[self.node]
        node.item_set = True
        newitem = ('four', 'type', "", 'PRESET', 4)
        items.append(newitem)
        node.set_item(newitem)
        return {'FINISHED'}

class ClearItemOperator(bpy.types.Operator):
    bl_idname = "example.clear_item"
    bl_label = "Clear Item"
    bl_options = {'INTERNAL'}

    node_tree: StringProperty()
    node: StringProperty()

    def execute(self, context):
        tree = bpy.data.node_groups[self.node_tree]
        node = tree.nodes[self.node]
        node.item_set = False
        return {'FINISHED'}


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


        col = layout.column(align=True)

        
        
        split = col.split(factor=0.85, align=True)
        split.scale_y =1.2      

        split.operator("mesh.change_angle", icon="DRIVER_ROTATIONAL_DIFFERENCE")

        
    
        if sc.bool_panel_arrow:
            split.prop(sc, "bool_panel_arrow", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(sc, "bool_panel_arrow", text="", icon='RIGHTARROW')

        if sc.bool_panel_arrow:
            
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            
            col_top.prop(w_m, "angle")
            col_top.prop(w_m, "anglebool" )
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
                    
        col = layout.column(align=False)
        col = layout.column(align=True)

        
        split = col.split(factor=0.85, align=True)
        split.scale_y =1.2
        
        split.operator("mesh.change_length",icon="DRIVER_DISTANCE")
        
    
        if sc.bool_panel_arrow2:
            split.prop(sc, "bool_panel_arrow2", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(sc, "bool_panel_arrow2", text="", icon='RIGHTARROW')

        if sc.bool_panel_arrow2:            
            box = col.column(align=True).box().column()            
            col_top = box.column(align=True)
            col_top.prop(w_m, "length")            
            col_top.prop(w_m, "lengthbool") 
                     
            # col_top.prop(ob, "lengthinput")
            # col_top.operator(bpy.ops.ui.eyedropper_id.idname())
            # col_top.operator(bpy.ops.wm.url_open(url = "https://github.com/rovh/Set-Precise-Mesh"))
            
"""Preferences"""
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


    def draw(self, context):
        layout = self.layout
        
        # col = layout.column()

        
        box = layout.box()
        box.label(icon="PREFERENCES", text = "Preferences")
        row = box.row()
        col = row.column()
        # col.label(text="Tab Category:")
        col.prop(self, "direction_of_length", text='Invert "Set Length" direction')
        # col.prop(self, "direction_of_angle", text='Invert "Set Angle" direction')
        col.operator("wm.menu_setprecisemesh_operator",icon="MENU_PANEL", text="Pop-up Menu (Hover cursor on it for more information)")
        col.prop(self, "bool_warning_global", text='Show Warning Panel in Blender (Global)')
        # row = layout.row()
        # row.scale_x = 0.1
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
    )
    data_block_2: bpy.props.StringProperty(
        name = "Number input",
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
        
"""Duplication of Main panel"""
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
    
"""Classes registration"""
blender_classes = [
    Dupli,
    Dupli2,
    # SetPresiceMesh_Panel,
    SetAngle,
    SetLength,
    Dialog_Warning_Operator,
    Dialog_Warning_Operator_2,
    Dialog_Warning_Operator_3,
    SetPreciseMesh_Props,
    SetPreciseMesh_Preferences,
    Popup_Menu_SetPreciseMesh_Operator,
    Header_SetPreciseMesh,
    Set_Cursor_To_Normal,
    Browser_Link,
    ChooseItemOperator,
    NewItemOperator,
    ClearItemOperator,
]

def register():
    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)
    # pynput.register()

    bpy.types.WindowManager.setprecisemesh = PointerProperty(type=SetPreciseMesh_Props)
    bpy.types.VIEW3D_HT_tool_header.append(header_draw)
    bpy.types.Scene.my_property = PointerProperty(type=bpy.types.Object)

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
            name="data_block",
            description="",
            default=False,
    )
    bpy.types.Scene.script_input_2 = bpy.props.BoolProperty(
            name="data_block",
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


if __name__ == "__main__":
    register()
