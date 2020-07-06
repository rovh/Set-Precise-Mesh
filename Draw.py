import bpy
import bgl
import blf
import gpu
from gpu_extras.batch import batch_for_shader


def draw_callback_px(self, context):

    measure = bpy.context.window_manager.setprecisemesh.measure

    font_id = 0  # XXX, need to find out how best to get this.

    blf.position(font_id, 75, 30, 0)
    blf.size(font_id, 20, 72)

    if self.remember == False:
        blf.draw(font_id, "Length:  " + str(measure))
    else:
        blf.draw(font_id, "Length:  " + str("No"))

class ModalDrawOperator(bpy.types.Operator):
    """Draw a line with the mouse"""
    bl_idname = "view3d.modal_operator"
    bl_label = "Simple Modal View3D Operator"

    remember: bpy.props.BoolProperty(options = {"SKIP_SAVE"})


    def modal(self, context, event):
        try:
            context.area.tag_redraw()
        except AttributeError:
            pass

        if event.type == 'MOUSEMOVE':
            try:
                self.remember = False
                bpy.ops.mesh.change_length(draw = 1)
            except RuntimeError:
                self.remember = True
                pass
            except ReferenceError:
                self.remember = True
                pass

        elif event.type in {'ESC', 'BACKSPACE'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            # the arguments we pass the the callback
            args = (self, context)
            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}



if __name__ == "__main__":
    register()
