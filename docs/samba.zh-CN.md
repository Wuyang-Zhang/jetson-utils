# Samba (SMB)

英文版本：[`samba.md`](samba.md)

这些笔记记录了如何在 Jetson 上安装 Samba 服务端，以实现 SMB/CIFS 网络文件共享协议，并让其他 Linux、Windows、Mac 客户端进行挂载访问。

* https://phoenixnap.com/kb/ubuntu-samba
* https://linuxconfig.org/how-to-configure-samba-server-share-on-ubuntu-20-04-focal-fossa-linux
* https://computingforgeeks.com/install-and-configure-samba-server-share-on-ubuntu/

#### 安装 Samba

```bash
$ sudo apt-get install samba
$ samba -V
$ systemctl status smbd
```

把用户加入 Samba 密码列表中（或者把这里的用户名替换成你希望用于 Samba 访问的 Linux 用户）

```bash
$ sudo smbpasswd -a my_username
```

#### 配置共享目录

把下面内容追加到 `/etc/samba/smb.conf` 末尾，其中：

* `my_share` 是客户端访问时 URL 中显示的共享名
* `path` 是你本地系统中要共享的目录路径
* `valid users` 里的 `my_username` 应替换成前面创建的 `USER`

```bash
$ sudo nano /etc/samba/smb.conf
```

```
[my_share]
comment = Samba share directory
path = /mnt/nvme/share
read only = no
writable = yes
browseable = yes
guest ok = no
valid users = @my_username
```

并在顶部 `[global]` 段下加入以下内容（https://unix.stackexchange.com/a/103418）

```
[global]
   map archive = no
```

验证配置并重启服务：

```bash
$ testparm
$ sudo systemctl restart smbd
```

#### 从 Windows 挂载

```
\\$HOSTNAME.local\my_share
Username = WORKGROUP\my_username
```

#### 从 Linux 命令行挂载

```bash
$ mount -t cifs -o username=my_username //JETSON_IP/my_share /mnt/jetson

# 将挂载项加入 /etc/fstab
//JETSON_IP/my_share /mnt/jetson cifs credentials=/.sambacreds 0 0

cat /.sambacreds
username=my_username
password=password
domain=WORKGROUP

df -hT | grep cifs
```
