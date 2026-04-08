name: Build and Deploy

on:
  push:
    branches:
      - main
  issues:
    types: [opened, edited, closed, deleted] # Ejecuta el workflow cuando se crea, edita o borra un issue

env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true

permissions:
  contents: write
  issues: read # Permiso necesario para leer los issues

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install PyGithub requests # Instala las bibliotecas necesarias

      # Aquí es donde se ejecuta el nuevo script
      - name: Generate products JSON
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} # Pasa el token al script
        run: python scripts/fetch_products.py

      # NUEVO PASO: Generar la tienda
      - name: Generate shop data
        run: python scripts/generar_tienda.py


      - name: Build site
        run: mkdocs build --strict
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Add prev/next links
        run: python add_prev_next.py site

      - name: Add CNAME
        run: echo "jim88.pp.ua" > ./site/CNAME

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
