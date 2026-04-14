import os
import sys
import frontmatter

# --- CONFIGURACIÓN (CAMBIA ESTO SEGÚN NECESITES) ---
# Ruta relativa a la carpeta que contiene los archivos a proteger
TARGET_DIR = "docs/acerca_mia/astrologia/"  # <-- Cambia aquí la ruta
# Nivel que quieres asignar. También podrías usar 'password: 'mi-clave''
PROTECTION_LEVEL = "astro"  
# Si no quieres usar un nivel, puedes usar una contraseña directa (comenta la línea de arriba y descomenta la de abajo):
# PROTECTION_PASSWORD = "mi-contraseña"
# =================================================

def process_markdown_file(filepath):
    """Añade la protección de nivel a un archivo Markdown."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        # Añade o actualiza el nivel
        post['level'] = PROTECTION_LEVEL
        # Si usas contraseña en lugar de nivel:
        # post['password'] = PROTECTION_PASSWORD
        
        # Vuelve a escribir el archivo
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        print(f"✅ Procesado: {filepath}")
    except Exception as e:
        print(f"❌ Error al procesar {filepath}: {e}")

def main():
    if not os.path.isdir(TARGET_DIR):
        print(f"Error: La carpeta '{TARGET_DIR}' no existe.")
        sys.exit(1)
    
    print(f"Procesando archivos en: {TARGET_DIR}")
    for filename in os.listdir(TARGET_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(TARGET_DIR, filename)
            process_markdown_file(filepath)
    print("¡Proceso completado!")

if __name__ == "__main__":
    main()
