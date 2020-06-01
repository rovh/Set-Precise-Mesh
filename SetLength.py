import bpy

import bmesh

import math
from math import *
# from math import radians
# from math import pi

from bmesh.types import BMVert

import mathutils
from mathutils import geometry
from mathutils import Matrix
from mathutils import Vector, Matrix, Quaternion, Euler

# import pickle

from . import __name__


def check(self):
    obj = bpy.context.object    
    # Check scale
    if obj.scale != Vector((1.0, 1.0, 1.0)) or obj.delta_scale != Vector((1.0, 1.0, 1.0)):
        bpy.ops.object.dialog_warning_operator('INVOKE_DEFAULT')

class SetLength_Plus(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.change_length_plus"
    bl_label = "Plus Length / Distance"
    bl_description = 'Add/plus the length/distance to the selected item \
    \n\
    \nYou can also assign shortcut\
    \nHow to do it: > right-click on this button > Assign Shortcut'
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        # The script crashes due to the fact that "self.report"
        # as I understand does not work  it in the case of embedding one operator in another

        try:
            bpy.ops.mesh.change_length(plus_length = 1)
        except RuntimeError:
            text = "You need to select 2 vertices"
            war = "ERROR"
            self.report({war}, text)


        # bpy.ops.mesh.change_length(plus_length = 1)


        return {"FINISHED"}

class SetLength_Minus(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.change_length_minus"
    bl_label = "Minus Length / Distance"
    bl_description = 'Reduse/Minus the length/distance of the selected item \
    \n\
    \nYou can also assign shortcut\
    \nHow to do it: > right-click on this button > Assign Shortcut'
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        # The script crashes due to the fact that "self.report"
        # as I understand does not work  it in the case of embedding one operator in another

        try:
            bpy.ops.mesh.change_length(plus_length = -1)
        except RuntimeError:
            text = "You need to select 2 vertices"
            war = "ERROR"
            self.report({war}, text)


        # bpy.ops.mesh.change_length(plus_length = 1)


        return {"FINISHED"}

class SetLength_Copy(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.change_length_copy"
    bl_label = "Set Length / Distance"
    bl_description = '  You can also assign shortcut \
    \n  How to do it: > right-click on this button > Assign Shortcut'
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        # The script crashes due to the fact that "self.report"
        # as I understand does not work  it in the case of embedding one operator in another

        # try:
        #     bpy.ops.mesh.change_length()
        # except RuntimeError:
        #     text = "You need to select 2 vertices"
        #     war = "ERROR"
        #     self.report({war}, text)

        bpy.ops.mesh.change_length()


        return {"FINISHED"}


class SetLength(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.change_length"
    bl_label = "Set Length / Distance"
    bl_description = 'Set Length / Distance \n You can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut'
    bl_options = {'REGISTER', 'UNDO'}

    plus_length: bpy.props.IntProperty() 
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        
        check(self)

        # Set values
        data_block_2 = bpy.context.window_manager.setprecisemesh.data_block_2
        
        """Replace syntax"""
        data_block_2 = data_block_2.replace(',', '.')
        data_block_2 = data_block_2.replace('^', '**')
        data_block_2 = data_block_2.replace(':', '/')


        script_input_2 = bpy.context.scene.script_input_2
        length_unit = bpy.context.scene.unit_settings.length_unit

        
        if script_input_2 == 1:

            try:
                eval(data_block_2)
            except SyntaxError:
                length = bpy.context.window_manager.setprecisemesh.length
            else:
                length = eval(data_block_2)
                length = length / bpy.context.scene.unit_settings.scale_length


                """Units Synchronization"""

                if  bpy.context.scene.unit_settings.system == 'METRIC' and length_unit == 'ADAPTIVE':
                    unit = length
                    bpy.context.window_manager.setprecisemesh.length =  unit
                    length = unit
                elif length_unit == "MICROMETERS":
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
                

                if bpy.context.scene.unit_settings.system == 'IMPERIAL'and length_unit == 'ADAPTIVE':
                    unit = length / 3.2808398950131
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
                
        
        # Get values
        prog = context.window_manager.setprecisemesh.projection_type_2
        settings = bpy.context.preferences.addons[__name__].preferences
        invert_direction = settings.direction_of_length


        # remember_length = bpy.types.Scene.remember_length

        # invert_direction_local = invert_direction_local
        # remember_invert_direction = False
        # result = 1
        # try:
        #     result = list(set(remember_length) ^ set(ind))
        #     pass
        # except TypeError:
        #     print("TypeError")
        #     pass
        # else:
        #     result = list(set(remember_length) ^ set(ind))
        #     result = len(result)
        #     if result == 0:
        #         # def remember_invert_direction_for_length():
        #         bpy.ops.ed.undo()
        #         remember_invert_direction = True
        #         print("it works")
                

        # bpy.types.Scene.remember_length = ind
        # print(bpy.types.Scene.remember_length)
        
        # print(result)
        # if remember_invert_direction == 1:
            # vec.reverse()
            # vec = remember_length.reverse()
            # ind = remember_length.reverse()
            # ind.reverse()
            # vec.reverse()
            # ind.reverse()

        

        offset = False 

        # Check number
        if len(vec) < 1:
            text = "You need to select from 1 vertices"
            war = "ERROR"
            self.report({war}, text)
            return{"FINISHED"}


        elif len(vec) == 1:

            v2 = vec[0] 

            offset = False 
            offset_unit = 50          

            if prog == "global_matrix":

                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, True, True)

                wm = bpy.context.active_object.matrix_world.copy()
                wm = wm.inverted()

                v2_prg = bpy.context.active_object.matrix_world  @ v2
                              
                v1 = mathutils.Vector((v2_prg[0], v2_prg[1] , 0)) # 1 selected simulate

                v1 = wm @ v1  

                if v1 == v2:
                    offset = True 

                    v2[0] = v2_prg[0]
                    v2[1] = v2_prg[1]
                    v2[2] = offset_unit
        
                    v2 = wm @ v2


                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, True, True)

            elif prog == "local_matrix":

                v2_prg = v2

                v1 = mathutils.Vector((v2_prg[0], v2_prg[1] , 0)) # 1 selected simulate

                if v1 == v2:
                    offset = True 

                    v2[0] = v2_prg[0]
                    v2[1] = v2_prg[1]
                    v2[2] =  offset_unit

            elif prog == "cursor_location":
                wm = bpy.context.active_object.matrix_world.copy()
                wm = wm.inverted()


                v1 = bpy.context.scene.cursor.location
                v2_prg = v1

                v1 = wm @ v1

                # if v1 == v2:
                #     offset = True 

                #     v2[0] = v2_prg[0]
                #     v2[1] = v2_prg[1]
                #     v2[2] = v2_prg[2] + offset_unit
        
                #     v2 = wm @ v2

            elif prog == "cursor_matrix":

                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, True, True)
                # bpy.context.scene.update_tag()
                # bpy.context.view_layer.update()
                # bpy.context.depsgraph.update()

                        
                obj_matrix = bpy.context.active_object.matrix_world.copy()
                obj_matrix_inverted = obj_matrix.inverted()


                cursor_loc =  bpy.context.scene.cursor.location


                cursor_matrix = bpy.context.scene.cursor.matrix.copy()
                cursor_matrix_inverted = cursor_matrix.inverted()


                mat_cur =  obj_matrix @ cursor_matrix_inverted
                # mat_cur =  cursor_matrix_inverted @ obj_matrix

                v2_prg =  mat_cur @ v2
                
                v1 = mathutils.Vector((v2_prg[0], v2_prg[1] , 0)) # 1 selected simulate

                mat_cur_inverted = mat_cur.inverted()
                v1 = mat_cur_inverted @ v1

                if v1 == v2:
                    offset = True

                    v2[0] = v2_prg[0]
                    v2[1] = v2_prg[1]
                    v2[2] = offset_unit   

                    v2 = mat_cur_inverted @ v2
                

                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, True, True)
                # bpy.context.scene.update_tag()
                # bpy.context.view_layer.update()

            elif prog == "custom_object_location": 

                obj_name = bpy.data.scenes[bpy.context.scene.name_full].my_property_2.name_full

                # obj_marx = bpy.data.objects[obj_name].matrix_world
                obj_loc = bpy.data.objects[obj_name].location

                wm = bpy.context.active_object.matrix_world.copy()
                wm = wm.inverted()

                v1 = obj_loc
                v1 = wm @ v1 

                # v1ch=v1-v2
                # v3ch=v3-v2
                # angle = v3ch.angle(v1ch, 0.0)
                # print(angle, "angle1111111111111")
                # if length_intersect != 0:

                # if angle == 0.0 :
                #     bpy.ops.object.dialog_warning_operator_3('INVOKE_DEFAULT')     

            elif prog == "custom_object_matrix":

                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, True, True)
                # bpy.context.scene.update_tag()
                # bpy.context.view_layer.update()

                obj_name = bpy.data.scenes[bpy.context.scene.name_full].my_property_2.name_full
                custom_obj_matrix = bpy.data.objects[obj_name].matrix_world

                custom_obj_matrix = custom_obj_matrix.copy()
                custom_obj_matrix_inverted = custom_obj_matrix.inverted()

                obj_matrix = bpy.context.active_object.matrix_world.copy()

                # mat = custom_obj_matrix_inverted @ obj_matrix
                mat = obj_matrix @ custom_obj_matrix_inverted

                v2_prg = mat @ v2
                
                v1 = mathutils.Vector((v2_prg[0], v2_prg[1] , 0)) # 1 selected simulate
                
                mat_inverted = mat.inverted()

                v1 = mat_inverted @ v1

                if v1 == v2 :
                    offset = True 

                    # v2 = mat_cur @ v2

                    v2[0] = v2_prg[0]
                    v2[1] = v2_prg[1]
                    v2[2] = offset_unit   

                    v2 = mat_inverted @ v2



                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, True, True)
                # bpy.context.scene.update_tag()
                # bpy.context.view_layer.update()

        else:


            # Invert direction for edge
            if invert_direction == 1:
                vec.reverse()
                ind.reverse()

            # Set values
            v1=vec[0]
            v2=vec[1]
            # lv=v2-v1

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
        try:
            if self.plus_length == 1:
                length = lengthtrue / (length + lengthtrue)
            elif self.plus_length == -1:
                length = lengthtrue / (-length + lengthtrue) 
            else:
                length = lengthtrue / length
        except ZeroDivisionError:
            bpy.ops.object.dialog_warning_operator_4('INVOKE_DEFAULT')
            return {"FINISHED"}

        # if offset == True:                     
            # length = length * (length / (length + offset_unit))

         
    
        context = bpy.context
        scene = context.scene
        ob = context.edit_object
        


        #Set Cursor location and mode
        if bool== 1:
            if prog != "cursor_matrix" and prog != "cursor_location":
                bpy.context.scene.cursor.location = bpy.context.active_object.matrix_world  @ mv
            pp = mv
        else:
            if prog != "cursor_matrix" and prog != "cursor_location":
                bpy.context.scene.cursor.location = bpy.context.active_object.matrix_world @ v1
            pp = v1
        
        if prog != "cursor_matrix" and prog != "cursor_location": 
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
                  
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bpy.context.object.update_from_editmode()
        bmesh.update_edit_mesh(me, True, True)

        return {'FINISHED'}


if __name__ == "__main__":
    register()

