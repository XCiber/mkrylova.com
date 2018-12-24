FROM alpine as builder
WORKDIR /app
ADD . /app
RUN apk add --no-cache hugo
RUN hugo -v -t vogue

FROM nginx:alpine as production
COPY --from=builder /app/public /usr/share/nginx/html
