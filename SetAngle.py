import bpy
import bmesh
from bmesh.types import BMVert
import math
from math import radians
from math import degrees
from math import pi
import mathutils
from mathutils import geometry
from mathutils import Vector, Matrix, Quaternion, Euler


# from pynput.keyboard import Key, Controller

# keyboard = Controller()





def check(self):
    obj = bpy.context.object
    text = 'Your object scale is not correct. Please, apply "Scale" \n Shortcut: Objetc Mode > Ctrl A > Apply "Scale"'
    war = "ERROR"
    
    #Check scale
    if obj.scale != Vector((1.0, 1.0, 1.0)):      
        self.report({war}, text)



def check2(self):
    obj = bpy.context.object
    text = 'Your object delta transform scale is not correct. Please, change it. \n How to do it: Properties Editor > Object Properties > Transform > Delta Transform > You need to set values: \n All Scales = 1'
    war = "ERROR"

    # Check delta scale
    if bpy.context.object.delta_scale != Vector((1.0, 1.0, 1.0)):
        self.report({war}, text)

def check3(self):
    obj = bpy.context.object
    text = "You need to select 3 vertices"
    war = "ERROR"
    self.report({war}, text)

    



class SetAngle(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.change_angle"
    bl_label = "Set Angle"
    bl_description = "Set Angle"
    bl_options = {'REGISTER', 'UNDO'}

    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None


    def execute(self, context):
                
        check(self)
        check2(self)

        bpy.context.object.update_from_editmode()

        
        height = bpy.data.objects[bpy.context.active_object.name_full].angle
        bool = bpy.data.objects[bpy.context.active_object.name_full].anglebool
        bool2 = bpy.data.objects[bpy.context.active_object.name_full].angleinput

        
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        bmesh.update_edit_mesh(me, True, True)
        
        vec = []
        ind = []

        for g in bm.select_history:
            # if len(vec)<3:
                vec.append(bm.verts[g.index].co)
                ind.append(g.index)


        # Check number
        if len(vec)<3:
            check3(self)
            return{"FINISHED"}


            

        
        bmesh.update_edit_mesh(me, True, True)
        
        mind=ind[1]

        v1=vec[0]
        v2=vec[1]
        v3=vec[2]
        oldv3=vec[2]
        

        # Angle between verteses
        v1ch=v1-v2
        v3ch=v3-v2
        angle = v3ch.angle(v1ch, 0.0)


        bm.verts[ind[0]].select = 0
        bm.verts[ind[1]].select = 0
        bm.verts[ind[2]].select = 1


        context = bpy.context
        scene = context.scene
        ob = context.edit_object

        #pp = Cursor location
        bpy.context.scene.cursor.location = bpy.context.active_object.matrix_world  @ v2
        


        vec1 = bpy.context.active_object.matrix_world  @ v1
        vec2 = bpy.context.active_object.matrix_world  @ v2
        vec3 = bpy.context.active_object.matrix_world  @ v3
         

        # Calculate global normal
        normallistgl = [vec1,vec2,vec3]
        normalgl = mathutils.geometry.normal(normallistgl)


        # Calculate local normal
        normallist = [v1,v2,v3]
        normal = mathutils.geometry.normal(normallist)

         
        # Set cursor direction
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
        pp = v2
        S.translation -= pp      
        
        
        if bool2 == 1:              
            R = Matrix.Rotation(angle, 4, (normal))
            
            bmesh.ops.rotate(bm, 
                    matrix=R,        
                    verts=[v for v in bm.verts if v.select],
                    space=S,
                    )
            bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'

                        
            bpy.context.object.update_from_editmode()
            bmesh.update_edit_mesh(me, True, True)


            bpy.ops.transform.rotate("INVOKE_DEFAULT")
            # bpy.context.active_operator.options.use_cursor_region = True
        

            bpy.context.object.update_from_editmode()
            bmesh.update_edit_mesh(me, True, True)
            
            
        else:
            
            
            R = Matrix.Rotation(angle-height, 4, (normal))
            
            bmesh.ops.rotate(bm, 
                    matrix=R,        
                    verts=[v for v in bm.verts if v.select],
                    space=S,
            )    
        
        
        
        
        
        if bool == 1:
            
            obj = context.active_object

        
        
            newv3 = obj.data.vertices[ind[2]].co

            print(oldv3, "old")
            print(newv3, "new")
            print(newv3, "new")
            print(bool, "bool")
            



            print(v1, "iv1")
            print(oldv3, "iv2")
            print(v2, "iv3")
            print(newv3, "iv4")

            
            iv1=v1
            iv2=newv3
            iv3=v2
            iv4=oldv3
            
            print(iv1, "iv1")
            print(iv2, "iv2")
            print(iv3, "iv3")
            print(iv4, "iv4")
            
            
             

            iv = geometry.intersect_line_line(iv1, iv2, iv3, iv4)
            if iv:
                iv = (iv[0] + iv[1]) / 2

                bm.verts[ind[2]].co = iv
                
                
                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, True, True)
            

        
        bpy.context.object.update_from_editmode()
        bmesh.update_edit_mesh(me, True, True)

        

            
        return {'FINISHED'}
if __name__ == "__main__":
    register()
