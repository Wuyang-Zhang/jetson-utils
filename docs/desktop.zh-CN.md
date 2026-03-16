# Desktop

英文版本：[`desktop.md`](desktop.md)

关于桌面环境、远程桌面配置，以及安装桌面 GUI 应用的一些记录。

### 桌面启动器

如何在 Ubuntu 桌面上创建一个用于启动应用程序的图标？

* https://www.reddit.com/r/Ubuntu/comments/xyyb40/comment/irjcn0r/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

```
[Desktop Entry]
   Encoding=UTF-8
   Version=1.0
   Type=Application
   Terminal=false
   Exec=/opt/chrome-linux/chrome
   Name=Chromium
   Icon=/opt/chrome-linux/product_logo_48.png
```

将该文件创建为 `~/.local/share/applications/chrome.desktop`

### Firefox（非 snap）

* https://www.omgubuntu.co.uk/2022/04/how-to-install-firefox-deb-apt-ubuntu-22-04

```
sudo snap remove firefox && \
sudo apt remove -y firefox && \
wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O- | sudo tee /etc/apt/keyrings/packages.mozilla.org.asc > /dev/null && \
echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" | sudo tee -a /etc/apt/sources.list.d/mozilla.list > /dev/null && \
echo '
Package: *
Pin: origin packages.mozilla.org
Pin-Priority: 1000

Package: firefox*
Pin: release o=Ubuntu
Pin-Priority: -1' | sudo tee /etc/apt/preferences.d/mozilla && \
sudo apt update && \
sudo apt install -y --no-install-recommends firefox
```

### Chromium（非 snap）

以下方法仅适用于 x86：

```
cd /opt && \
sudo wget https://download-chromium.appspot.com/dl/Linux_x64?type=snapshots -O chrome-linux.zip && \
sudo unzip chrome-linux.zip && \
sudo rm chrome-linux.zip && \
sudo ln -s /opt/chrome-linux/chrome /usr/local/bin/chrome
```

然后使用 `chrome-linux/chrome` 启动。

### NoMachine

* NoMachine - https://www.nomachine.com/documents
* [Linux x86_64 DEB Downloads](https://downloads.nomachine.com/download/?id=1)
* [Linux aarch64 DEB Downloads](https://downloads.nomachine.com/linux/?distro=Arm&id=30)

根据最新版本号分别选择 x86 或 ARM：

```
wget https://download.nomachine.com/download/8.14/Linux/nomachine_8.14.2_1_amd64.deb && \
sudo dpkg -i nomachine_8.14.2_1_amd64.deb
```

```
wget https://download.nomachine.com/download/8.16/Arm/nomachine_8.16.1_1_arm64.deb && \
sudo dpkg -i nomachine_8.16.1_1_arm64.deb
```

启动后，你应该能看到它对外开放的连接端口：

```
NoMachine was configured to run the following services:
NX> 700 NX service on port: 4000
```
