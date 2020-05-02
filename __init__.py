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
    "version" : (1.0, "Beta"),
    "location" : "View3D > Sidebar in Edit Mode > Item Tab and View Tab",
    "warning" : "",
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




bpy.types.Scene.my = bpy.props.BoolProperty(
        name="my",
        description="Radius",
        default=True,
    )
bpy.types.Scene.my2 = bpy.props.BoolProperty(
        name="my2",
        description="Radius",
        default=True,
    )

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

        my = bpy.data.scenes[bpy.context.scene.name_full].my
        my2 = bpy.data.scenes[bpy.context.scene.name_full].my2

        col = layout.column(align=True)

        
        split = col.split(factor=0.85, align=True)
        split.scale_y =1.2
        

        
        split.operator("mesh.change_angle", icon="DRIVER_ROTATIONAL_DIFFERENCE")

        
    
        if sc.my:
            split.prop(sc, "my", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(sc, "my", text="", icon='RIGHTARROW')

        if sc.my:
            
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
        
    
        if sc.my2:
            split.prop(sc, "my2", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(sc, "my2", text="", icon='RIGHTARROW')
        if sc.my2:
            
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
 
class Dupli2(SetPresiceMesh):
    bl_label = "Set Presice Mesh2"
    bl_idname = "VIEW3D_PT_edit_mesh_set_precise_mesh2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"
    bl_label = "Set Precise Mesh /CAD"
    
 
blender_classes = [
    Dupli,
    Dupli2,
    SetAngle,
    SetLength,

]


def register():
    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)
    # pynput.register()

    bpy.types.Object.angle = bpy.props.FloatProperty(
        name="Angle",
        description="Radius",
        min=0.0, max=360.0,
        default=0.0,
        step = 100.0,
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

if __name__ == "__main__":
    register()
