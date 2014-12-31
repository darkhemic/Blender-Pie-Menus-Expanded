# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

#based on the work of the "Pie Menus Official" by "Antony Riakiotakis"

bl_info = {
    "name": "Pie Menus Expanded",
    "author": "Christopher Williams",
    "version": (1, 0, 0),
    "description": "Enable Additional Pie Menus in Blender",
    "category": "User Interface",
}

import bpy
from bpy.types import Menu, Operator
from bpy.props import EnumProperty



class VIEW3D_PIE_object_mode(Menu):
    bl_label = "Mode"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        pie.operator_enum("OBJECT_OT_mode_set", "mode")


class VIEW3D_PIE_view(Menu):
    bl_label = "View"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        pie.operator_enum("VIEW3D_OT_viewnumpad", "type")
        pie.operator("VIEW3D_OT_view_persportho", text="Persp/Ortho", icon='RESTRICT_VIEW_OFF')


class VIEW3D_PIE_shade(Menu):
    bl_label = "Shade"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        pie.prop(context.space_data, "viewport_shade", expand=True)

        if context.active_object:
            if(context.mode == 'EDIT_MESH'):
                pie.operator("MESH_OT_faces_shade_smooth")
                pie.operator("MESH_OT_faces_shade_flat")
            else:
                pie.operator("OBJECT_OT_shade_smooth")
                pie.operator("OBJECT_OT_shade_flat")


class VIEW3D_manipulator_set(Operator):
    bl_label = "Set Manipulator"
    bl_idname = "view3d.manipulator_set"

    type = EnumProperty(
            name="Type",
            items=(('TRANSLATE', "Translate", "Use the manipulator for movement transformations"),
                   ('ROTATE', "Rotate", "Use the manipulator for rotation transformations"),
                   ('SCALE', "Scale", "Use the manipulator for scale transformations"),
                  ),
        )

    def execute(self, context):
        #show manipulator if user selects an option
        context.space_data.show_manipulator = True

        context.space_data.transform_manipulators = {self.type}

        return {'FINISHED'}


class VIEW3D_PIE_manipulator(Menu):
    bl_label = "Manipulator"


    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        pie.operator("view3d.manipulator_set", icon='MAN_TRANS', text="Translate").type = 'TRANSLATE'
        pie.operator("view3d.manipulator_set", icon='MAN_ROT', text="Rotate").type = 'ROTATE'
        pie.operator("view3d.manipulator_set", icon='MAN_SCALE', text="Scale").type = 'SCALE'
        pie.prop(context.space_data, "show_manipulator")


class VIEW3D_PIE_pivot(Menu):
    bl_label = "Pivot"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        pie.prop(context.space_data, "pivot_point", expand=True)
        if context.active_object.mode == 'OBJECT':
            pie.prop(context.space_data, "use_pivot_point_align", text="Center Points")


class VIEW3D_PIE_snap(Menu):
    bl_label = "Snapping"

    def draw(self, context):
        layout = self.layout

        toolsettings = context.tool_settings
        pie = layout.menu_pie()
        pie.prop(toolsettings, "snap_element", expand=True)
        pie.prop(toolsettings, "use_snap")
        

#added from pie_menu_template Select Mode Menu
class VIEW3D_PIE_select_mode(Menu):
    bl_label = "Select Mode"
    bl_idname = "VIEW3D_PIE_select_mode"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        pie.operator_enum("mesh.select_mode", "type")
        pie.operator("wm.call_menu_pie", text="Edge Tools", icon='PLUS').name = "VIEW3D_PIE_edges"
        pie.operator("wm.call_menu_pie", text="Vertex Tools", icon='PLUS').name = "VIEW3D_PIE_vertices"
        pie.operator("wm.call_menu_pie", text="Face Tools", icon='PLUS').name = "VIEW3D_PIE_faces"
        
        
#new classes to the offical pie Vertex Mode Menu
class VIEW3D_PIE_vertices(Menu):
    bl_label = "Vertex Tools"
    bl_idname = "VIEW3D_PIE_vertices"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        pie.operator("mesh.merge", text="Merge")
        pie.operator("mesh.vertices_smooth", text="Smooth")
        pie.operator("mesh.remove_doubles", text="Remove Doubles")
        pie.operator("mesh.vert_connect", text="Connect")
        pie.operator("transform.vert_slide", text="Slide")
        pie.operator("mesh.split", text="Split")
        pie.operator("mesh.rip_move", text="Rip")
        pie.operator("mesh.rip_move_fill", text="Rip / Fill")
        
        
        
        
#new classes to the offical pie Edge Mode Menu
class VIEW3D_PIE_edges(Menu):
    bl_label = "Edge Tools"
    bl_idname = "VIEW3D_PIE_edges"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        pie.operator("mesh.loopcut_slide", text="Loop Cut And Slide")
        pie.operator("mesh.bridge_edge_loops", text="Bridge Loops")
        pie.operator("mesh.bevel", text="Bevel")
        pie.operator("transform.edge_slide", text="Slide")
        pie.operator("mesh.fill", text="Fill")
        pie.operator("transform.edge_crease", text="Crease")
        pie.operator("mesh.mark_seam", text="Mark Seam").clear = False
        pie.operator("mesh.mark_seam", text="Clear Seam").clear = True
        
        


#new classes to the offical pie Face Mode Menus
class VIEW3D_PIE_faces(Menu):
    bl_label = "Face Tools"
    bl_idname = "VIEW3D_PIE_faces"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        pie.operator("mesh.knife_tool", text="Knife")
        pie.operator("mesh.subdivide", text="Subdivide")
        pie.operator("mesh.bisect", text="Bisect")
        pie.operator("view3d.edit_mesh_extrude_move_normal", text="Extrude")
        pie.operator("mesh.quads_convert_to_tris", text="Convert to Tris")
        pie.operator("mesh.tris_convert_to_quads", text="Convert to Quads")
        pie.operator("mesh.inset", text="Inset")
        pie.operator("mesh.poke", text="Poke")
        

addon_keymaps = []


def register():
    bpy.utils.register_class(VIEW3D_manipulator_set)

    #register menus
    bpy.utils.register_class(VIEW3D_PIE_object_mode)
    bpy.utils.register_class(VIEW3D_PIE_view)
    bpy.utils.register_class(VIEW3D_PIE_shade)
    bpy.utils.register_class(VIEW3D_PIE_manipulator)
    bpy.utils.register_class(VIEW3D_PIE_pivot)
    bpy.utils.register_class(VIEW3D_PIE_snap)
    bpy.utils.register_class(VIEW3D_PIE_select_mode)
    bpy.utils.register_class(VIEW3D_PIE_vertices)
    bpy.utils.register_class(VIEW3D_PIE_edges)
    bpy.utils.register_class(VIEW3D_PIE_faces)
    

    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS')
        kmi.properties.name = 'VIEW3D_PIE_object_mode'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'Z', 'PRESS')
        kmi.properties.name = 'VIEW3D_PIE_shade'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS')
        kmi.properties.name = 'VIEW3D_PIE_view'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'SPACE', 'PRESS')
        kmi.properties.name = 'VIEW3D_PIE_manipulator'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'PERIOD', 'PRESS')
        kmi.properties.name = 'VIEW3D_PIE_pivot'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS', ctrl=True, shift=True)
        kmi.properties.name = 'VIEW3D_PIE_snap'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'SPACE', 'PRESS', ctrl=True)
        kmi.properties.name = 'VIEW3D_PIE_select_mode'
        addon_keymaps.append(km)


def unregister():
    bpy.utils.unregister_class(VIEW3D_manipulator_set)
    bpy.utils.unregister_class(VIEW3D_PIE_object_mode)
    bpy.utils.unregister_class(VIEW3D_PIE_view)
    bpy.utils.unregister_class(VIEW3D_PIE_shade)
    bpy.utils.unregister_class(VIEW3D_PIE_manipulator)
    bpy.utils.unregister_class(VIEW3D_PIE_pivot)
    bpy.utils.unregister_class(VIEW3D_PIE_snap)
    bpy.utils.unregister_class(VIEW3D_PIE_select_mode)
    bpy.utils.unregister_class(VIEW3D_PIE_vertices)
    bpy.utils.unregister_class(VIEW3D_PIE_edges)
    bpy.utils.unregister_class(VIEW3D_PIE_faces)
    
    

    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        for km in addon_keymaps:
            for kmi in km.keymap_items:
                km.keymap_items.remove(kmi)

            wm.keyconfigs.addon.keymaps.remove(km)

    # clear the list
    del addon_keymaps[:]
