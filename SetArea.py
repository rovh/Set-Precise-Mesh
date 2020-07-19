import bpy

import bmesh
import math
import mathutils

from . import name

text_description_2 = "Face has not been found"

text_description = "Face has not been found\
\nYou need to select:\
\n * face\
\n * two edges that connected to the face\
\n * one edge if there is only one linked face\
\n * two unlinked vertices connected to the face\
"
text_description_2 ="\
\n You need to select:\
\n  * face\
\n  * two edges that connected to the face\
\n  * one edge if there is only one linked face\
\n  * two unlinked vertices connected to the face\
"

def report(type, self):
    if type == 'angle':
        text = "Angle point"
        # war = "INFO"
        # self.report({war}, text)
        bpy.ops.object.dialog_info_operator_set_area('INVOKE_DEFAULT', type = type, text = text)
    
    elif type == 'edge':
        text = "First Edge Center point"
        # war = "INFO"
        # self.report({war}, text)
        bpy.ops.object.dialog_info_operator_set_area('INVOKE_DEFAULT', type = type, text = text)
    
    elif type == 'median':
        text = "Median point"
        # war = "INFO"
        # self.report({war}, text)
        bpy.ops.object.dialog_info_operator_set_area('INVOKE_DEFAULT', type = type, text = text)

class Dialog_Info_Operator_Set_Area (bpy.types.Operator):
    bl_idname = "object.dialog_info_operator_set_area"
    bl_label = "INFO Panel Operaror"
        
    type: bpy.props.StringProperty()
    text: bpy.props.StringProperty()

    def execute(self, context):
        print(self.type)
        return {'FINISHED'}

    def invoke(self, context, event):
        x = event.mouse_x
        y = event.mouse_y 

        move_x = -30
        move_y = 50

        bpy.context.window.cursor_warp(x + move_x, y + move_y)
        # context.window_manager.invoke_popup(self, width = 200)
        # return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self, width=600, height=500)
        # return context.window_manager.invoke_popup(self)
        inv = context.window_manager.invoke_popup(self, width = 200)

        bpy.context.window.cursor_warp(x, y)

        return inv

        # return bpy.context.window_manager.invoke_popup(self)
        
    def draw(self, context):
        layout = self.layout
        type = self.type
        text = self.text

        if self.type == 'angle':
            layout.label(icon = 'SNAP_PERPENDICULAR', text = text)
        elif self.type == 'edge':
            layout.label(icon = 'SNAP_MIDPOINT', text = text)
        elif self.type == 'median':
            layout.label(icon = 'SNAP_FACE_CENTER', text = text)

class SetArea(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.change_area"
    bl_label = "Set Area " + name
    bl_description = 'Set Area of the face\n' + text_description_2 + '\n You can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut'
    # bl_options = {'REGISTER', 'UNDO'}
    bl_options = {'UNDO'}

    plus_area:  bpy.props.IntProperty (options = {"SKIP_SAVE"}) 
    eyedropper: bpy.props.BoolProperty(options = {"SKIP_SAVE"})
    draw:       bpy.props.BoolProperty(options = {"SKIP_SAVE"})
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None\
            and context.active_object.mode in {'EDIT'}\
            and context.active_object.type == "MESH"

    @classmethod
    def description(cls, context, properties):
        if properties.plus_area == 1:
            return "Plus Area"
        elif properties.plus_area == -1:
            return "Minus Area"
        elif properties.eyedropper == True:
            return "Get Area"
        else:
            pass

    def execute(self, context):

        area = context.window_manager.setprecisemesh.area
        data_block_3 = bpy.context.window_manager.setprecisemesh.data_block_3
        script_input_3 = bpy.context.scene.script_input_3
        length_unit = bpy.context.scene.unit_settings.length_unit

        if script_input_3 == 1:

            """Replace syntax"""
            data_block_3 = data_block_3.replace(',', '.')
            data_block_3 = data_block_3.replace('^', '**')
            data_block_3 = data_block_3.replace(':', '/')
            data_block_3 = data_block_3.replace('unit', str(area))
            data_block_3 = data_block_3.replace('u', str(area))
            # print(   re.search(r"\((\w+)\)", data_block_2)   )

            # data_block_2 = data_block_2.replace( 'psqrt(r(A-Za-z0-9)' , 'sqrt(r(A-Za-z0-9_])')

            try:
                eval(data_block_3)
            except SyntaxError:
                area = bpy.context.window_manager.setprecisemesh.area
            else:
                area = eval(data_block_3)
                area = area / bpy.context.scene.unit_settings.scale_length

                """Units Synchronization"""
                if  bpy.context.scene.unit_settings.system == 'METRIC' and length_unit == 'ADAPTIVE':
                    unit = area
                    bpy.context.window_manager.setprecisemesh.area =  unit
                    area = unit
                elif length_unit == "MICROMETERS":
                    unit = area / 1000000
                    bpy.context.window_manager.setprecisemesh.area =  unit
                    area = unit
                elif length_unit == "MILLIMETERS":
                    unit = area / 1000
                    bpy.context.window_manager.setprecisemesh.area =  unit
                    area = unit
                elif length_unit == "CENTIMETERS":
                    unit = area / 100
                    bpy.context.window_manager.setprecisemesh.area =  unit
                    area = unit
                elif length_unit == "METERS":
                    unit = area
                    bpy.context.window_manager.setprecisemesh.area =  unit
                    area = unit
                elif length_unit == "KILOMETERS":
                    unit = area * 1000
                    bpy.context.window_manager.setprecisemesh.area =  unit
                    area = unit
                

                if bpy.context.scene.unit_settings.system == 'IMPERIAL'and length_unit == 'ADAPTIVE':
                    unit = area / 3.2808398950131
                    bpy.context.window_manager.setprecisemesh.area =  unit
                    area = unit
                if length_unit == 'MILES':
                    unit = area  / 0.00062137119223733
                    bpy.context.window_manager.setprecisemesh.area =  unit
                    area = unit
                elif length_unit == 'FEET':
                    unit = area / 3.2808398950131
                    bpy.context.window_manager.setprecisemesh.area =  unit
                    area = unit
                elif length_unit == 'INCHES':
                    unit = area / 39.370078740157
                    bpy.context.window_manager.setprecisemesh.area =  unit
                    area = unit
                elif length_unit == 'THOU':
                    unit = area / 39.370078740157 / 1000
                    bpy.context.window_manager.setprecisemesh.area =  unit
                    area = unit
        else:
            area = bpy.context.window_manager.setprecisemesh.area

        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        selected_verts = [verts for verts in bm.verts if verts.select]
        selected_edges = [edge for edge in bm.edges if edge.select]
        selected_faces = [face for face in bm.faces if face.select]

        elem_list = [g for g in bm.select_history]

        scale_direction = False

        if len(selected_verts) == 0 and len(selected_edges) == 0 and len(selected_faces) == 0:

            text = text_description
            war = "ERROR"
            self.report({war}, text)
            return{"FINISHED"}

        if len(selected_verts) != 0 and len(selected_edges) == 0 and len(selected_faces) == 0:

            linked_faces_all = []

            for i in range(0, len(selected_verts) ):
                for k in range(0, len(selected_verts[i].link_faces) ):
                    linked_faces_all.append( selected_verts[i].link_faces[k] )

            for i in range(0, len(linked_faces_all) -1):
                for j in range(i+1, len(linked_faces_all) ):
                    if linked_faces_all[i].index == linked_faces_all[j].index:
                        needed_face = linked_faces_all[i]
                        needed_face.select = True
                        break

            area_true = needed_face.calc_area()
            center_median = needed_face.calc_center_median()

        if len(selected_verts) != 0 and len(selected_edges) != 0 and len(selected_faces) == 0:
        
            if len(selected_edges) == 1 and len(selected_edges[0].link_faces) == 1:
                needed_face = selected_edges[0].link_faces[0]
                needed_face.select = True
                area_true = needed_face.calc_area()
                center_median = needed_face.calc_center_median()

            elif len(selected_edges) == 1 and len(selected_edges[0].link_faces) != 1:
                # if len(selected_verts)>2:
                #     linked_faces_all = []
                #     verts_all = []
                #     verts_edge_all = []
                #     needed_face_list = []
                #     area_true = 0
                #     center_median = mathutils.Vector((0,0,0))
                #     # verts_free = []
                #     # needed_face_number = 0
                    
                #     for i in range(0, len(selected_edges) ):
                #         for k in range(0, len(selected_edges[i].verts) ):
                #             verts_edge_all.append( selected_edges[i].verts[k] )
                #     for i in range(0, len(selected_verts)):
                #         verts_all.append(selected_verts[i])
                #     verts_other = list(set(verts_all) - set(verts_edge_all))
                #     for i in range(0, len(verts_other)):
                #         for k in range(0, len(verts_other[i].link_faces)):
                #             linked_faces_all.append(verts_other[i].link_faces[k])

                #     for i in range(0, len(selected_edges)):
                #         for k in range(0, len(selected_edges[i].link_faces)):
                #             linked_faces_all.append(selected_edges[i].link_faces[k])


                #     for i in range(0, len(linked_faces_all) -1):
                #         for j in range(i+1, len(linked_faces_all) ):
                #             if linked_faces_all[i].index == linked_faces_all[j].index:
                #                 # needed_face_number += 1
                #                 needed_face = linked_faces_all[i]
                #                 needed_face_list.append(linked_faces_all[i])
                #                 area_true = needed_face.calc_area() + area_true
                #                 center_median = needed_face.calc_center_median() + center_median
                #                 needed_face.select = True
                #                 print(123123123123)
                #                 # break

                #     center_median = center_median/len(needed_face_list)
                    
                # else:
                text = text_description
                war = "ERROR"
                self.report({war}, text)
                return{"FINISHED"}

            elif len(selected_edges) > 1:
                # linked_faces = {}
                linked_faces_all = []
                needed_face = None
                needed_face_list = []
                area_true = 0
                center_median = mathutils.Vector((0,0,0))

                for i in range(0, len(selected_edges) ):
                    # linked_faces[i] = []
                    for k in range(0, len(selected_edges[i].link_faces) ):
                        # linked_faces[i].append( selected_edges[i].link_faces[k] )
                        linked_faces_all.append( selected_edges[i].link_faces[k] )

                for i in range(0, len(linked_faces_all) -1):
                    for j in range(i+1, len(linked_faces_all) ):
                        if linked_faces_all[i].index == linked_faces_all[j].index:

                            needed_face = linked_faces_all[i]
                            needed_face_list.append(linked_faces_all[i])
                            area_true = needed_face.calc_area() + area_true
                            center_median = needed_face.calc_center_median() + center_median

                            needed_face.select = True

                center_median = center_median / len(needed_face_list)

                if needed_face == None:
                    text = text_description
                    war = "ERROR"
                    self.report({war}, text)
                    return{"FINISHED"}
                            
                # needed_face.select = True
                # area_true = needed_face.calc_area()
                # center_median = needed_face.calc_center_median()

                # print(edges_of_needed_face)

                # for j in range(0, len(linked_faces) - 1):
                #     for i in range(0, len(linked_faces[j]) ):
                #         for l in range (0, len(linked_faces[j+1]) ):
                #             for k in range (0, len(linked_faces[l]) ):
                                # print("\n")
                                # print(linked_faces[j][i])
                                # print(linked_faces[j+1][k])

        if len(selected_verts) != 0 and len(selected_edges) != 0 and len(selected_faces) != 0:

            if len(selected_faces)>1:
                area_true = 0
                center_median = mathutils.Vector((0,0,0))
                needed_face_list = []

                for i in range(0, len(selected_faces)):
                    needed_face_list.append(selected_faces[i])

                for i in range(0, len(needed_face_list)):
                    area_true = needed_face_list[i].calc_area() + area_true
                    center_median = needed_face_list[i].calc_center_median() + center_median

                center_median = center_median/len(needed_face_list)

            else:
                needed_face = selected_faces[0]
                area_true = needed_face.calc_area()
                center_median = needed_face.calc_center_median()

        if self.eyedropper == True:
            context.window_manager.setprecisemesh.area = area_true
            return{"FINISHED"}
        
        # Create Matrix
        mat_loc =  mathutils.Matrix.Translation(( 0.0 ,  0.0 ,  0.0 ))                
        mat_sca =  mathutils.Matrix.Scale( 1.0 ,  4 ,  ( 0.0 ,  0.0 ,  1.0 ))
        mat_rot =  mathutils.Matrix.Rotation(0 ,  4 , "Z" )
        mat_out =  mat_loc @  mat_rot @  mat_sca
        S = mat_out

        scale_point = context.window_manager.setprecisemesh.scale_point

        if scale_point == "median_point":
            pass
        elif scale_point == "cursor_point":
            center_median = bpy.context.active_object.matrix_world.inverted() @ bpy.context.scene.cursor.location
        elif scale_point == "auto_point":
    
            verts_of_the_edge_1 = []
            verts_of_the_edge_2 = []

            if   len(elem_list)>1 and isinstance(elem_list[0], bmesh.types.BMEdge) and isinstance(elem_list[1], bmesh.types.BMEdge):

                common_vert = None

                for i in range (0, len(elem_list[0].verts)):
                    verts_of_the_edge_1.append(elem_list[0].verts[i])

                for i in range (0, len(elem_list[1].verts)):
                    verts_of_the_edge_2.append(elem_list[1].verts[i])

                for i in range(0, len(verts_of_the_edge_1)):
                    if verts_of_the_edge_1[i] in verts_of_the_edge_2:
                        common_vert = verts_of_the_edge_1[i].co
                        break

                if bool(common_vert) == True:
                    # center_median = bpy.context.active_object.matrix_world.inverted() @ common_vert
                    center_median = common_vert
                    report('angle', self)
                else:
                    verts_of_the_edge_1_median = mathutils.Vector((0,0,0))
                    for i in range (0, len(elem_list[0].verts)):
                        verts_of_the_edge_1_median = verts_of_the_edge_1_median + elem_list[0].verts[i].co

                    center_median = verts_of_the_edge_1_median/len(verts_of_the_edge_2)
                    report('edge', self)

            elif len(elem_list)>2 and isinstance(elem_list[0], bmesh.types.BMVert) and isinstance(elem_list[1], bmesh.types.BMVert) and isinstance(elem_list[2], bmesh.types.BMVert):

                linked_edges_of_the_vert_1 = []
                linked_edges_of_the_vert_2 = []
                linked_edges_of_the_vert_3 = []

                for i in range(0, len(elem_list[0].link_edges)):
                    linked_edges_of_the_vert_1.append(elem_list[0].link_edges[i].index)
                for i in range(0, len(elem_list[1].link_edges)):
                    linked_edges_of_the_vert_2.append(elem_list[1].link_edges[i].index)
                for i in range(0, len(elem_list[2].link_edges)):
                    linked_edges_of_the_vert_3.append(elem_list[2].link_edges[i].index)

                linked_edges_of_the_vert = 0

                for i in range(0, len(linked_edges_of_the_vert_1)):
                    if linked_edges_of_the_vert_1[i] in linked_edges_of_the_vert_2\
                    or linked_edges_of_the_vert_1[i] in linked_edges_of_the_vert_3:
                        linked_edges_of_the_vert += 1

                for i in range(0, len(linked_edges_of_the_vert_2)):
                    if linked_edges_of_the_vert_2[i] in linked_edges_of_the_vert_1\
                    or linked_edges_of_the_vert_2[i] in linked_edges_of_the_vert_3:
                        linked_edges_of_the_vert += 1

                for i in range(0, len(linked_edges_of_the_vert_3)):
                    if linked_edges_of_the_vert_3[i] in linked_edges_of_the_vert_1\
                    or linked_edges_of_the_vert_3[i] in linked_edges_of_the_vert_2:
                        linked_edges_of_the_vert += 1

                if linked_edges_of_the_vert == 4:
                    
                    center_median = elem_list[1].co
                    report('angle', self)

                elif linked_edges_of_the_vert == 2:
                    center_median = (elem_list[0].co + elem_list[1].co) / 2

                    report('edge', self)

                # print(linked_edges_of_the_vert_1)
                # print(linked_edges_of_the_vert_2)
                # print(linked_edges_of_the_vert_3)

            else:
                report("median", self)


        S.translation -= center_median

        if self.plus_area == 0:
            scale_factor_area = area / area_true
        elif self.plus_area == 1:
            scale_factor_area = (area + area_true) / area_true
        elif self.plus_area == -1:
            scale_factor_area = (area_true - area)  / area_true

        try:
            scale_factor_area = math.sqrt(scale_factor_area)
        except ValueError:
            scale_factor_area = 0

        if scale_direction == True:

            elem_list_verts = []
            edges_of_needed_face_list = []
            selected_edges_of_needed_face_list = []
            unselected_edges_of_needed_face_list = []
            selected_verts_of_needed_face_list = []
            unselected_verts_of_needed_face_list = []
            verts_tri_1 = []
            verts_tri_2 = []

            for i in range(0, len(elem_list)):
                for k in range(0, len(elem_list[i].verts)):
                    elem_list_verts.append(elem_list[i].verts[k])

            for i in range(0, len(needed_face.edges)):
                edges_of_needed_face_list.append(needed_face.edges[i])
                if needed_face.edges[i] in elem_list:
                    selected_edges_of_needed_face_list.append(needed_face.edges[i])
                else:
                    unselected_edges_of_needed_face_list.append(needed_face.edges[i])

            for i in range(0, len(selected_edges_of_needed_face_list)):
                for k in range(0, len(selected_edges_of_needed_face_list[i].verts)):
                    selected_verts_of_needed_face_list.append(selected_edges_of_needed_face_list[i].verts[k])

            for i in range(0, len(unselected_edges_of_needed_face_list)):
                for k in range(0, len(unselected_edges_of_needed_face_list[i].verts)):
                    unselected_verts_of_needed_face_list.append(unselected_edges_of_needed_face_list[i].verts[k])


            verts_tri_1.append(selected_edges_of_needed_face_list[0].verts[0])
            verts_tri_1.append(selected_edges_of_needed_face_list[0].verts[1])
            verts_tri_1.append(selected_edges_of_needed_face_list[1].verts[0])

            verts_tri_2.append(selected_edges_of_needed_face_list[0].verts[0])
            verts_tri_2.append(selected_edges_of_needed_face_list[0].verts[1])
            verts_tri_2.append(selected_edges_of_needed_face_list[1].verts[1])

            length_tri_1 = []
            length_tri_2 = []

            for i in range(-1, len(verts_tri_1)-1):
                length_tri_1.append( (verts_tri_1[i].co - verts_tri_1[i+1].co).length )
            for i in range(-1, len(verts_tri_2)-1):
                length_tri_2.append( (verts_tri_2[i].co - verts_tri_2[i+1].co).length )

            print(unselected_verts_of_needed_face_list)
            print(selected_verts_of_needed_face_list)

            # for i in range(0, len(verts_tri_1)):
            #     if verts_tri_1[i] in 
                # for k in range(0, len())
                # if 
                # verts_tri_1_perpendicular = 

            # p_1 = sum(length_tri_1)/2
            # area_tri_1 = math.sqrt( p_1*(p_1-length_tri_1[0])*(p_1-length_tri_1[1])*(p_1-length_tri_1[2]) )

            # p_2 = sum(length_tri_2)/2
            # area_tri_2 = math.sqrt( p_2*(p_2-length_tri_2[0])*(p_2-length_tri_2[1])*(p_2-length_tri_2[2]) )


            

            # print(selected_edges_of_needed_face_list)
            # print(verts_tri_1[0])
            # print(needed_face.edges, 3434343434)

            # n = needed_face.edges.get(verts_tri_1[0], fallback=None)
            # print(n, 1212121212)

            # print(length_tri_1[0])
            # print(area_true)
            # print(area_tri_1)
            # print(area_tri_2)
            # print(p_1)
            


            
            # print(verts_tri_1)
            # print(verts_tri_2)

            # unselected_edges_of_needed_face_list


            # print(selected_edges_of_needed_face_list)1
            # print(unselected_edges_of_needed_face_list)


            # vert_diagonal_1 = elem_list_verts[0]

            # for i in range(0, len(elem_list_verts)):
            #     if vert_diagonal_1.link_edges in elem_list_verts[i].link_edges:
            #         pass
            #     else:
            #         vert_diagonal_2 = elem_list_verts[i]

            # verts_tri_1.append(vert_diagonal_1)
            # verts_tri_2.append(vert_diagonal_2)
            # for i in range(0, len(elem_list_verts)):
            #     if vert_diagonal_1.link_edges in elem_list_verts[i].link_edges:
            #         verts_tri_1.append(elem_list_verts[i])
            #     if vert_diagonal_2.link_edges in elem_list_verts[i].link_edges:
            #         verts_tri_2.append(elem_list_verts[i])

            # print(verts_tri_1)
            # print(verts_tri_2)



            # print(elem_list_verts)
            # print(vert_diagonal_2)


            # needed_face


            pass
        else:

            # x_area = 1
            # y_area = 0
            # z_area = 1


            # x_area = scale_factor_area if x_area == 1 else 1
            # y_area = scale_factor_area if y_area == 1 else 1
            # z_area = scale_factor_area if z_area == 1 else 1

            # if x_area == 1 and y_area == 0 and z_area == 1:
            #     x_area = x_area**2
            #     print(123213123)

            scale_factor_area_Vector = (scale_factor_area, scale_factor_area, scale_factor_area)
            # scale_factor_area_Vector = (x_area**2, y_area, z_area)
            # scale_factor_area_Vector = (1, scale_factor_area **2, 1)
            # scale_factor_area_Vector = (scale_factor_area **2, 1, 1)
            # scale_factor_area_Vector = (1,1,scale_factor_area **2)

            bmesh.ops.scale(
                bm,
                vec = mathutils.Vector( scale_factor_area_Vector ),
                verts=[v for v in bm.verts if v.select],
                space=S
                )
            bmesh.update_edit_mesh(me, True)

        # if len(selected_faces) == 1:
        #     needed_face.select = False

        # for i in range(0, len(selected_verts)):
        #     bm.verts[selected_verts[i].index].select = True

        # for i in range(0, len(selected_edges)):
        #     bm.edges[selected_edges[i].index].select = True

        # for i in range(0, len(selected_faces)):
        #     bm.faces[selected_faces[i].index].select = True

        return {"FINISHED"}

if __name__ == "__main__":
    register()

