FROM alpine:latest AS builder
RUN apk add python3 py3-pip
RUN pip install -U build
RUN mkdir /kona
COPY . /kona
RUN cd /kona && python -m build .

FROM alpine:latest
RUN apk add python3 py3-pip
COPY --from=builder /kona/dist/konapy-*.whl /tmp
RUN pip install -U /tmp/konapy-*.whl
CMD kona
