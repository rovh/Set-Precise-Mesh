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
            # ('ADD', "Add", "")
            )
            )

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

        # if self.action == 'ADD':
        #     if context.object:

        #         # def ret(self):
        #         #     return bpy.ops.wm.menu_setprecisemesh_operator_2("INVOKE_DEFAULT")

        #         # context.window_manager.invoke_popup(self, width = 190)
                
        #         # def draw(self, context):

        #         # idx = context.scene.custom_index
        #         # scn = bpy.context.scene.custom[idx]

        #         item = scn.custom.add()
        #         # ret(self)
        #         # bpy.ops.wm.menu_setprecisemesh_operator_2("INVOKE_DEFAULT")
        #         # item.name_unit = bpy.context.scene.custom[idx].name_unit
        #         item.name = context.object.name
        #         item.obj_type = context.object.type
        #         item.obj_id = len(scn.custom)
        #         item.unit = bpy.context.window_manager.setprecisemesh.length
        #         scn.custom_index = len(scn.custom)-1
        #     else:
        #         self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}

class CUSTOM_OT_actions_add(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "custom.list_action_add"
    bl_label = "Add"
    bl_description = "Move items up and down, add and remove"
    bl_options = {'REGISTER'}
    # bl_options = {'BLOCKING'}
    # bl_options = {'INTERNAL'}

    name_input: StringProperty()
    unit_input: FloatProperty(
        name="Length",
        description="Length of the edge",
        default=1.0,
        step = 100.0,
        unit='LENGTH',
        precision = 6,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "unit_input", text = "")
        layout.prop(self, "name_input", text = "Name")


    def invoke(self, context, event):
        self.unit_input = bpy.context.window_manager.setprecisemesh.length
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        scn = context.scene
        idx = scn.custom_index

        try:
            item = scn.custom[idx]
        except IndexError:
            pass
            
        # if self.action == 'ADD':
        # if bpy.context.object:
        if bpy.context.active_object:
            item = scn.custom.add()

            # item.name = context.active_object.name
            # item.obj_type = context.active_object.type

            item.name_unit = self.name_input
            item.unit = self.unit_input

            # item.obj_id = len(scn.custom)
            # item.unit = bpy.context.window_manager.setprecisemesh.length
            scn.custom_index = len(scn.custom)-1
        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}

class CUSTOM_OT_actions_refresh(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "custom.list_action_refresh"
    bl_label = "Add"
    bl_description = "Move items up and down, add and remove"
    bl_options = {'REGISTER'}

    def execute(self, context):

        scn = context.scene
        idx = scn.custom_index

        try:
            item = scn.custom[idx]
        except IndexError:
            pass
            
        # if self.action == 'ADD':
        # if bpy.context.object:
        if bpy.context.active_object:
    
            bpy.context.window_manager.setprecisemesh.length = item.unit
            bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1, time_limit = 0.0)

        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")

        return {'RUNNING_MODAL'}
        # return {"FINISHED"}

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

# class CUSTOM_OT_removeDuplicates(Operator):
#     """Remove all duplicates"""
#     bl_idname = "custom.remove_duplicates"
#     bl_label = "Remove Duplicates"
#     bl_description = "Remove all duplicates"
#     bl_options = {'INTERNAL'}

#     def find_duplicates(self, context):
#         """find all duplicates by name"""
#         name_lookup = {}
#         for c, i in enumerate(context.scene.custom):
#             name_lookup.setdefault(i.name, []).append(c)
#         duplicates = set()
#         for name, indices in name_lookup.items():
#             for i in indices[1:]:
#                 duplicates.add(i)
#         return sorted(list(duplicates))

#     @classmethod
#     def poll(cls, context):
#         return bool(context.scene.custom)

#     def execute(self, context):
#         scn = context.scene
#         removed_items = []
#         # Reverse the list before removing the items
#         for i in self.find_duplicates(context)[::-1]:
#             scn.custom.remove(i)
#             removed_items.append(i)
#         if removed_items:
#             scn.custom_index = len(scn.custom)-1
#             info = ', '.join(map(str, removed_items))
#             self.report({'INFO'}, "Removed indices: %s" % (info))
#         else:
#             self.report({'INFO'}, "No duplicates")
#         return{'FINISHED'}

#     def invoke(self, context, event):
#         return context.window_manager.invoke_confirm(self, event)
# -------------------------------------------------------------------
#   Drawing
# -------------------------------------------------------------------
class CUSTOM_UL_items(UIList):


    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        scn = context.scene
        idx = scn.custom_index

        # if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # split = layout.split(factor=0.3)
            # split.label(text="Index: %d" % (index))
            # custom_icon = "OUTLINER_OB_%s" % item.obj_type
            #split.prop(item, "name", text="", emboss=False, translate=False, icon=custom_icon)
        row = layout.row(align = 0)

        row.scale_y = 1.1
        row.scale_x = 1.1
        # row.label(text=item.name, icon=custom_icon) # avoids renaming the item by accident
        

        row.prop(item, "name_unit", emboss=False, text = "")
        row.prop(item, "unit", emboss=0, text = "")
        row.operator("custom.list_action_refresh", text = "", icon = "EXPORT", emboss = 0)

        # length_remember_index_for_preset = bpy.context.window_manager.setprecisemesh.length_remember_index_for_preset

        # if bpy.context.scene.custom_index == length_remember_index_for_preset:
        # def do(self):
        #     bpy.ops.custom.list_action_refresh()

        # do(self)

        # bpy.context.window_manager.setprecisemesh.length = item.unit

        # bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1, time_limit = 0.0)
            
        # print("\n", idx)

            # print(item)

            # if bpy.context.scene.custom_index == idx:

            # row.prop(item, "unit", emboss=0, text = "")



            # row.label(text = str(item.name_unit) + ":")
            # row.label(text = str(item.unit))


            # layout.prop(vgroup, "name", text="", emboss=False, icon_value=icon)

    # def invoke(self, context, event):
    #     bpy.ops.custom.list_action_refresh()
        
    #     # print(222222222222222222222)
    #     pass   

    # def execute(self,context):
    #     bpy.ops.custom.list_action_refresh()
    #     return {'RUNNING_MODAL'}
        # return {"FINISHED"}

class CUSTOM_PT_objectList(Panel):
    """Adds a custom panel to the TEXT_EDITOR"""
    
    bl_idname = 'TEXT_PT_my_panel'
    # bl_space_type = "TEXT_EDITOR"
    # bl_region_type = "UI"
    bl_label = "Length Presets"

    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    # bl_context = "mesh_edit"

    # bl_options = {"HIDE_HEADER"}
    

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene

        rows = 4
        row = layout.row()
        row.template_list("CUSTOM_UL_items", "", scn, "custom", scn, "custom_index", rows=rows)

        col = row.column(align=True)
        col.scale_x = 1.1
        col.scale_y = 1.2

        # col.operator("custom.list_action", icon='ADD', text="").action = 'ADD'
        col.operator("custom.list_action_add", icon='ADD', text="")
        col.operator("custom.list_action", icon='REMOVE', text="").action = 'REMOVE'
        
        col.separator()

        col.operator("custom.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("custom.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("custom.clear_list", icon="X")
        # row.operator("custom.remove_duplicates", icon="GHOST_ENABLED")

# -------------------------------------------------------------------
#   Collection
# -------------------------------------------------------------------

class CUSTOM_objectCollection(PropertyGroup):
    #name: StringProperty() -> Instantiated by default
    unit: FloatProperty(
        name="Length",
        description="Length of the edge",
        step = 100.0,
        unit='LENGTH',
        precision = 6,
    )
    name_unit: StringProperty()
    # obj_type: StringProperty()
    # obj_id: IntProperty()

if __name__ == "__main__":
    register()