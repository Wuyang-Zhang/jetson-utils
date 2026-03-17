#!/usr/bin/env python3
#
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
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

# 这是采集 + 显示。
# 它主要验证的是：摄像头能否采到、图像能否进 CUDA、能否在本地窗口显示、这条链路里，输出端一般是 glDisplay。


import sys
import argparse
from jetson_utils import videoSource, videoOutput, Log

# 作用：
#   导入 sys 模块，用来读取命令行参数，以及在需要时退出程序。
# 原理：
#   Python 启动脚本时，会把整条命令拆成一个字符串列表放进 sys.argv。
#   程序也可以通过 sys.exit() 主动结束运行。
# 关键变量 / 维度：
#   sys.argv : 1 维字符串列表，每个元素都是 1 个命令行参数。

# 作用：
#   导入 argparse 模块，用来解析命令行参数。
# 原理：
#   argparse 可以把用户在终端输入的参数，转成程序里更容易使用的变量。
# 关键变量 / 维度：
#   argparse.ArgumentParser : 参数解析器类。

# 作用：
#   导入 jetson_utils 里的视频输入、视频输出和日志接口。
# 原理：
#   videoSource 负责“读视频”，videoOutput 负责“显示/输出视频”，Log 负责打印日志。
# 关键变量 / 维度：
#   videoSource : 视频输入接口。
#   videoOutput : 视频输出接口。
#   Log         : 日志输出接口。

# 作用：
#   创建命令行解析器，定义这个脚本接受哪些参数。
# 原理：
#   用户运行脚本时输入的内容，会按照这里定义的规则被解析。
# 关键变量 / 维度：
#   description : 字符串，脚本简介。
#   epilog      : 字符串，附加帮助信息。
parser = argparse.ArgumentParser(description="View various types of video streams", 
                                 formatter_class=argparse.RawTextHelpFormatter, 
                                 epilog=videoSource.Usage() + videoOutput.Usage() + Log.Usage())

# 作用：
#   定义第 1 个位置参数 input，表示输入视频流地址。
# 原理：
#   用户必须提供这个参数，比如摄像头、视频文件、RTSP 地址等。
# 关键变量 / 维度：
#   input : 1 个字符串，表示输入 URI。
parser.add_argument("input", type=str, help="URI of the input stream")

# 作用：
#   定义第 2 个位置参数 output，表示输出目标地址。
# 原理：
#   这个参数是可选的；如果不写，通常会使用默认显示窗口。
# 关键变量 / 维度：
#   output : 1 个字符串，表示输出 URI。
#   default="" : 空字符串，表示没有显式指定输出地址。
parser.add_argument("output", type=str, default="", nargs='?', help="URI of the output stream")

# 作用：
#   尝试解析用户输入的命令行参数。
# 原理：
#   parse_known_args() 会返回两个结果：
#   第 1 个是已识别参数，第 2 个是未识别参数。
#   这里只取第 1 个，是为了让底层库继续处理其余参数。
# 关键变量 / 维度：
#   args : Namespace 对象，保存解析后的参数值。
try:
	args = parser.parse_known_args()[0]
except:
	# 作用：
	#   参数解析失败时先输出一个空行，让帮助信息更清晰。
	# 原理：
	#   print("") 只会输出换行。
	# 关键变量 / 维度：
	#   "" : 空字符串，长度为 0。
	print("")

	# 作用：
	#   打印帮助说明，告诉用户这个脚本应该怎么运行。
	# 原理：
	#   print_help() 会把上面定义的参数格式显示出来。
	# 关键变量 / 维度：
	#   parser : 当前参数解析器对象。
	parser.print_help()

	# 作用：
	#   正常结束程序。
	# 原理：
	#   sys.exit(0) 会立刻退出脚本，0 表示正常退出。
	# 关键变量 / 维度：
	#   0 : 标量整数，表示退出码。
	sys.exit(0)

# 作用：
#   创建视频输入对象，用来从输入源中不断取出一帧一帧的图像。
# 原理：
#   videoSource 会根据 args.input 的内容自动选择后端，
#   比如摄像头、视频文件、网络流等。
#   argv=sys.argv 的意思是：把整条命令行也传给底层库继续解析。
# 关键变量 / 维度：
#   args.input : 1 个字符串，表示输入地址。
#   argv       : 1 维字符串列表，保存完整命令行参数。
#   input      : 视频输入对象。
input = videoSource(args.input, argv=sys.argv)    # 默认可能使用类似 1280x720、30FPS 这样的输入配置

# 作用：
#   创建视频输出对象，用来显示图像或把图像送到输出目标。
# 原理：
#   如果 output 是窗口，就会显示画面；
#   如果 output 是文件或流地址，就会写出视频。
#   同样，argv=sys.argv 也会把命令行参数继续传给底层输出模块。
# 关键变量 / 维度：
#   args.output : 1 个字符串，表示输出地址。
#   output      : 视频输出对象。
output = videoOutput(args.output, argv=sys.argv)  # 默认可能使用类似 1280x720、30FPS 这样的输出配置

# 作用：
#   记录已经处理了多少帧图像。
# 原理：
#   每成功处理 1 帧，就把这个计数加 1。
#   这个值主要用于打印日志和观察程序运行状态。
# 关键变量 / 维度：
#   numFrames : 标量整数，表示累计帧数。
numFrames = 0

# 作用：
#   主循环，不停读取图像、显示图像，直到输入结束或用户退出。
# 原理：
#   视频本质上就是一连串连续的图像帧，所以这里每次循环处理 1 帧。
# 关键变量 / 维度：
#   循环次数 : 通常接近视频帧数，或者接近每秒几十次。
while True:
    # 作用：
    #   从输入源抓取下一帧图像。
    # 原理：
    #   input.Capture() 会尝试拿到“下一张图”。
    #   如果成功，img 就是一个图像对象；如果暂时拿不到，可能返回 None。
    # 关键变量 / 维度：
    #   img : 图像对象，通常包含宽、高、像素数据等信息。
    img = input.Capture()

    # 作用： 判断这次抓帧有没有成功。
    # 原理：如果 img 是 None，通常表示超时或这一刻没有拿到新帧。 这种情况下跳过后续处理，直接继续下一轮循环。
    # 关键变量 / 维度： img is None : 布尔条件。
    if img is None: # 超时或暂时没有新帧
        continue  
        
    # 作用：
    #   定期打印日志，告诉你已经抓到了多少帧，以及图像大小是多少。
    # 原理：
    #   前 15 帧会连续打印，方便观察程序刚启动时的状态；
    #   之后改成每 25 帧打印一次，避免日志太多。
    # 关键变量 / 维度：
    #   numFrames  : 标量整数，当前帧计数。
    #   img.width  : 标量整数，图像宽度，单位像素。
    #   img.height : 标量整数，图像高度，单位像素。
    if numFrames % 25 == 0 or numFrames < 15:
        Log.Verbose(f"video-viewer:  captured {numFrames} frames ({img.width} x {img.height})")
	
    # 作用：
    #   帧计数加 1，表示这帧已经成功拿到了。
    # 原理：
    #   numFrames += 1 是 Python 里的“自增”写法。
    # 关键变量 / 维度：
    #   numFrames : 标量整数。
    numFrames += 1
	
    # 作用： 把当前图像交给输出端进行显示或写出。
    # 原理：output.Render(img) 可以理解成“把这一帧画出来”。
    # 关键变量 / 维度： img : 当前帧图像对象。
    output.Render(img)
    
    # 作用：
    #   更新窗口标题栏状态文字。
    # 原理：
    #   这里会把当前分辨率和 FPS 显示出来，方便观察运行情况。
    # 关键变量 / 维度：
    #   img.width            : 标量整数，图像宽度。
    #   img.height           : 标量整数，图像高度。
    #   output.GetFrameRate(): 标量浮点数，当前输出帧率。
    output.SetStatus("Video Viewer | {:d}x{:d} | {:.1f} FPS".format(img.width, img.height, output.GetFrameRate()))
	
    # 作用：
    #   检查输入流或输出流是否已经结束。
    # 原理：
    #   只要输入端或输出端任意一边停止工作，就退出循环。
    #   这样程序不会在流结束后继续空转。
    # 关键变量 / 维度：
    #   input.IsStreaming()  : 布尔值，输入是否还在工作。
    #   output.IsStreaming() : 布尔值，输出是否还在工作。
    if not input.IsStreaming() or not output.IsStreaming():
        # 作用：
        #   跳出循环，结束整个脚本。
        # 原理：
        #   break 会立刻终止当前 while True 循环。
        # 关键变量 / 维度：
        #   无新增变量，只改变程序执行流程。
        break

