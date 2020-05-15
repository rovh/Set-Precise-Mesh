# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Set Presice Mesh /CAD",
    "author" : "Rovh",
    "description" : "This addon allows you to set exact values for the mesh",
    "blender" : (2, 82, 0),
    "version" : (1,0,3),
    "location" : "View3D > Sidebar in Edit Mode > Item Tab and View Tab",
    "warning" : "",
    "wiki_url": "https://github.com/rovh/Set-Precise-Mesh",
    "category" : "Mesh"
}

import bpy

from .SetAngle import *
from .SetLength import *

from bpy import types
from bpy.props import (
        FloatProperty,
        BoolProperty,
        PointerProperty,
        EnumProperty,
        )


class DialogWarningOperator(bpy.types.Operator):
    bl_idname = "object.dialog_warning_operator"
    bl_label = "Warning Panel Operator"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event): 
        bool_warning = bpy.data.scenes[bpy.context.scene.name_full].bool_warning
        settings = bpy.context.preferences.addons[__name__].preferences
        bool_warning_global = settings.bool_warning_global

        if bool_warning_global == 1:
            if bool_warning == 1:
                # return context.window_manager.invoke_props_dialog(self)
                return context.window_manager.invoke_popup(self, width=700)
                # return context.window_manager.invoke_popup(self)
                # return context.window_manager.invoke_props_popup(self, event)
                # return context.window_manager.invoke_confirm(self, event)
            else:
                return {'FINISHED'}
        else:
            return {'FINISHED'}


    def draw(self, context):
        layout = self.layout
        layout.label(text='Warning' , icon="ERROR")

        if bpy.context.object.scale != Vector((1.0, 1.0, 1.0)):
            
            layout.label(text='Your object scale is not by default. Please, apply "Scale"')
            layout.label(text='Shortcut: Objetc Mode > Ctrl A > Apply "Scale"')

        elif bpy.context.object.delta_scale != Vector((1.0, 1.0, 1.0)):

            layout.label(text='Your object delta transform scale is not by default. Please, change it')
            layout.label(text='How to do it: Properties Editor > Object Properties > Transform > Delta Transform >')
            layout.label(text='> You need to set values: All Scales = 1')

        layout.prop(context.scene, "bool_warning", text="Show Warning Panel next time (Warning: Panel will show up in new Blender file even if you disable it)")
        layout.label(text="If you need to disable it globally (so that it does not show up in new Blender file), you need to go to Set Precise Mesh Preferences")
        layout.label(text="Warning Panel appears if object scale or delta scale is not by default")
        layout.label(text='You can find more info about this warning in README.md on Github page or in files')
        # layout.label(text='https://github.com/rovh/Set-Precise-Mesh')

class MenuSetPreciseMeshOperator(bpy.types.Operator):
    bl_idname = "wm.menu_setprecisemesh_operator"
    bl_label = "Pop-up Menu"
    bl_description = "To make it convenient to use the pop-up menu You can assign shortcut \n \
         (For exaple Alt+R )\n \
        How to do it: > right-click on this button > Assign Shortcut"
        
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event): 
        
        # return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self, width=600, height=500)
        # return context.window_manager.invoke_popup(self)
        return context.window_manager.invoke_popup(self, width = 200)
        # return context.window_manager.invoke_props_popup(self, event)
        # return context.window_manager.invoke_confirm(self, event)

    
    def draw(self, context):
        layout = self.layout

        scene = context.scene
        sc = scene
        ob = context.object

        w_m = context.window_manager.setprecisemesh

        # Get values
        bool_panel_arrow = bpy.data.scenes[bpy.context.scene.name_full].bool_panel_arrow
        bool_panel_arrow2 = bpy.data.scenes[bpy.context.scene.name_full].bool_panel_arrow2

        col = layout.column(align=True)

        
        split = col.split(factor=0.85, align=True)
        split.scale_y =1.2      

        split.operator("mesh.change_angle", icon="DRIVER_ROTATIONAL_DIFFERENCE")

        
    
        if sc.bool_panel_arrow:
            split.prop(sc, "bool_panel_arrow", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(sc, "bool_panel_arrow", text="", icon='RIGHTARROW')

        if sc.bool_panel_arrow:
            
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            
            col_top.prop(w_m, "angle")
            col_top.prop(w_m, "anglebool" )
            # col_top.prop(ob, "angleinput")         
                    
        col = layout.column(align=False)
        col = layout.column(align=True)

        
        split = col.split(factor=0.85, align=True)
        split.scale_y =1.2
        
        split.operator("mesh.change_length",icon="DRIVER_DISTANCE")
        
    
        if sc.bool_panel_arrow2:
            split.prop(sc, "bool_panel_arrow2", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(sc, "bool_panel_arrow2", text="", icon='RIGHTARROW')

        if sc.bool_panel_arrow2:            
            box = col.column(align=True).box().column()            
            col_top = box.column(align=True)
            col_top.prop(w_m, "length")            
            col_top.prop(w_m, "lengthbool")            
            # col_top.prop(ob, "lengthinput")


class SetPreciseMeshPreferences(bpy.types.AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__


    direction_of_length: BoolProperty(
            name="bool",
            description="Change direction",
            default=False,
            )

    direction_of_angle: BoolProperty(
            name="bool",
            description="Change direction",
            default=False,
            )
    bool_warning_global: BoolProperty(
            name="bool",
            description="Globally",
            default=True,
            )


    def draw(self, context):
        layout = self.layout
        layout.label(icon="PREFERENCES")

        row = layout.row()
        col = row.column()
        # col.label(text="Tab Category:")
        col.prop(self, "direction_of_length", text='Invert "Set Length" direction')
        # col.prop(self, "direction_of_angle", text='Invert "Set Angle" direction')
        col.operator("wm.menu_setprecisemesh_operator",icon="MENU_PANEL", text="Pop-up Menu (Hover cursor on it for more information)")
        col.prop(self, "bool_warning_global", text='Show Warning Panel in Blender (Global)')

class VIEW3D_PT_Set_Precise_Mesh(bpy.types.Header):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOL_HEADER'

    # @staticmethod
    # def draw_xform_template(layout, context):
    #     obj = context.active_object
    #     object_mode = 'OBJECT' if obj is None else obj.mode
    #     has_pose_mode = (
    #         (object_mode == 'POSE') or
    #         (object_mode == 'WEIGHT_PAINT' and context.pose_object is not None)
    #     )

    #     tool_settings = context.tool_settings

    #     # Mode & Transform Settings
    #     scene = context.scene

    #     # Orientation
    #     if object_mode in {'OBJECT', 'EDIT', 'EDIT_GPENCIL'} or has_pose_mode:
    #         orient_slot = scene.transform_orientation_slots[0]
    #         row = layout.row(align=True)

    #         sub = row.row()
    #         sub.ui_units_x = 4
    #         sub.prop_with_popover(
    #             orient_slot,
    #             "type",
    #             text="",
    #             panel="VIEW3D_PT_transform_orientations",
    #         )

    #     # Pivot
    #     if object_mode in {'OBJECT', 'EDIT', 'EDIT_GPENCIL', 'SCULPT_GPENCIL'} or has_pose_mode:
    #         layout.prop(tool_settings, "transform_pivot_point", text="", icon_only=True)

    #     # Snap
    #     show_snap = False
    #     if obj is None:
    #         show_snap = True
    #     else:
    #         if (object_mode not in {
    #                 'SCULPT', 'VERTEX_PAINT', 'WEIGHT_PAINT', 'TEXTURE_PAINT',
    #                 'PAINT_GPENCIL', 'SCULPT_GPENCIL', 'WEIGHT_GPENCIL'
    #         }) or has_pose_mode:
    #             show_snap = True
    #         else:

    #             paint_settings = UnifiedPaintPanel.paint_settings(context)

    #             if paint_settings:
    #                 brush = paint_settings.brush
    #                 if brush and hasattr(brush, "stroke_method") and brush.stroke_method == 'CURVE':
    #                     show_snap = True

    #     if show_snap:
    #         snap_items = bpy.types.ToolSettings.bl_rna.properties["snap_elements"].enum_items
    #         snap_elements = tool_settings.snap_elements
    #         if len(snap_elements) == 1:
    #             text = ""
    #             for elem in snap_elements:
    #                 icon = snap_items[elem].icon
    #                 break
    #         else:
    #             text = "Mix"
    #             icon = 'NONE'
    #         del snap_items, snap_elements

    #         row = layout.row(align=True)
    #         row.prop(tool_settings, "use_snap", text="")

    #         sub = row.row(align=True)
    #         sub.popover(
    #             panel="VIEW3D_PT_snapping",
    #             icon=icon,
    #             text=text,
    #         )

    #     # Proportional editing
    #     if object_mode in {'EDIT', 'PARTICLE_EDIT', 'SCULPT_GPENCIL', 'EDIT_GPENCIL', 'OBJECT'}:
    #         row = layout.row(align=True)
    #         kw = {}
    #         if object_mode == 'OBJECT':
    #             attr = "use_proportional_edit_objects"
    #         else:
    #             attr = "use_proportional_edit"

    #             if tool_settings.use_proportional_edit:
    #                 if tool_settings.use_proportional_connected:
    #                     kw["icon"] = 'PROP_CON'
    #                 elif tool_settings.use_proportional_projected:
    #                     kw["icon"] = 'PROP_PROJECTED'
    #                 else:
    #                     kw["icon"] = 'PROP_ON'
    #             else:
    #                 kw["icon"] = 'PROP_OFF'

    #         row.prop(tool_settings, attr, icon_only=True, **kw)
    #         sub = row.row(align=True)
    #         sub.active = getattr(tool_settings, attr)
    #         sub.prop_with_popover(
    #             tool_settings,
    #             "proportional_edit_falloff",
    #             text="",
    #             icon_only=True,
    #             panel="VIEW3D_PT_proportional_edit",
    #         )

    def draw(self, context):
    # def draw_xform_template(layout, context):
        layout = self.layout

        # layout.row(align=True).template_header()

        # self.draw_tool_settings(context)

        # layout.separator_spacer()

        # bpy.types.VIEW3D_HT_header.draw_xform_template(layout, context)

        # layout.separator_spacer()

        # self.draw_mode_settings(context)

        tool_settings = context.tool_settings
        view = context.space_data
        shading = view.shading
        show_region_tool_header = view.show_region_tool_header

        # if not show_region_tool_header:
        #     layout.row(align=True).template_header()   
         # layout.row(align=1).template_header()
        object_mode = context.active_object.mode


        if object_mode in {'EDIT'}:
            # layout.prop(tool_settings, "transform_pivot_point", text="", icon_only=True)
            # layout.separator(factor=1.0)
            # layout.separator()
            # sub = row.row(align=True)
            # layout.separator()
            # layout.separator(factor = 4.0)
            # layout.separator_spacer()
            # if context.space_data.show_region_tool_header == True or context.mode[:4] not in ('EDIT', 'OBJE'):
            # layout.separator_spacer()
            # layout.separator(factor=20.0)
            # layout.separator_spacer()
            # layout.separator(factor=-20.0)
            # layout.row(align=True).template_header()


            layout.separator_spacer()

            VIEW3D_HT_header.draw_xform_template(layout, context)

            layout.separator_spacer()

            # layout.menu("VIEW3D_HT_header.draw_xform_template(layout, context)")
            
            row = layout.row(align=1)
            
            sub = row.row()
            sub.ui_units_x = 4
            # layout.separator(factor=0)
            # layout.separator()
            row.operator("wm.menu_setprecisemesh_operator", text="Projection type", icon = "ADD")
            # layout.separator()

        # row = layout.row(align=True)
        # sub = row.row(align=True)

        
        # mode_string = context.mode
        # object_mode = 'EDIT' if obj is None else obj.mode
        # object_mode = obj.mode

        # has_pose_mode = (
        #     (object_mode == 'POSE') or
        #     (object_mode == 'WEIGHT_PAINT' and context.pose_object is not None)
        # )

        # Note: This is actually deadly in case enum_items have to be dynamically generated
        #       (because internal RNA array iterator will free everything immediately...).
        # XXX This is an RNA internal issue, not sure how to fix it.
        # Note: Tried to add an accessor to get translated UI strings instead of manual call
        #       to pgettext_iface below, but this fails because translated enumitems
        #       are always dynamically allocated.
        # act_mode_item = bpy.types.Object.bl_rna.properties["mode"].enum_items[object_mode]
        # act_mode_i18n_context = bpy.types.Object.bl_rna.properties["mode"].translation_context
        # row = layout.row(align=True)
        # row.prop(tool_settings, "use_snap", text="")

        # sub = row.row(align=True)
        # sub.popover(
        #     panel="VIEW3D_PT_snapping",
        #     icon=icon,
        #     text=text,
        # )
        
        # sub.active = getattr(tool_settings, attr)
        
        # sub.ui_units_x = 5.5
        # sub.operator_menu_enum(
        #     "object.mode_set", "mode",
        #     text=bpy.app.translations.pgettext_iface(act_mode_item.name, act_mode_i18n_context),
        #     icon=act_mode_item.icon,
        # )
        # TOPBAR_MT_editor_menus.draw_collapsible(context, layout)
        # if object_mode in {'EDIT'}:
        #     # layout.prop(tool_settings, "transform_pivot_point", text="", icon_only=True)
        #     # layout.separator(factor=1.0)
        #     # layout.separator()
        #     sub = row.row(align=True)
        #     sub.operator("wm.menu_setprecisemesh_operator", text="Projection type", icon = "ADD")
        # del act_mode_item
        # layout.separator_spacer()
        # layout.template_header_3D_mode()

        # Contains buttons like Mode, Pivot, Layer, Mesh Select Mode...
        # if obj:
        #     # Particle edit
        #     if object_mode == 'PARTICLE_EDIT':
        #         row = layout.row()
        #         row.prop(tool_settings.particle_edit, "select_mode", text="", expand=True)

        # # Grease Pencil
        # if obj and obj.type == 'GPENCIL' and context.gpencil_data:
        #     gpd = context.gpencil_data

        #     if gpd.is_stroke_paint_mode:
        #         row = layout.row()
        #         sub = row.row(align=True)
        #         sub.prop(tool_settings, "use_gpencil_draw_onback", text="", icon='MOD_OPACITY')
        #         sub.separator(factor=0.4)
        #         sub.prop(tool_settings, "use_gpencil_weight_data_add", text="", icon='WPAINT_HLT')
        #         sub.separator(factor=0.4)
        #         sub.prop(tool_settings, "use_gpencil_draw_additive", text="", icon='FREEZE')

        #     # Select mode for Editing
        #     if gpd.use_stroke_edit_mode:
        #         row = layout.row(align=True)
        #         row.prop(tool_settings, "gpencil_selectmode_edit", text="", expand=True)

        #     # Select mode for Sculpt
        #     if gpd.is_stroke_sculpt_mode:
        #         row = layout.row(align=True)
        #         row.prop(tool_settings, "use_gpencil_select_mask_point", text="")
        #         row.prop(tool_settings, "use_gpencil_select_mask_stroke", text="")
        #         row.prop(tool_settings, "use_gpencil_select_mask_segment", text="")

        #     if gpd.use_stroke_edit_mode or gpd.is_stroke_sculpt_mode or gpd.is_stroke_weight_mode:
        #         row = layout.row(align=True)
        #         row.prop(gpd, "use_multiedit", text="", icon='GP_MULTIFRAME_EDITING')

        #         sub = row.row(align=True)
        #         sub.active = gpd.use_multiedit
        #         sub.popover(
        #             panel="VIEW3D_PT_gpencil_multi_frame",
        #             text="Multiframe",
        #         )

        #     if gpd.use_stroke_edit_mode:
        #         row = layout.row(align=True)
        #         row.popover(
        #             panel="VIEW3D_PT_tools_grease_pencil_interpolate",
        #             text="Interpolate",
        #         )

        # overlay = view.overlay

        # VIEW3D_MT_editor_menus.draw_collapsible(context, layout)

        # layout.separator_spacer()

        # if object_mode in {'PAINT_GPENCIL', 'SCULPT_GPENCIL'}:
        #     # Grease pencil
        #     if object_mode == 'PAINT_GPENCIL':
        #         layout.prop_with_popover(
        #             tool_settings,
        #             "gpencil_stroke_placement_view3d",
        #             text="",
        #             panel="VIEW3D_PT_gpencil_origin",
        #         )

            # if object_mode in {'PAINT_GPENCIL', 'SCULPT_GPENCIL'}:
            #     layout.prop_with_popover(
            #         tool_settings.gpencil_sculpt,
            #         "lock_axis",
            #         text="",
            #         panel="VIEW3D_PT_gpencil_lock",
            #     )

            # if object_mode == 'PAINT_GPENCIL':
            #     # FIXME: this is bad practice!
            #     # Tool options are to be displayed in the topbar.
            #     if context.workspace.tools.from_space_view3d_mode(object_mode).idname == "builtin_brush.Draw":
            #         settings = tool_settings.gpencil_sculpt.guide
            #         row = layout.row(align=True)
            #         row.prop(settings, "use_guide", text="", icon='GRID')
            #         sub = row.row(align=True)
            #         sub.active = settings.use_guide
            #         sub.popover(
            #             panel="VIEW3D_PT_gpencil_guide",
            #             text="Guides",
            #         )

            # layout.separator_spacer()
        # elif not show_region_tool_header:
        #     # Transform settings depending on tool header visibility
        #     VIEW3D_HT_header.draw_xform_template(layout, context)

        #     layout.separator_spacer()

        # Viewport Settings
        # layout.popover(
        #     panel="VIEW3D_PT_object_type_visibility",
        #     icon_value=view.icon_from_show_object_viewport,
        #     text="",
        # )

        # Gizmo toggle & popover.
        # row = layout.row(align=True)
        # # FIXME: place-holder icon.
        # row.prop(view, "show_gizmo", text="", toggle=True, icon='GIZMO')
        # sub = row.row(align=True)
        # sub.active = view.show_gizmo
        # sub.popover(
        #     panel="VIEW3D_PT_gizmo_display",
        #     text="",
        # )

        # Overlay toggle & popover.
        # row = layout.row(align=True)
        # row.prop(overlay, "show_overlays", icon='OVERLAY', text="")
        # sub = row.row(align=True)
        # sub.active = overlay.show_overlays
        # sub.popover(panel="VIEW3D_PT_overlay", text="")

        # row = layout.row()
        # row.active = (object_mode == 'EDIT') or (shading.type in {'WIREFRAME', 'SOLID'})

        # While exposing 'shading.show_xray(_wireframe)' is correct.
        # this hides the key shortcut from users: T70433.
        # row.operator(
        #     "view3d.toggle_xray",
        #     text="",
        #     icon='XRAY',
        #     depress=(
        #         overlay.show_xray_bone if has_pose_mode else
        #         getattr(
        #             shading,
        #             "show_xray_wireframe" if shading.type == 'WIREFRAME' else
        #             "show_xray"
        #         )
        #     ),
        # )

        # row = layout.row(align=True)
        # row.prop(shading, "type", text="", expand=True)
        # sub = row.row(align=True)
        # # TODO, currently render shading type ignores mesh two-side, until it's supported
        # # show the shading popover which shows double-sided option.

        # # sub.enabled = shading.type != 'RENDERED'
        # sub.popover(panel="VIEW3D_PT_shading", text="")

    # bl_space_type = 'VIEW_3D'
    # # bl_region_type = 'TOOL_HEADER'
    # bl_label = "Transform"
    # bl_ui_units_x = 8

    # @staticmethod
    # def draw_xform_template(layout, context):
    #     obj = context.active_object
    #     object_mode = 'OBJECT' if obj is None else obj.mode
    #     has_pose_mode = (
    #         (object_mode == 'POSE') or
    #         (object_mode == 'WEIGHT_PAINT' and context.pose_object is not None)
    #     )

    #     tool_settings = context.tool_settings

    #     # Mode & Transform Settings
    #     scene = context.scene

    #     # Orientation
    #     if object_mode in {'OBJECT', 'EDIT', 'EDIT_GPENCIL'} or has_pose_mode:
    #         orient_slot = scene.transform_orientation_slots[0]
    #         row = layout.row(align=True)

    #         sub = row.row()
    #         sub.ui_units_x = 4
    #         sub.prop_with_popover(
    #             orient_slot,
    #             "type",
    #             text="",
    #             panel="VIEW3D_PT_transform_orientations",
    #         )
    # def draw(self, context):
    #     layout = self.layout
    #     layout.label(text="Projection Type")

    #     scene = context.scene
    #     # orient_slot = scene.transform_orientation_slots[0]
    #     # orientation = orient_slot.custom_orientation

    #     row = layout.row()
    #     col = row.column()

    #     layout = self.layout
    #     layout.row(align=True).template_header()
    #     # self.draw_tool_settings(context)
    #     # row.operator("wm.menu_setprecisemesh_operator", text="")
    #     # layout.separator_spacer()
    #     # VIEW3D_HT_header.draw_xform_template(layout, context)
    #     # row.operator("wm.menu_setprecisemesh_operator", text="")
    #     # layout.separator_spacer()
    #     # self.draw_mode_settings(context)
    #     # col.prop(self, "projection_type", expand=True)
    #     # row.operator("wm.menu_setprecisemesh_operator", text="", icon='ADD', emboss=False)
    #     row.operator("wm.menu_setprecisemesh_operator", text="")

        # if orientation:
        #     row = layout.row(align=False)
        #     row.prop(orientation, "name", text="", icon='OBJECT_ORIGIN')
        #     row.operator("transform.delete_orientation", text="", icon='X', emboss=False)

class SetPresiceMeshPanel(bpy.types.Panel):
    
    bl_label = "Set Presice Mesh"
    bl_idname = "VIEW3D_PT_edit_mesh_set_precise_mesh"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"
    bl_context = "mesh_edit"
    bl_options = {'DEFAULT_CLOSED'}
    bl_label = "Set Precise Mesh / CAD"
    
    def draw(self, context):
        layout = self.layout

        scene = context.scene
        sc = scene
        ob = context.object

        w_m = context.window_manager.setprecisemesh

        # Get values
        bool_panel_arrow = bpy.data.scenes[bpy.context.scene.name_full].bool_panel_arrow
        bool_panel_arrow2 = bpy.data.scenes[bpy.context.scene.name_full].bool_panel_arrow2


        col = layout.column(align=True)

        
        
        split = col.split(factor=0.85, align=True)
        split.scale_y =1.2      

        split.operator("mesh.change_angle", icon="DRIVER_ROTATIONAL_DIFFERENCE")

        
    
        if sc.bool_panel_arrow:
            split.prop(sc, "bool_panel_arrow", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(sc, "bool_panel_arrow", text="", icon='RIGHTARROW')

        if sc.bool_panel_arrow:
            
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            
            col_top.prop(w_m, "angle")
            col_top.prop(w_m, "anglebool" )
            col_top.prop(self, "projection_type")
            # col_top.prop(ob, "angleinput")
            row = layout.row(align=True)

            sub = row.row()
            sub.ui_units_x = 5
            sub.prop_with_popover(
                self,
                "projection_type",
                text="",
                panel="VIEW3D_PT_Set_Precise_Mesh",
            )         
                    
        col = layout.column(align=False)
        col = layout.column(align=True)

        
        split = col.split(factor=0.85, align=True)
        split.scale_y =1.2
        
        split.operator("mesh.change_length",icon="DRIVER_DISTANCE")
        
    
        if sc.bool_panel_arrow2:
            split.prop(sc, "bool_panel_arrow2", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(sc, "bool_panel_arrow2", text="", icon='RIGHTARROW')

        if sc.bool_panel_arrow2:            
            box = col.column(align=True).box().column()            
            col_top = box.column(align=True)
            col_top.prop(w_m, "length")            
            col_top.prop(w_m, "lengthbool")            
            # col_top.prop(ob, "lengthinput")

        

class SetPreciseMeshProps(bpy.types.PropertyGroup):
    """
    Fake module like class
    bpy.context.window_manager.setprecisemesh
    """
    angle: bpy.props.FloatProperty(
        name="Angle",
        description="Angle",
        min=0.0, max=360.0,
        default=0.0,
        step = 100.0,
        unit="ROTATION",
        precision = 6,
    )
    anglebool: bpy.props.BoolProperty(
        name="Change adjacent edge",
        description="Change the length of the opposite edge OR Change the length of the adjacent edge",
        default=False,
    )
    angleinput: bpy.props.BoolProperty(
        name="Input Mode",
        description="",
        default=False,
    )
    length: bpy.props.FloatProperty(
        name="Length",
        description="Length of the edge",
        default=1.0,
        step = 100.0,
        unit='LENGTH',
        precision = 6,
    )
    lengthbool: bpy.props.BoolProperty(
        name="Use two directions",
        description='Change length in two directions OR in the direction of the active vertex',
        default=False,
    )
    lengthinput: bpy.props.BoolProperty(
        name="Input Mode",
        description='User Mode',
        default=False,
    )
    projection_type: bpy.props.EnumProperty(
        name="Projection type",
        items=(
            ("global matrix", "Global Matrix", "Global Matrix"),
            ("local matrix", "Local Matrix", "Local Matrix"),
            ("cursor location", "Cursor Location", "Cursor Location"),
            ("cursor matrix", "Cursor Matrix", "Cursor Matrix"),
            ("custon object", "Custon Object", "Custon Object"),
            ),
        description="Algorithm used for interpolation",
        default='global matrix'
        )
        
    
class Dupli(SetPresiceMeshPanel):
    bl_label = "Set Presice Mesh1"
    bl_idname = "VIEW3D_PT_edit_mesh_set_precise_mesh1"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "View"
    bl_label = "Set Precise Mesh /CAD"
    # bl_order = 1
 
class Dupli2(SetPresiceMeshPanel):
    bl_label = "Set Presice Mesh2"
    bl_idname = "VIEW3D_PT_edit_mesh_set_precise_mesh2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"
    bl_label = "Set Precise Mesh /CAD"
    # bl_order = 1
    
 
blender_classes = [
    Dupli,
    Dupli2,
    SetAngle,
    SetLength,
    DialogWarningOperator,
    SetPreciseMeshProps,
    SetPreciseMeshPreferences,
    MenuSetPreciseMeshOperator,
    VIEW3D_PT_Set_Precise_Mesh,

]


def register():
    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)
    # pynput.register()

    bpy.types.WindowManager.setprecisemesh = PointerProperty(type=SetPreciseMeshProps)


    bpy.types.Scene.bool_panel_arrow = bpy.props.BoolProperty(
        name="bool_panel_arrow",
        description="",
        default=True,
    )
    bpy.types.Scene.bool_panel_arrow2 = bpy.props.BoolProperty(
        name="bool_panel_arrow2",
        description="",
        default=True,
    )
    bpy.types.Scene.bool_warning = bpy.props.BoolProperty(
        name="Show this warning panel next time",
        description="Warning Panel will appear if object scale or delta scale is not correct \n You can also enable it or disable in \n Property Editor > Scene Properties > Custom Properties",
        default=1,
        options = {"SKIP_SAVE"}
    )


def unregister():
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)

    del bpy.types.WindowManager.setprecisemesh

    del bpy.types.Scene.bool_panel_arrow
    del bpy.types.Scene.bool_panel_arrow2
    del bpy.types.Scene.bool_warning

if __name__ == "__main__":
    register()
