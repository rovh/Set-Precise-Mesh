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

    # Check scale
    if obj.scale != Vector((1.0, 1.0, 1.0)) or obj.delta_scale != Vector((1.0, 1.0, 1.0)):
        bpy.ops.object.dialog_warning_operator('INVOKE_DEFAULT') 
    
        
def check3(self):
    obj = bpy.context.object
    text = "You need to select more than 1 vertex"
    war = "ERROR"
    self.report({war}, text)


class SetAngle(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.change_angle"
    bl_label = "Set Angle"
    bl_description = "Set Angle \n You can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut"
    bl_options = {'REGISTER', 'UNDO'}

    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None    

    def execute(self, context):
                
        check(self)

        # bpy.context.object.update_from_editmode()

        # Get values
        height = bpy.context.window_manager.setprecisemesh.angle
        bool = bpy.context.window_manager.setprecisemesh.anglebool
        bool2 = bpy.context.window_manager.setprecisemesh.angleinput

        
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        bpy.context.object.update_from_editmode()
        bmesh.update_edit_mesh(me, True, True)
        
        #Create lists
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

        # Differrent cases for progection
        prog = context.window_manager.setprecisemesh.projection_type

        bpy.context.object.update_from_editmode()
        bmesh.update_edit_mesh(me, True, True)

        """Check list of selected vertices"""
        Clear_angle = 0

        if len(vec) == 4:
            length_selected_vert = "Four"
            v0=vec[0] # 1 selected
            v1=vec[1] # 2 selected
            v2=vec[2] # 3 selected
            v3=vec[3] # 4 selected
            oldv3 = mathutils.Vector( vec[3] ) # 4 selected

        elif len(vec)==2:
            length_selected_vert = "Two"
            Clear_angle = 0

            v2=vec[0] # 2 selected
            v3=vec[1] #  3 selected
            oldv3= mathutils.Vector( vec[1] ) # 3 selected

            if prog == "global_matrix":

                Clear_angle = False

                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, True, True)

                v2_prg = bpy.context.active_object.matrix_world  @ v2
                v1 = bpy.context.active_object.matrix_world  @ v3

                wm = bpy.context.active_object.matrix_world.copy()
                wm = wm.inverted()
                              
                v1 = mathutils.Vector((v1[0], v1[1] , v2_prg[2])) # 1 selected simulate
                
                v3_prg = bpy.context.active_object.matrix_world  @ v3
                if v3_prg == v1 :
                    # print("global matrix 1")
                    Clear_angle = 1
                    if v2_prg[2] < 0:
                        v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] - 1.0)  ))
                    else:
                        v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] + 1.0)  ))
                    v3 = wm @ v3
                    oldv3 = v3
                if v2_prg == v1:
                    bpy.ops.object.dialog_warning_operator_2('INVOKE_DEFAULT') 

                v1 = wm @ v1  

                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, True, True)

            elif prog == "local_matrix":

                v2_prg = v2
                v1 = v3
                v1 = mathutils.Vector((v1[0], v1[1] , v2_prg[2])) # 1 selected simulate
                v3_prg = v3

                if v3_prg == v1 :
                    Clear_angle = 1
                    if v2_prg[2] < 0:
                        v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] - 1.0)  ))
                    else:
                        v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] + 1.0)  ))
                    oldv3 = v3
                if v2_prg == v1:
                    bpy.ops.object.dialog_warning_operator_2('INVOKE_DEFAULT')

            elif prog == "cursor_location":
                wm = bpy.context.active_object.matrix_world.copy()
                wm = wm.inverted()

                v3_prg = bpy.context.active_object.matrix_world  @ v3
                v2_prg =  bpy.context.active_object.matrix_world @ v2

                v1 = bpy.context.scene.cursor.location

                v1 = wm @ v1

                v1ch=v1-v2
                v3ch=v3-v2
                angle = v3ch.angle(v1ch, 0.0)

                if angle == 0.0 :
                    bpy.ops.object.dialog_warning_operator_3('INVOKE_DEFAULT') 
               
            elif prog == "cursor_matrix":

                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, True, True)

                obj_matrix = bpy.context.active_object.matrix_world.copy()
                cursor_matrix = bpy.context.scene.cursor.matrix.copy()
                # cursor_loc =  bpy.context.scene.cursor.location
                cursor_matrix_loc = bpy.context.scene.cursor.matrix.translation

                # cursor_matrix = cursor_matrix.inverted()
                obj_matrix = obj_matrix.inverted()

                mat_cur = obj_matrix @ cursor_matrix
                # mat_cur =  cursor_matrix @ obj_matrix
                # mat_cur = cursor_matrix
    
                v1 =  v3
                v1 = mat_cur @ v1

                v2_prg =  v2
                v2_prg = mat_cur  @ v2_prg

                v3_prg =  v3
                v3_prg = mat_cur @ v3_prg

                v1 = mathutils.Vector((v1[0], v1[1] , v2_prg[2])) # 1 selected simulate

                mat_cur = mat_cur.inverted()

                # v3_prg = mat_cur @ v3_prg

                if v3_prg == v1:
                    Clear_angle = True

                    if v2_prg[2] < cursor_matrix_loc[0]:
                        v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] - 100.0)  ))
                        print("Location grater than")
                    else:
                        v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] + 100.0)  ))
                        print("Location lower than")
                    v3 = mat_cur @ v3
                    oldv3 = v3

                v1 = mat_cur @ v1


                # if v2_prg == v1:
                if v2_prg == v1:
                    bpy.ops.object.dialog_warning_operator_2('INVOKE_DEFAULT')

                

                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, True, True)


            elif prog == "custom_object_location": 

                obj_name = bpy.data.scenes[bpy.context.scene.name_full].my_property.name_full

                # obj_marx = bpy.data.objects[obj_name].matrix_world
                obj_loc = bpy.data.objects[obj_name].location

                wm = bpy.context.active_object.matrix_world.copy()
                wm = wm.inverted()

                v1 = obj_loc
                v1 = wm @ v1 

                v1ch=v1-v2
                v3ch=v3-v2
                angle = v3ch.angle(v1ch, 0.0)
                # print(angle, "angle1111111111111")
                # if length_intersect != 0:

                if angle == 0.0 :
                    bpy.ops.object.dialog_warning_operator_3('INVOKE_DEFAULT')     

            elif prog == "custom_object_matrix":

                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, True, True)

                obj_name = bpy.data.scenes[bpy.context.scene.name_full].my_property.name_full
                custom_obj_matrix = bpy.data.objects[obj_name].matrix_world
                obj_matrix = bpy.context.active_object.matrix_world.copy()

                custom_obj_matrix = custom_obj_matrix.copy()
                custom_obj_matrix = custom_obj_matrix.inverted()

                mat = obj_matrix @ custom_obj_matrix

                v3_prg =  v3
                v3_prg = mat @ v3_prg

                v2_prg =  v2
                v2_prg =  mat @ v2_prg

                v1 = v3
                v1 = mat @ v1
                
                v1 = mathutils.Vector((v1[0], v1[1] , v2_prg[2])) # 1 selected simulate
                
                mat = mat.inverted()

                

                if v3_prg == v1 :
                    Clear_angle = 1
                    
                    if v2_prg[2] < 0:
                        v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] - 100.0)  ))
                    else:
                        v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] + 100.0)  ))
                    v3 = mat @ v3
                    oldv3 = v3

                v1 = mat @ v1

                if v2_prg == v1:
                    bpy.ops.object.dialog_warning_operator_2('INVOKE_DEFAULT')   

                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, True, True)
        
        else:
            length_selected_vert = "Three"
            v1=vec[0] # 1 selected
            v2=vec[1] # 2 selected
            v3=vec[2] #  3 selected
            oldv3 = mathutils.Vector( vec[2] ) # 3 selected

        bpy.context.object.update_from_editmode()
        bmesh.update_edit_mesh(me, True, True)


        if Clear_angle == 1:
            angle = 0.0
        else:
            v1ch=v1-v2
            v3ch=v3-v2
            angle = v3ch.angle(v1ch, 0.0)


        bmesh.update_edit_mesh(me, True, True)

        """Select cases for number of selected vertices"""
        if length_selected_vert == "Four":
            # Select vertices
            bm.verts[ind[0]].select = 0
            bm.verts[ind[1]].select = 0
            bm.verts[ind[2]].select = 0
            bm.verts[ind[3]].select = 1

        if length_selected_vert == "Three":
            # Select vertices
            bm.verts[ind[0]].select = 0
            bm.verts[ind[1]].select = 0
            bm.verts[ind[2]].select = 1
            # print ("Warning ")
        
        if length_selected_vert == "Two":
            # Select vertices
            bm.verts[ind[0]].select = 0
            bm.verts[ind[1]].select = 1
            # print ("selection works")


        context = bpy.context
        scene = context.scene
        ob = context.edit_object

        #pp = Cursor location
        if prog != "cursor_location" and prog != "cursor_matrix":
            bpy.context.scene.cursor.location = bpy.context.active_object.matrix_world  @ v2
        

        # Create global coordinates
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
        if prog != "cursor_location" and prog != "cursor_matrix":
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
            # print(oldv3 , "Before old location of v3")
            # oldv3_for_test = oldv3
            
            R = Matrix.Rotation(angle-height, 4, (normal))
            
            bmesh.ops.rotate(bm, 
                    matrix=R,        
                    verts=[v for v in bm.verts if v.select],
                    space=S,
            )    
        
        
        if bool == 1:

            obj = context.active_object
            
            bpy.context.object.update_from_editmode()
            bmesh.update_edit_mesh(me, True, True)

            if length_selected_vert == "Four":

                bmesh.update_edit_mesh(me, True, True)

                newv3 = obj.data.vertices[ind[3]].co

                #New position
                iv1=v2
                iv2=newv3
                # iv2=oldv3

                #Old position
                iv3=v0
                iv4=oldv3
                # iv4=newv3
                iv = geometry.intersect_line_line(iv1, iv2, iv3, iv4)
                if iv:
                    iv = (iv[0] + iv[1]) / 2

                    bm.verts[ind[3]].co = iv
                    
                    bpy.context.object.update_from_editmode()
                    bmesh.update_edit_mesh(me, True, True)

            if length_selected_vert == "Three":     
                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, True, True)

                newv3 = obj.data.vertices[ind[2]].co
                
                # iv1=v1
                # iv2=newv3
                # iv3=v2
                # iv4=oldv3

                iv1=v1
                iv2=oldv3
                iv3=v2
                iv4=newv3

                # print(iv1, iv2, iv3, iv4, "qqqqqqqqqqqqqqq")
                
                iv = geometry.intersect_line_line(iv1, iv2, iv3, iv4)
                if iv:
                    iv = (iv[0] + iv[1]) / 2

                    bm.verts[ind[2]].co = iv
                    
                    bpy.context.object.update_from_editmode()
                    bmesh.update_edit_mesh(me, True, True)
            
            if length_selected_vert == "Two":
                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, True, True)

                # if  lenvec == 1:
                
                # else:
                newv3 = obj.data.vertices[ind[1]].co
                
                # iv1=v1
                # iv2=newv3
                # iv3=v2
                # iv4=oldv3

                iv1=v1
                iv2=oldv3
                iv3=v2
                iv4=newv3

                # print(iv1, iv2, iv3, iv4, "Vertecises used for intersection")
                
                iv = geometry.intersect_line_line(iv1, iv2, iv3, iv4)
                if iv:
                    iv = (iv[0] + iv[1]) / 2

                    bm.verts[ind[1]].co = iv

                    # print(newv3, oldv3, iv)
                    
                    
                    bpy.context.object.update_from_editmode()
                    bmesh.update_edit_mesh(me, True, True)
        
        bpy.context.object.update_from_editmode()
        bmesh.update_edit_mesh(me, True, True)
         
        return {'FINISHED'}
if __name__ == "__main__":
    register()
