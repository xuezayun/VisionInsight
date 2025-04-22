# -*- coding: utf-8 -*-
import os,sys,re,io
import edge_tts

import asyncio
from const_v import *
from moviepy.video.tools.subtitles import *
import shutil
import datetime
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from gtts import gTTS
from os import listdir
from os.path import join, isfile
# from moviepy.editor import VideoFileClip
from moviepy import *
from PIL import Image
import pyttsx3
import speech_recognition as sr
import pydub

    # 处理错误
from pydub import AudioSegment
import cv2

# def get_ffmpeg_path():
#     if getattr(sys, 'frozen', False):
#         # 如果是打包后的exe，使用PyInstaller的临时目录
#         if '_MEIPASS' in dir(sys):
#             base_path = sys._MEIPASS
#         else:
#             base_path = os.path.dirname(sys.executable)
#     else:
#         # 开发环境，基于脚本路径
#         base_path = os.path.dirname(__file__)

#     # 假设ffmpeg.exe在同一目录
#     ffmpeg_path = os.path.join(base_path, 'ffmpeg.exe')
#     return ffmpeg_path

# mp.ffmpeg_tools.ffmpeg_path = get_ffmpeg_path()
# os.environ["IMAGEIO_FFMPEG_EXE"] = get_ffmpeg_path()
# 功能	                          方法	                                                              被调用	
# 将文本合并成可以转为语音的文本	costruct_txt(text_path)	                                           generate_video	
# 将文字转成语音	              txt_2_mp3(txt,audio_file,voice)	                                  convert_txt_to_mp3	不是正统函数
# 将文本转为语音	              convert_txt_to_mp3(txt,audio_file)	                              generate_video	
# 依据路径合并mp4	              composite_video(src_video_path,target_video)		                 暂时没有用
# 给视频去音频	                  del_audio_fromvideo(src_video_file,target_video)		             暂时没有用
# 对视频格式转换	              convert_video(src_video_file,target_video)		                 暂时没有用
# 裁剪视频	                     del_video_bytime(src_video_file,target_video,start_time,end_time)	 暂时没有用
# 根据路径获取视频文件列表	      get_source_mp4_files(video_path)	composite_video	                  不是正统函数
# 根据图片路径合并到视频	      images_to_video(image_folder, output_path, target_size,fps=24)	   暂时没有用
# 根据文本音频视频文件合并成视频	generate_video(text_file,audio_file)		
# 根据文本和视频生成新的视频	   generate_video(text_file,src_video_file,target_video)		
# 备份文件	                     bak_file(source_file)		
# 重命名文件	                 rename_file(src_file,des_file)		

#将文本从文件中取出来，并形成可以转换语音的文字 ，本 generate_video调用
# def costruct_txt(text_file):
#     print("构造文本")
#     lst_time_txt = []
#     txt = ""
#     start_time = 0
#     end_time = 0
#     alpha_persecond = 4.27272727272727
#     totallen = 0
#     try:
#         # 打开文件
#         with open(text_file, 'r',encoding=V_TXT_ENCODING) as file:
#             # 逐行读取文件内容
#             for line in file:
#                 txtlen = len(line)
#                 print(txtlen)
#                 totallen+=txtlen
#                 end_time = start_time+ txtlen/alpha_persecond;
#                 temp_txt = line.strip()+"\n"
#                 txt = txt  + temp_txt 
#                 lst_time_txt.append(((start_time, end_time), temp_txt.strip()))
#                 # start_time = end_time+0.3
#                 start_time = end_time+0.01
#     except FileNotFoundError:
#         print(f"对不起,文本文件不存在，请确认路径是否正确：{text_file} .")
#     print(totallen)
#     return lst_time_txt,txt

def costruct_txt(text_file):
    print("构造文本")
    lst_time_txt = []
    txt = ""
    start_time = 0
    end_time = 0
    alpha_persecond = V_ALPHA_RATE
    print(f"alpha_persecond{alpha_persecond}")
    totallen = 0
    try:
        # 打开文件
        with open(text_file, 'r',encoding=V_TXT_ENCODING) as file:
            # 逐行读取文件内容
            for line in file:
                txtlen = len(line)
                print(txtlen)
                totallen+=txtlen
                end_time = start_time+ txtlen/alpha_persecond
                temp_txt = line.strip()+"\n"
                txt = txt  + temp_txt 
                lst_time_txt.append(((start_time, end_time), temp_txt.strip()))
                start_time = end_time+0.4045
    except FileNotFoundError:
        print(f"对不起,文本文件不存在，请确认路径是否正确：{text_file} .")
    print(totallen)
    return lst_time_txt,txt

#异步将文本合成音频
async def txt_2_mp3(txt,audio_file) -> None:  
    print("txt_2_mp3:"+audio_file)
    rate='0%'
    #,rate=rate
    VOICE = v_M_YunjianNeural
    communicate=edge_tts.Communicate(text=txt,voice=VOICE)
    await communicate.save(audio_file)

#由文本生成MP3
# def convert_txt_to_mp3(txt,audio_file):
#     # VOICE = v_M_YunjianNeural
#     asyncio.run(txt_2_mp3(txt,audio_file))  

# def convert_txt_to_mp3(txt,audio_file):
#     print('convert_txt_to_mp3')
#     myobj = gTTS(text=txt, lang=V_LANGUAGE)
#     # 保存为mp3文件
#     myobj.save(audio_file)

def convert_txt_to_mp3(txt,audio_file):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print(voices[3].id,voices[3].name)
    # for voice in voices:
    #     print(voice.id,voice.name)
    engine.setProperty('voice', voices[3].id)  # 选择KangKang
    engine.setProperty('rate', V_SPEECH_RATE)
    engine.setProperty('volume', 1.0)
    # engine.say(txt)
    engine.save_to_file(txt,audio_file)
    engine.runAndWait()
    print("convert_txt_to_mp3完成")


#将文件夹中的视频合成mp4文件
def composite_video(src_video_path,target_video):
    lst_videoclip = []
    lst_source_mp4 = get_source_mp4_files(src_video_path);
    print(len(lst_source_mp4))
    if len(lst_source_mp4) == 0:
        print("请确定MP4路径:{src_video_path} 中的文件存在")
    else:
        clips_list = [VideoFileClip(file) for file in lst_source_mp4]
        final_clip = concatenate_videoclips(clips_list)
        final_clip.write_videofile(target_video, codec='libx264')
        # 关闭所有加载的视频剪辑
        for clip in clips_list:
            clip.close()

#删除视频中的声音
def del_audio_fromvideo(src_video_file):
    # 加载视频文件
    video = VideoFileClip(src_video_file)
    # 删除声音（将音量设为0）
    video = video.without_audio()
    # 输出没有声音的视频
    video.write_videofile(V_SRC_MP4_TEMP_PATH)
    # 不要忘记释放资源
    video.close()
    #对文件进行重命名
    shutil.move(V_SRC_MP4_TEMP_PATH, src_video_file)

#转视频格式
def convert_video(src_video_file,target_video):
    # 加载视频文件
    video = VideoFileClip(src_video_file)
    # 输出没有声音的视频
    video.write_videofile(target_video)
    # 不要忘记释放资源
    video.close()


#删除指定时间之后的视频
def del_video_bytime(src_video_file,target_video,start_time):
    # 指定原始视频文件路径
    bak_file(src_video_file)
    # 创建剪辑对象，并指定截取的时间段
    clip = VideoFileClip(src_video_file).subclip(0, start_time)
    # 输出截取后的视频到新的文件
    clip.write_videofile(V_SRC_MP4_TEMP_PATH)
    # 关闭资源
    clip.close()
    shutil.move(V_SRC_MP4_TEMP_PATH, target_video)
    # shutil.copy(V_SRC_MP4_TEMP_PATH, target_video)
    # rename_file(V_SRC_MP4_TEMP_PATH,target_video)


#读取所有MP4文件
def get_source_mp4_files(video_path):
    lst_mp4 = []
    for root, dirs, files in os.walk(video_path):
        for file in files:
            if file.endswith('.mp4'):
                file_path = os.path.join(root, file)
                lst_mp4.append(file_path)
    return lst_mp4

#将图片集 合并成视频
def images_to_video(image_folder, output_path, target_size,fps=24):
    """
    将指定文件夹中的图片合成为一个视频文件。
    :param image_folder: 包含图片的文件夹路径
    :param output_path: 输出视频文件的路径
    :param fps: 视频的帧率,默认为24fps
    """
    # 获取文件夹中所有的文件名
    images = [join(image_folder, f) for f in listdir(image_folder) if isfile(join(image_folder, f))]
    # 按照文件名排序，确保图片顺序正确
    images.sort()
    print(images)
    resized_images = []
    for image in images:
        with Image.open(image) as im:
            img_resized = im.resize(target_size,Image.LANCZOS)
            img_np = np.array(img_resized)
            resized_images.append(img_np)
    # 创建一个ImageSequenceClip对象，fps参数设置视频帧率
    clip = ImageSequenceClip(resized_images, fps=fps)
    # 导出视频文件
    clip.write_videofile(output_path, codec='libx264')

#文本 和图片合成视频
def generate_video(text_file,src_video_file,target_video):
    # change_settings({"IMAGEMAGICK_BINARY": r"D:\\Tools\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})
    lst_setc,txt = costruct_txt(text_file)
    print("-------------------------------")
    print(f"txt_len:{len(txt)}")
    print(lst_setc)
    print("-------------------------------")
    # print(txt)
    # print(TextClip.list('font'))
    print("-------------------------------")

    convert_txt_to_mp3(txt,V_AUDIO)
    #加载音频文件
    audio_file = AudioFileClip(V_AUDIO)
    print(f"audio_file.duration:{audio_file.duration}")
    audio_duration = audio_file.duration
    #生成视频
    video_clip = VideoFileClip(src_video_file)
    print(video_clip.duration)
    video_duration = video_clip.duration
    print(f"audio_duration:{audio_duration}, video_duration:{video_duration}")
    if audio_duration<video_duration:
        del_video_bytime(src_video_file,target_video,audio_duration) 
    else :
        target_video = src_video_file#删除视频的指定时间之后的视频
    video_clip = VideoFileClip(target_video)
    #将音频和视频合成一个视频
    final_clip = video_clip.set_audio(audio_file)
    generator = lambda txt: TextClip(txt,font="华文隶书", fontsize=30, color='white')
    subtitles = SubtitlesClip(lst_setc, generator)
    #在视频中添加字幕
    final_clip_with_subtitles = CompositeVideoClip([final_clip,subtitles.set_pos(('center','bottom'))])
    #输出最终视频文件
    final_clip_with_subtitles.write_videofile(V_END_VIDEO,codec="libx264")
    video_clip.close()
    audio_file.close()
    final_clip_with_subtitles.close()

#备份文件
def bak_file(source_file):
    # 目标备份文件路径（通常会包含时间戳或版本号以区分不同备份）
    timestamp = datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")
    file_name = os.path.splitext(source_file)[0] 
    file_extension = os.path.splitext(source_file)[1] 
    backup_file =file_name+timestamp+file_extension
    # 检查目标目录是否存在，如果不存在则创建
    if not os.path.exists(os.path.dirname(backup_file)):
        os.makedirs(os.path.dirname(backup_file))
    # 复制文件
    shutil.copy2(source_file, backup_file)
    print(f"成功备份文件到 {backup_file}")

#对文件重命名
def rename_file(src_file,des_file):
    try:
        if os.path.exists(des_file):
            os.remove(des_file)
            print(f"存在的文件 {des_file} 已被删除.")
        os.rename(src_file, des_file)
    except FileNotFoundError:
        print(f"原文件 {src_file} 不存在.")
    except FileExistsError:
        print(f"新文件名 {des_file} 已经存在.")
    except PermissionError:
        print(f"没有足够的权限重命名 {src_file} 到 {des_file}.")


#异步将文本合成音频
async def dir_txt_2_mp3(txt,outpath) -> None:  
    rate='0%'
    #,rate=rate
    VOICE = v_M_YunjianNeural
    communicate=edge_tts.Communicate(text=txt,voice=VOICE)
    await communicate.save(outpath)

#由文本生成MP3
def convert_dir_txt_to_mp3_with_gtts(folder_path):
        # 指定要遍历的文件夹路径
    # folder_path = r'D:\超级书架\文学\宦海升沉录'
    # 使用os.walk遍历文件夹及其子文件夹
    language = 'zh-CN'  # 设置语言为中文，根据需要可以改为'en'（英文）等其他语言
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 检查文件是否为文本文件，例如.txt结尾
            if file.endswith('.txt'):
                # 获取完整文件路径
                file_path = os.path.join(root, file)
                # 打开并读取文件
                with open(file_path, 'r', encoding='utf-8') as f:
                    txt = f.read().replace('##',' ')
                    # 分离文件名和扩展名
                    base_name, ext = os.path.splitext(file)
                    audio_file_name = base_name+".mp3"
                    audio_file_path = os.path.join(folder_path, audio_file_name)
                    print(audio_file_path)
                    if not os.path.isfile(audio_file_path):
                        myobj = gTTS(text=txt, lang=language, slow=False)
                        # 保存为mp3文件
                        myobj.save(audio_file_path)
                        print(f"Text has been converted to {audio_file_path}")
                    else:
                        print(audio_file_path+" is exist")
#由文本生成MP3
def convert_dir_txt_to_mp3(folder_path):
        # 指定要遍历的文件夹路径
    # folder_path = r'D:\超级书架\文学\宦海升沉录'
    # 使用os.walk遍历文件夹及其子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 检查文件是否为文本文件，例如.txt结尾
            if file.endswith('.txt'):
                # 获取完整文件路径
                file_path = os.path.join(root, file)
                # 打开并读取文件
                with open(file_path, 'r', encoding='utf-8',errors='ignore') as f:
                    # txt = f.read().replace('##',' ')
                    txt = f.read()
                    # 分离文件名和扩展名
                    base_name, ext = os.path.splitext(file)
                    audio_file_name = base_name+".mp3"
                    audio_file_path = os.path.join(folder_path, audio_file_name)
                    print(audio_file_path)
                    if not os.path.isfile(audio_file_path):
                        asyncio.run(dir_txt_2_mp3(txt,audio_file_path))  
                    else:
                        print(audio_file_path+" is exist")

# 解析文本用到的类：
# PDFParser（文档分析器）：从文件中获取数据
# PDFDocument（文档对象）：保存文件数据
# PDFPageInterpreter（解释器）：处理页面内容
# PDFResourceManager（资源管理器）：存储共享资源
# PDFDevice:将解释器处理好的内容转换为我们所需要的
# PDFPageAggregator（聚合器）:读取文档对象
# LAParams（参数分析器）
# convert one PDF file to TXT file
def onePdfToTxt(filepath, outpath):
    try:
        #rb以二进制读模式打开本地pdf文件
        fp = open(filepath, 'rb')
        outfp = open(outpath, 'w', encoding='utf-8')
        #创建一个pdf文档分析器
        parser = PDFParser(fp)
        #创建一个PDF文档
        doc= PDFDocument(parser)
        # 连接分析器 与文档对象
        # parser.set_document(doc)
        # doc.set_parser(parser)
        # 提供初始化密码doc.initialize("lianxipython")
        # 如果没有密码 就创建一个空的字符串
        # doc.initialize("")
        # 检测文档是否提供txt转换，不提供就忽略
        if not doc.is_extractable:
            #raise PDFTextExtractionNotAllowed
            pass

        else:
            #创建PDf资源管理器
            resource = PDFResourceManager()
            #创建一个PDF参数分析器
            laparams = LAParams()
            #创建聚合器,用于读取文档的对象
            device = PDFPageAggregator(resource,laparams=laparams)
            #创建解释器，对文档编码，解释成Python能够识别的格式
            interpreter = PDFPageInterpreter(resource,device)
            # 循环遍历列表，每次处理一页的内容 doc.get_pages() 获取page列表
            for page in enumerate(PDFPage.create_pages(doc)):
                #利用解释器的process_page()方法解析读取单独页数
                interpreter.process_page(page[1])
                #使用聚合器get_result()方法获取内容
                layout = device.get_result()
                #这里layout是一个LTPage对象,里面存放着这个page解析出的各种对象
                for out in layout:
                    #判断是否含有get_text()方法，获取我们想要的文字
                    if hasattr(out,"get_text"):
                        text=out.get_text()
                        outfp.write(text+'\n')
            fp.close()
            outfp.close()
    except Exception as e:
         print (e)

# convert all PDF files in a folder to TXT files
def manyPdfToTxt (fileDir):
    files = os.listdir(fileDir)
    tarDir = fileDir+'txt'
    if not os.path.exists(tarDir):
        os.mkdir(tarDir)
    replace = re.compile(r'\.pdf',re.I)
    for file in files:
        filePath = fileDir+'\\'+file
        outPath = tarDir+'\\'+re.sub(replace, '', file)+'.txt'
        onePdfToTxt(filePath, outPath)
        print("saved in "+outPath)

def print_all_contains_word(file_path,word,save_path):
    lst_lines_all = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            file_name,suff = os.path.splitext(file)
            if suff != ".md":
                continue
            with open(os.path.join(root,file), 'r',encoding="utf-8") as filecontent:
                try:
                    lst_lines = filecontent.readlines()
                    for line in lst_lines:
                        if word in line:
                            # print(line.replace(" ",""))
                            lst_lines_all.append(line.replace(" ",""))
                            print(os.path.join(root,file))
                except Exception as e:
                    print(e)
    if len(lst_lines_all)>0:
        print("total:",len(lst_lines_all))
        with open(save_path,"w",encoding="utf-8") as save_file:
            save_file.writelines(lst_lines_all)



#将目录中的所有视频提取音频文件，并保存到指定的输出目录中
def extract_audio_from_videos(directory, output_directory):
    # 检查输出目录是否存在，如果不存在则创建
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # 遍历指定目录下的所有文件
    for filename in os.listdir(directory):
        # 构建完整的文件路径
        file_path = os.path.join(directory, filename)
        
        # 检查文件是否为视频文件（这里简单地通过扩展名判断）
        if filename.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.flv')):
            # 创建VideoFileClip对象
            video_clip = VideoFileClip(file_path)
            
            # 提取音频
            audio_clip = video_clip.audio
            
            # 构建输出文件名
            output_filename = os.path.splitext(filename)[0] + ".mp3"
            output_file_path = os.path.join(output_directory, output_filename)
            
            # 保存音频文件
            audio_clip.write_audiofile(output_file_path)
            
            # 释放资源
            audio_clip.close()
            video_clip.close()
            
            print(f"音频已从 {filename} 提取并保存为 {output_filename}")


def rename_files(folder_path):
    try:
        for filename in os.listdir(folder_path):
            # 匹配括号及其内容
            pattern = r'\([^)]*\)'
            new_filename = re.sub(pattern, '', filename)
            # 检查是否有修改
            if new_filename != filename:
                old_file_path = os.path.join(folder_path, filename)
                new_file_path = os.path.join(folder_path, new_filename)
                os.rename(old_file_path, new_file_path)
                print(f"已将 {filename} 重命名为 {new_filename}")
    except FileNotFoundError:
        print("错误: 指定的文件夹未找到!")
    except Exception as e:
        print(f"错误: 发生了一个未知错误: {e}")
def mp3_to_text(mp3_file, output_txt="output.txt"):
    """
    将MP3文件转换为文本并保存到文件。
    参数：
        mp3_file: 输入的MP3文件路径
        output_txt: 输出的文本文件路径
    """
    # 初始化语音识别器
    recognizer = sr.Recognizer()

    # 检查文件是否存在
    if not os.path.exists(mp3_file):
        print(f"错误：文件 {mp3_file} 不存在！")
        return

    try:
        # 将MP3转换为WAV（SpeechRecognition需要WAV格式）
        print("正在转换MP3为WAV...")
        audio = AudioSegment.from_mp3(mp3_file)
        wav_file = "temp_audio.wav"
        audio.export(wav_file, format="wav")

        # 读取WAV文件
        with sr.AudioFile(wav_file) as source:
            print("正在识别音频...")
            # 调整环境噪音（可选）
            recognizer.adjust_for_ambient_noise(source, duration=1)
            # 将音频转换为数据
            audio_data = recognizer.record(source)
            
            # 使用Google Speech Recognition进行识别
            text = recognizer.recognize_google(audio_data, language="zh-CN")  # 默认中文，可改为"en-US"等
            print("识别完成，结果如下：")
            print(text)

            # 保存到文本文件
            with open(output_txt, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"文本已保存到 {output_txt}")

        # 清理临时文件
        os.remove(wav_file)

    except sr.UnknownValueError:
        print("错误：无法识别音频内容，可能音频太模糊或无声。")
    except sr.RequestError as e:
        print(f"错误：无法连接到语音识别服务，{e}")
    except Exception as e:
        print(f"发生错误：{str(e)}")
        
def mp3_to_text_long(mp3_file, output_txt="output.txt", segment_length=60):
    """
    将长MP3文件分段转换为文本并保存。
    参数：
        mp3_file: 输入的MP3文件路径
        output_txt: 输出的文本文件路径
        segment_length: 每段音频的长度（秒）
    """
    # 检查文件是否存在
    if not os.path.exists(mp3_file):
        print(f"错误：文件 {mp3_file} 不存在！")
        return

    # 初始化语音识别器
    recognizer = sr.Recognizer()
    full_text = ""

    try:
        # 加载MP3文件
        print("正在加载MP3文件...")
        audio = AudioSegment.from_mp3(mp3_file)
        total_duration = len(audio) / 1000  # 转换为秒
        print(f"音频总时长: {total_duration:.2f} 秒")
        str_time = ''

        # 分段处理
        for i in range(0, len(audio), segment_length * 1000):
            segment = audio[i:i + segment_length * 1000]
            wav_file = f"temp_segment_{i//1000}.wav"
            print(f"正在处理 {i//1000}-{i//1000 + segment_length} 秒段...")
            str_time = f"{i//1000}-{i//1000 + segment_length}:"
            
            # 导出为WAV
            segment.export(wav_file, format="wav")

            # 识别音频
            with sr.AudioFile(wav_file) as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)  # 调整噪音
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language="zh-CN")
                    full_text += str_time+ text + " "
                    # full_text += text + " "
                    print(f"段 {i//1000} 识别结果: {text}")
                except sr.UnknownValueError:
                    print(f"段 {i//1000}：无法识别音频内容")
                    full_text += "[无法识别] "

            # 删除临时文件
            os.remove(wav_file)

        # 保存完整文本
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(full_text.strip())
        print(f"处理完成！文本已保存到 {output_txt}")

    except Exception as e:
         # 保存完整文本
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(full_text.strip())
        print(f"处理完成！文本已保存到 {output_txt}")
    finally:
        # 清理可能残留的临时文件
        for temp_file in [f for f in os.listdir() if f.startswith("temp_segment_")]:
            os.remove(temp_file)
#将视频中的文件截图
def extract_frames_by_difference(video_folder, start_pixel=(0, 0), end_pixel=None, start_time=0, end_time=None,
                                 threshold=0.5):
    """
    根据前后帧差异超过指定阈值提取视频截图，保存到video_folder下的screenshots子目录，文件名包含时间戳。

    参数：
        video_folder (str): 视频文件或文件夹路径
        start_pixel (tuple): 矩形区域左上角坐标 (x1, y1)，默认(0, 0)
        end_pixel (tuple): 矩形区域右下角坐标 (x2, y2)，默认None（整帧）
        start_time (float): 开始时间（秒），默认0
        end_time (float): 结束时间（秒），默认None（视频结束）
        threshold (float): 差异阈值，默认0.3（30%）
    """
    # 设置截图保存目录为video_folder下的screenshots子目录
    output_dir = os.path.join(video_folder, "screenshots")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 检查video_folder是文件夹还是文件
    if os.path.isdir(video_folder):
        video_files = [f for f in os.listdir(video_folder) if f.endswith((".mp4", ".avi", ".mkv"))]
        if not video_files:
            print(f"文件夹 {video_folder} 中没有视频文件")
            return
    else:
        video_files = [os.path.basename(video_folder)]
        video_folder = os.path.dirname(video_folder) or "."

    # 遍历所有视频文件
    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"无法打开视频文件: {video_path}")
            continue

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)  # 获取帧率
        if fps <= 0:  # 防止除以0
            fps = 30  # 默认值
        total_duration = frame_count / fps  # 视频总时长（秒）

        # 设置默认结束时间
        if end_time is None or end_time > total_duration:
            end_time = total_duration

        # 计算起始帧和结束帧
        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)

        if start_frame >= frame_count or end_frame > frame_count or start_frame >= end_frame:
            print(f"无效的时间区间: start_time={start_time}, end_time={end_time}, 总时长={total_duration}")
            cap.release()
            continue

        print(f"处理视频: {video_path}, 帧数: {frame_count}, 分辨率: {frame_width}x{frame_height}, FPS: {fps}")
        print(f"时间区间: {start_time}秒 - {end_time}秒, 对应帧: {start_frame} - {end_frame}")

        if end_pixel is None:
            end_pixel = (frame_width, frame_height)
        x1, y1 = start_pixel
        x2, y2 = end_pixel
        if x1 < 0 or y1 < 0 or x2 > frame_width or y2 > frame_height or x1 >= x2 or y1 >= y2:
            print(f"无效的矩形区域: start_pixel={start_pixel}, end_pixel={end_pixel}")
            cap.release()
            continue

        # 设置视频位置到起始帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        ret, prev_frame = cap.read()
        if not ret:
            cap.release()
            continue
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        frame_idx = start_frame

        while frame_idx < end_frame:
            ret, curr_frame = cap.read()
            if not ret:
                break
            frame_idx += 1
            curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
            diff = cv2.absdiff(prev_gray, curr_gray)
            non_zero_count = np.count_nonzero(diff)
            total_pixels = curr_gray.size
            diff_ratio = non_zero_count / total_pixels
            if diff_ratio > threshold:
                # 计算时间戳
                seconds = frame_idx / fps
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                secs = int(seconds % 60)
                timestamp = f"{hours:02d}-{minutes:02d}-{secs:02d}"
                # 生成文件名包含时间戳
                cropped_frame = curr_frame[y1:y2, x1:x2]
                output_path = os.path.join(output_dir, f"{os.path.splitext(video_file)[0]}_frame_{frame_idx:06d}_{timestamp}_cropped.jpg")
                cv2.imencode('.jpg', cropped_frame)[1].tofile(output_path)
                print(f"保存截图: {output_path}, 差异比例: {diff_ratio:.2f}")
            prev_gray = curr_gray.copy()

        cap.release()
        print(f"视频 {video_path} 处理完成，截图保存至: {output_dir}")

    print(f"所有视频处理完成，截图保存至: {output_dir}")
        
if __name__=="__main__":
    # TXT_DIR = r"D:\projects\pyproject\T-V\FILE\SRC_TXT"
    # convert_dir_txt_to_mp3(TXT_DIR)
    extract_audio_from_videos(r'D:\Tools\JiJiDown\Update\Download\【华语摇滚100首精选】放肆宣泄的青春_分P播放_卡拉OK歌词_眼睛酷美女壁纸评论区获取',r'C:\Users\zyh\Desktop\0323')
