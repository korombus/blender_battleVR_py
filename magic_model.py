import random

def CreateStarObject(C,D,pos=(0,0,0)):
    # 頂点座標
    verts = [[0.0015, -0.0034, 0.4340],[0.0000, 1.0000, 0.0000],[-0.2067, 0.2845, 0.0000],[-0.9511, 0.3090, 0.0000],
            [-0.3345, -0.1087, 0.0000],[-0.5878, -0.8090, 0.0000],[0.0000, -0.3517, 0.0000],[0.5878, -0.8090, 0.0000],
            [0.3345, -0.1087, 0.0000],[0.9511, 0.3090, 0.0000],[0.2067, 0.2845, 0.0000],[0.0000, -0.0000, -0.5236]]
    # 面を構成する頂点一覧
    faces = [[ 0,  1,  2],[ 0,  2,  3],[ 0,  3,  4, ],[ 0,  4,  5],[ 0,  5,  6],
            [ 0,  6,  7],[ 0,  7,  8],[ 0,  8,  9],[ 0,  9, 10],[ 0, 10,  1],
            [ 2,  1, 11],[ 1, 10, 11],[10,  9, 11],[ 9,  8, 11],[ 8,  7, 11],
            [ 7,  6, 11],[ 6,  5, 11],[ 5,  4, 11],[ 4,  3, 11],[ 3,  2, 11]]
    
    # 星形のメッシュを作成
    star_msh = D.meshes.new(name="magic_star_mesh")
    star_msh.from_pydata(verts, [], faces)
    star_msh.update()

    # 星形のオブジェクトを生成
    star_obj = D.objects.new(name="magic_star", object_data=star_msh)
    star_obj.location = pos

    # オブジェクトをシーンコレクションへリンク
    C.collection.objects.link(star_obj)
    bpy.ops.object.collection_link(collection='Collection')

    # オブジェクトをアクティブにする
    C.view_layer.objects.active = star_obj

def MaterialMagic(C,D,color,pos=(0,0,0)):
    # 魔法のオブジェクトを生成
    CreateStarObject(C,D,pos)
    
    # マテリアルを新たに設定
    material_glass = D.materials.new('Magic_Particle_Material')
    
    # ノードを使えるようにする
    material_glass.use_nodes = True

    material_tree = material_glass.node_tree

    # ノードの全削除
    for n in material_tree.nodes:
        material_tree.nodes.remove(n)

    # 出力ノードの作成
    output = material_tree.nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (300, 0)

    # 放射ノードの作成
    emission = material_tree.nodes.new(type='ShaderNodeEmission')
    emission.location = (0, 0)
    emission.inputs[0].default_value = color

    # ノードを接続
    material_tree.links.new(emission.outputs[0], output.inputs[0])

    # マテリアルを追加
    C.object.data.materials.append(material_glass)

def CreateMagicParticle(C,D,color, start_frame):
    # パーティクルを設定する魔法を事前に取得
    magic_obj = C.active_object

    # パーティクル用の魔法オブジェクトを生成
    MaterialMagic(C,D,color,(0,0,1000))
    particle_obj = C.active_object

    # アクティブオブジェクトを魔法に切り替え
    C.view_layer.objects.active = magic_obj

    # パーティクルシステムを追加
    bpy.ops.object.particle_system_add()

    # パーティクルを設定
    p_s = magic_obj.particle_systems[0].settings

    # 放射
    p_s.count = 30
    p_s.frame_start = start_frame
    p_s.frame_end = start_frame + 14
    p_s.lifetime = 20
    
    # 速度
    p_s.normal_factor = 7.0

    # レンダー
    p_s.render_type = 'OBJECT'
    p_s.particle_size = 0.5
    p_s.instance_object = particle_obj

    # フィールドの重み
    p_s.effector_weights.gravity = 0

def CreateWitchcraftAnimation(C,D, wc_obj, start_frame, end_frame):
    # 魔法陣の出現アニメーション

    # 回転はラジアンに直す必要があるので、そのための定数を用意
    ROTATE = 2*math.pi/360

    # 初期フレーム
    C.scene.frame_set(start_frame)
    wc_obj.rotation_euler[1] = 180 * ROTATE
    wc_obj.scale[0] = 0
    wc_obj.scale[1] = 0
    wc_obj.scale[2] = 0
    wc_obj.keyframe_insert(data_path="rotation_euler", index=-1)
    wc_obj.keyframe_insert(data_path="scale", index=-1)

    # 表示フレーム
    C.scene.frame_set(end_frame)
    wc_obj.rotation_euler[1] = 0
    wc_obj.scale[0] = 1
    wc_obj.scale[1] = 1
    wc_obj.scale[2] = 1
    wc_obj.keyframe_insert(data_path="rotation_euler", index=-1)
    wc_obj.keyframe_insert(data_path="scale", index=-1)


def CreateMagicAnimation(C,D,end_frame_pos, start_frame, end_frame):
    # 魔法を撃ち出して、着弾するまでのアニメーションを設定

    # アニメーションさせる魔法を取得
    magic_obj = C.active_object

    # 初期フレーム
    C.scene.frame_set(start_frame)
    magic_obj.location = (0, 0, 0)
    magic_obj.show_instancer_for_viewport = True
    magic_obj.show_instancer_for_render = True
    magic_obj.keyframe_insert(data_path="location", index=-1)
    magic_obj.keyframe_insert(data_path="show_instancer_for_viewport", index=-1)
    magic_obj.keyframe_insert(data_path="show_instancer_for_render", index=-1)

    # 撃ち出し始めの出現
    C.scene.frame_set(int(end_frame / 2))
    magic_obj.location = (0, 0, 0)
    magic_obj.show_instancer_for_viewport = True
    magic_obj.show_instancer_for_render = True
    magic_obj.keyframe_insert(data_path="location", index=-1)
    magic_obj.keyframe_insert(data_path="show_instancer_for_viewport", index=-1)
    magic_obj.keyframe_insert(data_path="show_instancer_for_render", index=-1)

    # 着弾したら非表示にする
    C.scene.frame_set(end_frame - 2)
    magic_obj.location = end_frame_pos
    magic_obj.show_instancer_for_viewport = False
    magic_obj.show_instancer_for_render = False
    magic_obj.keyframe_insert(data_path="location", index=-1)
    magic_obj.keyframe_insert(data_path="show_instancer_for_viewport", index=-1)
    magic_obj.keyframe_insert(data_path="show_instancer_for_render", index=-1)

if __name__ == '__main__':
    C = bpy.context
    D = bpy.data
    
    # 赤、青、緑、黄色
    colors = [(1,0,0,1),(0,0,1,1),(0,1,0,1),(1,1,0,1)]

    # 魔法陣のオブジェクト一覧を抽出
    # 魔法陣と同じ位置に魔法を作り出す
    witchcraft_object_list = [ obj for obj in D.objects if "Witchcraft" in obj.name ]

    start_frame = 0
    end_frame = 80
    threshold_frame = 20

    # 魔法陣すべてに魔法を充填
    for witchcraft in witchcraft_object_list:
        # 4色の中からランダムで選択
        choice_color = colors[random.randint(0,3)]
        # 魔法を生成
        MaterialMagic(C,D,choice_color)

        # 魔法陣を魔法の親に設定
        C.active_object.parent = witchcraft

        # 魔法陣にアニメーションを設定
        CreateWitchcraftAnimation(C,D,witchcraft,start_frame,start_frame + threshold_frame)

        # 魔法にパーティクルを設定
        CreateMagicParticle(C,D,choice_color,end_frame)

        # 魔法にアニメーションを設定
        # アニメーションの終着位置を計算
        # 向かう方向が敵と味方で計算方法が違うため条件を分ける
        # また、魔法陣はx軸方向に90度回転させているので、zとyが入れ替わる点に注意
        # 魔法陣の座標を(x,y,z), 魔法使いの座標を(Wx,Wy,Wz)とすると
        # 味方：-x, -z+Wz, y+Wy
        # 敵　：-x, z-Wz, -y-Wy
        if "Ally" in witchcraft.name:
            end_frame_pos = (-witchcraft.location.x, -witchcraft.location.z + D.objects["Wizard_Ally"].location.z, witchcraft.location.y + D.objects["Wizard_Ally"].location.y - 1)
        else:
            end_frame_pos = (-witchcraft.location.x, witchcraft.location.z - D.objects["Wizard_Enemy"].location.z, -witchcraft.location.y - D.objects["Wizard_Enemy"].location.y + 1)
        
        # 魔法にアニメーションを設定
        CreateMagicAnimation(C,D,end_frame_pos,start_frame,end_frame)

        start_frame += threshold_frame
        end_frame += threshold_frame