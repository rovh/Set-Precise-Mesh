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




class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"

    _timer = None

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            wm = context.window_manager
            wm.event_timer_remove(self._timer)
            return {'CANCELLED'}

        if event.type == 'TIMER':

            

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}


    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            args = (self, context)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}
        

if __name__ == "__main__":
    register()
