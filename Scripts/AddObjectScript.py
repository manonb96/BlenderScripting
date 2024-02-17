bl_info = { 
    "name": "Object Adder",
    "author": "Manon",
    "version": (1, 0),
    "blender": (2, 93, 6),
    "location": "View3d > Tool",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}

import bpy

class AddObjects(bpy.types.Panel): 
    bl_label = "AddObjects"
    bl_idname = "PT_AddObjectsPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Add'
    
    def draw(self, context): 
        layout = self.layout
        
        row = layout.row()
        row.label(text= "Add some new objects", icon='PLUS')
        row = layout.row()
        row.operator("mesh.primitive_cube_add", icon='CUBE')
        row.operator("mesh.primitive_torus_add", icon='MESH_TORUS')
        row = layout.row()
        layout.scale_y = 1.2
        
        row.operator("object.text_add")

class PanelA(bpy.types.Panel): 
    bl_label = "Scaling"
    bl_idname = "PT_PanelA"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Add'
    bl_parent_id = 'PT_AddObjectsPanel'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context): 
        layout = self.layout
        obj = context.object
        
        row = layout.row()
        row.label(text= "Select an option to scale your object", icon="OUTLINER_OB_ARMATURE") 
        row = layout.row() 
        row.operator("transform.resize")
        row = layout.row()
        layout.scale_y = 1.2
        col = layout.column()
        
        col.prop(obj, "scale")

class PanelB(bpy.types.Panel): 
    bl_label = "Specials"
    bl_idname = "PT_PanelB"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Add'
    bl_parent_id = 'PT_AddObjectsPanel'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context): 
        layout = self.layout
        
        row = layout.row()
        row.label(text= "Select a special object", icon="SOLO_ON")
        row = layout.row()
        row.operator("object.shade_smooth")      
        row.operator("object.subdivision_set")
        row = layout.row()        
        row.operator("object.modifier_add")         
    
def register():
    bpy.utils.register_class(AddObjects) 
    bpy.utils.register_class(PanelA) 
    bpy.utils.register_class(PanelB) 
    
def unregister():
    bpy.utils.unregister_class(AddObjects)
    bpy.utils.unregister_class(PanelA)
    bpy.utils.unregister_class(PanelB)

if __name__ == "__main__":
    register()