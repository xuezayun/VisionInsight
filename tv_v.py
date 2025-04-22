# -*- coding: utf-8 -*-
import utils;
from const_v import *
import tkinter as tk
import os
import threading
import time
from tkinter import filedialog, messagebox, ttk
import sys
from io import StringIO
import cv2
from PIL import Image, ImageTk

def composite_images_2_video():
    image_dir = r'D:\projects\pyproject\T-V\FILE\SRC_IMAGES'
    video_dir = r'D:\projects\pyproject\T-V\FILE\SRC_VIDEOS\target.mp4'
    target_size= (800,600)
    fps = 0.33
    utils.images_to_video(image_dir,video_dir,target_size,fps)

def generate_video():
    txt_file = V_SRC_TXT
    src_video_file = V_SRC_VIDEO
    target_video = V_TARGET_VIDEO
    print("starting generate_video...")
    # utils.del_audio_fromvideo(src_video_file) #删除视频中的音频 ，如果视频过长的话，可以导致处理时间过长
    print("after del_audio_fromvideo !")
    utils.generate_video(txt_file,src_video_file,target_video)
    print("generate_video completed !")

def composite_video():
    src_video_file = V_SRC_VIDEO
    target_video = V_TARGET_VIDEO
    utils.composite_video(src_video_file,target_video)


def convert_txt_to_audio(srctxt,target_audio):
    lst_setc,txt = utils.costruct_txt(srctxt)
    utils.convert_txt_to_mp3(txt,target_audio)

#从视频中提取语音到mp3
def extract_audio_from_videos(src_path,out_path):
    utils.extract_audio_from_videos(src_path,out_path)

#将mp3中的语音提取到文本文件
def extract_mp3_to_text_long(src_mp3_path,out_txt_file):
    utils.mp3_to_text_long(src_mp3_path,out_txt_file)

# 重定向print输出到Text控件
class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)

    def flush(self):
        pass

# 预览窗口类（增加时间选择功能）
class PreviewWindow:
    def __init__(self, parent, video_path):
        self.parent = parent
        self.video_path = video_path
        self.top = tk.Toplevel(parent.root)
        self.top.title("选择矩形区域和时间区间 - 第100帧预览")

        # 打开视频文件
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            messagebox.showerror("错误", f"无法打开视频文件: {video_path}")
            self.top.destroy()
            return

        # 获取视频属性
        self.orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = cap.get(cv2.CAP_PROP_FPS)

        if self.orig_width == 0 or self.orig_height == 0:
            messagebox.showerror("错误", f"无法获取视频分辨率: {video_path}")
            cap.release()
            self.top.destroy()
            return

        if self.fps <= 0:
            self.fps = 30  # 默认帧率
        self.total_duration = self.total_frames / self.fps  # 总时长（秒）

        # 读取第100帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, 100)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            messagebox.showerror("错误", "无法读取第100帧")
            self.top.destroy()
            return

        # 转换为RGB并调整大小
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img.thumbnail((800, 600))  # 调整大小适应窗口
        self.photo = ImageTk.PhotoImage(img)

        # 保存缩放后的宽高
        self.preview_width = img.width
        self.preview_height = img.height

        # 计算总窗口高度：预览区域 + 时间选择 + 按钮 + 边距
        padding = 50  # 上下边距
        time_frame_height = 50  # 时间选择和标签的高度
        button_height = 50  # 按钮高度
        total_height = self.preview_height + time_frame_height + button_height + padding * 3

        # 设置窗口大小，确保所有内容可见
        self.top.geometry(f"{max(self.preview_width, 800)}x{total_height}")

        # Canvas用于显示图像和绘制矩形
        self.canvas_frame = tk.Frame(self.top)
        self.canvas_frame.pack(pady=10, padx=10, fill="both")
        self.canvas = tk.Canvas(self.canvas_frame, width=self.preview_width, height=self.preview_height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

        # 矩形坐标（预览窗口坐标）
        self.start_pixel = None
        self.end_pixel = None
        self.rect_id = None

        # 时间选择界面
        time_frame = tk.Frame(self.top)
        time_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(time_frame, text="开始时间 (秒):", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.start_time = tk.DoubleVar(value=0)
        self.start_entry = tk.Entry(time_frame, textvariable=self.start_time, width=10, font=("Arial", 12))
        self.start_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(time_frame, text="结束时间 (秒):", font=("Arial", 12)).grid(row=0, column=2, padx=5, pady=5)
        self.end_time = tk.DoubleVar(value=self.total_duration)
        self.end_entry = tk.Entry(time_frame, textvariable=self.end_time, width=10, font=("Arial", 12))
        self.end_entry.grid(row=0, column=3, padx=5, pady=5)

        # 坐标显示标签（显示原始分辨率坐标）
        self.coord_label = tk.Label(self.top, text="start_pixel: None, end_pixel: None", font=("Arial", 12), wraplength=700)
        self.coord_label.pack(pady=5, padx=10)

        # 确认按钮
        self.confirm_button = tk.Button(self.top, text="确认", command=self.confirm, font=("Arial", 12), bg="#4CAF50",
                                        fg="white", width=20, padx=20)
        self.confirm_button.pack(pady=10, padx=10)

        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self.start_rect)
        self.canvas.bind("<B1-Motion>", self.update_rect)
        self.canvas.bind("<ButtonRelease-1>", self.end_rect)

    # 以下方法保持不变
    def start_rect(self, event):
        self.start_pixel = (event.x, event.y)
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(self.start_pixel[0], self.start_pixel[1], self.start_pixel[0], self.start_pixel[1], outline="red", width=2)

    def update_rect(self, event):
        if self.start_pixel and self.rect_id:
            self.canvas.coords(self.rect_id, self.start_pixel[0], self.start_pixel[1], event.x, event.y)
            self.end_pixel = (event.x, event.y)
            self.update_label()

    def end_rect(self, event):
        self.end_pixel = (event.x, event.y)
        self.update_label()

    def update_label(self):
        if self.start_pixel and self.end_pixel:
            # 计算缩放比例
            scale_x = self.orig_width / self.preview_width
            scale_y = self.orig_height / self.preview_height
            # 转换为原始分辨率坐标
            orig_start = (int(self.start_pixel[0] * scale_x), int(self.start_pixel[1] * scale_y))
            orig_end = (int(self.end_pixel[0] * scale_x), int(self.end_pixel[1] * scale_y))
            self.coord_label.config(text=f"start_pixel: {orig_start}, end_pixel: {orig_end}")

    def confirm(self):
        if self.start_pixel and self.end_pixel and self.start_time.get() < self.end_time.get():
            # 计算缩放比例并转换坐标
            scale_x = self.orig_width / self.preview_width
            scale_y = self.orig_height / self.preview_height
            self.parent.selected_start_pixel = (int(self.start_pixel[0] * scale_x), int(self.start_pixel[1] * scale_y))
            self.parent.selected_end_pixel = (int(self.end_pixel[0] * scale_x), int(self.end_pixel[1] * scale_y))
            self.parent.selected_start_time = self.start_time.get()  # 保存开始时间
            self.parent.selected_end_time = self.end_time.get()      # 保存结束时间
            self.top.destroy()
        else:
            messagebox.showwarning("警告", "请先选择有效的矩形区域和时间区间！")

# GUI类
class AudioTextExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vision Insight")
        self.root.geometry("800x700")
        self.root.configure(bg="#f0f0f0")

        main_frame = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)
        main_frame.pack(expand=True, fill="both")

        # 创建视频处理容器
        mp4_process_title = tk.Label(main_frame, text="视频提取音频和截图", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#333333")
        mp4_process_title.pack(anchor="w", pady=(0, 5))
        mp4_process_frame = tk.Frame(main_frame, bg="#f0f0f0", borderwidth=2, relief="groove")
        mp4_process_frame.pack(fill="x", pady=10)

        for i in range(10):
            mp4_process_frame.columnconfigure(i, weight=1)

        # 视频路径控件
        self.video_label = tk.Label(mp4_process_frame, text="视频路径:", font=("Arial", 12), bg="#f0f0f0", fg="#555555")
        self.video_label.grid(row=0, column=0, sticky="w", pady=5)

        self.video_path = tk.StringVar()
        self.video_entry = tk.Entry(mp4_process_frame, textvariable=self.video_path, font=("Arial", 10), relief="flat", bg="#ffffff")
        self.video_entry.grid(row=0, column=1, columnspan=8, sticky="ew", pady=5)

        self.video_button = tk.Button(mp4_process_frame, text="浏览", command=self.select_video, font=("Arial", 10), bg="#4CAF50", fg="white", relief="flat", padx=10)
        self.video_button.grid(row=0, column=9, sticky="ew", pady=5, padx=5)

        # MP3路径控件
        self.mp3_label = tk.Label(mp4_process_frame, text="MP3输出路径:", font=("Arial", 12), bg="#f0f0f0", fg="#555555")
        self.mp3_label.grid(row=1, column=0, sticky="w", pady=5)

        self.mp3_path = tk.StringVar()
        self.mp3_entry = tk.Entry(mp4_process_frame, textvariable=self.mp3_path, font=("Arial", 10), relief="flat", bg="#ffffff")
        self.mp3_entry.grid(row=1, column=1, columnspan=8, sticky="ew", pady=5)

        self.mp3_button = tk.Button(mp4_process_frame, text="浏览", command=self.select_mp3_output, font=("Arial", 10), bg="#4CAF50", fg="white", relief="flat", padx=10)
        self.mp3_button.grid(row=1, column=9, sticky="ew", pady=5, padx=5)

        # 添加预览按钮
        self.preview_button = tk.Button(mp4_process_frame, text="选择截图区域和时间", command=self.open_preview, font=("Arial", 12), bg="#FF9800", fg="white", relief="flat", padx=20, pady=5, justify="center")
        self.preview_button.grid(row=2, column=0, columnspan=3, sticky="w", pady=5)

        # 从视频提取MP3和图片按钮
        self.extract_screenshots_button = tk.Button(mp4_process_frame, text="提取截图", command=self.start_extract_screenshots,
                                              font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief="flat",
                                              padx=20, pady=5, justify="center")
        self.extract_screenshots_button.grid(row=2, column=3, columnspan=3, sticky="e", pady=5)

        self.extract_audio_button = tk.Button(mp4_process_frame, text="提取音频到MP3", command=self.start_extract_audio, font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief="flat", padx=20, pady=5, justify="center")
        self.extract_audio_button.grid(row=2, column=7, columnspan=3, sticky="e", pady=5)

        txt_process_title = tk.Label(main_frame, text="MP3提取文本", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#333333")
        txt_process_title.pack(anchor="w", pady=(0, 5))
        txt_process_frame = tk.Frame(main_frame, bg="#f0f0f0", borderwidth=2, relief="groove")
        txt_process_frame.pack(fill="x", pady=10)

        for i in range(10):
            txt_process_frame.columnconfigure(i, weight=1)

        self.mp3_input_label = tk.Label(txt_process_frame, text="MP3文件:", font=("Arial", 12), bg="#f0f0f0",
                                        fg="#555555")
        self.mp3_input_label.grid(row=4, column=0, sticky="w", pady=5)
        self.mp3_input_path = tk.StringVar()
        self.mp3_input_entry = tk.Entry(txt_process_frame, textvariable=self.mp3_input_path, width=40,
                                        font=("Arial", 10), relief="flat", bg="#ffffff")
        self.mp3_input_entry.grid(row=4, column=1, columnspan=8, sticky="ew", pady=5)
        self.mp3_input_button = tk.Button(txt_process_frame, text="浏览", command=self.select_mp3_input,
                                          font=("Arial", 10), bg="#4CAF50", fg="white", relief="flat", padx=10)
        self.mp3_input_button.grid(row=4, column=9, sticky="ew", pady=5, padx=5)

        self.txt_label = tk.Label(txt_process_frame, text="文本路径:", font=("Arial", 12), bg="#f0f0f0", fg="#555555")
        self.txt_label.grid(row=5, column=0, sticky="w", pady=5)
        self.txt_path = tk.StringVar()
        self.txt_entry = tk.Entry(txt_process_frame, textvariable=self.txt_path, width=40, font=("Arial", 10),
                                  relief="flat", bg="#ffffff")
        self.txt_entry.grid(row=5, column=1, columnspan=8, sticky="ew", pady=5)
        self.txt_button = tk.Button(txt_process_frame, text="浏览", command=self.select_txt_output, font=("Arial", 10),
                                    bg="#4CAF50", fg="white", relief="flat", padx=10)
        self.txt_button.grid(row=5, column=9, sticky="ew", pady=5, padx=5)

        self.extract_text_button = tk.Button(txt_process_frame, text="提取MP3到文本", command=self.start_extract_text,
                                             font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief="flat",
                                             padx=20, pady=5, justify="center")
        self.extract_text_button.grid(row=6, column=0, columnspan=10, sticky="ew", pady=15)

        # 进度条和日志容器
        log_process_title = tk.Label(main_frame, text="进度条和日志", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#333333")
        log_process_title.pack(anchor="w", pady=(0, 5))
        log_process_frame = tk.Frame(main_frame, bg="#f0f0f0", borderwidth=2, relief="groove")
        log_process_frame.pack(fill="x", pady=10)

        for i in range(10):
            log_process_frame.columnconfigure(i, weight=1)

        self.progress = ttk.Progressbar(log_process_frame, mode="determinate")
        self.progress.grid(row=7, column=0, columnspan=10, sticky="ew", padx=5, pady=5)
        self.progress["value"] = 0
        self.log_text = tk.Text(log_process_frame, font=("Arial", 10), relief="flat", bg="#ffffff")
        self.log_text.grid(row=8, column=0, columnspan=9, sticky="ew", padx=5, pady=5)
        scrollbar = ttk.Scrollbar(log_process_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=8, column=9, columnspan=1, sticky="ns")
        self.log_text["yscrollcommand"] = scrollbar.set
        self.log_text.config(state="normal")  # 确保Text可以被修改
        sys.stdout = TextRedirector(self.log_text)

        # 存储矩形坐标和时间区间
        self.selected_start_pixel = None
        self.selected_end_pixel = None
        self.selected_start_time = None
        self.selected_end_time = None

    def select_video(self):
        folder_path = filedialog.askdirectory(title="选择视频文件所在文件夹")
        if folder_path:
            self.video_path.set(folder_path)

    def select_mp3_output(self):
        folder_path = filedialog.askdirectory(title="选择MP3输出文件夹")
        if folder_path:
            self.mp3_path.set(folder_path)

    def select_mp3_input(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            self.mp3_input_path.set(file_path)
            txt_default = os.path.splitext(file_path)[0] + ".txt"
            self.txt_path.set(txt_default)

    def select_txt_output(self):
        folder_path = filedialog.askdirectory(title="选择MP3输出文件夹")
        if folder_path:
            self.txt_path.set(folder_path)
        # file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        # if file_path:
        #     self.txt_path.set(file_path)
    def open_preview(self):
        video_folder = self.video_path.get()
        if not video_folder:
            messagebox.showerror("错误", "请先选择视频文件夹！")
            return
        video_files = [f for f in os.listdir(video_folder) if f.endswith((".mp4", ".avi", ".mkv"))]
        if not video_files:
            messagebox.showerror("错误", "文件夹中没有视频文件！")
            return
        video_path = os.path.join(video_folder, video_files[0])
        PreviewWindow(self, video_path)

    def extract_screenshots(self):
        video_folder = self.video_path.get()
        if not video_folder or not self.selected_start_pixel or not self.selected_end_pixel or not self.selected_start_time or not self.selected_end_time:
            messagebox.showerror("错误", "请选择视频文件、截图区域和时间区间！")
            return False
        try:
            print(f"开始提取帧: 从 {video_folder}, 区域: {self.selected_start_pixel}, {self.selected_end_pixel}, 时间: {self.selected_start_time}-{self.selected_end_time} 秒")
            if self.selected_start_pixel and self.selected_end_pixel and self.selected_start_time and self.selected_end_time:
                utils.extract_frames_by_difference(video_folder, self.selected_start_pixel, self.selected_end_pixel, self.selected_start_time, self.selected_end_time)
            else:
                utils.extract_frames_by_difference(video_folder, "screenshots")
            print("截图提取完成！")
            return True
        except Exception as e:
            print(f"截图提取失败: {str(e)}")
            messagebox.showerror("错误", f"截图提取失败：{str(e)}")
            return False

        
    def update_progress(self, total_steps, interval):
        self.progress["maximum"] = total_steps
        for i in range(total_steps + 1):
            self.progress["value"] = i
            self.root.update_idletasks()
            self.log_text.see(tk.END)  # 确保日志始终滚动到最后
            time.sleep(interval)

    def extract_audio(self):
        video_folder = self.video_path.get()
        mp3_file = self.mp3_path.get()
        if not video_folder or not mp3_file:
            messagebox.showerror("错误", "请选择视频文件和MP3输出路径！")
            return False
        try:
            print(f"开始提取音频: 从 {video_folder} 到 {mp3_file}")  # 输出到日志框
            extract_audio_from_videos(video_folder, mp3_file)
            print("音频提取完成！")
            return True
        except Exception as e:
            print(f"音频提取失败: {str(e)}")
            messagebox.showerror("错误", f"音频提取失败：{str(e)}")
            return False

    def extract_text(self):
        mp3_file = self.mp3_input_path.get()
        txt_file = self.txt_path.get()
        if not mp3_file or not txt_file:
            messagebox.showerror("错误", "请选择MP3文件和文本输出路径！")
            return False
        try:
            print(f"开始提取文本: 从 {mp3_file} 到 {txt_file}")  # 输出到日志框
            extract_mp3_to_text_long(mp3_file, txt_file)
            print("文本提取完成！")
            return True
        except Exception as e:
            print(f"文本提取失败: {str(e)}")
            messagebox.showerror("错误", f"文本提取失败：{str(e)}")
            return False

    def start_extract_screenshots(self):
        self.extract_screenshots_button.config(state="disabled")
        self.progress["value"] = 0

        def run():
            success = self.extract_screenshots()
            if success:
                messagebox.showinfo("成功", "截图提取完成！")
            self.extract_screenshots_button.config(state="normal")

        threading.Thread(target=run, daemon=True).start()
        self.update_progress(total_steps=100, interval=0.05)


    def start_extract_audio(self):
        self.extract_audio_button.config(state="disabled")
        self.progress["value"] = 0
        def run():
            success = self.extract_audio()
            if success:
                messagebox.showinfo("成功", "音频提取完成！")
            self.extract_audio_button.config(state="normal")
        threading.Thread(target=run, daemon=True).start()
        self.update_progress(total_steps=100, interval=0.05)

    def start_extract_text(self):
        self.extract_text_button.config(state="disabled")
        self.progress["value"] = 0
        def run():
            success = self.extract_text()
            if success:
                messagebox.showinfo("成功", "文本提取完成！")
            self.extract_text_button.config(state="normal")
        threading.Thread(target=run, daemon=True).start()
        self.update_progress(total_steps=100, interval=0.05)

if __name__ == "__main__":
    root = tk.Tk()
    icon_path = os.path.abspath("favicon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    else:
        print(f"图标文件未找到: {icon_path}")
    app = AudioTextExtractorApp(root)
    root.mainloop()

    
    
    

