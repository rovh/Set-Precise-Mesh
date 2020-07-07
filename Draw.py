import bpy
import bgl
import blf
import gpu
from gpu_extras.batch import batch_for_shader

# class Pop_Up_Set_Cursor_To_Normal (bpy.types.Operator):
#     """Tooltip"""
#     bl_idname = "mesh.set_cursor_to_normal_pop_up"
#     bl_label = "Set the Cursor to the normal"
#     bl_description = "Set the cursor location to the selected vertex/edge/face and set the cursor direction along its normal\
#         \nYou can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut"
#     # bl_options = {'REGISTER', 'UNDO'}
#     bl_options = {'UNDO'}

#     def execute(self, context):
#         return {'FINISHED'}

#     # def invoke(self, context, event):
#     #     return context.window_manager.invoke_popup(self, width = 200)


#     def draw(self, context):

#         layout=self.layout

#         col = layout.column(align = 1)
#         col.scale_y = 1.2
        

#         if len(selected_verts) == 0 and len(selected_edges) == 0 and len(selected_faces) == 0:
#             col.label(icon = "ERROR")
#             col.label(text = "You need to select one element (vertex/edge/face)")
#         if len(selected_verts) > 1:
#             col.operator("mesh.set_cursor", text="Vertices", icon = "VERTEXSEL").get_from_verts = True
#         if len(selected_edges) != 0:
#             col.operator("mesh.set_cursor", text="Edges", icon = "EDGESEL").get_from_edges = True
#         if len(selected_faces) != 0:
#             col.operator("mesh.set_cursor", text="Faces", icon = "FACESEL").get_from_faces = True


def draw():
    v1 = bpy.context.window_manager.setprecisemesh.vertex_for_measure_1
    v2 = bpy.context.window_manager.setprecisemesh.vertex_for_measure_2
    remember = bpy.context.window_manager.setprecisemesh.remember 

    if remember == False:
        coords = [ (v1[0], v1[1], v1[2]), (v2[0], v2[1], v2[2])]
        shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        batch = batch_for_shader(shader, 'LINES', {"pos": coords})

        shader.bind()
        shader.uniform_float("color", (1, 1, 0, 1))
        batch.draw(shader)
    else:
        pass


def draw_callback_px(self, context):

    measure = bpy.context.window_manager.setprecisemesh.measure
    remember = bpy.context.window_manager.setprecisemesh.remember 

    font_id = 0  # XXX, need to find out how best to get this.

    blf.position(font_id, 75, 30, 0)
    blf.size(font_id, 20, 72)

    if remember == False:
        blf.draw(font_id, "Length:  " + str(measure))
    else:
        blf.draw(font_id, "Length:  " + str("No"))

class ModalDrawOperator_Set_Precise_Mesh_Length(bpy.types.Operator):
    """Draw a line with the mouse"""
    bl_idname = "view3d.modal_operator_setprecisemesh_draw_length"
    bl_label = "Display Length"

    def modal(self, context, event):

        remember = bpy.context.window_manager.setprecisemesh.remember 

        try:
            context.area.tag_redraw()
        except AttributeError:
            pass

        if event.type == 'MOUSEMOVE' or event.value == 'ANY':
            try:
                remember = False
                bpy.ops.mesh.change_length(draw = 1)
            except RuntimeError:
                remember = True
                pass
            except ReferenceError:      
                remember = True
                pass

        elif event.type in {'ESC', 'SPACE'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle_2, 'WINDOW')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':  
            args = (self, context)

            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
            self._handle_2 = bpy.types.SpaceView3D.draw_handler_add(draw, (), 'WINDOW', 'POST_VIEW')

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}



if __name__ == "__main__":
    register()
