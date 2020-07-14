import bpy

import bmesh
import math
import mathutils

from . import name



class SetArea(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.change_area"
    bl_label = "Set Area " + name
    bl_description = 'You can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut'
    # bl_options = {'REGISTER', 'UNDO'}
    bl_options = {'UNDO'}

    plus_length: bpy.props.IntProperty(options = {"SKIP_SAVE"}) 
    eyedropper: bpy.props.BoolProperty(options = {"SKIP_SAVE"})
    draw:       bpy.props.BoolProperty(options = {"SKIP_SAVE"})
    lengthbool_SKIP_SAVE: bpy.props.BoolProperty(options = {"SKIP_SAVE"})
    @classmethod
    def poll(cls, context):
        return context.active_object is not None\
            and context.active_object.mode in {'EDIT'}\
            and context.active_object.type == "MESH"

    def execute(self, context):

        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        selected_verts = [verts for verts in bm.verts if verts.select]
        selected_edges = [edge for edge in bm.edges if edge.select]
        selected_faces = [face for face in bm.faces if face.select]

        if len(selected_verts) == 0 and len(selected_edges) == 0 and len(selected_faces) == 0:

            text = "You need to select vertex/edge/face"
            war = "ERROR"
            self.report({war}, text)
            return{"FINISHED"}

        if len(selected_verts) != 0 and len(selected_edges) != 0 and len(selected_faces) == 0:

            if len(selected_edges) <2:
                text = "You need to select vertex/edge/face"
                war = "ERROR"
                self.report({war}, text)
                return{"FINISHED"}
            else:
                
                selected_edges_faces_info = {}
                linked_faces = {}
                linked_faces_all = []
                for i in range(0, len(selected_edges) ):
                    linked_faces[i] = []
                    for k in range(0, len(selected_edges[i].link_faces) ):
                        linked_faces[i].append( selected_edges[i].link_faces[k] )
                        linked_faces_all.append( selected_edges[i].link_faces[k] )

                for i in range(0, len(linked_faces_all) -1):

                    for j in range(i+1, len(linked_faces_all) ):

                        if linked_faces_all[i].index == linked_faces_all[j].index:
                            needed_face = linked_faces_all[i]

                            # needed_face = needed_face.calc_area()
                            # needed_face = needed_face.calc_center_median()

                            # print(needed_face, "need")
                            # print("Yes")
                            break


                # print(edges_of_needed_face)

                


                # for j in range(0, len(linked_faces) - 1):
                #     for i in range(0, len(linked_faces[j]) ):
                #         for l in range (0, len(linked_faces[j+1]) ):
                #             for k in range (0, len(linked_faces[l]) ):
                                # print("\n")
                                # print(linked_faces[j][i])
                                # print(linked_faces[j+1][k])


            pass

        if len(selected_verts) != 0 and len(selected_edges) != 0 and len(selected_faces) != 0:

            if len(selected_faces)>1:
                text = "You need to select vertex/edge/face"
                war = "ERROR"
                self.report({war}, text)
                return{"FINISHED"}
            else:
                needed_face = selected_faces[0]

        area = needed_face.calc_area()
        center_median = bpy.context.active_object.matrix_world @ needed_face.calc_center_median()
                
        print(area)
        print(center_median)

        # Create Matrix
        mat_loc =  mathutils.Matrix.Translation(( 0.0 ,  0.0 ,  0.0 ))        
        # mat_loc =  mathutils.Matrix.Translation(( center_median))        
        mat_sca =  mathutils.Matrix.Scale( 1.0 ,  4 ,  ( 0.0 ,  0.0 ,  1.0 ))
        mat_rot =  mathutils.Matrix.Rotation(0 ,  4 , "Z" )

        mat_out =  mat_loc @  mat_rot @  mat_sca

        S = mat_out

        S.translation -= center_median

        bmesh.ops.scale(
            bm,
            vec = mathutils.Vector( (2,2,2) ),
            verts=[v for v in bm.verts if v.select],
            space=S
            )

        bmesh.update_edit_mesh(me, True)

        return {"FINISHED"}

if __name__ == "__main__":
    register()

