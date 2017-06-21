FROM ubuntu:xenial

MAINTAINER "Jamie Lennox <jamielennox@gmail.com>"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
            build-essential \
            ca-certificates \
            curl \
            debootstrap \
            git \
            kpartx \
            libffi-dev \
            libssl-dev \
            python3 \
            python3-dev \
            qemu-utils \
            sudo \
            wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget -O- https://bootstrap.pypa.io/get-pip.py | python3

RUN groupadd -r nodepool && \
    useradd -r -g nodepool -d /var/lib/nodepool -m nodepool

RUN mkdir -p /etc/nodepool

COPY . /opt/nodepool

# it'd be nice not to specify a version but I don't think COPY is taking the
# .git dir. Doesn't really matter, we're never going to upgrade the version
# within the container.
RUN PBR_VERSION=2.5.99 pip install --no-cache-dir /opt/nodepool
RUN pip install git+https://github.com/jamielennox/diskimage-builder.git@docker#egg=diskimage-builder

#USER nodepool
