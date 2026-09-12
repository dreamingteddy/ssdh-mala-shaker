# Build a Bowl

A dependency-free interactive frontend using the images in `images/`.

## Run locally

From this folder, run:

```sh
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/flask --app app run --debug
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000).

Choose up to six ingredients by clicking a card, or drag a card into the bowl. Click an ingredient in the bowl to remove it. The **Save** button renders and downloads a named PNG directly in the browser.

## Run with Docker

Build and start the container:

```sh
docker build -t build-a-bowl .
docker run --rm -p 5000:5000 build-a-bowl
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Publish with GitHub Pages

Create a GitHub repository and, from this directory, run:

```sh
git init
git add index.html app.py requirements.txt README.md images
git commit -m "Create Build a Bowl app"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

In the repository’s **Settings → Pages**, select **Deploy from a branch**, then choose `main` and `/ (root)`.

GitHub Pages uses `index.html` and `images/` only; `app.py` is not run there. The Flask setup above remains available for local development.

## Copyright

Copyright © 2026 dreamingteddy. All rights reserved.

The source code, design, and included image assets are owned by dreamingteddy. No permission is granted to copy, modify, or redistribute this project or its assets without written permission.
