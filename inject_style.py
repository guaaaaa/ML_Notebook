from pathlib import Path

# Tailwind CDN + your styles
tailwind = '<script src="https://cdn.tailwindcss.com"></script>'
custom_style = """
<style>
  body {
    background: linear-gradient(to right, #fbc2eb, #a6c1ee);
    font-family: 'Segoe UI', sans-serif;
    padding: 2rem;
  }
  h1, h2, h3 {
    color: #111827;
  }
  .output_wrapper, .prompt {
    background: rgba(255, 255, 255, 0.5);
    padding: 1rem;
    border-radius: 0.5rem;
  }
</style>
"""

# Inject into each HTML file in ./site
site_dir = Path("site")
for html_file in site_dir.glob("*.html"):
    if html_file.name == "index.html":
        continue  # skip main page
    content = html_file.read_text(encoding="utf-8")
    if "<head>" in content:
        content = content.replace(
            "<head>", f"<head>\n{tailwind}\n{custom_style}", 1
        )
        html_file.write_text(content, encoding="utf-8")
        print(f"✅ Styled: {html_file.name}")
