import bpy

from bpy.props import (IntProperty,
                       BoolProperty,
                       StringProperty,
                       CollectionProperty,
                       FloatProperty,
                       )

from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       UIList)

# -------------------------------------------------------------------
#   Operators
# -------------------------------------------------------------------

class CUSTOM_OT_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "custom.list_action"
    bl_label = "List Actions"
    bl_description = "Move items up and down, add and remove"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", "")))

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.custom_index

        try:
            item = scn.custom[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scn.custom) - 1:
                # item_next = scn.custom[idx+1].name
                scn.custom.move(idx, idx+1)
                scn.custom_index += 1

            elif self.action == 'UP' and idx >= 1:
                # item_prev = scn.custom[idx-1].name
                scn.custom.move(idx, idx-1)
                scn.custom_index -= 1
            elif self.action == 'REMOVE':
                # info = 'Item "%s" removed from list' % (scn.custom[idx].name)
                scn.custom_index -= 1
                scn.custom.remove(idx)

        if self.action == 'ADD':
            if context.object:

                # context.window_manager.invoke_popup(self, width = 190)
                bpy.ops.wm.menu_setprecisemesh_operator_2("INVOKE_DEFAULT")
            
                # def draw(self, context):


                item = scn.custom.add()
                item.name = context.object.name
                item.obj_type = context.object.type
                item.obj_id = len(scn.custom)
                item.unit = bpy.context.window_manager.setprecisemesh.length
                scn.custom_index = len(scn.custom)-1
            else:
                self.report({'INFO'}, "Nothing selected in the Viewport")
        return {"FINISHED"}

    def draw(self, context):
        col_top.prop(w_m, "data_block", text = "")

    # return inv

class CUSTOM_OT_pop_up(Operator):
    """Clear all items of the list"""
    bl_idname = "wm.menu_setprecisemesh_operator_2"
    bl_label = "Pop-up Menu"
    bl_description = "To make it convenient to use the pop-up menu You can assign shortcut \n \
         ( For exaple Ctrl + Alt + Wheel Down )\n \
        How to do it: > right-click on this button > Assign Shortcut"
        
    def execute(self, context):

        # context.window_manager.invoke_popup(self, width = 200)
        return {'FINISHED'}

    def invoke(self, context, event):
        # x = event.mouse_x
        # y = event.mouse_y 

        # move_x = 0
        # move_y = 60

        # bpy.context.window.cursor_warp(x + move_x, y + move_y)
        # context.window_manager.invoke_popup(self, width = 200)
        return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self, width=600, height=500)
        # return context.window_manager.invoke_popup(self)
        # inv = context.window_manager.invoke_popup(self, width = 200)
        
        # bpy.context.window.cursor_warp(x, y)

        # return inv

        # return {"INTERFACE"}

        # if self.return == {"CANCELLED"}:
            # context.window_manager.invoke_popup(self, width = 200)
        # return

        # return context.window_manager.invoke_props_popup(self, event)
        # return context.window_manager.invoke_confirm(self, event)
    def draw(self, context):
        layout = self.layout

        w_m = context.window_manager.setprecisemesh

        layout.prop(w_m, "data_block", text = "")
        # bpy.types.VIEW3D_PT_edit_mesh_set_precise_mesh1.draw(self, context)


class CUSTOM_OT_clearList(Operator):
    """Clear all items of the list"""
    bl_idname = "custom.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.custom)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.custom):
            context.scene.custom.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return{'FINISHED'}

class CUSTOM_OT_removeDuplicates(Operator):
    """Remove all duplicates"""
    bl_idname = "custom.remove_duplicates"
    bl_label = "Remove Duplicates"
    bl_description = "Remove all duplicates"
    bl_options = {'INTERNAL'}

    def find_duplicates(self, context):
        """find all duplicates by name"""
        name_lookup = {}
        for c, i in enumerate(context.scene.custom):
            name_lookup.setdefault(i.name, []).append(c)
        duplicates = set()
        for name, indices in name_lookup.items():
            for i in indices[1:]:
                duplicates.add(i)
        return sorted(list(duplicates))

    @classmethod
    def poll(cls, context):
        return bool(context.scene.custom)

    def execute(self, context):
        scn = context.scene
        removed_items = []
        # Reverse the list before removing the items
        for i in self.find_duplicates(context)[::-1]:
            scn.custom.remove(i)
            removed_items.append(i)
        if removed_items:
            scn.custom_index = len(scn.custom)-1
            info = ', '.join(map(str, removed_items))
            self.report({'INFO'}, "Removed indices: %s" % (info))
        else:
            self.report({'INFO'}, "No duplicates")
        return{'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)
# -------------------------------------------------------------------
#   Drawing
# -------------------------------------------------------------------
class CUSTOM_UL_items(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # split = layout.split(factor=0.3)
        row = layout.row()
        # split.label(text="Index: %d" % (index))
        custom_icon = "OUTLINER_OB_%s" % item.obj_type
        #split.prop(item, "name", text="", emboss=False, translate=False, icon=custom_icon)
        row.label(text=item.name, icon=custom_icon) # avoids renaming the item by accident
        row.label(text = str(item.unit))

    def invoke(self, context, event):
        pass   

class CUSTOM_PT_objectList(Panel):
    """Adds a custom panel to the TEXT_EDITOR"""
    bl_idname = 'TEXT_PT_my_panel'
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_label = "Custom Object List Demo"

    # bl_space_type = 'PROPERTIES'
    # bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene

        rows = 2
        row = layout.row()
        row.template_list("CUSTOM_UL_items", "", scn, "custom", scn, "custom_index", rows=rows)

        col = row.column(align=True)
        col.operator("custom.list_action", icon='ADD', text="").action = 'ADD'
        col.operator("custom.list_action", icon='REMOVE', text="").action = 'REMOVE'
        col.separator()
        col.operator("custom.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("custom.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("custom.clear_list", icon="X")
        row.operator("custom.remove_duplicates", icon="GHOST_ENABLED")

# -------------------------------------------------------------------
#   Collection
# -------------------------------------------------------------------

class CUSTOM_objectCollection(PropertyGroup):
    #name: StringProperty() -> Instantiated by default
    unit: FloatProperty()
    name: StringProperty()
    obj_type: StringProperty()
    obj_id: IntProperty()

if __name__ == "__main__":
    register()