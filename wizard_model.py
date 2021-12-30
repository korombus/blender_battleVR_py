import math

def WizardHead(C,D,color,pos,rot):
    # モンキーを生成
    bpy.ops.mesh.primitive_monkey_add(location=pos, rotation=rot)
    
    # マテリアルを設定
    material_glass = D.materials.new("wizard_head")
    # マテリアルのノードを使えるようにする
    material_glass.use_nodes = True
    material_tree = material_glass.node_tree

    # ノードの全削除
    for n in material_tree.nodes:
        material_tree.nodes.remove(n)
    
    # 出力ノードの作成
    output = material_tree.nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (300, 0)

    # グラスBSDFノード作成
    glass_bsdf = material_tree.nodes.new(type='ShaderNodeBsdfGlass')
    glass_bsdf.location = (0,0)

    # カラーランプの作成
    color_ramp = material_tree.nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (-300, 0)
    # 色を設定。
    color_ramp.color_ramp.elements[0].color = color
    color_ramp.color_ramp.elements[0].position = 0.6
    color_ramp.inputs[0].default_value = 0.5

    # ノードを接続
    # カラーランプ -> グラスBSDF
    material_tree.links.new(color_ramp.outputs[0], glass_bsdf.inputs[0])

    # グラスBSDF -> 出力
    material_tree.links.new(glass_bsdf.outputs[0], output.inputs[0])

    # マテリアルを追加
    C.object.data.materials.append(material_glass)


def WizardBody(C,D,color):
    # 体になる円錐を生成
    bpy.ops.mesh.primitive_cone_add(location=(0,0,-0.5))

    # マテリアルを設定
    material_glass = D.materials.new("wizard_body")
    # マテリアルのノードを使えるようにする
    material_glass.use_nodes = True
    material_tree = material_glass.node_tree

    # ノードの全削除
    for n in material_tree.nodes:
        material_tree.nodes.remove(n)
    
    # 出力ノードの作成
    output = material_tree.nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (300, 0)

    # グラスBSDFノード作成
    glass_bsdf = material_tree.nodes.new(type='ShaderNodeBsdfGlass')
    glass_bsdf.location = (0,0)

    # カラーランプの作成
    color_ramp = material_tree.nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (-300, 0)
    # 色を設定。
    color_ramp.color_ramp.elements[0].color = color
    color_ramp.color_ramp.elements[0].position = 0.1

    color_ramp.color_ramp.elements[1].color = (1,1,0,1)
    color_ramp.color_ramp.elements[1].position = 0.5

    # レイヤーウェイトを作成
    layer_weight = material_tree.nodes.new(type='ShaderNodeLayerWeight')
    layer_weight.location = (-600, 0)
    # ブレンドを設定。
    layer_weight.inputs[0].default_value = 0.5

    # ノードを接続
    # レイヤーウェイト -> カラーランプ
    material_tree.links.new(layer_weight.outputs[1], color_ramp.inputs[0])

    # カラーランプ -> グラスBSDF
    material_tree.links.new(color_ramp.outputs[0], glass_bsdf.inputs[0])

    # グラスBSDF -> 出力
    material_tree.links.new(glass_bsdf.outputs[0], output.inputs[0])

    # マテリアルを追加
    C.object.data.materials.append(material_glass)


def WizardModel(color, pos, rot):
    C = bpy.context
    D = bpy.data

    # 頭部分を生成
    WizardHead(C,D,color,pos, rot)
    # 頭オブジェクトを事前に取得
    head_obj = C.active_object
    
    # 体部分を生成
    WizardBody(C,D,color)
    # 体の親オブジェクトに頭を設定
    C.active_object.parent = head_obj

if __name__ == '__main__':
    # 回転はラジアンに直す必要があるので、そのための定数を用意
    ROTATE = 2*math.pi/360

    # 味方の魔法使い(青)
    WizardModel((0,0,1,1), (0,10,1.5), (0,0,0))

    # 敵の魔法使い(赤)
    WizardModel((1,0,0,1), (0,-10,1.5), (0,0,180*ROTATE))