def CameraSetting(C,D):
    # 回転はラジアンに直す必要があるので、そのための定数を用意
    ROTATE = 2*math.pi/360

    # カメラ配置
    bpy.ops.object.camera_add(location=(0,0,4), rotation=(90*ROTATE, 0, 180*ROTATE))
    C.active_object.name = "Camera"

    D.cameras[-1].type = 'PANO'
    D.cameras[-1].cycles.panorama_type = "EQUIRECTANGULAR"

if __name__ == '__main__':
    C = bpy.context
    D = bpy.data

    CameraSetting(C,D)