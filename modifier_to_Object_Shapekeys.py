import bpy  

# First object is source, second one is the one with the hooks.
source_object = bpy.context.view_layer.objects.selected[0]
mesh_modifier_object = bpy.context.view_layer.objects.selected[1]

show_shape_key_tracker = False
modShapeKey_list = []

# Removing the source from the selected list.
bpy.context.view_layer.objects.selected[1].select_set(False)

mesh_modifier_object.show_only_shape_key = False
# Tracking the user's show shapekey selection. 
if source_object.show_only_shape_key == False:
    source_object.show_only_shape_key = True
    show_shape_key_tracker = True
    
    
# Adding a shapekey if none exists:
if not mesh_modifier_object.data.shape_keys: 
    mesh_modifier_object.shape_key_add(name='Basis', from_mix=False)
    
# Setting every shapekey to 0 in the hook modifier object.
[setattr(x, 'value', 0) for x in mesh_modifier_object.data.shape_keys.key_blocks]

# The outside loop enumerates through each of the shape keys in the source object. 
for index, blocks in enumerate(source_object.data.shape_keys.key_blocks[1:], 1):
    print(index, ' ', blocks.name)
    source_object.active_shape_key_index = index
    sourceKeyName = source_object.active_shape_key.name
    
    print(index)
    # Going through each modifier in the stack and saving it as a shapekey. The name is taken from the source. Each created shapekey is kept track by a list.
    for modifier in mesh_modifier_object.modifiers: 
        if modifier.type == 'HOOK':
            bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=True,modifier=modifier.name)       
            recentShapekey = mesh_modifier_object.data.shape_keys.key_blocks[-1]
            recentShapekey.name = 'temp_' + source_object.active_shape_key.name    
            modShapeKey_list.append(recentShapekey)
    # Setting the source object index to basis and creating a new shapekey as a mix. The modifier shape keys are then removed and the list is cleared.         
    source_object.active_shape_key_index = 0
    [setattr(tempshapekeys, 'value', 1) for tempshapekeys in modShapeKey_list]
    mesh_modifier_object.shape_key_add(name = sourceKeyName, from_mix=True)
    for tempshapekeys in modShapeKey_list: mesh_modifier_object.shape_key_remove(tempshapekeys)
    
    modShapeKey_list.clear()


# Cleaning up
source_object.active_shape_key_index = 0
mesh_modifier_object.active_shape_key_index = 0

# Setting the Shape key selection to how it was.
if show_shape_key_tracker == True:
    source_object.show_only_shape_key = False
    show_shape_key_tracker = False