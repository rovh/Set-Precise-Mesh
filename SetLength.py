import bpy

import bmesh

import math
from math import radians
from math import pi

from bmesh.types import BMVert

import mathutils
from mathutils import geometry
from mathutils import Matrix
from mathutils import Vector, Matrix, Quaternion, Euler







def check(self):
    obj = bpy.context.object

    text = 'Your object transforms are not correct. Please, apply "All Transforms" \n Shortcut: Objetc Mode > Ctrl A > Apply "All Transforms"'
    
    war = "ERROR"
        #Check rotation
    if obj.rotation_quaternion != Quaternion((1.0, 0.0, 0.0, 0.0)):
        self.report({war}, text)
        
    elif obj.rotation_euler[0] != 0.0:
        self.report({war}, text)
    elif obj.rotation_euler[1] != 0.0:
        self.report({war}, text)
    elif obj.rotation_euler[2] != 0.0 :
        self.report({war}, text)
        
        #Check location
    elif obj.location != Vector((0.0, 0.0, 0.0)):
        self.report({war}, text)
        
        #Check scale
    elif obj.scale != Vector((1.0, 1.0, 1.0)):      
        self.report({war}, text)




class SetLength(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.change_length"
    bl_label = "Set Length"
    bl_description = "Set Length"
    bl_options = {'REGISTER', 'UNDO'}

 


    @classmethod
    def poll(cls, context):
        
        return context.active_object is not None

    def execute(self, context):
        
        check(self)

        
        length = bpy.data.objects[bpy.context.active_object.name_full].length
        bool = bpy.data.objects[bpy.context.active_object.name_full].lengthbool
        bool2 = bpy.data.objects[bpy.context.active_object.name_full].lengthinput
        
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        vec = []
        ind = []
        
        for g in bm.select_history:
            if len(vec)<3:
                vec.append(bm.verts[g.index].co)
#                print(g.index)
                ind.append(g.index)
                
        v1=vec[0]
        v2=vec[1]
        lv=v2-v1
        normal = lv

        # Length of the edge
        lengthtrue =lv.length
        
        
        # Center of the edge
        mv = (v1+v2)/2
        
        # Scale factor
        length = lengthtrue/length
        
        context = bpy.context
        scene = context.scene
        ob = context.edit_object
        
        #Set Cursor        
        if bool== 1:
            
            bpy.context.scene.cursor.location = mv
            pp = bpy.context.scene.cursor.location
        else:
            bpy.context.scene.cursor.location = v1
            pp = bpy.context.scene.cursor.location
            
            
        
        
        obj_camera = bpy.data.scenes[bpy.context.scene.name_full].cursor

        loc_camera = bpy.data.scenes[bpy.context.scene.name_full].cursor.matrix.to_translation()
         
        point =  normal
         
        direction = point 
        # point the cameras '-Z' and use its 'Y' as up
        rot_quat = direction.to_track_quat('-Z', 'Y')

        obj_camera.rotation_euler = rot_quat.to_euler()
        
        
        
        
        
        
        S = ob.matrix_world.copy()
        S.translation -= pp
        
        
        
        if bool2 == 1:         
                                
            m = bpy.context.scene.tool_settings.transform_pivot_point
            bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'

            bpy.ops.transform.resize("INVOKE_DEFAULT")
            

            # Length of the edge
            
            bpy.context.scene.tool_settings.transform_pivot_point = m

            bmesh.update_edit_mesh(me, True)

                   
        else:
        
        
            R = Matrix.Scale(1/length, 3, (lv))
  
            bmesh.ops.rotate(bm, 
                    matrix=R,        
                    verts=[v for v in bm.verts if v.select],
                    space=S)
                    
            
            bmesh.update_edit_mesh(me, True)
                  
            
            
        return {'FINISHED'}



if __name__ == "__main__":
    register()

