import bpy

import bmesh

import math
# from math import radians
# from math import pi

from bmesh.types import BMVert

import mathutils
from mathutils import geometry
from mathutils import Matrix
from mathutils import Vector, Matrix, Quaternion, Euler

from . import __name__


def check(self):
    obj = bpy.context.object    

    # Check scale
    if obj.scale != Vector((1.0, 1.0, 1.0)) or obj.delta_scale != Vector((1.0, 1.0, 1.0)):
        bpy.ops.object.dialog_warning_operator('INVOKE_DEFAULT') 


def check3(self):
    obj = bpy.context.object
    text = "You need to select 2 vertices"
    war = "ERROR"
    self.report({war}, text)



class SetLength(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.change_length"
    bl_label = "Set Length / Distance"
    bl_description = 'Set Length / Distance \n You can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut'
    bl_options = {'REGISTER', 'UNDO'}

 


    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        
        check(self)

        # Set values
        data_block_2 = bpy.context.window_manager.setprecisemesh.data_block_2

        data_block_2 = data_block_2.replace(',', '.')
        data_block_2 = data_block_2.replace('^', '**')

        script_input_2 = bpy.context.scene.script_input_2
        length_unit = bpy.context.scene.unit_settings.length_unit

        
        if script_input_2 == 1:

            try:
                eval(data_block_2)
            except SyntaxError:
                length = bpy.context.window_manager.setprecisemesh.length
            else:
                length = eval(data_block_2)
                


                if length_unit == "MICROMETERS":
                    unit = length / 1000000
                    bpy.context.window_manager.setprecisemesh.length =  unit
                    length = unit
                elif length_unit == "MILLIMETERS":
                    unit = length / 1000
                    bpy.context.window_manager.setprecisemesh.length =  unit
                    length = unit
                elif length_unit == "CENTIMETERS":
                    unit = length / 100
                    bpy.context.window_manager.setprecisemesh.length =  unit
                    length = unit
                elif length_unit == "METERS":
                    unit = length
                    bpy.context.window_manager.setprecisemesh.length =  unit
                    length = unit
                elif length_unit == "KILOMETERS":
                    unit = length * 1000
                    bpy.context.window_manager.setprecisemesh.length =  unit
                    length = unit


                if length_unit == 'MILES':
                    unit = length  / 0.00062137119223733
                    bpy.context.window_manager.setprecisemesh.length =  unit
                    length = unit
                elif length_unit == 'FEET':
                    unit = length / 3.2808398950131
                    bpy.context.window_manager.setprecisemesh.length =  unit
                    length = unit
                elif length_unit == 'INCHES':
                    unit = length / 39.370078740157
                    bpy.context.window_manager.setprecisemesh.length =  unit
                    length = unit
                elif length_unit == 'THOU':
                    unit = length / 39.370078740157 / 1000
                    bpy.context.window_manager.setprecisemesh.length =  unit
                    length = unit
        else:
            length = bpy.context.window_manager.setprecisemesh.length




        bool = bpy.context.window_manager.setprecisemesh.lengthbool
        bool2 = bpy.context.window_manager.setprecisemesh.lengthinput
        
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        # Create list
        vec = []
        ind = []
        
        #Append to lists
        for g in bm.select_history:
            # if len(vec)<3:
                vec.append(bm.verts[g.index].co)
                ind.append(g.index)
                
        # Check number
        if len(vec)<2:
            check3(self)
            return{"FINISHED"}

        # Get values
        settings = bpy.context.preferences.addons[__name__].preferences
        invert_direction = settings.direction_of_length

        # Invert direction for edge
        if invert_direction == 1:
            vec.reverse()
            ind.reverse()

        # Set values
        v1=vec[0]
        v2=vec[1]
        lv=v2-v1


        # Get global normal 
        norv1 = bpy.context.active_object.matrix_world  @ v1
        norv2 = bpy.context.active_object.matrix_world  @ v2
        normalgl = norv2 - norv1

        

        # Length of the edge
        lengthtrue =lv.length
        
        
        # Center of the edge
        mv = (v1+v2)/2
        
        # Scale factor
        length = lengthtrue/length
        


        context = bpy.context
        scene = context.scene
        ob = context.edit_object
        


        #Set Cursor location and mode      
        if bool== 1:
            
            bpy.context.scene.cursor.location = bpy.context.active_object.matrix_world  @ mv
            pp = mv
        else:
            bpy.context.scene.cursor.location = bpy.context.active_object.matrix_world @ v1
            pp = v1
            
            
        
        # Set cursor rotation
        obj_camera = bpy.data.scenes[bpy.context.scene.name_full].cursor
        loc_camera = bpy.data.scenes[bpy.context.scene.name_full].cursor.matrix.to_translation()
        direction = normalgl
        # point the cameras '-Z' and use its 'Y' as up
        rot_quat = direction.to_track_quat('-Z', 'Y')
        obj_camera.rotation_euler = rot_quat.to_euler()
        
        
        # Create Matrix
        mat_loc =  mathutils.Matrix.Translation(( 0.0 ,  0.0 ,  0.0 ))        
        mat_sca =  mathutils.Matrix.Scale( 1.0 ,  4 ,  ( 0.0 ,  0.0 ,  1.0 ))
        mat_rot =  mathutils.Matrix.Rotation(0 ,  4 , "Z" )

        mat_out =  mat_loc @  mat_rot @  mat_sca
        
        
        S = mat_out
        S.translation -= pp
        
        
        
        if bool2 == 1:         
                                
            m = bpy.context.scene.tool_settings.transform_pivot_point
            bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'

            bpy.ops.transform.resize("INVOKE_DEFAULT")
            

            # Length of the edge
            
            bpy.context.scene.tool_settings.transform_pivot_point = m

            bmesh.update_edit_mesh(me, True)

                   
        else:
        
        
            R = Matrix.Scale(1/length, 4, (lv))
  
            bmesh.ops.rotate(bm, 
                    matrix=R,        
                    verts=[v for v in bm.verts if v.select],
                    space=S)
                    
            
            bmesh.update_edit_mesh(me, True)
                  
            
            
        return {'FINISHED'}



if __name__ == "__main__":
    register()

