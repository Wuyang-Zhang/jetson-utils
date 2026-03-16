/*
 * Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 */
 
#include "videoSource.h"
#include "imageLoader.h"

#include "gstCamera.h"
#include "gstDecoder.h"

#include "logging.h"


/*
 * 作用：
 *   初始化所有 videoSource 后端共享的基础状态。
 *
 * 原则：
 *   这个构造函数不会打开设备，也不会分配帧缓冲。
 *   它只负责设置确定性的默认值，具体后端相关的初始化由派生类在
 *   Open()/Capture() 期间稍后完成。
 *
 * 关键变量 / 维度：
 *   options        : videoOptions 结构体，包含流元数据和配置。
 *   mStreaming     : 标量 bool，表示流是否已打开的状态标志。
 *   mLastTimestamp : 标量 uint64_t，单位为纳秒的时间戳。
 *   mRawFormat     : 标量枚举，表示原始像素格式。
 */
// 构造函数
videoSource::videoSource( const videoOptions& options ) : mOptions(options)
{
	mStreaming = false;
	mLastTimestamp = 0;
	mRawFormat = IMAGE_UNKNOWN;
}


/*
 * 作用：
 *   为通过 videoSource 指针进行多态清理提供基类析构函数。
 *
 * 原则：
 *   基类本身在这个编译单元中不持有需要显式释放的资源。
 *   各后端特定的释放逻辑放在派生类析构函数中实现。
 */
// 析构函数
videoSource::~videoSource()
{

}

/*
 * 作用：
 *   工厂入口，根据解析后的 URI 选择具体的输入后端。
 *
 * 原则：
 *   分发逻辑由协议驱动：
 *   - file    -> 如果是受支持的视频容器/编码格式则选择 gstDecoder，否则选择 imageLoader
 *   - rtp/... -> 选择 gstDecoder，因为网络流需要解码管线
 *   - csi/v4l2-> 选择 gstCamera，因为来源是采集设备
 *   这样可以让上层只依赖抽象的 videoSource API。
 *
 * 关键变量 / 维度：
 *   src          : 标量指针，指向选中的后端实例；失败时为 NULL。
 *   uri          : URI 结构体，表示解析后的资源描述符。
 *   uri.protocol : 单个字符串标记，表示传输方式或后端类别。
 *   uri.extension: 单个字符串标记，表示磁盘资源的文件扩展名。
 */
// 创建实例
videoSource* videoSource::Create( const videoOptions& options )
{
	videoSource* src = NULL;
	
	const URI& uri = options.resource;

	if( uri.protocol == "file" )
	{
		if( gstDecoder::IsSupportedExtension(uri.extension.c_str()) )
			src = gstDecoder::Create(options);
		else
			src = imageLoader::Create(options);
	}
	else if( uri.protocol == "rtp" || uri.protocol == "rtsp" || uri.protocol == "webrtc" )
	{
		src = gstDecoder::Create(options);
	}
	else if( uri.protocol == "csi" || uri.protocol == "v4l2" )
	{
		src = gstCamera::Create(options);
	}
	else
	{
		LogError(LOG_VIDEO "videoSource -- unsupported protocol (%s)\n", uri.protocol.size() > 0 ? uri.protocol.c_str() : "null");
	}

	if( !src )
		return NULL;

	LogSuccess(LOG_VIDEO "created %s from %s\n", src->TypeToStr(), src->GetResource().string.c_str());
	src->GetOptions().Print(src->TypeToStr());
	return src;
}

/*
 * 作用：
 *   便捷重载，把资源字符串和命令行参数合并成完整的 videoOptions 对象。
 *
 * 原则：
 *   Parse() 会把 CLI 和资源输入统一整理成一个配置对象，再由上面的
 *   主工厂函数完成后端选择。这样所有创建路径都会收敛到同一套分发实现。
 *
 * 关键变量 / 维度：
 *   opt         : videoOptions 结构体副本，可修改的本地配置。
 *   resource    : C 字符串句柄，表示用户提供的 URI 或路径。
 *   positionArg : 标量 int，资源在 argv 中的位置索引。
 */
// 创建实例
videoSource* videoSource::Create( const char* resource, const commandLine& cmdLine, int positionArg, const videoOptions& options )
{
	videoOptions opt = options;

	if( !opt.Parse(resource, cmdLine, videoOptions::INPUT, positionArg) )
	{
		LogError(LOG_VIDEO "videoSource -- failed to parse command line options\n");
		return NULL;
	}

	return Create(opt);
}

/*
 * 作用：
 *   为直接传入原始 argc/argv 的调用方提供适配重载。
 *
 * 原则：
 *   先把 argc/argv 包装成 commandLine，再复用上面的重载，避免重复解析逻辑。
 */
// 创建实例
videoSource* videoSource::Create( const char* resource, const int argc, char** argv, int positionArg, const videoOptions& options )
{
	return Create(resource, commandLine(argc, argv), positionArg, options);
}

/*
 * 作用：
 *   当资源仅来自命令行参数时提供简化创建入口。
 *
 * 原则：
 *   传入 NULL 资源字符串，让 Parse() 从 cmdLine 中解析 URI。
 */
// 创建实例
videoSource* videoSource::Create( const commandLine& cmdLine, int positionArg )
{
	return Create(NULL, cmdLine, positionArg);
}

/*
 * 作用：
 *   为基于命令行驱动的 source 创建提供原始 argc/argv 的快捷入口。
 *
 * 原则：
 *   把 argc/argv 转成 commandLine，然后转发到共享重载。
 */
// 创建实例
videoSource* videoSource::Create( const int argc, char** argv, int positionArg )
{
	return Create(commandLine(argc, argv), positionArg);
}

/*
 * 作用：
 *   为已经有资源字符串和可选默认 videoOptions、但没有 argv 上下文的调用方
 *   提供快捷入口。
 *
 * 原则：
 *   使用空参数列表转发到 argc/argv 重载，这样所有创建路径仍然会收敛到
 *   同一套解析和工厂流程。
 */
// 创建实例
videoSource* videoSource::Create( const char* resource, const videoOptions& options )
{
	return Create(resource, 0, NULL, -1, options);
}

/*
 * 作用：
 *   将抽象流标记为活动状态。
 *
 * 原则：
 *   基类实现只切换共享状态位。派生类可以在调用基类实现之前或之后，
 *   扩展为实际的设备启动或管线启动逻辑。
 *
 * 关键变量 / 维度：
 *   mStreaming : 标量 bool，true 表示该 source 被认为处于打开状态。
 */
// 打开
bool videoSource::Open()
{
	mStreaming = true;
	return true;
}

/*
 * 作用：
 *   将抽象流标记为非活动状态。
 *
 * 原则：
 *   基类实现只更新共享状态标志。具体后端负责按需停止相机采集、
 *   解码管线或文件迭代。
 *
 * 关键变量 / 维度：
 *   mStreaming : 标量 bool，false 表示已关闭或到达 EOS。
 */
// 关闭
void videoSource::Close()
{
	mStreaming = false;
}

/*
 * 作用：
 *   把后端类型 ID 转换成人类可读的类名。
 *
 * 原则：
 *   这是一个运行时的小型类型映射，用于日志和诊断。
 *   输入的 type 是具体后端通过 GetType() 返回的标量标签值。
 *
 * 关键变量 / 维度：
 *   type : 标量 uint32_t 后端标签，会与 gstCamera/gstDecoder/
 *          imageLoader 的静态 Type 常量比较。
 */
// 类型转字符串
const char* videoSource::TypeToStr( uint32_t type )
{
	if( type == gstCamera::Type )
		return "gstCamera";
	else if( type == gstDecoder::Type )
		return "gstDecoder";
	else if( type == imageLoader::Type )
		return "imageLoader";

	return "(unknown)";
}


