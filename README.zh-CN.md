# jetson-utils
英文版本：[`README.md`](README.md)

面向 NVIDIA Jetson 的 C++ / CUDA / Python 多媒体工具集：

| 目录 | 说明 |
|------|------|
| [`cpp/`](cpp/) | 各类系统与媒体相关工具，提供 C++ 接口 |
| [`cpp/camera/`](cpp/camera/) | 基于 GStreamer 的相机采集，支持 V4L2 和 MIPI CSI |
| [`cpp/codec/`](cpp/codec/) | 基于 GStreamer 的硬件视频编码与解码 |
| [`cpp/display/`](cpp/display/) | OpenGL 窗口与渲染功能 |
| [`cpp/image/`](cpp/image/) | 图像加载与保存 |
| [`cpp/input/`](cpp/input/) | 来自 `/dev/input` 的人机交互设备（HID） |
| [`cpp/network/`](cpp/network/) | Socket、IPv4/IPv6、WebRTC/RTSP 服务端 |
| [`cpp/parsers/`](cpp/parsers) | 文件系统、CSV/JSON/XML 解析与命令行处理 |
| [`cpp/threads/`](cpp/threads/) | 多线程、锁与事件机制 |
| [`cpp/video/`](cpp/video/) | 视频流接口 |
| [`cuda/`](cuda/) | CUDA 图像处理函数 |
| [`docs/`](docs/) | Linux 命令与相关资料链接汇总 |
| [`python/`](python/) | Python 工具、示例与 C++ 绑定 |
| [`scripts/`](scripts/) | Bash 或 Python 编写的独立脚本 |

### 文档

`jetson-utils` 的相关文档可以参考：

* [API Reference](https://github.com/dusty-nv/jetson-inference#api-reference)
* [Camera Streaming and Multimedia](https://github.com/dusty-nv/jetson-inference/blob/master/docs/aux-streaming.md)
* [Image Manipulation with CUDA](https://github.com/dusty-nv/jetson-inference/blob/master/docs/aux-image.md)

另外，一些 Linux 相关的链接、技巧和备忘内容保存在 [`docs/`](docs/) 目录下。

### 从源码构建（C++ / CUDA）

下面的步骤会构建并安装 C++ / CUDA 库 `libjetson-utils.so`，同时也会构建 Python 扩展模块：

```bash
git clone https://github.com/dusty-nv/jetson-utils
cd jetson-utils
mkdir build
cd build
cmake ../
make -j$(nproc)
sudo make install
sudo ldconfig
```

如果缺少依赖项，可以运行 [`jetson-inference/CMakePreBuild.sh`](https://github.com/dusty-nv/jetson-inference/blob/master/CMakePreBuild.sh) 脚本。

### 使用 Pip 安装（仅 Python）

下面这种方式会安装 [`python/jetson_utils`](/python/jetson_utils) 中纯 Python 的原生模块。这些模块不依赖 C++ 扩展绑定，可单独安装；如果本地同时构建了 C++ 扩展，则会叠加使用。

```bash
pip3 install -e /path/to/your/jetson-utils
```

也可以直接从 GitHub 安装：

```bash
pip3 install git+https://github.com/dusty-nv/jetson-utils
```
