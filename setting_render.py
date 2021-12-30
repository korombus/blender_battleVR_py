if __name__ == '__main__':
    # レンダリング設定
    bpy.data.scenes["Scene"].render.engine = "CYCLES"

    # レンダリング用のGPUを設定
    bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "CUDA"
    bpy.data.scenes["Scene"].cycles.device = "GPU"
    for d in bpy.context.preferences.addons["cycles"].preferences.devices:
        d["use"] = 1 # Using all devices, include GPU and CPU

    bpy.data.scenes["Scene"].render.filepath = "FILE_ROOT_PATH"
    bpy.data.scenes["Scene"].render.fps = 30
    bpy.data.scenes["Scene"].render.image_settings.file_format = "FFMPEG"
    bpy.data.scenes["Scene"].render.ffmpeg.format = "MPEG4"
    bpy.data.scenes["Scene"].render.ffmpeg.codec = "H264"
    bpy.data.scenes["Scene"].render.ffmpeg.audio_codec = "AAC"