
FROM redis:6.0-alpine
WORKDIR /app
COPY sentinel.conf /app
CMD ["redis-sentinel" , "sentinel.conf"]
    