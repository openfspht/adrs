FROM alpine:3.24 AS build

ARG MDBOOK_VERSION=0.5.4
ARG MDBOOK_MERMAID_VERSION=0.17.1

RUN apk add --no-cache python3 curl

RUN case "$(uname -m)" in \
      x86_64)  ARCH=x86_64  ;; \
      aarch64) ARCH=aarch64 ;; \
      *) echo "unsupported architecture: $(uname -m)" >&2; exit 1 ;; \
    esac && \
    curl -fsSL "https://github.com/rust-lang/mdBook/releases/download/v${MDBOOK_VERSION}/mdbook-v${MDBOOK_VERSION}-${ARCH}-unknown-linux-musl.tar.gz" \
      | tar -xz -C /usr/local/bin mdbook && \
    curl -fsSL "https://github.com/badboy/mdbook-mermaid/releases/download/v${MDBOOK_MERMAID_VERSION}/mdbook-mermaid-v${MDBOOK_MERMAID_VERSION}-${ARCH}-unknown-linux-musl.tar.gz" \
      | tar -xz -C /usr/local/bin mdbook-mermaid

WORKDIR /src
COPY . .
RUN python3 generate-book.py

FROM nginxinc/nginx-unprivileged:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /src/book /usr/share/nginx/html

EXPOSE 8080
