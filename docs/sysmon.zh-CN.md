# System Monitoring

英文版本：[`sysmon.md`](sysmon.md)

一些系统监控、日志查看和状态汇报工具，类似于增强版 `top`，可以显示更多系统信息或利用率指标。

```
sudo apt install -y \
    nvtop htop ctop \
    bmon tcptrack iftop \
    tmux terminator screen
```

#### nvidia-smi

`nvidia-smi` 随 JetPack 6 提供，但可用字段相对有限。

```
watch -n 1 nvidia-smi -l 1
nvidia-smi pmon -i 0
```

#### btop（带 GPU 支持）

下面这套方法是 x86 上使用的方式（Jetson 上尚未验证）

```
git clone https://github.com/aristocratos/btop

docker run --gpus all -it --rm \
  -v $PWD/btop:/btop \
  --workdir /btop \
  nvcr.io/nvidia/pytorch:24.10-py3 \
    make

sudo chown $USER btop/bin/btop && \
sudo chmod +x btop/bin/btop && \
sudo cp btop/bin/btop /usr/local/bin
```

#### ctop

* https://github.com/bcicen/ctop
* https://github.com/jesseduffield/lazydocker

```
sudo wget https://github.com/bcicen/ctop/releases/download/v0.7.7/ctop-0.7.7-linux-amd64 -O /usr/local/bin/ctop
sudo chmod +x /usr/local/bin/ctop
```

#### tmux

jetson-utils 自带的 [`tmux-run`](/scripts/tmux-run) 可以通过 tmux / terminator，将给定命令并行启动到各自的终端面板中：

```
tmux-run 'htop' 'nvtop' 'bmon' 'ctop'
```

每个要执行的命令都应该单独放在引号中。

* https://tmuxcheatsheet.com/
* 支持通过 SSH 使用（`Ctrl+B` 是命令模式）

#### goaccess

* 用于实时查看服务器访问日志
* https://goaccess.io/get-started

```
sudo apt install -y goaccess
goaccess -c /var/log/nginx/access.log
```

nginx 对应应选择的日志格式是 `NCSA Combined Log Format`

```
goaccess access.log -o /var/www/html/report.html --log-format=COMBINED --real-time-html
```
