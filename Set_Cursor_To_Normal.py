import bpy

import bmesh
from bpy import types
import mathutils



class Pop_Up_Set_Cursor_To_Normal (bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.set_cursor_to_normal_pop_up"
    bl_label = "Set the Cursor to the normal"
    bl_description = "Set the cursor location to the selected vertex/edge/face and set the cursor direction along its normal\
        \nYou can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut"
    # bl_options = {'REGISTER', 'UNDO'}
    bl_options = {'UNDO'}

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):

        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bpy.context.object.update_from_editmode()
        bmesh.update_edit_mesh(me, True)

        selected_verts = [verts for verts in bm.verts if verts.select]
        selected_edges = [edge for edge in bm.edges if edge.select]
        selected_faces = [face for face in bm.faces if face.select]            

        if len(selected_verts) != 0 and len(selected_edges) == 0 and len(selected_faces) == 0:
            if len(selected_verts) == 1:

                bpy.ops.mesh.set_cursor(get_from_verts = True)

                text = "Cursor was moved"
                war = "INFO"
                self.report({war}, text)

        if len(selected_verts) != 0 and len(selected_edges) != 0 and len(selected_faces) == 0:
            if len(selected_edges) == 1:
                bpy.ops.mesh.set_cursor(get_from_edges = True)

                text = "Cursor was moved"
                war = "INFO"
                self.report({war}, text)
                
        if len(selected_verts) != 0 and len(selected_edges) != 0 and len(selected_faces) != 0:
            if len(selected_faces) == 1:
                bpy.ops.mesh.set_cursor(get_from_faces = True)

                text = "Cursor was moved"
                war = "INFO"
                self.report({war}, text)
                

        # # context.window_manager.invoke_popup(self, width = 200)
        # return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self, width=600, height=500)
        if len(selected_verts) == 0 and len(selected_edges) == 0 and len(selected_faces) == 0:
            return context.window_manager.invoke_popup(self)
            # return {"FINISHED"}
        else:
            return context.window_manager.invoke_popup(self, width = 100)
            # return {"FINISHED"}


        # inv = context.window_manager.invoke_popup(self, width = 200)

        # bpy.context.window.cursor_warp(x, y)

        # return inv

    def draw(self, context):

        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bpy.context.object.update_from_editmode()
        bmesh.update_edit_mesh(me, True)

        selected_verts = [verts for verts in bm.verts if verts.select]
        selected_edges = [edge for edge in bm.edges if edge.select]
        selected_faces = [face for face in bm.faces if face.select]

        # w_m = context.window_manager.setprecisemesh

        layout=self.layout

        col = layout.column(align = 1)
        col.scale_y = 1.2
        

        if len(selected_verts) == 0 and len(selected_edges) == 0 and len(selected_faces) == 0:
            col.label(icon = "ERROR")
            col.label(text = "You need to select one element (vertex/edge/face)")
        if len(selected_verts) > 1:
            col.operator("mesh.set_cursor", text="Vertices", icon = "VERTEXSEL").get_from_verts = True
        if len(selected_edges) != 0:
            col.operator("mesh.set_cursor", text="Edges", icon = "EDGESEL").get_from_edges = True
        if len(selected_faces) != 0:
            col.operator("mesh.set_cursor", text="Faces", icon = "FACESEL").get_from_faces = True

class Set_Cursor_To_Normal (bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.set_cursor"
    bl_label = "Set the Cursor to the normal"
    bl_description = "Set the cursor location to the selected vertex/edge/face and set the cursor direction along its normal\
        \nYou can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut"
    # bl_options = {'REGISTER', 'UNDO'}
    bl_options = {'UNDO'}

    get_from_verts: bpy.props.BoolProperty(options={'SKIP_SAVE'}, default = 0)
    get_from_edges: bpy.props.BoolProperty(options={'SKIP_SAVE'}, default = 0)
    get_from_faces: bpy.props.BoolProperty(options={'SKIP_SAVE'}, default = 0)

    @classmethod
    def description(cls, context, properties):
        if properties.get_from_verts == True:
            return "Calculate normal(direction) from selected vertices"
        elif properties.get_from_edges == True:
            return "Calculate normal(direction) from selected edges"
        elif properties.get_from_faces == True:
            return "Calculate normal(direction) from selected faces"
        else:
            pass

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bpy.context.object.update_from_editmode()
        bmesh.update_edit_mesh(me, True)

        
        #Create lists
        # face_ind = []
        # edge_ind = []
        # vec_ind  = []

        # face_list = []
        # edge_list = []
        # vec_list  = []


        selected_verts = [verts for verts in bm.verts if verts.select]
        selected_edges = [edge for edge in bm.edges if edge.select]
        selected_faces = [face for face in bm.faces if face.select]

        wm = bpy.context.active_object.matrix_world.copy()
        wm_inverted = wm.inverted()

        # print("\n")        


        """Maybe it will be need"""
        # if len(selected_verts) != 0 and len(selected_edges) == 0 and len(selected_faces) == 0:
        #     print(bm.select_history)
        #     for v in bm.select_history:
        #         if v.select:
        #             # vec_list.append(bm.verts[v.index].co)
        #             vec_list.append(v)
        #             vec_ind.append(v.index)

        # if len(selected_verts) != 0 and len(selected_edges) != 0 and len(selected_faces) == 0:

        #     for e in bm.select_history:
        #         if e.select:
        #             # edge_list.append(bm.edges[e.index])
        #             edge_list.append(e)
        #             edge_ind.append(e.index)

        # if len(selected_verts) != 0 and len(selected_edges) != 0 and len(selected_faces) != 0:

        #     for f in bm.select_history:
        #         if f.select:
        #             # face_list.append(bm.faces[f.index])
        #             face_list.append(f)
        #             # try:
        #             #     # list_2 = list(set(selected_faces) & set(lst2))
        #             #     # if bm.faces[f.index] == selected_faces[:]:
        #             #     face_list.append(selected_faces[f.index])
        #             # except IndexError:
        #             #     pass
        #             # else:
        #             #     face_list.append(selected_faces[f.index])
        #             face_ind.append(f.index)
    



        # for geom in bm.select_history:
        #     if isinstance(geom, bmesh.types.BMFace):
        #         print(geom.index, "geom.index")
        
        # print(f.select)
        # print(len(vec_ind))
        # print(len(edge_ind))
        # print(len(face_ind))

        # print(selected_faces, "selected_faces")
        # print(selected_edges, "selected_edges")
        # print(selected_verts, "selected_verts")

        # print(vec_list,  "vec_list")
        # print(edge_list, "edge_list")
        # print(face_list, "face_list")

        # print(vec_ind,  "vec_ind")
        # print(edge_ind, "edge_ind")
        # print(face_ind, "face_ind")


        if len(selected_verts) == 0 and len(selected_edges) == 0 and len(selected_faces) == 0:

            text = "You need to select vertex/edge/face"
            war = "ERROR"
            self.report({war}, text)
            return{"FINISHED"}

        normal = mathutils.Vector((0,0,0))
        location = mathutils.Vector((0,0,0))

        if self.get_from_verts == True:

            if len(selected_verts) == 0:
                text = "You need to select vertex"
                war = "ERROR"
                self.report({war}, text)
                return{"FINISHED"}
    
            for i in range (-1, len(selected_verts)-1):
                normal = (selected_verts[i].normal @ wm_inverted) + normal
                location = (wm @ selected_verts[i].co) + location

            location = location / len(selected_verts)

        if self.get_from_edges == True:

            if len(selected_edges) == 0:
                text = "You need to select edge"
                war = "ERROR"
                self.report({war}, text)
                return{"FINISHED"}

            for i in range (-1, len(selected_edges)-1):
                edge_verts = selected_edges[i].verts

                location_of_edge = ((wm @ edge_verts[0].co) + (wm @ edge_verts[1].co)) /2
                location = location_of_edge + location

                faces_of_edge = selected_edges[i].link_faces

                normals_of_the_faces = []

                for f in range(0, len(faces_of_edge)):
                # for f in range(-1, len(faces_of_edge) - 1):
                    normals_of_the_faces.append(faces_of_edge[f].normal @ wm_inverted) 

                if len(normals_of_the_faces) == 2:

                    normal_from_face = ((normals_of_the_faces[0]) + (normals_of_the_faces[1])) /2
                    normal_from_face = (normal_from_face) + (location_of_edge) 
                    normal_projection_from_face = mathutils.geometry.intersect_point_line(normal_from_face, (wm @ edge_verts[0].co), (wm @ edge_verts[1].co))
                    normal_projection_from_face = normal_projection_from_face[0]
                    # normal_from_face = normal_projection_from_face
                    normal_from_face = (normal_from_face - normal_projection_from_face)
                    normal = normal + normal_from_face

                else:

                    normal_from_face = normals_of_the_faces[0]
                    normal_from_face = (normal_from_face) + (location_of_edge) 
                    normal_projection_from_face = mathutils.geometry.intersect_point_line(normal_from_face, (wm @ edge_verts[0].co), (wm @ edge_verts[1].co))
                    normal_projection_from_face = normal_projection_from_face[0]
                    # normal_from_face = normal_projection_from_face
                    normal_from_face = (normal_from_face - normal_projection_from_face)
                    normal = normal + normal_from_face
            
            location = location / len(selected_edges)

        if self.get_from_faces == True:

            if len(selected_faces) == 0:
                text = "You need to select face"
                war = "ERROR"
                self.report({war}, text)
                return{"FINISHED"}

            for i in range (-1, len(selected_faces)-1):

                location = (wm @ selected_faces[i].calc_center_median()) + location
                normal = (selected_faces[i].normal @ wm_inverted) + normal

            location = location / len(selected_faces)
            
        bpy.context.scene.cursor.location = location
        # Set cursor direction
        obj_camera = bpy.data.scenes[bpy.context.scene.name_full].cursor       
        direction = normal
        # point the cameras '-Z' and use its 'Y' as up
        rot_quat = direction.to_track_quat('-Z', 'Y')
        obj_camera.rotation_euler = rot_quat.to_euler()
        rot_quat =  rot_quat.to_euler()



        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bpy.context.object.update_from_editmode()
        bmesh.update_edit_mesh(me, True)


        return {'FINISHED'}
