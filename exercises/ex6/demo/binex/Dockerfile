FROM docker.io/ubuntu:jammy

RUN apt-get update && apt-get -y install qemu-user gdb-multiarch
RUN apt-get install python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential -y
RUN apt-get install gdb python3 python3-pip -y
RUN pip3 install --upgrade pwntools
RUN apt-get install binutils -y
RUN apt-get install curl -y
RUN bash -c "$(curl -fsSL https://gef.blah.cat/sh)"
RUN apt-get install tmux file procps -y
ENV LC_CTYPE=C.UTF-8
