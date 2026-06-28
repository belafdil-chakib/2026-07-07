# docker build -t pytorch:latest .

# Container
# $dockerPath = ${PWD}.Path -replace '\\','/' -replace '^(.:)', '/$($matches[1].ToLower())'
# $volumePath = Join-Path $PWD "volume"
# docker run -dit --name pytorch -p 8889:8889 -p 8080:8080 -p 11434:11434 -v volume:/workdir/volume pytorch:latest

FROM ubuntu:26.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Paris

RUN apt-get update && apt-get install -y \
    software-properties-common curl zstd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workdir

# COPY CODE
COPY datasets /workdir/datasets
COPY 1_Tutos /workdir/1_Tutos
COPY 2_Fondamentaux /workdir/2_Fondamentaux
COPY 3_LinearRegression /workdir/3_LinearRegression
COPY 4_DeepLearning /workdir/4_DeepLearning
COPY 999_Corrigés /workdir/999_Corrigés

# Copy startup script
COPY run_all.sh /workdir
RUN chmod +x /workdir/run_all.sh

# Install uv + venv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"
RUN uv venv --python 3.12

# Install Python deps from pyproject.toml + uv.lock
COPY pyproject.toml uv.lock /workdir/
RUN uv sync --no-install-project --frozen

# # Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Expose ports: 11434 for Ollama, 8889 for Jupyter, 8080 open-webui
EXPOSE 11434 8889 8080

CMD ["/workdir/run_all.sh"]
