import bpy

# from bpy import types

import bmesh

# from bpy import types
# from bpy.props import (
#         FloatProperty,
#         BoolProperty,
#         PointerProperty,
#         EnumProperty,
#         StringProperty,
#         )


class Pop_Up_Set_Mesh_Position (bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.set_mesh_position_pop_up"
    bl_label = "Set Mesh Position Pop up menu"
    bl_description = "Set the cursor location to the selected vertex/edge/face and rotate it by normal\
        \nYou can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def invoke(self, context, event):

        # bpy.context.window.cursor_warp(x + move_x, y + move_y)
        # context.window_manager.invoke_popup(self, width = 200)
        # return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self, width=600, height=500)
        # return context.window_manager.invoke_popup(self)
        inv = context.window_manager.invoke_popup(self, width = 200)

        return inv

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
        sub_col.operator("mesh.set_mesh_position_global", text="global")
        sub_col.scale_y = 1.5


        # space
        sub_col = col_right.column(align = 0)
        sub_col.scale_y = 0.15
        sub_col = sub_col.label(text = "")

        # Cursor menu
        sub_col = col_right.column(align = 1)
        sub_col.operator("mesh.set_mesh_position_local", text="local")
        sub_col.scale_y = 1.5
        # space
        # sub_col = col_right.column(align = 0)
        # sub_col.scale_y = 0.15
        # sub_col = sub_col.label(text = "")

        # # Cursor menu
        # sub_col = col_right.column(align = 1)
        # sub_col.prop_enum( w_m, "projection_type", "normal_matrix")
        # sub_col.prop_enum( w_m, "projection_type", "cursor_matrix")

        # space
        sub_col = col_right.column(align = 0)
        sub_col.scale_y = 0.15
        sub_col = sub_col.label(text = "")

        # Object menu
        sub_col = col_right.column(align = 1)
        sub_col.prop_enum( w_m, "projection_type", "custom_object_location")
        
        sub_col.prop_enum( w_m, "projection_type", "custom_object_matrix")

        # Make space object selection box
        prog = context.window_manager.setprecisemesh.projection_type
        if prog == "custom_object_location" or  prog == "custom_object_matrix":
            sub_col.prop(context.scene, "my_property", text = "")

        # sub_col.prop(context.scene, "my_property", text = "")
    
    def execute(self, context):
        return {"FINISHED"}



class Set_Mesh_Position_Global (bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.set_mesh_position_global"
    bl_label = "Set Mesh Position Global"
    bl_description = "Set the cursor location to the selected vertex/edge/face and rotate it by normal\
        \nYou can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        bpy.ops.mesh.set_mesh_position(position = "global")
        return {"FINISHED"}

class Set_Mesh_Position_Local (bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.set_mesh_position_local"
    bl_label = "Set Mesh Position Global"
    bl_description = "Set the cursor location to the selected vertex/edge/face and rotate it by normal\
        \nYou can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        bpy.ops.mesh.set_mesh_position(position = "local")
        return {"FINISHED"}

class Set_Mesh_Position_Cursor (bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.set_mesh_position_cursor"
    bl_label = "Set Mesh Position Cursor"
    bl_description = "Set the cursor location to the selected vertex/edge/face and rotate it by normal\
        \nYou can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        bpy.ops.mesh.set_mesh_position(position = "cursor")
        return {"FINISHED"}

class Set_Mesh_Position_Object (bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.set_mesh_position_object"
    bl_label = "Set Mesh Position Object"
    bl_description = "Set the cursor location to the selected vertex/edge/face and rotate it by normal\
        \nYou can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        bpy.ops.mesh.set_mesh_position(position = "object")
        return {"FINISHED"}



class Set_Mesh_Position (bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.set_mesh_position"
    bl_label = "Set Mesh Position"
    bl_description = "Set the cursor location to the selected vertex/edge/face and rotate it by normal\
        \nYou can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut"
    bl_options = {'REGISTER', 'UNDO'}

    position: bpy.props.StringProperty(
        default = "global"
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):

        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        bpy.context.object.update_from_editmode()
        # bmesh.update_edit_mesh(me, True, True)

        # bpy.context.object.update_from_editmode()
        # bmesh.update_edit_mesh(me, True, True)
        # bpy.context.scene.update_tag()
        # bpy.context.view_layer.update()
        # mat_loc =  mathutils.Matrix.Translation(( 0.0 ,  0.0 ,  0.0 ))        
        # mat_sca =  mathutils.Matrix.Scale( 1.0 ,  4 ,  ( 0.0 ,  0.0 ,  1.0 ))
        # mat_rot =  mathutils.Matrix.Rotation(0 ,  4 , "Z" )

        # mat_out =  mat_loc @  mat_rot @  mat_sca

        cursor_matrix_old = bpy.context.scene.cursor.matrix.copy()

        selected_verts = [verts for verts in bm.verts if verts.select]
        selected_edges = [edge for edge in bm.edges if edge.select]
        selected_faces = [face for face in bm.faces if face.select]

        wm = bpy.context.active_object.matrix_world.copy()
        wm_inverted = wm.inverted()


        if len(selected_verts) == 0 and len(selected_edges) == 0 and len(selected_faces) == 0:

            text = "You need to select one vertex/edge/face"
            war = "ERROR"
            self.report({war}, text)
            return{"FINISHED"}

        if len(selected_verts) != 0 and len(selected_edges) == 0 and len(selected_faces) == 0:

            if len(selected_verts) > 1:
                text = "You need to select only one vertex"
                war = "ERROR"
                self.report({war}, text)
                return{"FINISHED"}

            
            bpy.context.scene.cursor.location = wm @ selected_verts[0].co

            normal = selected_verts[0].normal @ wm_inverted

            obj_camera = bpy.data.scenes[bpy.context.scene.name_full].cursor       
            direction = normal
            # point the cameras '-Z' and use its 'Y' as up
            rot_quat = direction.to_track_quat('-Z', 'Y')
            obj_camera.rotation_euler = rot_quat.to_euler()
            rot_quat =  rot_quat.to_euler()

        if len(selected_verts) != 0 and len(selected_edges) != 0 and len(selected_faces) == 0:

            if len(selected_edges) > 1:
                text = "You need to select only one edge"
                war = "ERROR"
                self.report({war}, text)
                return{"FINISHED"}

            
            edge_verts = selected_edges[0].verts


            location_of_edge = ((wm @ edge_verts[0].co) + (wm @ edge_verts[0].co)) / 2
            bpy.context.scene.cursor.location = location_of_edge

            # diraction_for_edge = (wm @ edge_verts[1].co) - (wm @ edge_verts[0].co)


            normal = ((edge_verts[0].normal @ wm_inverted) + (edge_verts[1].normal @ wm_inverted)) / 2


            obj_camera = bpy.data.scenes[bpy.context.scene.name_full].cursor       
            direction = normal
            # point the cameras '-Z' and use its 'Y' as up
            # rot_quat = direction.to_track_quat('-Z', 'Y')
            rot_quat = direction.to_track_quat('-Z', 'Y')
            obj_camera.rotation_euler = rot_quat.to_euler()
            rot_quat =  rot_quat.to_euler()
            
        if len(selected_verts) != 0 and len(selected_edges) != 0 and len(selected_faces) != 0:

            if len(selected_faces) > 1:
                text = "You need to select only one face"
                war = "ERROR"
                self.report({war}, text)
                return{"FINISHED"}


            my_location = wm @ selected_faces[0].calc_center_median()
            normalgl = selected_faces[0].normal @ wm_inverted

                        
            bpy.context.scene.cursor.location = my_location

            # Set cursor direction
            obj_camera = bpy.data.scenes[bpy.context.scene.name_full].cursor       
            direction = normalgl
            # point the cameras '-Z' and use its 'Y' as up
            rot_quat = direction.to_track_quat('-Z', 'Y')
            obj_camera.rotation_euler = rot_quat.to_euler()
            rot_quat =  rot_quat.to_euler()

        obj_matrix = bpy.context.active_object.matrix_world.copy()

        cursor_matrix = bpy.context.scene.cursor.matrix.copy()
        cursor_matrix_inverted = cursor_matrix.inverted()
        mat_cur =  cursor_matrix_inverted @ obj_matrix



        # position = "global"
        # position = "local"
        # position = "cursor"
        # position = "object"
        position = self.position

        if position == "global":
            bpy.context.active_object.matrix_world = mat_cur

        elif position == "local":
            # bpy.context.active_object.matrix_world = mat_cur @ obj_matrix
            bpy.context.active_object.matrix_world = obj_matrix @ mat_cur
        
        elif position == "cursor":
            bpy.context.active_object.matrix_world = cursor_matrix_old @ mat_cur

        elif position == "object":

            obj_name = bpy.data.scenes[bpy.context.scene.name_full].object_position.name_full
            obj_marx = bpy.data.objects[obj_name].matrix_world

            # obj_marx = bpy.data.objects["Empty"].matrix_world
            bpy.context.active_object.matrix_world = obj_marx @ mat_cur



        bpy.context.scene.cursor.matrix = cursor_matrix_old



        # mat_out = mat_out.to_4x4()
        # bpy.context.active_object.matrix_world = mat_out




        


        

        bpy.context.object.update_from_editmode()
        bmesh.update_edit_mesh(me, True, True)
        return {"FINISHED"}

if __name__ == "__main__":
    register()