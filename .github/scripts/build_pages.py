import os
import shutil
import re
import glob

# Course definition and styling
COURSES = {
    'AppliedTS': {
        'title': 'Applied Time Series',
        'subtitle': 'Métodos Cuantitativos II (Series de Tiempo Aplicadas)',
        'color': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', # Purple gradient
        'shadow': 'rgba(118, 75, 162, 0.3)'
    },
    'MTX1': {
        'title': 'Econometría I',
        'subtitle': 'Introducción a la Econometría y Regresión Lineal',
        'color': 'linear-gradient(135deg, #13f1fc 0%, #0470dc 100%)', # Blue gradient
        'shadow': 'rgba(4, 112, 220, 0.3)'
    },
    'MTX2': {
        'title': 'Econometría II',
        'subtitle': 'Heteroscedasticidad, Autocorrelación y Modelos de Panel',
        'color': 'linear-gradient(135deg, #ff9966 0%, #ff5e62 100%)', # Orange gradient
        'shadow': 'rgba(255, 94, 98, 0.3)'
    },
    'MTX3': {
        'title': 'Econometría III',
        'subtitle': 'Series de Tiempo Teóricas y Multivariadas',
        'color': 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)', # Green gradient
        'shadow': 'rgba(56, 239, 125, 0.3)'
    }
}

def get_html_title(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(15000) # Read first 15k chars to capture SLIDE_CONFIG
            
            # Check for ioslides subtitle first (which is the actual topic of the presentation)
            js_title_match = re.search(r"title:\s*['\"](.*?)['\"]", content)
            js_subtitle_match = re.search(r"subtitle:\s*['\"](.*?)['\"]", content)
            
            if js_subtitle_match:
                subtitle = js_subtitle_match.group(1).strip()
                if subtitle:
                    # Optional: prefix with title if it's not the generic course name,
                    # but usually subtitle alone is much cleaner (e.g. "Introducción", "Regresión Simple")
                    return subtitle
            
            # Fallback to HTML title tag
            match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                # Remove common pandoc/rmarkdown noise
                title = re.sub(r'\s*Slide Presentation\s*', '', title, flags=re.IGNORECASE)
                if title:
                    return title
    except Exception:
        pass
    
    # Fallback to filename formatting
    base = os.path.basename(filepath)
    name, _ = os.path.splitext(base)
    # E.g. MTX1--01--Regresion Simple -> Regresion Simple
    parts = name.split('--')
    if len(parts) >= 3:
        return parts[2].replace('-', ' ').replace('_', ' ')
    elif len(parts) >= 2:
        return parts[1].replace('-', ' ').replace('_', ' ')
    return name.replace('-', ' ').replace('_', ' ')


def generate_course_index(course_id, course_path, dest_path):
    course_info = COURSES[course_id]
    
    # Find all HTML files in destination path (excluding index.html)
    html_files = glob.glob(os.path.join(dest_path, "*.html"))
    html_files = [f for f in html_files if os.path.basename(f) != "index.html"]
    
    # Sort files naturally
    html_files.sort()
    
    items_html = ""
    for hf in html_files:
        filename = os.path.basename(hf)
        title = get_html_title(hf)
        
        # Check for corresponding PDF
        pdf_filename = filename.replace(".html", ".pdf")
        pdf_path = os.path.join(dest_path, pdf_filename)
        pdf_exists = os.path.exists(pdf_path)
        
        pdf_button = ""
        if pdf_exists:
            pdf_button = f'<a href="{pdf_filename}" target="_blank" class="btn btn-outline-danger btn-sm ms-2"><i class="bi bi-file-pdf"></i> PDF</a>'
            
        items_html += f"""
        <div class="list-group-item d-flex justify-content-between align-items-center py-3">
            <div class="ms-2 me-auto">
                <div class="fw-bold topic-title">{title}</div>
                <span class="text-muted text-sm">{filename}</span>
            </div>
            <div>
                <a href="{filename}" class="btn btn-primary btn-sm"><i class="bi bi-play-fill"></i> Ver Diapositiva</a>
                {pdf_button}
            </div>
        </div>
        """
        
    if not items_html:
        items_html = "<div class='text-center py-4 text-muted'>No se encontraron diapositivas para este curso.</div>"

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{course_info['title']} - Materiales del Curso</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        :root {{
            --primary-gradient: {course_info['color']};
            --shadow-color: {course_info['shadow']};
        }}
        body {{
            background-color: #f4f6f9;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        .header-section {{
            background: var(--primary-gradient);
            color: white;
            padding: 60px 0;
            border-bottom-left-radius: 24px;
            border-bottom-right-radius: 24px;
            box-shadow: 0 10px 30px var(--shadow-color);
            margin-bottom: 40px;
        }}
        .back-btn {{
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            transition: all 0.2s ease;
        }}
        .back-btn:hover {{
            color: white;
            padding-left: 5px;
        }}
        .card-container {{
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.05);
            padding: 30px;
            margin-bottom: 50px;
        }}
        .list-group-item {{
            border-left: none;
            border-right: none;
            border-top: 1px solid #edf2f7;
            border-bottom: 1px solid #edf2f7;
            transition: background-color 0.2s;
        }}
        .list-group-item:hover {{
            background-color: #f8fafc;
        }}
        .topic-title {{
            color: #2d3748;
            font-size: 1.1rem;
        }}
        .text-sm {{
            font-size: 0.85rem;
        }}
        .btn-primary {{
            background: var(--primary-gradient);
            border: none;
            box-shadow: 0 4px 10px var(--shadow-color);
        }}
        .btn-primary:hover {{
            opacity: 0.9;
        }}
    </style>
</head>
<body>
    <div class="header-section">
        <div class="container">
            <a href="../index.html" class="back-btn"><i class="bi bi-arrow-left"></i> Volver al Inicio</a>
            <h1 class="display-5 fw-bold mt-3">{course_info['title']}</h1>
            <p class="lead mb-0">{course_info['subtitle']}</p>
        </div>
    </div>
    
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-9">
                <div class="card-container">
                    <h3 class="mb-4 text-secondary"><i class="bi bi-journal-text"></i> Diapositivas y Materiales</h3>
                    <div class="list-group list-group-flush">
                        {items_html}
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    with open(os.path.join(dest_path, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)

def build_site():
    dest_root = "public"
    if os.path.exists(dest_root):
        shutil.rmtree(dest_root)
    os.makedirs(dest_root)
    
    # 1. Copy docs of each course to public/<course>/
    for course_id in COURSES.keys():
        docs_src = os.path.join(course_id, "docs")
        if os.path.isdir(docs_src):
            docs_dest = os.path.join(dest_root, course_id)
            print(f"Copying {docs_src} -> {docs_dest}")
            shutil.copytree(docs_src, docs_dest)
            
            # Generate index.html if it's missing or if it's MTX1, MTX2, MTX3
            has_existing_index = os.path.exists(os.path.join(docs_dest, "index.html"))
            if not has_existing_index or course_id in ['MTX1', 'MTX2', 'MTX3']:
                print(f"Generating index page for {course_id}")
                generate_course_index(course_id, course_id, docs_dest)
        else:
            print(f"Directory {docs_src} not found, skipping...")
            
    # 2. Build the main landing page
    main_index_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cursos de Métodos Cuantitativos y Econometría</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        body {{
            background-color: #f8fafc;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #1e293b;
        }}
        .hero-section {{
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            color: white;
            padding: 80px 0;
            margin-bottom: 50px;
            border-bottom: 5px solid #3b82f6;
        }}
        .hero-title {{
            font-weight: 800;
            letter-spacing: -0.05rem;
        }}
        .course-card {{
            border: none;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.04);
            transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
            height: 100%;
            background: white;
            display: flex;
            flex-direction: column;
        }}
        .course-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 20px 38px rgba(0,0,0,0.1);
        }}
        .card-gradient-bar {{
            height: 8px;
            width: 100%;
        }}
        .card-body {{
            padding: 30px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .course-badge {{
            display: inline-block;
            padding: 6px 12px;
            font-size: 0.75rem;
            font-weight: 700;
            border-radius: 30px;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .btn-view {{
            border-radius: 30px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.2s;
        }}
        .author-footer {{
            margin-top: 80px;
            padding: 40px 0;
            border-top: 1px solid #e2e8f0;
            background: white;
            color: #64748b;
        }}
    </style>
</head>
<body>

    <!-- Hero Section -->
    <div class="hero-section text-center">
        <div class="container">
            <h1 class="display-4 hero-title mb-3">Materiales de Econometría y Series de Tiempo</h1>
            <p class="lead text-white-50 max-width-600 mx-auto">
                Diapositivas interactivas, códigos de R y recursos académicos para estudiantes y profesionales.
            </p>
        </div>
    </div>

    <!-- Main Course Grid -->
    <div class="container">
        <div class="row g-4 justify-content-center">
            
            <!-- AppliedTS -->
            <div class="col-md-6 col-lg-5">
                <div class="course-card">
                    <div class="card-gradient-bar" style="background: {COURSES['AppliedTS']['color']}"></div>
                    <div class="card-body">
                        <div>
                            <span class="course-badge" style="background: rgba(118, 75, 162, 0.1); color: #764ba2;">Aplicado / Métodos II</span>
                            <h3 class="card-title fw-bold mb-2">{COURSES['AppliedTS']['title']}</h3>
                            <p class="card-text text-secondary mb-4">{COURSES['AppliedTS']['subtitle']}</p>
                        </div>
                        <a href="AppliedTS/index.html" class="btn btn-outline-primary btn-view w-100 mt-3" style="border-color: #764ba2; color: #764ba2;">
                            <i class="bi bi-box-arrow-in-right"></i> Explorar Curso
                        </a>
                    </div>
                </div>
            </div>

            <!-- MTX1 -->
            <div class="col-md-6 col-lg-5">
                <div class="course-card">
                    <div class="card-gradient-bar" style="background: {COURSES['MTX1']['color']}"></div>
                    <div class="card-body">
                        <div>
                            <span class="course-badge" style="background: rgba(4, 112, 220, 0.1); color: #0470dc;">Introductorio</span>
                            <h3 class="card-title fw-bold mb-2">{COURSES['MTX1']['title']}</h3>
                            <p class="card-text text-secondary mb-4">{COURSES['MTX1']['subtitle']}</p>
                        </div>
                        <a href="MTX1/index.html" class="btn btn-outline-primary btn-view w-100 mt-3" style="border-color: #0470dc; color: #0470dc;">
                            <i class="bi bi-box-arrow-in-right"></i> Explorar Curso
                        </a>
                    </div>
                </div>
            </div>

            <!-- MTX2 -->
            <div class="col-md-6 col-lg-5">
                <div class="course-card">
                    <div class="card-gradient-bar" style="background: {COURSES['MTX2']['color']}"></div>
                    <div class="card-body">
                        <div>
                            <span class="course-badge" style="background: rgba(255, 94, 98, 0.1); color: #ff5e62;">Intermedio</span>
                            <h3 class="card-title fw-bold mb-2">{COURSES['MTX2']['title']}</h3>
                            <p class="card-text text-secondary mb-4">{COURSES['MTX2']['subtitle']}</p>
                        </div>
                        <a href="MTX2/index.html" class="btn btn-outline-primary btn-view w-100 mt-3" style="border-color: #ff5e62; color: #ff5e62;">
                            <i class="bi bi-box-arrow-in-right"></i> Explorar Curso
                        </a>
                    </div>
                </div>
            </div>

            <!-- MTX3 -->
            <div class="col-md-6 col-lg-5">
                <div class="course-card">
                    <div class="card-gradient-bar" style="background: {COURSES['MTX3']['color']}"></div>
                    <div class="card-body">
                        <div>
                            <span class="course-badge" style="background: rgba(56, 239, 125, 0.1); color: #11998e;">Avanzado / Teórico</span>
                            <h3 class="card-title fw-bold mb-2">{COURSES['MTX3']['title']}</h3>
                            <p class="card-text text-secondary mb-4">{COURSES['MTX3']['subtitle']}</p>
                        </div>
                        <a href="MTX3/index.html" class="btn btn-outline-primary btn-view w-100 mt-3" style="border-color: #11998e; color: #11998e;">
                            <i class="bi bi-box-arrow-in-right"></i> Explorar Curso
                        </a>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <!-- Footer -->
    <div class="author-footer text-center">
        <div class="container">
            <h5 class="fw-bold mb-2">Dr. Alejandro Mosiño</h5>
            <p class="mb-0">Universidad de Guanajuato</p>
        </div>
    </div>

</body>
</html>
"""
    with open(os.path.join(dest_root, "index.html"), "w", encoding="utf-8") as f:
        f.write(main_index_html)
    
    print("Static site build complete in './public/' directory.")

if __name__ == "__main__":
    build_site()
