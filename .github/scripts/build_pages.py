import os
import shutil
import re

# Directory definitions
WEBPAGE_DIR = "../Repo--Webpage"
TEMPLATES_DIR = ".github/templates"
DEST_ROOT = "public"

# Mapping of course IDs to their template file names
COURSES_MAP = {
    'MTX1': 'econometria-i.html',
    'MTX2': 'econometria-ii.html',
    'MTX3': 'series-tiempo-tecnico.html',
    'AppliedTS': 'series-tiempo-empirico.html'
}

def sync_templates_locally():
    """
    If running locally and the webpage repo is present next to this one,
    sync the latest files into the templates folder.
    """
    if not os.path.isdir(WEBPAGE_DIR):
        print(f"Webpage directory not found at '{WEBPAGE_DIR}'. Skipping local templates sync...")
        return
        
    print(f"Sincronizando plantillas desde {WEBPAGE_DIR}...")
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    
    # Files to sync
    sync_tasks = [
        (os.path.join(WEBPAGE_DIR, "docencia.html"), os.path.join(TEMPLATES_DIR, "docencia.html")),
        (os.path.join(WEBPAGE_DIR, "css/style.css"), os.path.join(TEMPLATES_DIR, "style.css")),
        (os.path.join(WEBPAGE_DIR, "js/main.js"), os.path.join(TEMPLATES_DIR, "main.js"))
    ]
    
    for course_id, template_name in COURSES_MAP.items():
        src_path = os.path.join(WEBPAGE_DIR, "docencia", template_name)
        dest_path = os.path.join(TEMPLATES_DIR, template_name)
        sync_tasks.append((src_path, dest_path))
        
    for src, dest in sync_tasks:
        if os.path.exists(src):
            print(f"  Copying: {src} -> {dest}")
            shutil.copy2(src, dest)
        else:
            print(f"  Warning: Source not found: {src}")

def process_landing_page():
    """
    Reads the landing template, updates menu/course links, and saves to public/index.html.
    """
    src_path = os.path.join(TEMPLATES_DIR, "docencia.html")
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Landing template not found at {src_path}")
        
    print("Procesando página de inicio (landing)...")
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace relative links with absolute links pointing to the main website
    # We replace index.html first so it doesn't double-replace docencia.html -> index.html -> https://amosino.net/
    replacements = [
        ('href="index.html"', 'href="https://amosino.net/"'),
        ('href="investigacion.html"', 'href="https://amosino.net/investigacion.html"'),
        ('href="libros.html"', 'href="https://amosino.net/libros.html"'),
        ('href="proyectos.html"', 'href="https://amosino.net/proyectos.html"'),
        ('href="blog/index.html"', 'href="https://amosino.net/blog/index.html"'),
        ('href="docencia.html"', 'href="index.html"')  # Keep relative since this is the courses landing page
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    # Update course page links to point to the folders in mtx--courses
    course_links = {
        'href="docencia/econometria-i.html"': 'href="MTX1/index.html"',
        'href="docencia/econometria-ii.html"': 'href="MTX2/index.html"',
        'href="docencia/series-tiempo-tecnico.html"': 'href="MTX3/index.html"',
        'href="docencia/series-tiempo-empirico.html"': 'href="AppliedTS/index.html"'
    }
    
    for old, new in course_links.items():
        content = content.replace(old, new)
        
    # Save output
    dest_path = os.path.join(DEST_ROOT, "index.html")
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_course_page(course_id, template_name):
    """
    Reads the course template, updates menu links to absolute, updates slide links to relative,
    and saves to public/<course_id>/index.html.
    """
    src_path = os.path.join(TEMPLATES_DIR, template_name)
    if not os.path.exists(src_path):
        print(f"Warning: Template for {course_id} not found at {src_path}. Skipping page generation...")
        return
        
    print(f"Procesando página para el curso {course_id}...")
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace relative navigation links to point to the main site
    # Replace ../index.html first, then ../docencia.html -> ../index.html
    replacements = [
        ('href="../index.html"', 'href="https://amosino.net/"'),
        ('href="../investigacion.html"', 'href="https://amosino.net/investigacion.html"'),
        ('href="../libros.html"', 'href="https://amosino.net/libros.html"'),
        ('href="../proyectos.html"', 'href="https://amosino.net/proyectos.html"'),
        ('href="../blog/index.html"', 'href="https://amosino.net/blog/index.html"'),
        ('href="../docencia.html"', 'href="../index.html"')  # Link back to the courses index
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    # Convert absolute slide links on GitHub Pages into local relative links
    # e.g., https://amosino.github.io/mtx--courses/MTX1/MTX1--01--RLS.html -> ./MTX1--01--RLS.html
    absolute_url_prefix = f"https://amosino.github.io/mtx--courses/{course_id}/"
    content = content.replace(absolute_url_prefix, "./")
    
    # Save output
    dest_dir = os.path.join(DEST_ROOT, course_id)
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, "index.html")
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(content)

def build_site():
    # 1. Sync templates locally if run from user's machine
    sync_templates_locally()
    
    # 2. Re-create public directory
    if os.path.exists(DEST_ROOT):
        shutil.rmtree(DEST_ROOT)
    os.makedirs(DEST_ROOT)
    
    # 3. Copy course slides and PDFs
    for course_id in COURSES_MAP.keys():
        docs_src = os.path.join(course_id, "docs")
        if os.path.isdir(docs_src):
            docs_dest = os.path.join(DEST_ROOT, course_id)
            print(f"Copying {docs_src} -> {docs_dest}")
            shutil.copytree(docs_src, docs_dest)
            
            # Remove any existing index.html inside the copied docs folder if it exists
            copied_index = os.path.join(docs_dest, "index.html")
            if os.path.exists(copied_index):
                os.remove(copied_index)
        else:
            print(f"Directory {docs_src} not found, skipping slide copy...")
            
    # 4. Copy static css/js files from templates
    css_dest_dir = os.path.join(DEST_ROOT, "css")
    js_dest_dir = os.path.join(DEST_ROOT, "js")
    os.makedirs(css_dest_dir, exist_ok=True)
    os.makedirs(js_dest_dir, exist_ok=True)
    
    shutil.copy2(os.path.join(TEMPLATES_DIR, "style.css"), os.path.join(css_dest_dir, "style.css"))
    shutil.copy2(os.path.join(TEMPLATES_DIR, "main.js"), os.path.join(js_dest_dir, "main.js"))
    
    # 5. Process and generate the HTML index pages
    process_landing_page()
    
    for course_id, template_name in COURSES_MAP.items():
        process_course_page(course_id, template_name)
        
    print(f"Static site build complete in './{DEST_ROOT}/' directory.")

if __name__ == "__main__":
    build_site()
