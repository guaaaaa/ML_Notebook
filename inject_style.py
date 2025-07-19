from pathlib import Path

# Tailwind CDN + Font Awesome + Google Fonts
head_injections = """
<script src="https://cdn.tailwindcss.com"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
"""

# Main theme styling based on your index.html
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
    border-radius: 1.5rem; /* rounded-3xl */
    padding: 2rem;
    margin: 2rem auto;
    max-width: 90%;
  }

  /* Adjust the width for larger screens */
  @media (min-width: 1024px) {
    .glass-container {
      max-width: 80%;
    }
  }

  /* Override notebook elements to use light text */
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

  /* Style for code cells and outputs */
  .glass-container .input_area pre,
  .glass-container .output_wrapper,
  .glass-container .output {
    background: rgba(0, 0, 0, 0.2) !important;
    border-radius: 0.5rem;
    padding: 1rem;
  }

  /* Adjust the prompt (input code) */
  .glass-container .input_area {
    background: rgba(0, 0, 0, 0.2) !important;
    border-radius: 0.5rem;
  }

  /* Style for tables */
  .glass-container table {
    background: rgba(0, 0, 0, 0.2) !important;
    color: white;
  }

  /* Add some spacing between cells */
  .glass-container .cell {
    margin-bottom: 1.5rem;
  }

  /* Override links */
  .glass-container a {
    color: #93c5fd; /* light blue for links */
  }

  .glass-container a:hover {
    color: #bfdbfe; /* lighter blue on hover */
    text-decoration: underline;
  }
</style>
"""

# Inject into each HTML file in ./site
site_dir = Path("site")
for html_file in site_dir.glob("*.html"):
    if html_file.name == "index.html":
        continue  # skip main page
        
    content = html_file.read_text(encoding="utf-8")
    
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