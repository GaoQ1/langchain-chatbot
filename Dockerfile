FROM ubuntu:18.04 AS builder

RUN sed -i 's#archive.ubuntu.com#mirrors.aliyun.com#g' /etc/apt/sources.list  \
    && sed -i 's#security.ubuntu.com#mirrors.aliyun.com#g' /etc/apt/sources.list

ENV LANG=zh_CN.UTF-8 LANGUAGE=zh_CN:zh LC_ALL=zh_CN.UTF-8 DEBIAN_FRONTEND=noninteractive

RUN rm -rf  /etc/apt/sources.list.d/  && apt update

RUN apt-get update && apt-get install -y --no-install-recommends \
    zsh \
    curl \
    wget \
    unzip \
    supervisor \
    ca-certificates \
    language-pack-zh-hans

RUN locale-gen zh_CN.UTF-8
RUN dpkg-reconfigure locales

CMD ["supervisord", "-n"]


FROM Builder AS conda
ENV MINICONDA_VERSION 3
ENV CONDA_FORGE https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
RUN chsh -s `which zsh`
RUN curl -o ~/miniconda.sh -O  https://mirrors.bfsu.edu.cn/anaconda/miniconda/Miniconda${MINICONDA_VERSION}-latest-Linux-x86_64.sh  && \
    chmod +x ~/miniconda.sh && \
    ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh
RUN ln /opt/conda/bin/conda /usr/local/bin/conda
RUN conda init zsh
RUN conda install mamba -n base -c ${CONDA_FORGE}
RUN ln /opt/conda/bin/mamba /usr/local/bin/mamba && mamba init zsh


FROM Builder AS python
# ENV WORKDIR /app
# WORKDIR ${WORKDIR}
# ADD environment.yml /environment.yml
# RUN mamba update -n base -c ${CONDA_FORGE} conda -y && mamba env create -f /environment.yml -c ${CONDA_FORGE} && rm -rf /root/.cache

# RUN echo "\
# [program:be]\n\
# directory=/app\n\
# command=/opt/conda/envs/py38/bin/gunicorn server:app --workers 1 --worker-class=utils.r_uvicorn_worker.RestartableUvicornWorker  --bind 0.0.0.0:8080 --reload\n\
# autorestart=true\n\
# startretries=100\n\
# redirect_stderr=true\n\
# stdout_logfile=/var/log/be.log\n\
# stdout_logfile_maxbytes=50MB\n\
# environment=PYTHONUNBUFFERED=1, PYTHONIOENCODING=utf-8\n\
# " > /etc/supervisor/conf.d/be.conf

FROM Builder AS clash
WORKDIR /opt/clash
RUN mkdir -p /root/.config/clash && \
    wget -O /root/.config/clash/Country.mmdb https://download.fastgit.ixmu.net/Dreamacro/maxmind-geoip/releases/latest/download/Country.mmdb
RUN wget https://download.fastgit.ixmu.net/Dreamacro/clash/releases/download/v1.11.8/clash-linux-amd64-v1.11.8.gz && \
    gunzip clash-linux-amd64-v1.11.8.gz && \
    mv clash-linux-amd64-v1.11.8 clash && \
    chmod +x clash 
RUN wget https://download.fastgit.ixmu.net/haishanh/yacd/archive/refs/heads/gh-pages.zip && \
    unzip gh-pages.zip && \
    mv yacd-gh-pages ui && \
    rm gh-pages.zip
ADD ./clash_config.yaml /opt/clash/config.yaml
RUN echo "\
[program:clash] \n\
command=/opt/clash/clash -f /opt/clash/config.yaml\n\
autorestart=True\n\
autostart=True\n\
redirect_stderr = true\n\
stdout_logfile=/var/log/clash.log\n\
stdout_logfile_maxbytes=50MB\n\
" > /etc/supervisor/conf.d/clash.conf
EXPOSE 7890 7891 9090