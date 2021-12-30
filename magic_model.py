import random

def CreateStarObject(C,D):
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
    star_obj.location = (0, 0, -1000)

    # オブジェクトをシーンコレクションへリンク
    C.collection.objects.link(star_obj)
    bpy.ops.object.collection_link(collection='Collection')

    # オブジェクトをアクティブにする
    C.view_layer.objects.active = star_obj

def MaterialMagic(C,D,color):
    # 魔法のパーティクルオブジェクトを生成
    CreateStarObject(C,D)
    
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

if __name__ == '__main__':
    C = bpy.context
    D = bpy.data
    
    # 赤、青、緑、黄色
    colors = [(1,0,0,1),(0,0,1,1),(0,1,0,1),(1,1,0,1)]


    # 4色の中からランダムで選択
    MaterialMagic(C,D,colors[random.randint(0,3)])