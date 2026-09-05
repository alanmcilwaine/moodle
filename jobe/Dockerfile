FROM trampgeek/jobeinabox@sha256:2720e97aeb988fc2ce9f522845d264124ebc266f042f3619d0d5caf2f04037b2

ARG TARGETARCH
ADD https://go.dev/dl/go1.27.1.linux-${TARGETARCH}.tar.gz /tmp/go.tar.gz

# Checksums from https://go.dev/dl/?mode=json
RUN case "${TARGETARCH}" in \
      amd64) expected=63d339f0da5ab53635a56f2490a7984dfe12dfcff22ad749f63edaf590168445 ;; \
      arm64) expected=3450b45a3f9ee8568792736a5c5e70a1f2e9b36c35a8f74958c03e51d7d92bec ;; \
      *) echo "unsupported architecture: ${TARGETARCH}" >&2; exit 1 ;; \
    esac && \
    echo "${expected}  /tmp/go.tar.gz" | sha256sum -c - && \
    tar -C /usr/local -xzf /tmp/go.tar.gz && \
    rm /tmp/go.tar.gz && \
    # The CodeRunner wrapper strips PATH to os.defpath, so go must live in /usr/bin.
    ln -s /usr/local/go/bin/go /usr/bin/go && \
    ln -s /usr/local/go/bin/gofmt /usr/bin/gofmt

# Pre-warm the stdlib cache to avoid a cold compile under Jobe's CPU limit.
RUN GOCACHE=/tmp/.go-cache go build std && chmod -R a+rwX /tmp/.go-cache
