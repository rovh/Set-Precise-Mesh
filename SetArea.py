import bpy

import bmesh
import math
import mathutils

from . import name



class SetArea(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.change_area"
    bl_label = "Set Area " + name
    bl_description = 'You can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut'
    # bl_options = {'REGISTER', 'UNDO'}
    bl_options = {'UNDO'}

    plus_area: bpy.props.IntProperty(options = {"SKIP_SAVE"}) 
    eyedropper: bpy.props.BoolProperty(options = {"SKIP_SAVE"})
    draw:       bpy.props.BoolProperty(options = {"SKIP_SAVE"})
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None\
            and context.active_object.mode in {'EDIT'}\
            and context.active_object.type == "MESH"

    @classmethod
    def description(cls, context, properties):
        if properties.plus_length == 1:
            return "Plus Area"
        elif properties.plus_length == -1:
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

        # for g in bm.select_history:
        #     elem_list.append(g)

        # print(elem_list)

        scale_direction = False

        if len(selected_verts) == 0 and len(selected_edges) == 0 and len(selected_faces) == 0:

            text = "You need to select vertex/edge/face"
            war = "ERROR"
            self.report({war}, text)
            return{"FINISHED"}

        if len(selected_verts) != 0 and len(selected_edges) == 0 and len(selected_faces) == 0:
            
            # if len(selected_verts) <1:
            #     text = "You need to select vertex/edge/face"
            #     war = "ERROR"
            #     self.report({war}, text)
            #     return{"FINISHED"}

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

            if len(selected_edges) <1:
                text = "You need to select vertex/edge/face"
                war = "ERROR"
                self.report({war}, text)
                return{"FINISHED"}
        
            if len(selected_edges) == 1 and len(selected_edges[0].link_faces) == 1:
                needed_face = selected_edges[0].link_faces[0]
                needed_face.select = True
                area_true = needed_face.calc_area()
                center_median = needed_face.calc_center_median()

            elif len(selected_edges) == 1 and len(selected_edges[0].link_faces) != 1:
                text = "You need to select "
                war = "ERROR"
                self.report({war}, text)
                return{"FINISHED"}

            if len(selected_edges) > 1:
                linked_faces = {}
                linked_faces_all = []
                needed_face = None
                needed_face_list = []
                area_true = 0
                center_median = mathutils.Vector((0,0,0))

                for i in range(0, len(selected_edges) ):
                    linked_faces[i] = []
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
                    text = "Face has not been found"
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
        
        # center_median = bpy.context.active_object.matrix_world @ needed_face.calc_center_median()

        # Create Matrix
        mat_loc =  mathutils.Matrix.Translation(( 0.0 ,  0.0 ,  0.0 ))                
        mat_sca =  mathutils.Matrix.Scale( 1.0 ,  4 ,  ( 0.0 ,  0.0 ,  1.0 ))
        mat_rot =  mathutils.Matrix.Rotation(0 ,  4 , "Z" )
        mat_out =  mat_loc @  mat_rot @  mat_sca
        S = mat_out
        S.translation -= center_median


        if self.plus_area == 0:
            scale_factor_area = area / area_true
        elif self.plus_area == 1:
            scale_factor_area = (area + area_true) / area_true
        elif self.plus_area == -1:
            scale_factor_area = (area_true - area)  / area_true

        scale_factor_area = math.sqrt(scale_factor_area)

        if scale_direction == True:

            elem_list_verts = []

            for i in range(0, len(elem_list)):
                for k in range(0, len(elem_list[i].verts)):
                    elem_list_verts.append(elem_list[i].verts[k])

            edges_of_needed_face_list = []
            unselected_edges_of_needed_face_list = []
            selected_edges_of_needed_face_list = []
            for i in range(0, len(needed_face.edges)):
                edges_of_needed_face_list.append(needed_face.edges[i])
                if needed_face.edges[i] in elem_list:
                    selected_edges_of_needed_face_list.append(needed_face.edges[i])
                else:
                    unselected_edges_of_needed_face_list.append(needed_face.edges[i])
            
            # print(selected_edges_of_needed_face_list)
            # print(unselected_edges_of_needed_face_list)

            unselected_edges_of_needed_face_list

            vert_diagonal_1 = elem_list_verts[0]

            for i in range(0, len(elem_list_verts)):
                if vert_diagonal_1.link_edges in elem_list_verts[i].link_edges:
                    pass
                else:
                    vert_diagonal_2 = elem_list_verts[i]

            verts_tri_1 = []
            verts_tri_2 = []
            # verts_tri_1.append(vert_diagonal_1)
            # verts_tri_2.append(vert_diagonal_2)
            for i in range(0, len(elem_list_verts)):
                if vert_diagonal_1.link_edges in elem_list_verts[i].link_edges:
                    verts_tri_1.append(elem_list_verts[i])
                if vert_diagonal_2.link_edges in elem_list_verts[i].link_edges:
                    verts_tri_2.append(elem_list_verts[i])

            print(verts_tri_1)
            print(verts_tri_2)



            # print(elem_list_verts)
            # print(vert_diagonal_2)


            needed_face


            pass

        else:

            # scale_factor_area_Vector = (x_area, y_area, z_area)
            scale_factor_area_Vector = (scale_factor_area, scale_factor_area, scale_factor_area)
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

