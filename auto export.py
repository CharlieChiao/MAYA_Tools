import maya.cmds as cmds
import string

selection = cmds.ls(sl=True)
parentlist = []
PATH = "G:/Project/Personal/TestAutoSave"

def move_pivot_to_bbox_bottom_center(obj_name):
    bbox = cmds.xform(obj_name, query=True, boundingBox=True)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox
    center_x = (xmin + xmax) / 2.0
    center_y = ymin
    center_z = (zmin + zmax) / 2.0
    cmds.xform(obj_name, pivots=(center_x, center_y, center_z), worldSpace=True)

def export_selected_to_fbx(path, obj):
    if not cmds.pluginInfo("fbxmaya", query=True, loaded=True):
        cmds.loadPlugin("fbxmaya")
    
    selected_objects = cmds.ls(selection=True)
    
    if not obj:
        print("No objects selected for export.")
        return
    
    obj_name = "{}".format(obj)

    if obj_name.__contains__("["):
        obj_name = obj_name[2:-2]
    
    export_file_path = "{}/{}.fbx".format(path, obj_name)
    
    cmds.FBXExportSmoothingGroups("-v", True)
    cmds.FBXExportHardEdges("-v", False)
    cmds.FBXExportTangents("-v", False)
    cmds.FBXExportSmoothMesh("-v", True)
    cmds.FBXExportInstances("-v", False)
    
    cmds.FBXExport("-f", export_file_path, "-s")

def freeze_transform(obj):
    cmds.makeIdentity(obj, apply=True, t=1, r=1, s=1, n=0, pn=1)

def delete_history(obj):
    cmds.delete(obj, constructionHistory=True)

def Save (path, obj):
    freeze_transform(obj)
    delete_history(obj)
    original_translate = cmds.xform(obj, query=True, translation=True, worldSpace=True)
    original_position = cmds.xform(obj, query=True, piv=True, worldSpace=True)
    if (original_translate[0] == 0.0) & (original_translate[1] == 0.0) & (original_translate[2] == 0.0):
        cmds.xform(obj, translation=(-original_position[0],-original_position[1],-original_position[2]), worldSpace=True)
        export_selected_to_fbx(path, obj)
        cmds.xform(obj, translation=(0, 0, 0), worldSpace=True)
    else:
        cmds.xform(obj, translation=(0, 0, 0), worldSpace=True)
        export_selected_to_fbx(path, obj)
        cmds.xform(obj, translation=original_translate, worldSpace=True)

for index, obj in enumerate(selection):
    parent = cmds.listRelatives(obj,p=1)
    
    isUnique = False
    if parent :
        if len(parentlist) > 0:
            for i in range(len(parentlist)):
                if parent == parentlist[i]:
                    isUnique = False
                    break
                else:
                    isUnique = True
        else:            
            parentlist.append(parent)
            print(parent)
        if isUnique:
            parentlist.append(parent)
            print(parent)
    else:
        cmds.select(obj)
        move_pivot_to_bbox_bottom_center(selection[index])
        Save(PATH, obj)
        print(obj)
        

for index, group in enumerate(parentlist):
    cmds.select(group)
    move_pivot_to_bbox_bottom_center(parentlist[index])
    Save(PATH, group)
