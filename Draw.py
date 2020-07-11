import bpy
import bgl
import blf
import gpu
from gpu_extras.batch import batch_for_shader

from . import __name__

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
    v1 = bpy.context.window_manager.setprecisemesh.length_display_coordinate_1
    v2 = bpy.context.window_manager.setprecisemesh.length_display_coordinate_2
    length_display_stop = bpy.context.window_manager.setprecisemesh.length_display_stop 

    if length_display_stop == False and bpy.context.active_object is not None:
        if bpy.context.active_object.mode in {'EDIT'}:

            coords = [ (v1[0], v1[1], v1[2]), (v2[0], v2[1], v2[2])]
            shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
            batch = batch_for_shader(shader, 'LINES', {"pos": coords})

            shader.bind()
            shader.uniform_float("color", (1, 1, 0, 0))
            batch.draw(shader)
        else:
            pass
    else:
        pass

def draw_callback_px(self, context):

    length_display_number = bpy.context.window_manager.setprecisemesh.length_display_number
    length_display_stop = bpy.context.window_manager.setprecisemesh.length_display_stop 

    font_id = 0  # XXX, need to find out how best to get this.

    blf.position(font_id, 75, 30, 0)
    blf.size(font_id, 20, 72)
    
    if context.active_object is not None:
        if context.active_object.mode in {'EDIT'}:
            if length_display_stop == False:

                length_unit = bpy.context.scene.unit_settings.length_unit

                if  bpy.context.scene.unit_settings.system == 'METRIC' and length_unit == 'ADAPTIVE':
                    unit_index = ""
                
                elif length_unit == "MICROMETERS":
                    unit_index = "um"
                    length_display_number = length_display_number * 1000000
                
                elif length_unit == "MILLIMETERS":
                    unit_index = "mm"
                    length_display_number = length_display_number * 1000
                
                elif length_unit == "CENTIMETERS":
                    unit_index = "cm"
                    length_display_number = length_display_number * 100
                
                elif length_unit == "METERS":
                    unit_index = "m"
                
                elif length_unit == "KILOMETERS":
                    unit_index = "km"
                    length_display_number = length_display_number / 1000
                

                if bpy.context.scene.unit_settings.system == 'IMPERIAL'and length_unit == 'ADAPTIVE':
                    unit_index = ""
                    length_display_number = length_display_number * 3.2808398950131

                elif length_unit == 'MILES':
                    unit_index = "mi"
                    length_display_number = length_display_number * 0.00062137119223733
                
                elif length_unit == 'FEET':
                    unit_index = "'"
                    length_display_number = length_display_number * 3.2808398950131
                
                elif length_unit == 'INCHES':
                    unit_index = "''"
                    length_display_number = length_display_number * 39.370078740157
                
                elif length_unit == 'THOU':
                    unit_index = "thou"
                    length_display_number = length_display_number * 39.370078740157 * 1000

                length_display_number = round(length_display_number, self.round_precision)
                length_display_number = str(length_display_number)

                blf.draw(font_id, "Length:  " + length_display_number + " " + unit_index)
            else:
                blf.draw(font_id, "Length:  " + "No")
        else:
            pass

class ModalDrawOperator_Set_Precise_Mesh_Length(bpy.types.Operator):
    """Draw a line with the mouse"""
    bl_idname = "view3d.modal_operator_setprecisemesh_draw_length"
    bl_label = "Display Length"
    bl_description = "Display Length between two selected elements in left buttom corner"

    def modal(self, context, event):

        length_display_stop = bpy.context.window_manager.setprecisemesh.length_display_stop 
        draw_length_line = bpy.context.window_manager.setprecisemesh.draw_length_line

        if draw_length_line == False:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle_2, 'WINDOW')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            try:
                context.area.tag_redraw()
            except AttributeError:
                pass
            return {'FINISHED'}
        
        else:
            try:
                context.area.tag_redraw()
            except AttributeError:
                pass

            if event.type == 'MOUSEMOVE' or event.value == 'ANY':
                try:
                    length_display_stop = False
                    bpy.ops.mesh.change_length(draw = 1)
                except RuntimeError:
                    length_display_stop = True
                    pass
                except ReferenceError:      
                    length_display_stop = True
                    pass

        # elif event.type in {'ESC', 'SPACE'}:
        #     bpy.types.SpaceView3D.draw_handler_remove(self._handle_2, 'WINDOW')
        #     bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        #     return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        draw_length_line = bpy.context.window_manager.setprecisemesh.draw_length_line
        settings = bpy.context.preferences.addons[__name__].preferences
        self.round_precision = settings.round_precision

        if draw_length_line == True:
            bpy.context.window_manager.setprecisemesh.draw_length_line = False
            return {'RUNNING_MODAL'}
        else:
            bpy.context.window_manager.setprecisemesh.draw_length_line = True

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
