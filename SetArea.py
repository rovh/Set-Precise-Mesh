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
                array = {}
                for i in range(-1, len(selected_edges) - 1):

                    array[i] = selected_edges[i].link_faces

                for i in range(-1, len(selected_edges) - 2):

                    array[i+1] = list( set(array[i]) & set(array[i+1]) )

                    print(i)

                print(array[len(selected_edges)-1])

                
                    


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

