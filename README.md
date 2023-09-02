## kona
Friendly and cute telegram bot 😳

### How to run
```
git clone https://github.com/nyansquared/konapy.git
cd konapy
docker build . -t konapy:latest
docker create -e KONACHAN_NYA_TGTOKEN='YOUR_TELEGRAM_TOKEN' --name konapy konapy:latest
podman generate systemd --new --files --name konapy
systemctl enable --now "$(pwd)/container-konapy.service"
```

