import bpy
import bmesh
from bmesh.types import BMVert
import math
from math import *
from math import radians
from math import degrees
from math import pi
import mathutils
from mathutils import geometry
from mathutils import Vector, Matrix, Quaternion, Euler
from . import name


# from pynput.keyboard import Key, Controller

# keyboard = Controller()

def check(self):
    # Check scale
    obj = bpy.context.object
    if obj.scale != Vector((1.0, 1.0, 1.0)) or obj.delta_scale != Vector((1.0, 1.0, 1.0)):
        bpy.ops.object.dialog_warning_operator('INVOKE_DEFAULT') 

# def recalculate(self):

class SetAngle(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.change_angle"
    bl_label = "Set Angle   " + name
    bl_description = "Set Angle \n You can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut"
    bl_options = {'UNDO'}

    Clear_angle_globally: bpy.props.IntProperty(options={'SKIP_SAVE'})
    eyedropper: bpy.props.BoolProperty(options={'SKIP_SAVE'})

    @classmethod
    def poll(cls, context):
        return context.active_object is not None\
            and context.active_object.mode in {'EDIT'}\
            and context.active_object.type == "MESH"

    @classmethod
    def description(cls, context, properties):
        if properties.Clear_angle_globally == 1:
            return "Plus Angle"
        elif properties.Clear_angle_globally == -1:
            return "Minus Angle"
        elif properties.eyedropper == True:
            return "Get Angle"
        else:
            pass


    def execute(self, context):
        
        check(self)
        

        # Get values
        data_block = bpy.context.window_manager.setprecisemesh.data_block
        script_input = bpy.context.scene.script_input
        system_rotation = bpy.context.scene.unit_settings.system_rotation
        height = bpy.context.window_manager.setprecisemesh.angle

        """Replace syntax"""
        data_block = data_block.replace(',', '.')
        data_block = data_block.replace('^', '**')
        data_block = data_block.replace(':', '/')

        height_copy = degrees(height) if system_rotation == 'DEGREES' else height
        data_block = data_block.replace('unit', str(height_copy))
        data_block = data_block.replace('u', str(height_copy))

        if script_input == 1:

            try:
                eval(data_block)
            except SyntaxError:
                height = bpy.context.window_manager.setprecisemesh.angle
            else:
                height = eval(data_block)
                

                """Units Synchronization"""

                if  system_rotation == 'DEGREES':
                    bpy.context.window_manager.setprecisemesh.angle = radians(height)
                    height = radians(height)

                else:
                    bpy.context.window_manager.setprecisemesh.angle = height
        else:
            height = bpy.context.window_manager.setprecisemesh.angle
            

        bool = bpy.context.window_manager.setprecisemesh.anglebool
        bool2 = bpy.context.window_manager.setprecisemesh.angleinput

        
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        bpy.context.object.update_from_editmode()
        # bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)
        bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)

        # recalculate = 0
        # for cycle in range (0, recalculate + 1):
        #     print("cycle")

        # bpy.context.object.update_from_editmode()
        # bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)

        #Create lists
        vec = []
        ind = []

        #Append to lists
        for g in bm.select_history:
            # if len(vec)<3:
            if isinstance(g, bmesh.types.BMVert) == False:
                text = '"Set Angle" works only with vertices'
                war = "ERROR"
                self.report({war}, text)
                return{"FINISHED"}
                break

            vec.append(bm.verts[g.index].co)
            ind.append(g.index)



        # Check number
        if len(vec)<2 or len(vec) > 4:

            # This check causes an RuntimeError

            text = "You need to select from 1 to 4 vertices"
            war = 'ERROR'
            self.report({war}, text)
            return {"FINISHED"}

        # Differrent cases for progection
        prog = context.window_manager.setprecisemesh.projection_type

        bpy.context.object.update_from_editmode()
        # bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)
        bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)

        """Check list of selected vertices"""
        Clear_angle = False

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
                bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)

                v2_prg = bpy.context.active_object.matrix_world  @ v2
                v1 = bpy.context.active_object.matrix_world  @ v3

                wm = bpy.context.active_object.matrix_world.copy()
                wm = wm.inverted()
                              
                v1 = mathutils.Vector((v1[0], v1[1] , v2_prg[2])) # 1 selected simulate
                
                v3_prg = bpy.context.active_object.matrix_world  @ v3
                if v3_prg == v1 :
    
                    Clear_angle = 1

                    v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] + 1.0)  ))

                    # if v2_prg[2] < 0:
                    #     v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] - 1.0)  ))
                    # else:
                    #     v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] + 1.0)  ))

                    v3 = wm @ v3
                    oldv3 = v3
                if v2_prg == v1:
                    bpy.ops.object.dialog_warning_operator_2('INVOKE_DEFAULT') 

                v1 = wm @ v1  

                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)

            elif prog == "local_matrix":

                v2_prg = v2
                v1 = v3
                v1 = mathutils.Vector((v1[0], v1[1] , v2_prg[2])) # 1 selected simulate
                v3_prg = v3

                if v3_prg == v1 :
                    Clear_angle = 1

                    v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] + 1.0)  ))

                    # if v2_prg[2] < 0:
                    #     v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] - 1.0)  ))
                    # else:
                    #     v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] + 1.0)  ))

                    oldv3 = v3
                if v2_prg == v1:
                    bpy.ops.object.dialog_warning_operator_2('INVOKE_DEFAULT')

            elif prog == "cursor_location":
                wm = bpy.context.active_object.matrix_world.copy()
                wm = wm.inverted()

                # v3_prg = bpy.context.active_object.matrix_world  @ v3
                v2_prg =  bpy.context.active_object.matrix_world @ v2

                v1 = bpy.context.scene.cursor.location

                # length_of_v1 = (v2_prg - v1).length
                # print(length_of_v1)


                v1 = wm @ v1

                v1ch=v1-v2
                v3ch=v3-v2
                angle = v3ch.angle(v1ch, 0.0)

                if angle == 0.0 :
                    bpy.ops.object.dialog_warning_operator_3('INVOKE_DEFAULT') 
               
            elif prog == "cursor_matrix":

                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)
                # bpy.context.scene.update_tag()
                # bpy.context.view_layer.update()
                # bpy.context.depsgraph.update()

                        
                obj_matrix = bpy.context.active_object.matrix_world.copy()
  

                cursor_matrix = bpy.context.scene.cursor.matrix.copy()
                cursor_matrix_inverted = cursor_matrix.inverted()


        
                # mat_cur =  cursor_matrix_inverted @ obj_matrix
                mat_cur =  obj_matrix @ cursor_matrix_inverted


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

                    v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] - 100.0)  ))

                    # if v2_prg[2] < 0:
                    # if v2_prg[2] < cursor_matrix_loc[2]:
                    #     print(v2_prg[2])
                    #     print(cursor_matrix_loc[2])
                    #     v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] - 100.0)  ))
                    #     print("Location grater than")
                    # else:
                    #     v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] + 100.0)  ))
                    #     print("Location lower than")

                    v3 = mat_cur @ v3
                    oldv3 = v3

                
                if v2_prg == v1:
                # if v2 == v1:
                    bpy.ops.object.dialog_warning_operator_2('INVOKE_DEFAULT')

                v1 = mat_cur @ v1

                

                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)
                # bpy.context.scene.update_tag()
                # bpy.context.view_layer.update()

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
                bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)
                # bpy.context.scene.update_tag()
                # bpy.context.view_layer.update()

                obj_name = bpy.data.scenes[bpy.context.scene.name_full].my_property.name_full
                custom_obj_matrix = bpy.data.objects[obj_name].matrix_world

                custom_obj_matrix = custom_obj_matrix.copy()
                custom_obj_matrix_inverted = custom_obj_matrix.inverted()

                obj_matrix = bpy.context.active_object.matrix_world.copy()


                # mat = custom_obj_matrix_inverted @ obj_matrix
                mat = obj_matrix @ custom_obj_matrix_inverted


                v3_prg =  v3
                v3_prg = mat @ v3_prg

                v2_prg =  v2
                v2_prg =  mat @ v2_prg

                v1 = v3
                v1 = mat @ v1
                
                v1 = mathutils.Vector((v1[0], v1[1] , v2_prg[2])) # 1 selected simulate
                
                mat = mat.inverted()

                if v3_prg == v1 :
                    Clear_angle = True

                    v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] + 100.0)  ))
                    
                    # if v2_prg[2] < 0:
                    # if v2_prg[2] < custom_obj_loc[2]:
                    #     v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] - 100.0)  ))
                    # else:
                    #     v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] + 100.0)  ))
                    v3 = mat @ v3
                    oldv3 = v3

                if v2_prg == v1:
                    bpy.ops.object.dialog_warning_operator_2('INVOKE_DEFAULT')

                v1 = mat @ v1


                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)
                # bpy.context.scene.update_tag()
                # bpy.context.view_layer.update()

            # elif prog == "normal_matrix":

            #     bpy.context.object.update_from_editmode()
            #     bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)
            #     # bpy.context.scene.update_tag()
            #     # bpy.context.view_layer.update()
            #     # bpy.context.depsgraph.update()

                        
            #     obj_matrix = bpy.context.active_object.matrix_world.copy()
            #     # cursor_loc =  bpy.context.scene.cursor.location
            #     mat_loc =  mathutils.Matrix.Translation(( 0.0 ,  0.0 ,  0.0 ))        
            #     mat_sca =  mathutils.Matrix.Scale( 1.0 ,  4 ,  ( 0.0 ,  0.0 ,  1.0 ))
            #     mat_rot =  mathutils.Matrix.Rotation(0 ,  4 , "Z" )

            #     mat_out =  mat_loc @  mat_rot @  mat_sca

            #     # cursor_matrix = bpy.context.scene.cursor.matrix.copy()
            #     # cursor_matrix = cursor_matrix.inverted()
            #     # obj_matrix = obj_matrix.inverted()

            #     # mat_cur = obj_matrix @ cursor_matrix
            #     mat_cur = obj_matrix
            #     # mat_cur = cursor_matrix

            #     # cursor_matrix_loc = bpy.context.scene.cursor.matrix.translation
            #     # cursor_matrix_loc = mat_cur @ cursor_matrix_loc
            #     # cursor_matrix_loc = mat_cur @ cursor_matrix_loc

            #     v_normal = obj.data.vertices[ind[1]].normal
            #     v_normal = mat_cur @ v_normal
            #     print(v_normal, "v_normal")


            #     v2_prg =  v2
            #     v2_prg = mat_cur  @ v2_prg

            #     v_normal = mathutils.Vector( ( v_normal[0], v_normal[1], v2_prg[2]  ) )

            #     v1 =  v_normal
            #     # v1 = mat_cur @ v1



            #     # v3_prg =  v3
            #     # v3_prg = mat_cur @ v3_prg

            #     # v1 = mathutils.Vector((v1[0], v1[1] , v2_prg[2])) # 1 selected simulate

            #     mat_cur = mat_cur.inverted()

            #     v1 = mat_cur @ v1

                # v3_prg = mat_cur @ v3_prg

                # if v3_prg == v1:
                #     Clear_angle = True

                #     v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] - 100.0)  ))

                    # if v2_prg[2] < 0:
                    # if v2_prg[2] < cursor_matrix_loc[2]:
                    #     print(v2_prg[2])
                    #     print(cursor_matrix_loc[2])
                    #     v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] - 100.0)  ))
                    #     print("Location grater than")
                    # else:
                    #     v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] + 100.0)  ))
                    #     print("Location lower than")

                    # v3 = mat_cur @ v3
                    # oldv3 = v3
        
        else:
            length_selected_vert = "Three"
            v1=vec[0] # 1 selected
            v2=vec[1] # 2 selected
            v3=vec[2] #  3 selected
            oldv3 = mathutils.Vector( vec[2] ) # 3 selected

        bpy.context.object.update_from_editmode()
        # bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)
        bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)


        if Clear_angle == 1:
            angle = 0.0
        elif self.Clear_angle_globally == 1:
            angle = 0.0
        elif self.Clear_angle_globally == -1:
            height = -height
            angle = 0.0
        else:
            v1ch=v1-v2
            v3ch=v3-v2
            angle = v3ch.angle(v1ch, 0.0)

        if self.eyedropper == True:
            bpy.context.window_manager.setprecisemesh.angle = angle
            return {"FINISHED"}
        
        # bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)
        bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)

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
            # loc_camera = bpy.data.scenes[bpy.context.scene.name_full].cursor.matrix.to_translation()         
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
            bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)


            bpy.ops.transform.rotate("INVOKE_DEFAULT")
            # bpy.context.active_operator.options.use_cursor_region = True
        

            bpy.context.object.update_from_editmode()
            bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)
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
            bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)

            if length_selected_vert == "Four":

                bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)

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
                    bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)

            if length_selected_vert == "Three":     
                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)

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
                # print(iv)
                if iv:
                    iv = (iv[0] + iv[1]) / 2

                    bm.verts[ind[2]].co = iv
                    
                    bpy.context.object.update_from_editmode()
                    bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)
            
            if length_selected_vert == "Two":
                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)

                
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
                    bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)
        
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bpy.context.object.update_from_editmode()
        # bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)
        bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)

         
        return {'FINISHED'}

if __name__ == "__main__":
    register()
