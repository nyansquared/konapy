## konachan_nya
Telegram bot 😳

### How to run
```
git clone git@github.com:/kotobun/konachan_nya
cd konachan_nya
docker build . -t konabot:latest
docker create -e KONACHAN_NYA_TGTOKEN='YOUR_TELEGRAM_TOKEN' --name konabot konabot:latest
podman generate systemd --new --files --name konabot
systemctl enable --now "$(pwd)/container-konabot.service"
```

