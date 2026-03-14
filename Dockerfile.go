# Go SSRF proxy sidecar (optional - needed for SSRF module)
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go/go.mod ./
COPY go/cmd/ ./cmd/
RUN go build -o /proxy ./cmd/proxy

FROM alpine:3.19
RUN apk --no-cache add ca-certificates
COPY --from=builder /proxy /proxy
EXPOSE 9000
CMD ["/proxy"]
