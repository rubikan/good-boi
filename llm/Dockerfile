# Copied and adapted from https://github.com/bartowski1182/koboldcpp-docker

FROM python:3.10-slim

WORKDIR /koboldcpp

RUN apt-get update && apt-get install -y git \
    build-essential \
    libclblast-dev \
    libopenblas-dev \
    && git clone https://github.com/LostRuins/koboldcpp.git --branch v1.62.2 ./ \
    && pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt \
    && make LLAMA_OPENBLAS=1 LLAMA_CLBLAST=1 \
    && apt-get clean s&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 80

# Use koboldcpp.py as the entrypoint when the container launches
CMD ["python", "koboldcpp.py"]
