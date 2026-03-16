# Docker

英文版本：[`docker.md`](docker.md)

一些用于管理 Docker 镜像和运行环境的常用命令。

### 磁盘清理

```bash
sudo docker system prune  # 使用 -a 可清理全部，而不仅仅是 dangling 镜像
sudo docker rmi -f $(sudo docker images | grep "<none>" | awk "{print \$3}")
```

* https://forums.docker.com/t/command-to-remove-all-unused-images/20/5
* https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes

### 按过滤条件删除镜像

```bash
sudo docker rmi -f $(sudo docker images --filter=reference="*CONTAINER*:*TAG*" -q)
sudo docker rmi -f $(sudo docker images --filter=since=CONTAINER:TAG -q)
sudo docker rmi -f $(sudo docker images --filter=before=CONTAINER:TAG -q)
```

* https://stackoverflow.com/a/47265229
* https://docs.docker.com/engine/reference/commandline/images/#filter

### 修改默认 Runtime

编辑 `/etc/docker/daemon.json`，加入 `"default-runtime": "nvidia"`

* https://github.com/dusty-nv/jetson-containers#docker-default-runtime

### 修改数据根目录

编辑 `/etc/docker/daemon.json`，加入 `"data-root": "/path/to/data"`

```json
{
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    },

    "default-runtime": "nvidia",
    "data-root": "/mnt/nvme/docker"
}
```

编辑 `/lib/systemd/system/docker.service`，加入 `Environment=DOCKER_TMPDIR=/path/to/tmp`

```
[Service]
Type=notify
# the default is not to use systemd for cgroups because the delegate issues still
# exists and systemd currently does not support the cgroup feature set required
# for containers run by docker
Environment=DOCKER_TMPDIR=/mnt/nvme/docker/tmp
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
ExecReload=/bin/kill -s HUP $MAINPID
TimeoutSec=0
RestartSec=2
Restart=always
```

* https://www.ibm.com/docs/en/z-logdata-analytics/5.1.0?topic=compose-relocating-docker-root-directory
* https://github.com/spotify/docker-client/issues/1028#issuecomment-392803461

### 保存容器镜像

```bash
sudo docker save myimage:latest | gzip > myimage_latest.tar.gz
```

### 加载容器镜像

```bash
docker load > myimage_latest.tar.gz
```

### 守护进程状态

```bash
sudo systemctl status docker.service
sudo journalctl -fu docker.service   # 查看 dockerd 日志
sudo docker info
```

### Docker Compose

`docker-compose` 已被废弃，建议后续改用 `docker compose`

```
sudo apt install -y docker-compose-v2
```

```
docker compose up --build
```

以前的独立版 `docker-compose` 可以这样安装：

```
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
sudo chmod +x /usr/local/bin/docker-compose && \
docker-compose --version
```

#### 在远程主机上执行

* https://www.docker.com/blog/how-to-deploy-on-remote-docker-hosts-with-docker-compose/

```
DOCKER_HOST="ssh://user@remotehost" docker-compose up -d
```
