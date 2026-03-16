# NFS

英文版本：[`nfs.md`](nfs.md)

用于搭建 NFS 文件共享服务，让局域网中的其他 Linux 设备挂载目录。
这与 Samba/SMB 不同，NFS 不适用于 Windows 兼容场景。

NFS 默认不加密，因此除非同时配合 VPN，否则通常只建议在局域网中使用。不过对于大文件传输，它可能有更高性能。其他方案还包括面向 Windows 兼容性的 [Samba](samba.zh-CN.md)（SMB）以及 [SSHFS](#sshfs)。

* https://ubuntu.com/server/docs/network-file-system-nfs

### 安装 NFS 服务

```
sudo apt install -y nfs-kernel-server && \
sudo systemctl start nfs-kernel-server.service
```

### 导出网络共享目录

把下面内容添加到 `/etc/exports` 中（将 `/mnt/nvme` 替换成你想共享的服务端路径）

```
/mnt/nvme *(rw,sync,no_subtree_check,no_root_squash)
```

（除了导出的目录本身外，服务端上的符号链接客户端无法跟随访问）

```
sudo exportfs -a && \
systemctl status nfs-server
```

### 从客户端挂载（Linux）

下面这些命令会在其他 Linux 设备上安装 NFS 客户端，并挂载服务端共享目录。挂载完成后，它会像客户端本地硬盘一样显示，只是底层走的是网络访问。

```
sudo apt install -y nfs-common && \
sudo mkdir /mnt/nfs && \
sudo mount $NFS_HOST:/mnt/nvme /mnt/nfs
```

将 `$NFS_HOST` 替换为导出 NFS 共享的主机名，或者先执行 `export NFS_HOST=my-jetson`

### 挂载 Google Drive（rclone）

[`rclone`](https://github.com/rclone/rclone) 是 Linux 下挂载 Google Drive（GDrive）的推荐工具： https://rclone.org/drive/

[`roundsync`](https://github.com/newhinton/Round-Sync) 是一个前端工具，支持 Linux x86、ARM 和 Android： https://roundsync.com/

### SSHFS

与 NFS 不同，SSHFS 自带身份验证和加密能力，因为它构建在 SSH 之上。因此它通常更容易安装，或者在很多 Linux 环境中已经预先可用。

* https://www.reddit.com/r/linuxadmin/comments/17ur9vb/why_use_sshfs_over_nfs/

```
sudo apt-get install sshfs
sudo mkdir -p /mnt/sshfs
sudo sshfs -o allow_other,default_permissions SSH_USER@SSH_HOST:/mnt/nvme /mnt/sshfs
```

将 `SSH_USER` 和 `SSH_HOST` 替换成服务端的登录用户名和主机名。
