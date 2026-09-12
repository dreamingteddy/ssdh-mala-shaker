# Build a Bowl

A dependency-free interactive frontend using the images in `images/`.

## Run locally

From this folder, run:

```sh
python3 -m http.server 8000
```

Then open [http://localhost:8000](http://localhost:8000).

Choose up to six ingredients by clicking a card, or drag a card into the bowl. Click an ingredient in the bowl to remove it.

## Publish with GitHub Pages

Create a GitHub repository and, from this directory, run:

```sh
git init
git add index.html README.md images
git commit -m "Create Build a Bowl frontend"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

In the repository’s **Settings → Pages**, select **Deploy from a branch**, then choose `main` and `/ (root)`.
