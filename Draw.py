import bpy
import bgl
import blf
import gpu
from gpu_extras.batch import batch_for_shader


def draw_callback_px(self, context):
    print("mouse points", len(self.mouse_path))

    font_id = 0  # XXX, need to find out how best to get this.

    # draw some text
    blf.position(font_id, 60, 30, 0)
    blf.size(font_id, 20, 72)
    blf.draw(font_id, "Hello Word " + str(len(self.mouse_path)))

    # 50% alpha, 2 pixel width line
    # shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    # bgl.glEnable(bgl.GL_BLEND)
    # bgl.glLineWidth(2)
    # batch = batch_for_shader(shader, 'LINE_STRIP', {"pos": self.mouse_path})
    # shader.bind()
    # shader.uniform_float("color", (0.0, 0.0, 0.0, 0.5))
    # batch.draw(shader)

    # # restore opengl defaults
    # bgl.glLineWidth(1)
    # bgl.glDisable(bgl.GL_BLEND)


class ModalDrawOperator(bpy.types.Operator):
    """Draw a line with the mouse"""
    bl_idname = "view3d.modal_operator"
    bl_label = "Simple Modal View3D Operator"

    def modal(self, context, event):
        context.area.tag_redraw()

        # if event.type == 'MOUSEMOVE':
        #     self.mouse_path.append((event.mouse_region_x, event.mouse_region_y))
        if event.type == 'TIMER':
            self.mouse_path.append((event.mouse_region_x, event.mouse_region_y))

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')

            self.cancel(context)
            return {'FINISHED'}

        return {'RUNNING_MODAL'}
        # return {'PASS_THROUGH'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        
    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            wm = context.window_manager
            self._timer = wm.event_timer_add(0.1, window=context.window)
            wm.modal_handler_add(self)
            args = (self, context)

            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')

            self.mouse_path = []

            context.window_manager.modal_handler_add(self)


            return {'RUNNING_MODAL'}
            # return {'PASS_THROUGH'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}


        


if __name__ == "__main__":
    register()
