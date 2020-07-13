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


class PRESETS_OT_Angle_Object_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_angle_object.list_action"
    bl_label = "Actions"
    bl_description = "Move items up and down or remove"
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
        scn = context.active_object
        idx = scn.presets_angle_index

        try:
            item = scn.presets_angle[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scn.presets_angle) - 1:
                # item_next = scn.presets_angle[idx+1].name
                scn.presets_angle.move(idx, idx+1)
                scn.presets_angle_index += 1

            elif self.action == 'UP' and idx >= 1:
                # item_prev = scn.presets_angle[idx-1].name
                scn.presets_angle.move(idx, idx-1)
                scn.presets_angle_index -= 1
            elif self.action == 'REMOVE':
                # info = 'Item "%s" removed from list' % (scn.presets_angle[idx].name)
                scn.presets_angle_index -= 1
                scn.presets_angle.remove(idx)

        # if self.action == 'ADD':
        #     if context.object:

        #         # def ret(self):
        #         #     return bpy.ops.wm.menu_setprecisemesh_operator_2("INVOKE_DEFAULT")

        #         # context.window_manager.invoke_popup(self, width = 190)
                
        #         # def draw(self, context):

        #         # idx = context.scene.presets_angle_index
        #         # scn = bpy.context.scene.presets_angle[idx]

        #         item = scn.presets_angle.add()
        #         # ret(self)
        #         # bpy.ops.wm.menu_setprecisemesh_operator_2("INVOKE_DEFAULT")
        #         # item.name = bpy.context.scene.presets_angle[idx].name
        #         item.name = context.object.name
        #         item.obj_type = context.object.type
        #         item.obj_id = len(scn.presets_angle)
        #         item.unit = bpy.context.window_manager.setprecisemesh.length
        #         scn.presets_angle_index = len(scn.presets_angle)-1
        #     else:
        #         self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}

class PRESETS_OT_Angle_Object_actions_add(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_angle_object.list_action_add"
    bl_label = "Add"
    bl_description = "Add item"
    bl_options = {'REGISTER'}
    # bl_options = {'BLOCKING'}
    # bl_options = {'INTERNAL'}

    name_input: StringProperty(
        name = "Name")
    unit_input: FloatProperty(
        name="Angle",
        description="Angle",
        min=-360.0, max=360.0,
        default=0.0,
        step = 100.0,
        unit="ROTATION",
        precision = 6,)

    def draw(self, context):
        layout = self.layout

        # row = layout.row()
        # row.alignment = "RIGHT"
        # row.scale_x = 1.7
        layout.prop(self, "unit_input", text = "")

        layout.prop(self, "name_input", text = "Name")


    def invoke(self, context, event):
        self.unit_input = bpy.context.window_manager.setprecisemesh.angle
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        scn = context.active_object
        idx = scn.presets_angle_index

        try:
            item = scn.presets_angle[idx]
        except IndexError:
            pass
            
        if bpy.context.active_object:

            for i in range(-1, len(scn.presets_angle) - 1):
                if scn.presets_angle[i].name == self.name_input and i != len(scn.presets_angle) - 1:
                    text = "A preset with this name already exists"
                    war = "WARNING"
                    self.report({war}, text)
                    break

            item = scn.presets_angle.add()

            item.name = self.name_input
            item.unit = self.unit_input


            # item.obj_id = len(scn.presets_angle)
            scn.presets_angle_index = len(scn.presets_angle) - 1
        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}

class PRESETS_OT_Angle_Object_actions_refresh(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_angle_object.list_action_refresh"
    bl_label = "Export"
    bl_description = "Export item"
    bl_options = {'REGISTER'}

    my_index: IntProperty()

    def execute(self, context):

        bpy.context.active_object.presets_angle_index = self.my_index

        scn = context.active_object
        idx = scn.presets_angle_index

        try:
            item = scn.presets_angle[idx]
        except IndexError:
            pass
            
        if bpy.context.active_object:
    
            bpy.context.window_manager.setprecisemesh.angle = item.unit

            # bpy.context.region.tag_redraw()
            # context.area.tag_redraw()
            # bpy.context.scene.update()

            # for region in context.area.regions:
            #     if region.type == "UI":
            #         region.tag_redraw()

            # bpy.data.scenes.update()

            
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1, time_limit = 0.0)
            bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1)
            print("Warning because of Set Precise Mesh")



            # bpy.ops.wm.redraw_timer(type = "UNDO", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN", iterations = 1, time_limit = 0.0)

            # bpy.ops.wm.redraw_timer(type = "DRAW_SWAP", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW", iterations = 1, time_limit = 0.0)

        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}

class PRESETS_OT_Angle_Object_actions_import(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_angle_object.list_action_import"
    bl_label = "Import"
    bl_description = "Import item"
    bl_options = {'REGISTER'}

    my_index: IntProperty()

    def execute(self, context):

        scn = context.active_object
        idx = scn.presets_angle_index

        try:
            item = scn.presets_angle[self.my_index]
        except IndexError:
            pass
            
        if bpy.context.active_object:
    
            item.unit = bpy.context.window_manager.setprecisemesh.angle

            # bpy.context.region.tag_redraw()
            # context.area.tag_redraw()
            # bpy.context.scene.update()

            # for region in context.area.regions:
            #     if region.type == "UI":
            #         region.tag_redraw()

            # bpy.data.scenes.update()

            
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1, time_limit = 0.0)
            bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1)
            print("Warning because of Set Precise Mesh")



            # bpy.ops.wm.redraw_timer(type = "UNDO", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN", iterations = 1, time_limit = 0.0)

            # bpy.ops.wm.redraw_timer(type = "DRAW_SWAP", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW", iterations = 1, time_limit = 0.0)

            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1, time_limit = 0.0)

        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}

class PRESETS_OT_Angle_Object_Rename(Operator):
    """Clear all items of the list"""
    bl_idname = "presets_angle_object.rename"
    bl_label = "Rename"
    bl_description = "Rename item"
    bl_options = {'INTERNAL'}

    name_input: StringProperty()
    my_index: IntProperty()

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name_input", text = "Name")

    def invoke(self, context, event):

        scn = context.active_object

        try:
            item = scn.presets_angle[self.my_index]
        except IndexError:
            pass

        self.name_input = item.name

        return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self)
        # return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):

        scn = context.active_object

        try:
            item = scn.presets_angle[self.my_index]
        except IndexError:
            pass


        if bpy.context.active_object:

            for i in range(-1, len(scn.presets_angle) - 1):
                if scn.presets_angle[i].name == self.name_input and i != self.my_index:
                    text = "A preset with this name already exists"
                    war = "WARNING"
                    self.report({war}, text)
                    break
            
            item.name = self.name_input
        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")


        return {"FINISHED"}

class PRESETS_OT_Angle_Object_clearList(Operator):
    """Clear all items of the list"""
    bl_idname = "presets_angle_object.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.active_object.presets_angle)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.active_object.presets_angle):
            context.active_object.presets_angle.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return{'FINISHED'}



class PRESETS_OT_Length_Object_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_length_object.list_action"
    bl_label = "Actions"
    bl_description = "Move items up and down or remove"
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
        scn = context.active_object
        idx = scn.presets_length_index

        try:
            item = scn.presets_length[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scn.presets_length) - 1:
                # item_next = scn.presets_length[idx+1].name
                scn.presets_length.move(idx, idx+1)
                scn.presets_length_index += 1

            elif self.action == 'UP' and idx >= 1:
                # item_prev = scn.presets_length[idx-1].name
                scn.presets_length.move(idx, idx-1)
                scn.presets_length_index -= 1
            elif self.action == 'REMOVE':
                # info = 'Item "%s" removed from list' % (scn.presets_length[idx].name)
                scn.presets_length_index -= 1
                scn.presets_length.remove(idx)

        # if self.action == 'ADD':
        #     if context.object:

        #         # def ret(self):
        #         #     return bpy.ops.wm.menu_setprecisemesh_operator_2("INVOKE_DEFAULT")

        #         # context.window_manager.invoke_popup(self, width = 190)
                
        #         # def draw(self, context):

        #         # idx = context.scene.presets_length_index
        #         # scn = bpy.context.scene.presets_length[idx]

        #         item = scn.presets_length.add()
        #         # ret(self)
        #         # bpy.ops.wm.menu_setprecisemesh_operator_2("INVOKE_DEFAULT")
        #         # item.name = bpy.context.scene.presets_length[idx].name
        #         item.name = context.object.name
        #         item.obj_type = context.object.type
        #         item.obj_id = len(scn.presets_length)
        #         item.unit = bpy.context.window_manager.setprecisemesh.length
        #         scn.presets_length_index = len(scn.presets_length)-1
        #     else:
        #         self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}

class PRESETS_OT_Length_Object_actions_add(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_length_object.list_action_add"
    bl_label = "Add"
    bl_description = "Add item"
    bl_options = {'REGISTER'}
    # bl_options = {'BLOCKING'}
    # bl_options = {'INTERNAL'}

    name_input: StringProperty(
        name = "Name")
    unit_input: FloatProperty(
        name="Length",
        description="Length of the edge",
        default=1.0,
        step = 100.0,
        unit='LENGTH',
        precision = 6,)

    def draw(self, context):
        layout = self.layout

        # row = layout.row()
        # row.alignment = "RIGHT"
        # row.scale_x = 1.7
        layout.prop(self, "unit_input", text = "")

        layout.prop(self, "name_input", text = "Name")


    def invoke(self, context, event):
        self.unit_input = bpy.context.window_manager.setprecisemesh.length
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        scn = context.active_object
        idx = scn.presets_length_index

        try:
            item = scn.presets_length[idx]
        except IndexError:
            pass
            
        if bpy.context.active_object:

            for i in range(-1, len(scn.presets_length) - 1):
                if scn.presets_length[i].name == self.name_input and i != len(scn.presets_length) - 1:
                    text = "A preset with this name already exists"
                    war = "WARNING"
                    self.report({war}, text)
                    break

            item = scn.presets_length.add()

            item.name = self.name_input
            item.unit = self.unit_input


            # item.obj_id = len(scn.presets_length)
            scn.presets_length_index = len(scn.presets_length) - 1
        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}

class PRESETS_OT_Length_Object_actions_refresh(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_length_object.list_action_refresh"
    bl_label = "Export"
    bl_description = "Export item"
    bl_options = {'REGISTER'}

    my_index: IntProperty()

    def execute(self, context):

        bpy.context.scene.presets_length_index = self.my_index

        scn = context.active_object
        idx = scn.presets_length_index

        try:
            item = scn.presets_length[idx]
        except IndexError:
            pass
            
        if bpy.context.active_object:
    
            bpy.context.window_manager.setprecisemesh.length = item.unit

            # bpy.context.region.tag_redraw()
            # context.area.tag_redraw()
            # bpy.context.scene.update()

            # for region in context.area.regions:
            #     if region.type == "UI":
            #         region.tag_redraw()

            # bpy.data.scenes.update()

            
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1, time_limit = 0.0)
            bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1)
            print("Warning because of Set Precise Mesh")



            # bpy.ops.wm.redraw_timer(type = "UNDO", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN", iterations = 1, time_limit = 0.0)

            # bpy.ops.wm.redraw_timer(type = "DRAW_SWAP", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW", iterations = 1, time_limit = 0.0)

        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}

class PRESETS_OT_Length_Object_actions_import(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_length_object.list_action_import"
    bl_label = "Import"
    bl_description = "Import item"
    bl_options = {'REGISTER'}

    my_index: IntProperty()

    def execute(self, context):

        scn = context.active_object
        idx = scn.presets_length_index

        try:
            item = scn.presets_length[self.my_index]
        except IndexError:
            pass
            
        if bpy.context.active_object:
    
            item.unit = bpy.context.window_manager.setprecisemesh.length

            # bpy.context.region.tag_redraw()
            # context.area.tag_redraw()
            # bpy.context.scene.update()

            # for region in context.area.regions:
            #     if region.type == "UI":
            #         region.tag_redraw()

            # bpy.data.scenes.update()

            
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1, time_limit = 0.0)
            bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1)
            print("Warning because of Set Precise Mesh")



            # bpy.ops.wm.redraw_timer(type = "UNDO", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN", iterations = 1, time_limit = 0.0)

            # bpy.ops.wm.redraw_timer(type = "DRAW_SWAP", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW", iterations = 1, time_limit = 0.0)

            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1, time_limit = 0.0)

        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}

class PRESETS_OT_Length_Object_Rename(Operator):
    """Clear all items of the list"""
    bl_idname = "presets_length_object.rename"
    bl_label = "Rename"
    bl_description = "Rename item"
    bl_options = {'INTERNAL'}

    name_input: StringProperty()
    my_index: IntProperty()

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name_input", text = "Name")

    def invoke(self, context, event):

        scn = context.active_object

        try:
            item = scn.presets_length[self.my_index]
        except IndexError:
            pass

        self.name_input = item.name

        return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self)
        # return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):

        scn = context.active_object

        try:
            item = scn.presets_length[self.my_index]
        except IndexError:
            pass


        if bpy.context.active_object:

            for i in range(-1, len(scn.presets_length) - 1):
                if scn.presets_length[i].name == self.name_input and i != self.my_index:
                    text = "A preset with this name already exists"
                    war = "WARNING"
                    self.report({war}, text)
                    break
            
            item.name = self.name_input
        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")


        return {"FINISHED"}

class PRESETS_OT_Length_Object_clearList(Operator):
    """Clear all items of the list"""
    bl_idname = "presets_length_object.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.active_object.presets_length)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.active_object.presets_length):
            context.active_object.presets_length.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return{'FINISHED'}



       
class PRESETS_UL_items_Angle_Object(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        scn = context.active_object
        idx = scn.presets_angle_index

        row = layout.row(align = 0)

        row.scale_y = 1.1

        row.operator("presets_angle_object.list_action_refresh", text = item.name, emboss = 0, depress=0).my_index = index
        # row.prop(item, "name", emboss=False, text = "")
        row.prop(item, "unit", emboss=0, text = "", expand = 1)

        row.operator("presets_angle_object.list_action_import", text = "", icon = "IMPORT", emboss = 0).my_index = index
        row.operator("presets_angle_object.rename", text = "", icon = "SORTALPHA", emboss = 0).my_index = index

class PRESETS_PT_presets_List_Angle_Object(Panel):
    """Adds a custom panel to the TEXT_EDITOR"""
    
    bl_idname = 'OBJECT_PT_presets_angle'
    bl_label = "Angle Presets"
    bl_options = {'DEFAULT_CLOSED'}

    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    # bl_context = "mesh_edit"

    @classmethod
    def poll(cls, context):
        return bpy.context.active_object != None\
            and bpy.context.active_object.mode in {'EDIT'}

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon = "DRIVER_ROTATIONAL_DIFFERENCE")

    def draw(self, context):

        if bpy.context.active_object.mode in {'EDIT'}:
        
            layout = self.layout
            scn = bpy.context.active_object

            rows = 5
            row = layout.row()
            row.template_list("PRESETS_UL_items_Angle_Object", "", scn, "presets_angle", scn, "presets_angle_index", rows=rows)

            col = row.column(align=True)
            col.scale_x = 1.1
            col.scale_y = 1.2

            # col.operator("presets_angle.list_action", icon='ADD', text="").action = 'ADD'
            col.operator("presets_angle_object.list_action_add", icon='ADD', text="")
            col.operator("presets_angle_object.list_action", icon='REMOVE', text="").action = 'REMOVE'
            
            col.separator(factor = 0.4)

            col.operator("presets_angle_object.list_action", icon='TRIA_UP', text="").action = 'UP'
            col.operator("presets_angle_object.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

            col.separator(factor = 0.4)
            # row = layout.row()
            # col = row.column(align=True)
            # row = col.row(align=True)
            col.operator("presets_angle_object.clear_list", icon="TRASH", text = "")
            # row.operator("presets_angle.remove_duplicates", icon="GHOST_ENABLED")



class PRESETS_UL_items_Length_Object(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        scn = context.active_object
        idx = scn.presets_length_index

        row = layout.row(align = 0)

        row.scale_y = 1.1

        row.operator("presets_length_object.list_action_refresh", text = item.name, emboss = 0, depress=0).my_index = index
        row.prop(item, "unit", emboss=0, text = "", expand = 1)

        row.operator("presets_length_object.list_action_import", text = "", icon = "IMPORT", emboss = 0).my_index = index
        row.operator("presets_length_object.rename", text = "", icon = "SORTALPHA", emboss = 0).my_index = index

class PRESETS_PT_presets_List_Length_Object(Panel):
    """Adds a custom panel to the TEXT_EDITOR"""
    
    bl_idname = 'OBJECT_PT_presets_length'
    bl_label = "Length / Distance Presets"
    bl_options = {'DEFAULT_CLOSED'}

    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return bpy.context.active_object != None\
            and bpy.context.active_object.mode in {'EDIT'}

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon = "DRIVER_DISTANCE")

    def draw(self, context):

        if bpy.context.active_object.mode in {'EDIT'}:
        
            layout = self.layout
            # scn = bpy.context.scene
            scn =  bpy.context.active_object

            rows = 5
            row = layout.row()
            row.template_list("PRESETS_UL_items_Length_Object", "", scn, "presets_length", scn, "presets_length_index", rows = rows)

            col = row.column(align=True)
            col.scale_x = 1.1
            col.scale_y = 1.2

            # col.operator("presets_length.list_action", icon='ADD', text="").action = 'ADD'
            col.operator("presets_length_object.list_action_add", icon='ADD', text="")
            col.operator("presets_length_object.list_action", icon='REMOVE', text="").action = 'REMOVE'
            
            col.separator(factor = 0.4)

            col.operator("presets_length_object.list_action", icon='TRIA_UP', text="").action = 'UP'
            col.operator("presets_length_object.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

            col.separator(factor = 0.4)
            # row = layout.row()
            # col = row.column(align=True)
            # row = col.row(align=True)
            col.operator("presets_length_object.clear_list", icon="TRASH", text = "")
            # row.operator("presets_length.remove_duplicates", icon="GHOST_ENABLED")


if __name__ == "__main__":
    register()