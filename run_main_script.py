import bpy
import random
import math

## 固定値設定 #############################################################
# 実行ファイルパス一覧
FILE_ROOT_PATH = 'D:/blender_battleVR_py/'
setrendr_file_name = FILE_ROOT_PATH + "setting_render.py"
magicobj_file_name = FILE_ROOT_PATH + "magic_model.py"
fieldins_file_name = FILE_ROOT_PATH + "field_model.py"
wizardob_file_name = FILE_ROOT_PATH + "wizard_model.py"

# SEファイルパス一覧
SE_ROOT_PATH = FILE_ROOT_PATH + 'se/'
#sound_begin = (SE_ROOT_PATH + "花火・一発_begin.wav", SE_ROOT_PATH + "花火・一発_begin.wav")
#sound_bomb = (SE_ROOT_PATH + "花火・一発_bomb.wav", SE_ROOT_PATH + "nc178345_bomb.wav")

# シーンのエンドフレーム
FRAME_END = 600
##########################################################################

#オブジェクト全選択
bpy.ops.object.select_all(action='SELECT') 
#オブジェクト全削除
bpy.ops.object.delete(True)

# シーケンスエディタを生成
if bpy.context.scene.sequence_editor:
    bpy.context.scene.sequence_editor_clear()
bpy.context.scene.sequence_editor_create()

# レンダリング設定
exec(compile(open(setrendr_file_name).read().replace("FILE_ROOT_PATH", FILE_ROOT_PATH), setrendr_file_name, 'exec'))

# フィールドを生成
exec(compile(open(fieldins_file_name).read(), fieldins_file_name, 'exec'))

# 魔法使いモデルを生成
exec(compile(open(wizardob_file_name).read(), wizardob_file_name, 'exec'))

# 魔法に使用するオブジェクトの作成
exec(compile(open(magicobj_file_name).read(), magicobj_file_name, 'exec'))