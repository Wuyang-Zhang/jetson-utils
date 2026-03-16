#!/usr/bin/env python3
#
# Copyright (c) 2023, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

# 作用：
#   导入 sys 模块，用于读取当前进程的命令行参数，以及在必要时退出程序。
# 原理：
#   sys.argv 保存启动脚本时的原始参数列表，sys.exit() 可直接结束当前进程。
# 关键变量 / 维度：
#   sys.argv : Python 列表，维度为 1 维，元素类型为字符串。
import sys

# 作用：
#   导入 argparse 模块，用于定义和解析命令行参数。
# 原理：
#   argparse 通过 ArgumentParser 对象声明参数规则，再把命令行文本转换成结构化结果。
# 关键变量 / 维度：
#   argparse.ArgumentParser : 解析器类，负责命令行接口定义。
import argparse

# 作用：
#   从 jetson_utils 中导入视频输入、视频输出和日志接口。
# 原理：
#   videoSource 负责采集或解码输入流，videoOutput 负责显示或编码输出，Log 用于统一日志输出。
# 关键变量 / 维度：
#   videoSource : 类/工厂接口，输出逐帧图像对象。
#   videoOutput : 类/工厂接口，接收逐帧图像对象并渲染或写出。
#   Log         : 日志接口，输出调试和运行状态信息。
from jetson_utils import videoSource, videoOutput, Log

# 作用：
#   创建命令行解析器，定义这个脚本的帮助信息和参数格式。
# 原理：
#   ArgumentParser 会根据 description、formatter_class 和 epilog 生成帮助文本，
#   同时负责后续的命令行解析。
# 关键变量 / 维度：
#   description     : 字符串，脚本功能简介。
#   formatter_class : 类对象，控制帮助文本格式。
#   epilog          : 字符串，追加到帮助文本末尾的扩展说明。
parser = argparse.ArgumentParser(description="Test various video streaming APIs", 
                                 formatter_class=argparse.RawTextHelpFormatter, 
                                 epilog=videoSource.Usage() + videoOutput.Usage() + Log.Usage())

# 作用：
#   定义位置参数 input，表示输入视频流的 URI。
# 原理：
#   nargs='?' 表示该参数可选；如果用户未提供，则使用 default 默认值。
# 关键变量 / 维度：
#   "input"        : 参数名，字符串。
#   type=str       : 解析后数据类型为字符串。
#   default        : 默认输入 URI，这里是 1 个字符串路径。
#   help           : 帮助信息字符串。
parser.add_argument("input", type=str, default="/dev/video0", nargs='?', help="URI of the input stream")

# 作用：
#   定义位置参数 output，表示输出视频流或输出文件的 URI。
# 原理：
#   与 input 一样，该参数也是可选位置参数，未提供时使用默认输出路径。
# 关键变量 / 维度：
#   "output"       : 参数名，字符串。
#   type=str       : 解析后数据类型为字符串。
#   default        : 默认输出 URI，这里是 1 个字符串路径。
#   help           : 帮助信息字符串。
parser.add_argument("output", type=str, default="images/test/test_video.mp4", nargs='?', help="URI of the output stream")

# 作用：
#   尝试解析命令行参数，得到脚本运行所需的输入输出配置。
# 原理：
#   parse_known_args() 会返回一个二元结果：
#   第 1 项是已识别参数对象，第 2 项是未识别参数列表。
#   这里只取第 1 项，因为底层库也可能消费额外参数。
# 关键变量 / 维度：
#   args : Namespace 对象，包含 input/output 等解析结果。
try:
	args = parser.parse_known_args()[0]
except:
	# 作用：
	#   如果解析失败，则先输出一个空行，让帮助文本显示得更清晰。
	# 原理：
	#   print("") 仅输出换行，不携带其他内容。
	# 关键变量 / 维度：
	#   "" : 空字符串，长度为 0。
	print("")

	# 作用：
	#   打印命令行帮助，告诉用户可用参数和默认值。
	# 原理：
	#   print_help() 会输出解析器中已经注册的参数定义。
	# 关键变量 / 维度：
	#   parser : ArgumentParser 实例。
	parser.print_help()

	# 作用：
	#   结束程序，退出码为 0。
	# 原理：
	#   sys.exit(0) 会抛出 SystemExit，并以成功状态终止脚本。
	# 关键变量 / 维度：
	#   0 : 标量整数，表示正常退出。
	sys.exit(0)
    
    
# 作用：
#   创建视频输入对象，用于从摄像头、文件或流媒体中持续获取图像帧。
# 原理：
#   videoSource 会根据 args.input 和 argv 中的参数自动选择后端，
#   例如 V4L2、GStreamer 解码器或其他支持的输入协议。
# 关键变量 / 维度：
#   args.input : 字符串，1 个输入 URI。
#   argv       : 1 维字符串列表，保存完整命令行参数。
#   options    : Python 字典，包含输入流配置项。
input = videoSource(args.input, 
                    argv=sys.argv,
                    options={
                        # 作用：
                        #   指定输入图像的目标宽度。
                        # 原理：
                        #   某些输入后端会尝试按该宽度协商采集或解码输出尺寸。
                        # 关键变量 / 维度：
                        #   width : 标量整数，单位为像素。
                        'width': 1920,
                        # 作用：
                        #   指定输入图像的目标高度。
                        # 原理：
                        #   与 width 一起定义期望的视频分辨率。
                        # 关键变量 / 维度：
                        #   height : 标量整数，单位为像素。
                        'height': 1080,
                        # 作用：
                        #   指定输入流期望的帧率。
                        # 原理：
                        #   输入后端会尽量按该帧率进行采集或时间协商。
                        # 关键变量 / 维度：
                        #   framerate : 标量整数，单位为 FPS。
                        'framerate': 30, 
                    })
           
# 作用：
#   创建视频输出对象，用于显示采集到的图像，或将图像编码到输出文件/流。
# 原理：
#   videoOutput 会根据 args.output 的 URI 类型选择显示窗口、编码器或流输出后端。
# 关键变量 / 维度：
#   args.output : 字符串，1 个输出 URI。
#   argv        : 1 维字符串列表，保存完整命令行参数。
#   options     : Python 字典，包含编码与输出配置项。
output = videoOutput(args.output,
                     argv=sys.argv,
                     options={
                        # 作用：
                        #   指定编码输出时的目标码率。
                        # 原理：
                        #   码率越高，通常画质越好，但文件体积或带宽占用也更高。
                        # 关键变量 / 维度：
                        #   bitrate : 标量整数，单位为 bit/s。
                        'bitrate': 2500000,
                        # 作用：
                        #   指定输出视频编码格式。
                        # 原理：
                        #   编码器会根据 codec 名称选择对应的压缩算法。
                        # 关键变量 / 维度：
                        #   codec : 字符串，这里为 'h264'。
                        'codec': 'h264'
                     })
                     
# 作用：
#   初始化已处理帧计数器。
# 原理：
#   每成功拿到并处理一帧图像，就把计数加 1，用于日志节流和运行统计。
# 关键变量 / 维度：
#   numFrames : 标量整数，表示累计处理的帧数。
numFrames = 0

# 作用：
#   持续循环采集和输出视频帧，直到输入结束、输出结束或用户主动退出。
# 原理：
#   while True 形成主处理循环，每轮完成一次“采集 -> 日志 -> 渲染 -> 状态更新 -> 退出判断”。
# 关键变量 / 维度：
#   循环频率 : 近似与输入帧率一致，通常为每秒数十次。
while True:
    # 作用：
    #   从输入源抓取下一帧图像。
    # 原理：
    #   Capture() 通常会阻塞直到拿到新帧、超时或流结束，然后返回图像对象或 None。
    # 关键变量 / 维度：
    #   img : 图像对象；若成功，包含 width/height/pixel data；失败或超时可能为 None。
    img = input.Capture()

    # 作用：判断当前抓帧是否超时或暂时没有可用图像。
    # 原理：当 Capture() 返回 None 时，不进行后续渲染，直接进入下一轮轮询。
    # 关键变量 / 维度：
    #   img is None : 布尔条件，标记本轮是否拿到有效帧。
    if img is None: # timeout
        # 作用： 跳过本轮剩余逻辑，继续等待下一帧。
        # 原理：continue 会立即进入 while 的下一次迭代。
        # 关键变量 / 维度： 无新增变量；控制流直接回到循环起点。
        continue  
        
    # 作用：
    #   以较低频率输出调试日志，同时在前 15 帧内连续输出，便于启动阶段观察状态。
    # 原理：
    #   numFrames % 25 == 0 控制每 25 帧打印一次；
    #   numFrames < 15 保证刚开始时前 15 帧都可见。
    # 关键变量 / 维度：
    #   numFrames : 标量整数，当前已完成帧计数。
    #   25        : 日志采样周期，单位为帧。
    #   15        : 启动阶段连续日志阈值，单位为帧。
    if numFrames % 25 == 0 or numFrames < 15:
        # 作用：
        #   输出当前帧计数和图像尺寸，方便确认采集状态是否正常。
        # 原理：
        #   f-string 会把 numFrames、img.width 和 img.height 格式化到日志字符串中。
        # 关键变量 / 维度：
        #   img.width  : 标量整数，图像宽度，单位像素。
        #   img.height : 标量整数，图像高度，单位像素。
        Log.Verbose(f"test-video:  captured {numFrames} frames ({img.width} x {img.height})")
	
    # 作用：
    #   将已处理帧数加 1。
    # 原理：
    #   这表示当前帧已经通过了有效性判断，并将进入输出阶段。
    # 关键变量 / 维度：
    #   numFrames : 标量整数，执行后自增 1。
    numFrames += 1
	
    # 作用：把当前图像发送到输出端进行显示或编码写出。
    # 原理：Render() 会依据 output 后端类型执行窗口显示、视频编码或网络发送。
    # 关键变量 / 维度：img : 当前帧图像对象，通常是 2 维图像数据加元信息。
    output.Render(img)
    
    # 作用：
    #   更新输出窗口或输出端的状态字符串。
    # 原理：
    #   SetStatus() 通常会刷新标题栏或运行状态信息，展示分辨率和当前输出帧率。
    # 关键变量 / 维度：
    #   img.width            : 标量整数，当前帧宽度。
    #   img.height           : 标量整数，当前帧高度。
    #   output.GetFrameRate(): 标量浮点数，当前输出端统计帧率，单位 FPS。
    output.SetStatus("Video Test | {:d}x{:d} | {:.1f} FPS".format(img.width, img.height, output.GetFrameRate()))
	
    # 作用：
    #   检查输入端或输出端是否已经结束流，若结束则退出主循环。
    # 原理：
    #   只要任一端不再处于 streaming 状态，就说明继续处理已经没有意义。
    # 关键变量 / 维度：
    #   input.IsStreaming()  : 布尔值，表示输入流是否仍在工作。
    #   output.IsStreaming() : 布尔值，表示输出流是否仍在工作。
    if not input.IsStreaming() or not output.IsStreaming():
        # 作用：
        #   跳出无限循环，结束脚本的主处理流程。
        # 原理： break 会终止当前 while True 循环，程序随后自然执行到文件末尾退出。
        # 关键变量 / 维度：无新增变量；只改变控制流。
        break

