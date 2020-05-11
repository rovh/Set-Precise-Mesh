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
    "name" : "Set Presice Mesh",
    "author" : "Rovh",
    "description" : "This addon allows you to set exact values for the mesh",
    "blender" : (2, 82, 0),
    "version" : (1),
    "location" : "View3D > Sidebar in Edit Mode > Item Tab and View Tab",
    "warning" : "",
    # "wiki_url": "https://github.com/rovh/Set-Precise-Mesh",
    "category" : "Mesh"
}

import bpy

from .SetAngle import *
from .SetLength import *

from bpy import types
from bpy.props import (
        FloatProperty,
        BoolProperty
        )



class DialogWarningOperator(bpy.types.Operator):
    bl_idname = "object.dialog_warning_operator"
    bl_label = "Warning Panel Operator"

    def execute(self, context):
        return {'FINISHED'}


    def invoke(self, context, event): 
        bool123 = bpy.data.scenes[bpy.context.scene.name_full].bool_warning
        if bool123 == 1:
            # return context.window_manager.invoke_props_dialog(self)
            return context.window_manager.invoke_popup(self, width=600, height=500)
            # return context.window_manager.invoke_popup(self)
            # return context.window_manager.invoke_props_popup(self, event)
            # return context.window_manager.invoke_confirm(self, event)
        else:
            return {'FINISHED'}


    def draw(self, context):
        layout = self.layout
        layout.label(text='Warning' , icon="ERROR")

        if bpy.context.object.scale != Vector((1.0, 1.0, 1.0)):
            
            layout.label(text='Your object scale is not correct. Please, apply "Scale"')
            layout.label(text='Shortcut: Objetc Mode > Ctrl A > Apply "Scale"')

        elif bpy.context.object.delta_scale != Vector((1.0, 1.0, 1.0)):

            layout.label(text='Your object delta transform scale is not correct. Please, change it')
            layout.label(text='How to do it: Properties Editor > Object Properties > Transform > Delta Transform >')
            layout.label(text='> You need to set values: All Scales = 1')

        layout.prop(context.scene, "bool_warning", text="Show Warning Panel next time")
        layout.label(text="Warning Panel will appear if object scale or delta scale is not correct")
        layout.label(text='You can find more info about this warning in README.md on Github page or in files')
        # layout.label(text='https://github.com/rovh/Set-Precise-Mesh')


class SetPresiceMesh(bpy.types.Panel):
    
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
            
            col_top.prop(ob, "angle")
            col_top.prop(ob, "anglebool" )
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
            col_top.prop(ob, "length")            
            col_top.prop(ob, "lengthbool")            
            # col_top.prop(ob, "lengthinput")
        
        
    
class Dupli(SetPresiceMesh):
    bl_label = "Set Presice Mesh1"
    bl_idname = "VIEW3D_PT_edit_mesh_set_precise_mesh1"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "View"
    bl_label = "Set Precise Mesh /CAD"
    # bl_order = 1
 
class Dupli2(SetPresiceMesh):
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

]


def register():
    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)
    # pynput.register()



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
        description="Warning Panel will appear if object scale or delta scale is not correct \n You can enable it or disable in \n Property Editor > Scene Properties > Custom Properties",
        default=1,
        options = {"SKIP_SAVE"}
    )
    bpy.types.Object.angle = bpy.props.FloatProperty(
        name="Angle",
        description="Radius",
        min=0.0, max=360.0,
        default=0.0,
        step = 100.0,
        unit="ROTATION",
        precision = 6,
    )
    bpy.types.Object.anglebool = bpy.props.BoolProperty(
        name="Change adjacent edge",
        description="Change the length of the opposite edge OR Change the length of the adjacent edge",
        default=False,
    )
    bpy.types.Object.angleinput = bpy.props.BoolProperty(
        name="Input Mode",
        description="",
        default=False,
    )
    bpy.types.Object.length = bpy.props.FloatProperty(
        name="Length",
        description="Length of the edge",
        default=1.0,
        step = 100.0,
        unit='LENGTH',
        precision = 6,
    )
    bpy.types.Object.lengthbool = bpy.props.BoolProperty(
        name="Use two directions",
        description='Change length in two directions OR in the direction of the active vertex',
        default=False,
    )
    bpy.types.Object.lengthinput = bpy.props.BoolProperty(
        name="Input Mode",
        description='User Mode',
        default=False,
    )

def unregister():
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)

    del bpy.types.Object.angle
    del bpy.types.Object.anglebool
    del bpy.types.Object.length
    del bpy.types.Object.lengthbool
    del bpy.types.Object.lengthinput

    del bpy.types.Scene.bool_panel_arrow
    del bpy.types.Scene.bool_panel_arrow2
    del bpy.types.Scene.bool_warning

if __name__ == "__main__":
    register()
