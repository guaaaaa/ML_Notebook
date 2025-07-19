from pathlib import Path
import re

# Head injections with dependencies
head_injections = """
<script src="https://cdn.tailwindcss.com"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
"""

# Main theme styling with fixes
custom_style = """
<style>
  :root {
    --primary: #6366f1;
    --secondary: #8b5cf6;
    --accent: #ec4899;
    --dark: #0f172a;
    --light: #f8fafc;
  }

  body {
    font-family: "Poppins", sans-serif;
    background: linear-gradient(-45deg, #0f172a, #1e293b, #1e1b4b, #312e81);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: var(--light);
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
    margin: 0;
    padding: 2rem;
  }

  @keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }

  body::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(
        circle at 10% 20%,
        rgba(99, 102, 241, 0.1) 0%,
        transparent 20%
      ),
      radial-gradient(
        circle at 90% 80%,
        rgba(139, 92, 246, 0.1) 0%,
        transparent 20%
      ),
      radial-gradient(
        circle at 50% 30%,
        rgba(236, 72, 153, 0.1) 0%,
        transparent 30%
      );
    z-index: -1;
  }

  .glass-container {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    border-radius: 1.5rem;
    padding: 2rem;
    margin: 2rem auto;
    max-width: 90%;
  }

  /* Fix for JupyterLab theme line */
  body > .jp-Notebook {
    display: none !important;
  }

  /* Center all images */
  img {
    display: block;
    margin: 1.5rem auto;
    max-width: 90%;
  }

  /* Dark theme for code cells */
  .input_area,
  .highlight,
  .highlight pre,
  .highlight .c1,
  .highlight .cm,
  .highlight .kd,
  .highlight .kn,
  .highlight .o,
  .highlight .p,
  .highlight .nb,
  .highlight .k,
  .highlight .mf,
  .highlight .mi,
  .highlight .s,
  .highlight .s1,
  .highlight .s2,
  .highlight .se,
  .highlight .si,
  .highlight .nt {
    background-color: rgba(0, 0, 0, 0.3) !important;
    color: #f8fafc !important;
    border-radius: 0.5rem;
  }

  /* Output styling */
  .output_wrapper,
  .output,
  .output_subarea,
  .output_text {
    background-color: rgba(0, 0, 0, 0.3) !important;
    color: #f8fafc !important;
    border-radius: 0.5rem;
    padding: 1rem;
  }

  /* Text styling */
  .glass-container,
  .glass-container h1,
  .glass-container h2,
  .glass-container h3,
  .glass-container h4,
  .glass-container h5,
  .glass-container h6,
  .glass-container p,
  .glass-container div {
    color: #f8fafc;
  }

  /* Tables */
  .glass-container table {
    background: rgba(0, 0, 0, 0.3) !important;
    color: white;
    border-collapse: collapse;
    width: 100%;
    margin: 1rem 0;
  }

  .glass-container th, .glass-container td {
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 0.5rem;
    text-align: left;
  }

  /* Links */
  .glass-container a {
    color: #93c5fd;
    text-decoration: none;
  }

  .glass-container a:hover {
    color: #bfdbfe;
    text-decoration: underline;
  }

  /* Code blocks */
  .highlight {
    margin: 1.5rem 0;
    padding: 1rem;
    overflow: auto;
  }

  /* Remove white backgrounds */
  .jp-RenderedHTMLCommon,
  .jp-InputArea,
  .jp-Cell-inputWrapper,
  .jp-Cell-outputWrapper {
    background: transparent !important;
  }

  /* Fix spacing */
  .cell {
    margin-bottom: 2rem;
  }
</style>
"""

# Inject into each HTML file in ./site
site_dir = Path("site")
for html_file in site_dir.glob("*.html"):
    if html_file.name == "index.html":
        continue  # skip main page
        
    content = html_file.read_text(encoding="utf-8")
    
    # Remove the JupyterLab theme line
    content = re.sub(
        r'class="jp-Notebook" data-jp-theme-light="true" data-jp-theme-name="JupyterLab Light">',
        "",
        content
    )
    
    # Inject head content
    if "<head>" in content:
        content = content.replace(
            "<head>", 
            f"<head>\n{head_injections}\n{custom_style}", 
            1
        )
    
    # Wrap body content in glass container
    if "<body>" in content:
        content = content.replace("<body>", '<body><div class="glass-container">', 1)
        content = content.replace("</body>", "</div></body>", 1)
    elif "<body " in content:  # Handle body with attributes
        content = content.replace("<body ", '<body><div class="glass-container">', 1)
        content = content.replace("</body>", "</div></body>", 1)
    
    html_file.write_text(content, encoding="utf-8")
    print(f"✅ Styled: {html_file.name}")