# 1-first_image

A tiny web app packaged as a Docker image, written in plain Python
(standard library only, `http.server` — no Flask, no external packages).
It listens on port `5000` inside the container and responds with a short
text message.

## Files

- `app.py` — the web server (one route, returns a short message)
- `Dockerfile` — builds the image

## Build the image

```bash
docker build -t first-image .
```

## Run the container (publishing the port to the host)

```bash
docker run -d --name first_image_container -p 8082:5000 first-image
```

- `5000` (right side) is the port the app actually listens on **inside**
  the container — it matches the `EXPOSE 5000` in the Dockerfile.
- `8080` (left side) is the port on **your machine**; change it if it's
  already taken.

## Confirm it answers

```bash
curl http://localhost:8082
```

Expected output:

```
Hello from my first Docker image!
```

## Clean up

```bash
docker stop first_image_container
docker rm first_image_container
```