FROM ghcr.io/astral-sh/uv:python3.13-alpine

# 安裝依賴
RUN apk add --no-cache gcc
RUN apk add --no-cache musl-dev
RUN apk add --no-cache python3-dev
RUN apk add --no-cache tzdata
RUN apk add --no-cache jq
WORKDIR /app
RUN uv venv

# 安裝依賴
ADD pyproject.toml .
RUN uv pip install .
ADD src src