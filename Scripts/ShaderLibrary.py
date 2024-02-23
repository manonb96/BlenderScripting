bl_info = {
    "name": "Shader Library",
    "author": "Manon",
    "version": (1, 0),
    "blender": (2, 93, 6),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

import bpy

class SHADER_PT_main_panel(bpy.types.Panel):
    bl_label = "Shader Library"
    bl_idname = "shader_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shader Library'

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()   
        row.operator('shader.diamond_operator', icon='HANDLETYPE_ALIGNED_VEC')
        
        row = layout.row()
        row.operator('shader.neon_operator', icon='EXPERIMENTAL')

# Create a custom operator for shader with keyframe
class SHADER_OT_neon(bpy.types.Operator):
    bl_label = "Neon"
    bl_idname = 'shader.neon_operator'
    
    def execute(self, context):
        curr_frame = bpy.context.scene.frame_current
        
        material_neon = bpy.data.materials.new(name="Neon")
        material_neon.use_nodes = True
        
        tree = material_neon.node_tree        
        tree.nodes.remove(tree.nodes.get('Principled BSDF'))
        
        material_output = tree.nodes.get('Material Output')
        material_output.location = (400,0)
        
        emiss_node = tree.nodes.new('ShaderNodeEmission')
        emiss_node.location = (200,0)
        emiss_node.inputs[0].default_value = (0.163182, 1, 1, 1)
        emiss_node.inputs[1].default_value = 2
        emiss_node.inputs[1].keyframe_insert("default_value", frame= curr_frame)
        
        data_path = f'nodes["{emiss_node.name}"].inputs[1].default_value'
        
        fcurves = tree.animation_data.action.fcurves 
        fc = fcurves.find(data_path)
        if fc:
            new_mod = fc.modifiers.new('NOISE')
            new_mod.strength = 10
            new_mod.depth = 1
        

        tree.links.new(emiss_node.outputs[0], material_output.inputs[0])
        
        return  {'FINISHED'}

# Create a custom operator for the Diamond Shader    
class SHADER_OT_diamond(bpy.types.Operator): 
    bl_label = "Diamond"
    bl_idname = 'shader.diamond_operator'
    
    def execute(self, context):
        material_diamond = bpy.data.materials.new(name="Diamond")
        material_diamond.use_nodes = True
        material_diamond.node_tree.nodes.remove(material_diamond.node_tree.nodes.get('Principled BSDF'))
        
        material_output = material_diamond.node_tree.nodes.get('Material Output')
        material_output.location = (400,0)
        
        glass1_node = material_diamond.node_tree.nodes.new('ShaderNodeBsdfGlass')
        glass1_node.location = (-600,0)
        glass1_node.inputs[0].default_value = (1, 0, 0, 1)
        glass1_node.inputs[2].default_value = 1.446 
        
        glass2_node = material_diamond.node_tree.nodes.new('ShaderNodeBsdfGlass')
        glass2_node.location = (-600,-200)
        glass2_node.inputs[0].default_value = (0, 1, 0, 1)
        glass2_node.inputs[2].default_value = 1.450

        glass3_node = material_diamond.node_tree.nodes.new('ShaderNodeBsdfGlass')
        glass3_node.location = (-600,-400)
        glass3_node.inputs[0].default_value = (0, 0, 1, 1)        
        glass3_node.inputs[2].default_value = 1.450
        
        add1_node = material_diamond.node_tree.nodes.new('ShaderNodeAddShader')
        add1_node.location = (-400,-75)
        add1_node.label = "Add 1"
        add1_node.hide = True
        add1_node.select = False 
        
        add2_node = material_diamond.node_tree.nodes.new('ShaderNodeAddShader')
        add2_node.location = (-200, -100)
        add2_node.label = "Add 2"
        add2_node.hide = True
        add2_node.select = False   
        
        glass4_node = material_diamond.node_tree.nodes.new('ShaderNodeBsdfGlass')
        glass4_node.location = (-200,-250)
        glass4_node.inputs[0].default_value = (1, 1, 1, 1)
        glass4_node.inputs[2].default_value = 1.450     
         
        mix1_node = material_diamond.node_tree.nodes.new('ShaderNodeMixShader')
        mix1_node.location = (0, -175)
        mix1_node.label = "Mix1"
        mix1_node.select = False
        
        material_diamond.node_tree.links.new(glass1_node.outputs[0], add1_node.inputs[0])
        material_diamond.node_tree.links.new(glass2_node.outputs[0], add1_node.inputs[1])
        material_diamond.node_tree.links.new(add1_node.outputs[0], add2_node.inputs[0])
        material_diamond.node_tree.links.new(glass3_node.outputs[0], add2_node.inputs[1])
        material_diamond.node_tree.links.new(add2_node.outputs[0], mix1_node.inputs[1])
        material_diamond.node_tree.links.new(glass4_node.outputs[0], mix1_node.inputs[2])
        material_diamond.node_tree.links.new(mix1_node.outputs[0], material_output.inputs[0])
        
        bpy.context.object.active_material = material_diamond
        
        return {'FINISHED'}
                                  

def register():
    bpy.utils.register_class(SHADER_PT_main_panel)
    bpy.utils.register_class(SHADER_OT_diamond)
    bpy.utils.register_class(SHADER_OT_neon)


def unregister():
    bpy.utils.unregister_class(SHADER_PT_main_panel)
    bpy.utils.unregister_class(SHADER_OT_diamond)
    bpy.utils.unregister_class(SHADER_OT_neon)


if __name__ == "__main__":
    register()        