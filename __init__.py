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
    "version" : (1,0,3),
    "location" : "View3D > Sidebar in Edit Mode > Item Tab and View Tab",
    "warning" : "",
    "wiki_url": "https://github.com/rovh/Set-Precise-Mesh",
    "category" : "Mesh"
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
        )


class DialogWarningOperator(bpy.types.Operator):
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

class MenuSetPreciseMeshOperator(bpy.types.Operator):
    bl_idname = "wm.menu_setprecisemesh_operator"
    bl_label = "Pop-up Menu"
    bl_description = "To make it convenient to use the pop-up menu You can assign shortcut \n \
         (For exaple Alt+R )\n \
        How to do it: > right-click on this button > Assign Shortcut"
        
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event): 
        
        # return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self, width=600, height=500)
        # return context.window_manager.invoke_popup(self)
        return context.window_manager.invoke_popup(self, width = 200)
        # return context.window_manager.invoke_props_popup(self, event)
        # return context.window_manager.invoke_confirm(self, event)

    
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
            # col_top.prop(ob, "angleinput")         
                    
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


class SetPreciseMeshPreferences(bpy.types.AddonPreferences):
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
        layout.label(icon="PREFERENCES")

        row = layout.row()
        col = row.column()
        # col.label(text="Tab Category:")
        col.prop(self, "direction_of_length", text='Invert "Set Length" direction')
        # col.prop(self, "direction_of_angle", text='Invert "Set Angle" direction')
        col.operator("wm.menu_setprecisemesh_operator",icon="MENU_PANEL", text="Pop-up Menu (Hover cursor on it for more information)")
        col.prop(self, "bool_warning_global", text='Show Warning Panel in Blender (Global)')

class Header_Set_Precise_Mesh(bpy.types.Operator):
   
    bl_idname = "wm.header_setprecisemesh_operator"
    bl_label = "Header Menu"
    bl_description = "To make it convenient to use the pop-up menu You can assign shortcut \n \
         (For exaple Alt+R )\n \
        How to do it: > right-click on this button > Assign Shortcut"
        
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event): 
        
        # return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self, width=600, height=500)
        return context.window_manager.invoke_popup(self)
        # return context.window_manager.invoke_popup(self, width = 200)
        # return context.window_manager.invoke_props_popup(self, event)
        # return context.window_manager.invoke_confirm(self, event)
    def draw(self, context):
        # row = layout.row()
        # col = row.column()
        # col.prop(orient_slot, "type", expand=True)
        # w_m = context.window_manager.setprecisemesh
        # col.prop(w_m, "projection_type" , expand=True)
        layout=self.layout

        column = layout.column(align=True)
        # row = column.row()
        # row.prop(self, "tabs", expand=True)
        w_m = context.window_manager.setprecisemesh
        column.prop(w_m, "projection_type" , expand=True)




def header_search_draw2(self, context):
    layout = self.layout
    object_mode = context.active_object.mode


    if object_mode in {'EDIT'}:

        # layout.menu("VIEW3D_HT_header.draw_xform_template(layout, context)")
        
        row = layout.row(align=1)
        
        sub = row.row()
        sub.ui_units_x = 3
        layout.separator()
        row.operator("wm.header_setprecisemesh_operator", text="Projection type", icon = "AXIS_TOP")


class SetPresiceMeshPanel(bpy.types.Panel):
    
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
            col_top.prop(self, "projection_type")
            # col_top.prop(ob, "angleinput")
            row = layout.row(align=True)

            sub = row.row()
            sub.ui_units_x = 5
            sub.prop_with_popover(
                self,
                "projection_type",
                text="",
                panel="VIEW3D_PT_Set_Precise_Mesh",
            )         
                    
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

        

class SetPreciseMeshProps(bpy.types.PropertyGroup):
    """
    Fake module like class
    bpy.context.window_manager.setprecisemesh
    """
    angle: bpy.props.FloatProperty(
        name="Angle",
        description="Angle",
        min=0.0, max=360.0,
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
    projection_type: bpy.props.EnumProperty(
        name="Projection type",
        items=(
            ("global_matrix"  , "Global Matrix"  , "Global Matrix"  , "WORLD_DATA" , 0),
            ("local_matrix"   , "Local Matrix"   , "Local Matrix"   ,          ),
            ("cursor_location", "Cursor Location", "Cursor Location",        ),
            ("cursor_matrix"  , "Cursor Matrix"  , "Cursor Matrix"  ,         ),
            ("custon_object"  , "Custon Object"  , "Custon Object"  ,           ),
        ),
        description="Algorithm used for interpolation",
        default='global_matrix'
        )
        
    
class Dupli(SetPresiceMeshPanel):
    bl_label = "Set Presice Mesh1"
    bl_idname = "VIEW3D_PT_edit_mesh_set_precise_mesh1"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "View"
    bl_label = "Set Precise Mesh /CAD"
    # bl_order = 1
 
class Dupli2(SetPresiceMeshPanel):
    bl_label = "Set Presice Mesh2"
    bl_idname = "VIEW3D_PT_edit_mesh_set_precise_mesh2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"
    bl_label = "Set Precise Mesh /CAD"
    # bl_order = 1
    
 
blender_classes = [
    Dupli,
    Dupli2,
    SetAngle,
    SetLength,
    DialogWarningOperator,
    SetPreciseMeshProps,
    SetPreciseMeshPreferences,
    MenuSetPreciseMeshOperator,
    Header_Set_Precise_Mesh,


]


def register():
    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)
    # pynput.register()

    bpy.types.WindowManager.setprecisemesh = PointerProperty(type=SetPreciseMeshProps)
    # bpy.types.VIEW3D_MT_editor_menus.append(header_search_draw2)
    # bpy.types.VIEW3D_HT_header.append(header_search_draw2)
    bpy.types.VIEW3D_HT_tool_header.append(header_search_draw2)

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
    bpy.types.Scene.bool_warning = bpy.props.BoolProperty(
        name="Show this warning panel next time",
        description="Warning Panel will appear if object scale or delta scale is not correct \n You can also enable it or disable in \n Property Editor > Scene Properties > Custom Properties",
        default=1,
        options = {"SKIP_SAVE"}
    )


def unregister():
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)

    del bpy.types.WindowManager.setprecisemesh

    del bpy.types.Scene.bool_panel_arrow
    del bpy.types.Scene.bool_panel_arrow2
    del bpy.types.Scene.bool_warning

    # bpy.types.VIEW3D_MT_editor_menus.remove(header_search_draw2)
    # bpy.types.VIEW3D_HT_header.remove(header_search_draw2)
    bpy.types.VIEW3D_HT_tool_header.remove(header_search_draw2)


if __name__ == "__main__":
    register()
