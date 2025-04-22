'''
Description: 
Date: 2024-01-23 06:25:14
LastEditTime: 2024-11-01 18:47:11
FilePath: \T-V\tvv_v\const_v.py
'''
# -*- coding: utf-8 -*-
v_F_XiaoxiaoNeural = "zh-CN-XiaoxiaoNeural"
v_F_XiaoyiNeural = "zh-CN-XiaoyiNeural"
v_M_YunjianNeural = "zh-CN-YunjianNeural"
v_M_YunxiNeural = "zh-CN-YunxiNeural"
v_M_YunxiaNeural = "zh-CN-YunxiaNeural"
v_M_YunyangNeural = "zh-CN-YunyangNeural"
v_F_liaoning_XiaobeiNeural = "zh-CN-liaoning-XiaobeiNeural"
v_F_shaanxi_XiaoniNeural = "zh-CN-shaanxi-XiaoniNeural"
v_F_HK_HiuGaaiNeural = "zh-HK-HiuGaaiNeural"
v_F_HK_HiuMaanNeural = "zh-HK-HiuMaanNeural"
v_F_WanLungNeural = "zh-HK-WanLungNeural"
v_M_HsiaoChenNeural = "zh-HK-HsiaoChenNeural"
v_F_TW_XiaoyiNeural = "zh-TW-XiaoyiNeural"
v_M_TW_YunJheNeural = "zh-TW-YunJheNeural"

#读取内容的文本
V_SRC_TXT = r"D:\projects\pyproject\T-V\FILE\SRC_TXT/txt.txt"
V_SRC_VIDEO = r"D:\projects\pyproject\T-V\FILE\SRC_VIDEOS/src_video.mp4"
V_TARGET_VIDEO = r"D:\projects\pyproject\T-V\FILE\TARGET_VIDEOS/target_video.mp4"
V_AUDIO = r"D:\projects\pyproject\T-V\FILE\SRC_AUDIOS/audio.mp3"
V_SRC_MP4_TEMP_PATH = r"D:\projects\pyproject\T-V\FILE\TEMP_VIDEO\temp_video.mp4"
V_END_VIDEO = r"D:\projects\pyproject\T-V\FILE\END_FILE/end_video.mp4"
V_LANGUAGE = 'zh-CN'
#文本编码
V_TXT_ENCODING='utf-8'
#中文字体
# V_YH_FONT=r"D:\projects\pyproject\T-V\tvv_v/fonts/MSYH.TTC"
V_HWZS_FONT=r"D:\projects\pyproject\T-V\tvv_v/fonts/华文中宋.TTF"

#去除水印
V_CON_REMOVE_WATERMASK = 1
#去除字幕
V_CON_REMOVE_SUBTITLE = 2

#阈值分割所用阈值
V_THRESHOLD=80
#膨胀运算核尺寸
V_KERNEY_SIZE=5
#语速每分钟多个单词
V_SPEECH_RATE = 150
V_ALPHA_RATE = V_SPEECH_RATE/33.56

CONST_VOICE = v_M_YunjianNeural
VIDEO_PATH = r"D:/projects/pyproject/T-V/FILE/raw/rawvideo"
OUTPUT_PATH = r"D:/projects/pyproject/T-V/FILE/raw/rawoutput"
TEMP_VIDEO = r"D:/projects/pyproject/T-V/FILE/raw/temp.mp4"