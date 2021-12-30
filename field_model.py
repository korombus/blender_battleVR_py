def FieldModel(C,D):
    # 光源の太陽を生成
    bpy.ops.object.light_add(type='SUN', location=(0,0,100))

    # 大地を生成
    bpy.ops.mesh.primitive_plane_add(size=1000)
    material_ground = D.materials.new('Ground_Material')
    material_ground.diffuse_color = (0,0.087,0,0)
    # マテリアルを追加
    C.object.data.materials.append(material_ground)

    # 空を生成
    # 空はBlenderに元々搭載されているアドオンである「Dynamic Sky」を使用する
    import addon_utils
    addon_utils.enable("lighting_dynamic_sky")
    
    # dynamyc_skyのワールドマテリアルを生成
    # 生成時にレンダーエンジンが自動的に「Cycle」に変更される。
    # その際に初期状態だと描画デバイスが「CPU」になっているため、
    # 必要に応じて「GPU」に切り替えること。
    # Cycleになる理由は、このアドオンが「Cycle」での使用を想定しているため。
    # 但し、レンダーエンジンを「Eevee」にしても問題なく描画されるため、
    # 必要に応じてレンダーエンジンの切り替えも行うこと。（確認するだけならばEeveeの方が軽い）
    bpy.ops.sky.dyn()
    dyn_sky = D.worlds.get(C.scene.dynamic_sky_name)
    
    # 空の色
    dyn_sky.node_tree.nodes["Sky_and_Horizon_colors"].inputs[1].default_value = (0,0,1,1)
    # 地平線の色
    dyn_sky.node_tree.nodes["Sky_and_Horizon_colors"].inputs[2].default_value = (0,0.1,1,1)
    # 雲の透過率
    dyn_sky.node_tree.nodes["Cloud_opacity"].inputs[0].default_value = 0.3
    # 雲の密度
    dyn_sky.node_tree.nodes["Cloud_density"].inputs[0].default_value = 0.47

    # ワールドマテリアルにdynamyc_skyを設定
    C.scene.world = dyn_sky

    
if __name__ == '__main__':
    C = bpy.context
    D = bpy.data

    FieldModel(C,D)