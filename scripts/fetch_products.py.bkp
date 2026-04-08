#!/usr/bin/env python3
"""
Script para extraer productos desde Issues de GitHub y generar un archivo products.json.
"""
import os
import json
import requests
from datetime import datetime
from github import Github

# Configuración
REPO_NAME = "jimraynor88/jimraynor88.github.io" # Ajusta según tu repositorio
LABEL_NAME = "producto" # Solo los issues con esta etiqueta se consideran productos

def get_product_issues():
    """Obtiene los issues del repositorio que tienen la etiqueta 'producto'."""
    # Lee el token desde una variable de entorno (más seguro)
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError("Se necesita un GITHUB_TOKEN en las variables de entorno.")

    g = Github(token)
    repo = g.get_repo(REPO_NAME)
    label = repo.get_label(LABEL_NAME)
    return repo.get_issues(state='all', labels=[label])

def parse_issue_content(issue):
    """Parsea el contenido del issue para extraer el front matter y la descripción."""
    lines = issue.body.split('\n')
    front_matter = {}
    reading_front_matter = False
    desc_lines = []

    for line in lines:
        if line.strip() == '---':
            reading_front_matter = not reading_front_matter
            continue
        if reading_front_matter and ':' in line:
            key, value = line.split(':', 1)
            front_matter[key.strip()] = value.strip()
        elif not reading_front_matter and line.strip():
            desc_lines.append(line)

    # Mapear los campos del front matter a nuestro formato
    product = {
        "id": issue.number,
        "title": front_matter.get('title'),
        "price": float(front_matter.get('price', 0)),
        "currency": front_matter.get('currency', 'EUR'),
        "image": front_matter.get('image'),
        "status": front_matter.get('status', 'draft'),
        "description": '\n'.join(desc_lines),
        "created_at": issue.created_at.isoformat(),
        "updated_at": issue.updated_at.isoformat(),
    }
    return product

def main():
    products = []
    for issue in get_product_issues():
        if issue.state == 'closed':
            continue
        product = parse_issue_content(issue)
        products.append(product)

    # Ordenar productos (ej. por fecha de creación)
    products.sort(key=lambda p: p['created_at'], reverse=True)

    # Guardar en un archivo JSON
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print(f"✅ {len(products)} productos exportados a products.json")

if __name__ == "__main__":
    main()
