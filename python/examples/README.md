# Python Examples

这个目录放的是 `jetson-utils` 的 Python 示例脚本，主要分成 3 类：

- 视频输入输出：摄像头、视频文件、窗口显示、视频编码输出
- CUDA 图像与数组互操作：`cudaImage` 和 NumPy / OpenCV / PyTorch 之间互相转换
- 基础能力测试：日志、OpenGL 显示、CUDA stream

如果你是初学者，建议先看下面这几个文件：

1. [`video-viewer.py`](video-viewer.py)：最容易理解，输入视频并显示出来
2. [`test-video.py`](test-video.py)：输入视频再编码输出到文件
3. [`test-display.py`](test-display.py)：只看窗口显示，不涉及视频采集
4. [`cuda-examples.py`](cuda-examples.py)：看常见 CUDA 图像处理操作
5. [`cuda-to-numpy.py`](cuda-to-numpy.py) / [`cuda-from-numpy.py`](cuda-from-numpy.py)：理解 Python 数组和 CUDA 图像怎么互转

## 文件逐个说明

### 视频相关

#### [`video-viewer.py`](video-viewer.py)

作用：
从输入源读取视频帧，然后直接显示到窗口或输出端。

你可以把它理解成：
“打开一个视频输入，再一帧一帧地显示出来。”

适合看什么：

- `videoSource()` 怎么创建输入
- `videoOutput()` 怎么创建输出
- `Capture()` / `Render()` 这套最基础的视频处理循环
- 如何用 `SetStatus()` 在窗口标题栏显示 FPS

适合人群：
刚开始接触 `jetson-utils` 视频接口的人。

#### [`test-video.py`](test-video.py)

作用：
从输入源采集视频，并把结果输出到另一个视频目标，通常是编码成视频文件。

你可以把它理解成：
“读进来的视频，再保存/编码出去。”

和 `video-viewer.py` 的区别：

- `video-viewer.py` 偏向“看画面”
- `test-video.py` 偏向“采集 + 编码输出”

适合看什么：

- `options={...}` 方式如何给输入/输出传固定参数
- 输入分辨率、帧率、编码格式、码率这些参数怎么设置
- 视频采集与输出链路的完整最小例子

#### [`cuda-streams.py`](cuda-streams.py)

作用：
演示如何使用多个 CUDA stream 做异步处理和同步。

你可以把它理解成：
“同一块 GPU 上开多条工作队列，让数据拷贝、缩放、视频输入输出在不同 stream 上协作。”

这个脚本分两部分：

- 前半部分：加载一张图片，放到 CUDA stream 上做 `cudaResize()` 再保存
- 后半部分：如果提供视频输入输出参数，就演示视频帧在不同 CUDA stream 间同步

适合看什么：

- `cudaStreamCreate()` / `cudaStreamWaitEvent()`
- `cudaEventRecord()`
- 为什么视频输入和视频输出有时要用不同 stream

适合人群：
已经知道基础视频流程，想理解异步 CUDA 执行的人。

### CUDA 图像处理相关

#### [`cuda-examples.py`](cuda-examples.py)

作用：
演示一些常见的 CUDA 图像处理操作。

里面主要做了这些事：

- 加载图片
- 复制图片
- 转灰度
- 裁剪
- 缩放
- 转回彩色
- 画圆、画线、画矩形
- 保存结果

适合看什么：

- `loadImage()` / `saveImage()`
- `cudaConvertColor()`
- `cudaCrop()`
- `cudaResize()`
- `cudaDrawCircle()` / `cudaDrawLine()` / `cudaDrawRect()`

适合人群：
想快速知道 `jetson-utils` 能对图像做哪些基础 CUDA 操作的人。

#### [`cuda-array-interface.py`](cuda-array-interface.py)

作用：
演示 `cudaImage` 的 `__cuda_array_interface__` / 数组接口兼容能力。

它会：

- 分配一块 CUDA 图像内存
- 按规律填充数据
- 分别用 NumPy、CuPy、Numba、PyCUDA 测试加法操作

这个文件的重点不是“图像显示”，而是：
“`jetson-utils` 的 CUDA 图像数据，能不能被别的 Python GPU 生态直接拿来用。”

适合看什么：

- `cudaAllocMapped()`
- `__cuda_array_interface__`
- 第三方 GPU 库和 `jetson-utils` 之间的数据互通

适合人群：
要把 `jetson-utils` 和其他 Python GPU 工具链混用的人。

### CUDA 和 NumPy/OpenCV/PyTorch 互转

#### [`cuda-from-numpy.py`](cuda-from-numpy.py)

作用：
把 NumPy 数组拷贝到 CUDA 图像内存，再保存成图片。

你可以把它理解成：
“先在 CPU 里用 NumPy 生成图，再送到 GPU 侧。”

适合看什么：

- `cudaFromNumpy()`
- NumPy 数组形状 `(height, width, channels)` 和图像的关系
- 不同通道数和数据类型对图像输出的影响

#### [`cuda-to-numpy.py`](cuda-to-numpy.py)

作用：
把 CUDA 图像映射成 NumPy 数组。

你可以把它理解成：
“GPU 图像数据，怎样在 Python 里按数组方式看和算。”

适合看什么：

- `cudaImage(...)`
- `cudaToNumpy()`
- `cudaImage` 和 NumPy 共享数据时的表现

和 `cuda-from-numpy.py` 的区别：

- `cuda-from-numpy.py` 是 CPU 数组 -> CUDA
- `cuda-to-numpy.py` 是 CUDA -> NumPy 视图/映射

#### [`cuda-from-cv.py`](cuda-from-cv.py)

作用：
把 OpenCV 读出来的图像转换成 CUDA 图像。

这个脚本强调的重点是：
OpenCV 默认是 `BGR` 排列，而很多图像处理逻辑更常用 `RGB`。

里面主要做了这些事：

- `cv2.imread()` 读图
- 用 `cudaFromNumpy()` 把 OpenCV 图像送到 CUDA
- 用 `cudaConvertColor()` 把 BGR 转成 RGB
- 保存结果

适合看什么：

- OpenCV 图像和 CUDA 图像之间的桥接
- `isBGR=True` 的用途

#### [`cuda-to-cv.py`](cuda-to-cv.py)

作用：
把 CUDA 图像转成 OpenCV 图像，再用 OpenCV 保存。

里面主要做了这些事：

- `loadImage()` 读入 CUDA 图像
- 转成 OpenCV 更常用的 `bgr8`
- `cudaDeviceSynchronize()` 等 GPU 完成
- `cudaToNumpy()` 映射成 OpenCV/NumPy 数组
- `cv2.imwrite()` 保存

适合看什么：

- CUDA -> OpenCV 的数据流
- 为什么转给 OpenCV 前往往要先做颜色通道转换

#### [`cuda-to-pytorch.py`](cuda-to-pytorch.py)

作用：
把 `cudaImage` 映射成 PyTorch GPU tensor。

重点是：
这里通常不是“复制一份数据”，而是“共享同一块 GPU 内存”。

里面主要做了这些事：

- 创建 `cudaImage`
- 用 `torch.as_tensor(cuda_img, device='cuda')` 生成 tensor
- 修改 tensor
- 再检查 `cudaImage` 是否同步变化

适合看什么：

- `__cuda_array_interface__` 和 PyTorch 的互通
- “零拷贝/共享内存视图” 这种概念

#### [`cuda-from-pytorch.py`](cuda-from-pytorch.py)

作用：
把 PyTorch 的 GPU tensor 反向映射成 `cudaImage`。

里面主要做了这些事：

- 先创建一个 GPU tensor
- 调整成适合图像的内存布局
- 根据 tensor 推断图像格式
- 用同一块 GPU 内存构造 `cudaImage`
- 再对 `cudaImage` 做归一化，看 tensor 是否同步变化

适合看什么：

- `tensor.data_ptr()` 的作用
- `cudaImage(ptr=..., width=..., height=..., format=...)`
- tensor 和 `cudaImage` 共用同一块显存的效果

### 基础测试脚本

#### [`test-display.py`](test-display.py)

作用：
测试 OpenGL 显示窗口是否能正常创建和刷新。

你可以把它理解成：
“只开一个窗口，不处理视频，也不处理图片。”

适合看什么：

- `glDisplay` 怎么创建
- 窗口标题、窗口大小、全屏、最大化怎么设置
- `BeginRender()` / `EndRender()` 的基础渲染循环

适合人群：
想先确认本机显示环境没问题的人。

#### [`test-logging.py`](test-logging.py)

作用：
测试 `jetson-utils` 的日志系统。

里面主要做了这些事：

- 打印不同级别日志：`Error`、`Warning`、`Info`、`Verbose`、`Debug`
- 动态切换日志级别
- 观察哪些日志会显示，哪些会被过滤

适合看什么：

- `Log.SetLevel()`
- `Log.GetLevel()`
- 不同日志级别的区别

#### [`test-cuda.sh`](test-cuda.sh)

作用：
这是一个批处理脚本，用来顺序运行多个 CUDA 相关 Python 示例。

它不是教学脚本，而是“快速回归测试脚本”。

里面做的事情很简单：

- 依次执行 NumPy / OpenCV / PyTorch / CUDA stream 这些示例
- 一旦某个命令失败，脚本就停止

适合什么时候用：

- 你改了底层 CUDA / Python 绑定后，想快速跑一遍示例检查有没有坏
- 你想一次性验证多个示例是否都还能运行

## 一个简单的理解方式

如果只从“数据流”角度看，这个目录基本可以理解成：

- `video-viewer.py` / `test-video.py`
  处理“视频流”
- `cuda-examples.py`
  处理“CUDA 图像操作”
- `cuda-from-*`
  把别的库的数据送进 `jetson-utils`
- `cuda-to-*`
  把 `jetson-utils` 的数据送给别的库
- `test-display.py` / `test-logging.py`
  测基础设施
- `cuda-streams.py`
  测更底层的异步执行机制

## 运行前提示

这些示例大多依赖已经正确安装并可用的 `jetson-utils` Python 绑定。部分脚本还有额外依赖：

- OpenCV 相关：需要 `cv2`
- PyTorch 相关：需要 `torch`
- CuPy / Numba / PyCUDA 相关：需要对应第三方包

如果你只是想先跑最基础的示例，优先试：

```bash
python3 video-viewer.py /dev/video0
python3 test-display.py
python3 test-logging.py
```
