import random

def CreateWitchCraftModel(C,D,type,color,pos,rot):
    # 魔法陣のためのPlaneを追加
    bpy.ops.mesh.primitive_plane_add(size=5, location=pos, rotation=rot)
    C.active_object.name = "Witchcraft_" + type

    # マテリアルを設定
    material_glass = D.materials.new("witchcraft")
    # マテリアルのノードを使えるようにする
    material_glass.use_nodes = True
    material_tree = material_glass.node_tree

    # ノードの全削除
    for n in material_tree.nodes:
        material_tree.nodes.remove(n)
    
    # 出力ノードの作成
    output = material_tree.nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (300, 0)

    # 画像テクスチャの作成
    texture_image = material_tree.nodes.new(type='ShaderNodeTexImage')
    texture_image.image = bpy.data.images[random.randint(0,4)]

    # 透過BSDFの作成
    bsdf_transparent = material_tree.nodes.new(type='ShaderNodeBsdfTransparent')

    # 放射の作成
    emission = material_tree.nodes.new(type='ShaderNodeEmission')
    emission.inputs[1].default_value = 10

    # RGBの作成
    rgb_material = material_tree.nodes.new(type='ShaderNodeRGB')
    rgb_material.outputs[0].default_value = color

    # シェーダーミックスの作成
    shader_mix = material_tree.nodes.new(type='ShaderNodeMixShader')

    # 画像テクスチャ -> シェーダーミックス
    material_tree.links.new(texture_image.outputs[1], shader_mix.inputs[0])

    # 透過BSDF -> シェーダーミックス
    material_tree.links.new(bsdf_transparent.outputs[0], shader_mix.inputs[1])

    # RGB -> 放射
    material_tree.links.new(rgb_material.outputs[0], emission.inputs[0])

    # 放射 -> シェーダーミックス
    material_tree.links.new(emission.outputs[0], shader_mix.inputs[2])

    # シェーダーミックス -> 出力
    material_tree.links.new(shader_mix.outputs[0], output.inputs[0])

    # マテリアルを追加
    C.object.data.materials.append(material_glass)

if __name__ == '__main__':
    C = bpy.context
    D = bpy.data

    witchcraft_image = WITCHECRAFT_IMAGES

    # 事前に魔法陣の画像をloadしておく
    # すでにloadされている場合は、二重でloadされないように制約を付ける
    # bpy.opsから逐次ロードする方法もあるが、bpy.dataに事前ロードしてデータベースを作っておいた方が
    # 複数回呼び出す場合は、Blenderにとって都合が良いらしい。
    # （bpy.opsは基本的に揮発性のようなので、複数回使う画像はキャッシュしておいた方が良いのはその通り）
    for wcf_img in witchcraft_image:
        bpy.data.images.load(wcf_img, check_existing=True)

    # 回転はラジアンに直す必要があるので、そのための定数を用意
    ROTATE = 2*math.pi/360

    # 味方の魔法陣数
    ally_witchcraft_num = 5
    # 敵の魔法陣数
    enemy_witchcraft_num = 5
    
    # 赤、青、緑、黄色
    colors = [(1,0,0,1),(0,0,1,1),(0,1,0,1),(1,1,0,1)]

    # 味方の魔法陣を生成
    for ally_witchcraft in range(ally_witchcraft_num):
        pos = (random.uniform(-5,5), D.objects["Wizard_Ally"].location.y + 13, random.uniform(4, 15))
        rot = (90*ROTATE,0,0)
        # 魔法陣を生成
        CreateWitchCraftModel(C,D,"Ally",colors[random.randint(0,3)],pos,rot)

    # 敵の魔法陣を生成
    for enemy_witchcraft in range(enemy_witchcraft_num):
        pos = (random.uniform(-5,5), D.objects["Wizard_Enemy"].location.y - 13, random.uniform(4, 15))
        rot = (-90*ROTATE,0,0)
        CreateWitchCraftModel(C,D,"Enemy",colors[random.randint(0,3)],pos,rot)

    # 魔法陣範囲
    # 味方
    # x: -5 ~ 5
    # y: 13
    # z: 4 ~ 15

    # 敵
    # x: -5 ~ 5
    # y: -13
    # z: 4 ~ 15