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
                print("\n")
                print("\n")
                selected_edges_faces_info = {}
                linked_faces = {}
                for i in range(0, len(selected_edges) ):
                    # print(i)
                    for k in range(0, len(selected_edges[i].link_faces) ):
                        linked_faces[i] = []
                        # linked_faces[i].append( selected_edges[i].link_faces[k] )
                        linked_faces[i].append( selected_edges[i].link_faces[k] )

                    print(linked_faces[i])
                    # print(selected_edges[i].link_faces[0])
                    # print(selected_edges[i].link_faces[1])
                    # selected_edges_faces_info[i] = selected_edges[i].link_faces

                    # print(len(selected_edges_faces_info[i]))
                    # print(selected_edges_faces_info[i])
                    # print(selected_edges)

                    # print(selected_edges_faces_info[i][k], '123123123', k)


                # for i in range(-1, len(selected_edges) - 2):

                #     linked_faces[i+1] = list( set(linked_faces[i]) & set(linked_faces[i+1]) )

                #     print(linked_faces[i])

                # for i in range(-1, len(linked_faces) - 2):
                #     for k in range (i-1, len(linked_faces) - 2):
                #         if linked_faces[i].index == linked_faces[i+1].index:
                #             print("Yes")

                # print(array[len(selected_edges)-1])

                
                    


            pass

        if len(selected_verts) != 0 and len(selected_edges) != 0 and len(selected_faces) != 0:

            pass

        


        # bmesh.ops.scale(
        #     bm,
        #     vec = mathutils.Vector( ( 1, 1, 1/length )),
        #     verts=[v for v in bm.verts if v.select],
        #     space=S
        #     )

        return {"FINISHED"}

if __name__ == "__main__":
    register()

