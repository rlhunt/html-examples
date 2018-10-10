#!/usr/bin/env python3

from glob import glob
from os import path
import os
import re
import sys
import shutil
import markdown

def generate_index(dir):
    # Read the header

    readme_path = path.join(dir, "README.md")
    index_path = path.join(dir, "INDEX.md")

    header = ""
    if path.exists(readme_path):
        header = open(readme_path).read()
    elif path.exists(index_path):
        header = open(index_path).read()

    # Gather the files

    locals = glob(path.join(dir, "*"))
    all = glob(path.join(dir, "*/**"), recursive=True)

    # Filter the files

    locals = [x for x in locals if not path.isdir(x)]

    hiddenExtensions = [".css", ".md", "index.html"]
    def shouldHide(path):
        for extension in hiddenExtensions:
            if path.endswith(extension):
                return True
        return False
    locals = list(filter(lambda x: not shouldHide(x), locals))
    all = list(filter(lambda x: not shouldHide(x), all))

    # Sort the lists
    locals.sort()
    all.sort()

    # Create the markdown file

    md = header

    if len(locals) > 0:
        md += "## Contents\n"
        for file in locals:
            rel_path = file.replace(dir, "")
            md += str.format(" * [{}]({})", rel_path, rel_path) + "\n"
        md += "\n"

    if len(all) > 0:
        md += "## Subdirectories\n"
        for file in all:
            rel_path = file.replace(dir, "")
            if path.isdir(file):
                md += str.format(" * [{}]({})", rel_path, path.join(rel_path, "index.html")) + "\n"
            else:
                md += str.format(" * [{}]({})", rel_path, rel_path) + "\n"
        md += "\n"

    # Generate the body

    body = markdown.markdown(md, extensions=['markdown.extensions.nl2br'])

    # Generate the Html

    html = \
"""<!DOCTYPE html>
<meta charset="utf=8"/>
<html>
<head>
<style type="text/css">
html {{
    background-color: #3D9970
}}
body {{
    margin: 1em;
    border-radius: 1em;
    padding: 1.5em;
    background-color: white;
    font-family: sans-serif;
}}
h1 {{
    margin-top: 0px;
}}
</style>
</head>
<body>
{0}
</body>
</html>
""".format(body)

    with open(path.join(dir, "index.html"), "w") as out:
        out.write(html)

def generate_site(out_dir):
    out_dir = path.join(out_dir, "")

    if path.isdir(out_dir):
        shutil.rmtree(out_dir)

    shutil.copytree(".",
                    out_dir,
                    ignore=shutil.ignore_patterns("*.py", "index.html", ".git"))

    generate_index(out_dir)
    for (dir, _, _) in os.walk(out_dir):
        dir = path.join(dir, "")
        generate_index(dir)

generate_site(sys.argv[1])
