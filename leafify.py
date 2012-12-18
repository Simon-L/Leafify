# DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO. 
#
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

# Contributors: FergusL, Aiena
# Contact: #blenderpython @ irc.freenode.net
 
bl_info = {
    "name": "Leafify",
    "author": "FergusL on #blenderpython @ irc.freenode.net",
    "version": (0, 1),
    "blender": (2, 6, 5),
    "location": "View3D > Tools",
    "description": "Scroll down the Tools menu in 3D View to find the options! Hit Spacebar and type Leafify to find me!",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}

import bpy
import bmesh
from mathutils import Vector


def leafify(self, context):
    
    offset = context.scene.leafify_offset
    
    # Flip normals of selected faces
    bpy.ops.mesh.flip_normals()
     
    bm = bmesh.from_edit_mesh(context.selected_objects[0].data)
    
    sel_faces = [face for face in bm.faces if face.select]
    bpy.ops.mesh.select_all(action = 'DESELECT')
    
    # Add new faces based on existing faces with vertical OFFSET
    for face in sel_faces :
        addVerts = []
        for vert in face.verts :
            # Add vertices to a list to pass to bm.faces.new() 
            addVerts.append(bm.verts.new((vert.co.x + offset.x, vert.co.y + offset.y, vert.co.z + offset.z)))
        bm.faces.new(addVerts, face).select = True # Faces are added and set to be selected
    # Flip normals of added faces
    bpy.ops.mesh.flip_normals()
    # Update mesh data
    bmesh.update_edit_mesh(bpy.context.selected_objects[0].data)

class OBJECT_OT_leafify(bpy.types.Operator):
    """Duplicates and flips selected faces to replicate dual-sided meshes"""
    bl_idname = "mesh.leafify"
    bl_label = "Leafify"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        if context.scene.leafify_offset == Vector((0.0,0.0,0.0)) :
            self.report({'INFO'}, "Please use offset values above 0")
            return { 'FINISHED' }
            
        else :
            leafify(self, context)
            return {'FINISHED'}

class LeafifyPanel(bpy.types.Panel):
    """Vector offset options for Leafify"""
    bl_label = "Leafify options"
    bl_idname = "OBJECT_PT_leafify_props"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOL_PROPS'
    bl_context = "mesh_edit"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(context.scene, 'leafify_offset')
        row = layout.row()
        row.operator("mesh.leafify", icon = 'UV_VERTEXSEL')

def add_object_manual_map():
    url_manual_prefix = "http://www.pasteall.org/"
    url_manual_mapping = (
        ("38138", "Modeling/Objects"),
        )
    return url_manual_prefix, url_manual_mapping


def register():
    
    bpy.utils.register_module(__name__)
    bpy.utils.register_manual_map(add_object_manual_map)
    
    bpy.types.Scene.leafify_offset = bpy.props.FloatVectorProperty(
        name="LeafifyOffset",
        default=(0.0,0.0,0.0),
        subtype='TRANSLATION',
        description="Offset between faces",
        min = 0.0,
        soft_min = 0.0
        )

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.utils.unregister_manual_map(add_object_manual_map)


if __name__ == "__main__":
    register()
