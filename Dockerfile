FROM archlinux/archlinux

RUN pacman -Sy --noconfirm python python-pip

RUN mkdir /konabot

COPY main.py /konabot

COPY requirements.txt /konabot

WORKDIR /konabot

RUN mkdir /konabot/.env

RUN python -m venv /konabot/.env

RUN . /konabot/.env/bin/activate && pip install -r /konabot/requirements.txt

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT /entrypoint.sh
