import bpy

import bmesh
from bpy import types
import mathutils


class Set_Cursor_To_Normal (bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.set_cursor"
    bl_label = "Set the Cursor to the normal"
    bl_description = "Set the cursor location to the selected vertex/edge/face and set the cursor direction along its normal\
        \nYou can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut"
    bl_options = {'REGISTER', 'UNDO'}

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

        elem_list = []
        for g in bm.select_history:
            elem_list.append(g)

        selected_verts = [verts for verts in bm.verts if verts.select]
        selected_edges = [edge for edge in bm.edges if edge.select]
        selected_faces = [face for face in bm.faces if face.select]

        wm = bpy.context.active_object.matrix_world.copy()
        wm_inverted = wm.inverted()      


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
        # print(face_ind, "face_ind").

        if len(selected_verts) == 0 and len(selected_edges) == 0 and len(selected_faces) == 0:
            text = "You need to select one vertex/edge/face"
            war = "ERROR"
            self.report({war}, text)
            return{"FINISHED"}

        my_location = mathutils.Vector((0,0,0))
        normal = mathutils.Vector((0,0,0))

        print(elem_list)

        for i in range(-1, len(elem_list) - 1):

            if isinstance(elem_list[i], bmesh.types.BMVert) == True:

                my_location = elem_list[i].co + my_location

                normal = (elem_list[i].normal @ wm_inverted) + normal

            if isinstance(elem_list[i], bmesh.types.BMEdge) == True:

                edge_verts = elem_list[i].verts

                location_of_edge = ((wm @ edge_verts[0].co) + (wm @ edge_verts[1].co)) /2
                my_location = location_of_edge + my_location

                faces_of_edge = elem_list[i].link_faces

                normals_of_the_faces = []

                for f in range(-1, len(faces_of_edge) - 1):
                    normals_of_the_faces.append(faces_of_edge[f].normal @ wm_inverted) 


                normal_from_face = ((normals_of_the_faces[0]) + (normals_of_the_faces[1])) /2
                normal_from_face = (normal_from_face) + (location_of_edge)
                normal_projection_from_face = mathutils.geometry.intersect_point_line(normal_from_face, (wm @ edge_verts[0].co), (wm @ edge_verts[1].co))
                normal_projection_from_face = normal_projection_from_face[0]
                # normal_from_face = normal_projection_from_face
                normal_from_face = (normal_from_face - normal_projection_from_face)

                normal = normal_from_face + normal

            if isinstance(elem_list[i], bmesh.types.BMFace) == True:

                my_location = (elem_list[i].calc_center_median()) + my_location

                normal = (elem_list[i].normal @ wm_inverted) + normal

            
        my_location = my_location / len(elem_list)
        bpy.context.scene.cursor.location = wm @ my_location

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