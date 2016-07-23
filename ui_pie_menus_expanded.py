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
    "version": (2, 0, 0),
    "blender": (2, 77, 0),
    "description": "Enable Additional Pie Menus in Blender",
    "category": "User Interface",
}

import bpy
from bpy.types import Menu, Operator
from bpy.props import EnumProperty
from bl_ui.properties_paint_common import UnifiedPaintPanel



class VIEW3D_PIE_Tools_System(Menu):
    bl_label = "Tools"
    bl_idname = "VIEW3D_PIE_Tools_System"
    def draw(self, context):
        layout = self.layout
   
        if context.active_object.mode == 'EDIT':
                pie = layout.menu_pie()
                pie.operator_enum("mesh.select_mode", "type")
                pie.operator("wm.call_menu_pie", text="Face Tools", icon='PLUS').name = "VIEW3D_PIE_faces"
                pie.operator("wm.call_menu_pie", text="Vertex Tools", icon='PLUS').name = "VIEW3D_PIE_vertices"
                pie.operator("wm.call_menu_pie", text="Edge Tools", icon='PLUS').name = "VIEW3D_PIE_edges"
        else:
            if context.active_object.mode == 'SCULPT':
                pie = layout.menu_pie()
                pie.operator("wm.call_menu_pie", text="Tan Brushes", icon='BRUSH_SMOOTH').name = "VIEW3D_PIE_Sculpt_Brushes_Tan"
                pie.operator("wm.call_menu_pie", text="Gray Brushes", icon='BRUSH_CLAY').name = "VIEW3D_PIE_Sculpt_Brushes_Gray"
                pie.operator("wm.call_menu_pie", text="Red Brushes", icon='BRUSH_GRAB').name = "VIEW3D_PIE_Sculpt_Brushes_Red"
                #pie.operator("wm.call_menu_pie", text ="Stroke Methods", icon='PLUS').name = "VIEW3D_PIE_Brush_Strokes"
                #pie.operator("wm.call_menu_pie", text="Curves", icon='PLUS').name = "VIEW3D_PIE_Sculpt_Curves"
                
            else:
                pie = layout.menu_pie()
                pie.operator_enum("OBJECT_OT_mode_set", "mode")

class VIEW3D_PIE_Mode_Selection(Menu):
    bl_label = "Mode Selection"
    bl_idname = "VIEW3D_PIE_Mode_Selection"
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
        
class VIEW3D_PIE_Brush_Strokes(Menu):
    bl_label = "Brush Strokes"
    bl_idname = "VIEW3D_PIE_Brush_Strokes"
    def draw(self, context):
        layout = self.layout
        
        settings = UnifiedPaintPanel.paint_settings(context)
        brush = settings.brush
        
        pie = layout.menu_pie()
        pie.operator_enum("brush", "stroke_method")       
        
        
class VIEW3D_PIE_Sculpt_Curves(Menu):
    bl_label = "Sculpt Curves"
    bl_idname = "VIEW3D_PIE_Sculpt_Curves"

    def draw(self, context):
        layout = self.layout
        settings = UnifiedPaintPanel.paint_settings(context)
        brush = settings.brush
        
        sculpt_tool = brush.sculpt_tool
        
        pie = layout.menu_pie()
        pie.operator_enum("brush.curve_preset", "shape")         
        
        
        
class VIEW3D_PIE_Sculpt_Brushes_Gray(Menu):
    bl_label = "Gray Brushes"
    bl_idname = "VIEW3D_PIE_Sculpt_Brushes_Gray"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("paint.brush_select", text='Claystrips', icon='BRUSH_CLAY_STRIPS').sculpt_tool= 'CLAY_STRIPS'
        pie.operator("paint.brush_select", text='Blob', icon='BRUSH_BLOB').sculpt_tool= 'BLOB'
        pie.operator("paint.brush_select", text='Layer', icon='BRUSH_LAYER').sculpt_tool= 'LAYER'
        pie.operator("paint.brush_select", text="Crease", icon='BRUSH_CREASE').sculpt_tool='CREASE'
        pie.operator("paint.brush_select", text="Clay", icon='BRUSH_CLAY').sculpt_tool='CLAY'
        pie.operator("paint.brush_select", text='Brush', icon='BRUSH_SCULPT_DRAW').sculpt_tool='DRAW'
        pie.operator("paint.brush_select", text='Inflate/Deflate', icon='BRUSH_INFLATE').sculpt_tool='INFLATE'
       
        
        
class VIEW3D_PIE_Sculpt_Brushes_Red(Menu):
    bl_label = "Red Brushes"
    bl_idname = "VIEW3D_PIE_Sculpt_Brushes_Red"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("paint.brush_select", text='Twist', icon='BRUSH_ROTATE').sculpt_tool= 'ROTATE'
        pie.operator("paint.brush_select", text='Nudge', icon='BRUSH_NUDGE').sculpt_tool= 'NUDGE'
        pie.operator("paint.brush_select", text='Thumb', icon='BRUSH_THUMB').sculpt_tool= 'THUMB'
        pie.operator("paint.brush_select", text='Snakehook', icon='BRUSH_SNAKE_HOOK').sculpt_tool= 'SNAKE_HOOK'
        pie.operator("paint.brush_select", text='Grab', icon='BRUSH_GRAB').sculpt_tool='GRAB'
        
        
class VIEW3D_PIE_Sculpt_Brushes_Tan(Menu):
    bl_label = "Tan Brushes"
    bl_idname = "VIEW3D_PIE_Sculpt_Brushes_Tan"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("paint.brush_select", text='Scrape/Peaks', icon='BRUSH_SCRAPE').sculpt_tool= 'SCRAPE'
        pie.operator("paint.brush_select", text='Fill/Deepen', icon='BRUSH_FILL').sculpt_tool='FILL'
        pie.operator("paint.brush_select", text='Smooth', icon='BRUSH_SMOOTH').sculpt_tool= 'SMOOTH'
        pie.operator("paint.brush_select", text='Pinch/Magnify', icon='BRUSH_PINCH').sculpt_tool= 'PINCH'
        pie.operator("paint.brush_select", text='Flatten', icon='BRUSH_FLATTEN').sculpt_tool='FLATTEN'
        pie.operator("paint.brush_select", text='Mask', icon='BRUSH_MASK').sculpt_tool='MASK'          
                
addon_keymaps = []


def register():
    bpy.utils.register_class(VIEW3D_manipulator_set)

    #register menus
    bpy.utils.register_class(VIEW3D_PIE_Tools_System)
    bpy.utils.register_class(VIEW3D_PIE_Mode_Selection)
    bpy.utils.register_class(VIEW3D_PIE_view)
    bpy.utils.register_class(VIEW3D_PIE_shade)
    bpy.utils.register_class(VIEW3D_PIE_manipulator)
    bpy.utils.register_class(VIEW3D_PIE_pivot)
    bpy.utils.register_class(VIEW3D_PIE_snap)
    bpy.utils.register_class(VIEW3D_PIE_vertices)
    bpy.utils.register_class(VIEW3D_PIE_edges)
    bpy.utils.register_class(VIEW3D_PIE_faces)
    bpy.utils.register_class(VIEW3D_PIE_Sculpt_Brushes_Gray)
    bpy.utils.register_class(VIEW3D_PIE_Sculpt_Brushes_Red)
    bpy.utils.register_class(VIEW3D_PIE_Sculpt_Brushes_Tan)
    bpy.utils.register_class(VIEW3D_PIE_Brush_Strokes)
    bpy.utils.register_class(VIEW3D_PIE_Sculpt_Curves)
    

    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS')
        kmi.properties.name = 'VIEW3D_PIE_Mode_Selection'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'Z', 'PRESS')
        kmi.properties.name = 'VIEW3D_PIE_shade'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS')
        kmi.properties.name = 'VIEW3D_PIE_view'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'SPACE', 'PRESS', ctrl=True)
        kmi.properties.name = 'VIEW3D_PIE_manipulator'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'PERIOD', 'PRESS')
        kmi.properties.name = 'VIEW3D_PIE_pivot'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS', ctrl=True, shift=True)
        kmi.properties.name = 'VIEW3D_PIE_snap'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'SPACE', 'PRESS')
        kmi.properties.name = 'VIEW3D_PIE_Tools_System'
        addon_keymaps.append(km)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PIE_Tools_System)
    bpy.utils.unregister_class(VIEW3D_manipulator_set)
    bpy.utils.unregister_class(VIEW3D_PIE_Mode_Selection)
    bpy.utils.unregister_class(VIEW3D_PIE_view)
    bpy.utils.unregister_class(VIEW3D_PIE_shade)
    bpy.utils.unregister_class(VIEW3D_PIE_manipulator)
    bpy.utils.unregister_class(VIEW3D_PIE_pivot)
    bpy.utils.unregister_class(VIEW3D_PIE_snap)
    bpy.utils.unregister_class(VIEW3D_PIE_vertices)
    bpy.utils.unregister_class(VIEW3D_PIE_edges)
    bpy.utils.unregister_class(VIEW3D_PIE_faces)
    bpy.utils.unregister_class(VIEW3D_PIE_Sculpt_Brushes_Gray)
    bpy.utils.unregister_class(VIEW3D_PIE_Sculpt_Brushes_Red)
    bpy.utils.unregister_class(VIEW3D_PIE_Sculpt_Brushes_Tan)
    bpy.utils.unregister_class(VIEW3D_PIE_Brush_Strokes)
    bpy.utils.unregister_class(VIEW3D_PIE_Sculpt_Curves)
    

    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        for km in addon_keymaps:
            for kmi in km.keymap_items:
                km.keymap_items.remove(kmi)

            wm.keyconfigs.addon.keymaps.remove(km)

    # clear the list
    del addon_keymaps[:]
