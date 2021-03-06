if __name__ == '__main__':
    # レンダリング設定
    bpy.data.scenes["Scene"].render.engine = "CYCLES"

    # 解像度
    bpy.data.scenes["Scene"].render.resolution_x = 1920
    bpy.data.scenes["Scene"].render.resolution_y = 960

    # レンダリングタイルの大きさを設定
    bpy.data.scenes["Scene"].render.tile_x = 300
    bpy.data.scenes["Scene"].render.tile_y = 300

    # レンダリング用のGPUを設定
    bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "CUDA"
    bpy.data.scenes["Scene"].cycles.device = "GPU"
    for d in bpy.context.preferences.addons["cycles"].preferences.devices:
        d["use"] = 1 # Using all devices, include GPU and CPU
    
    bpy.data.scenes["Scene"].cycles.progressive = "BRANCHED_PATH"
    bpy.data.scenes["Scene"].cycles.aa_samples = 256
    bpy.data.scenes["Scene"].cycles.preview_aa_samples = 128

    bpy.data.scenes["Scene"].render.filepath = "FILE_ROOT_PATH"
    bpy.data.scenes["Scene"].render.fps = 30
    bpy.data.scenes["Scene"].render.image_settings.file_format = "FFMPEG"
    bpy.data.scenes["Scene"].render.ffmpeg.format = "MPEG4"
    bpy.data.scenes["Scene"].render.ffmpeg.codec = "H264"
    bpy.data.scenes["Scene"].render.ffmpeg.audio_codec = "AAC"