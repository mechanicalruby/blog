import os
import glob
import shutil
import io
from pathlib import Path
import mistune, frontmatter

# build configuration
input_path = "base/"
output_path = "output/"
blog_path = "blog/"

# func: create normal page with generic header/footer
def compile_base_page(input_file, output_file):
    with open(output_file,'wb') as final_page:
        for srcfilelist in ['t_header.html',input_file,'t_footer.html']:
            with open(srcfilelist, 'rb') as srcfiles:
                shutil.copyfileobj(srcfiles, final_page)
                final_page.write(b"\n"); # create newline at edge
    return True

# func: create blog page with generic header/footer
def compile_blog_page(input_file, output_file):
    with open(output_file,'wb') as final_page:
        for srcfilelist in ['t_header.html',input_file,'t_footer.html']:
            with open(srcfilelist, 'rb') as srcfiles:
                shutil.copyfileobj(srcfiles, final_page)
                final_page.write(b"\n"); # create newline at edge
    return True

# func: create blog page with generic header/footer, render from markdown
def compile_blog_page_markdown(input_file, output_file):
    # lack of frontmatter exits the script, check if it's there
    check = frontmatter.check(input_file)
    if(check == False):
        print('[ERROR] No frontmatter, skipping post ' + str(input_file))
        return False

    # now get all the stuff we need
    obj = frontmatter.load(input_file)
    rendered_html = mistune.html(obj.content)

    # string literal... sorry for the indentation
    wrapped_html = f"""
<title>{obj['title']} - MechanicalRuby</title>

<main class="main">\n
<h1 class="blog-header">{obj['title']}</h1>\n
<p class="blog-timestamp">published <time>{obj['date']}</time></p>\n
{rendered_html}\n
<a href="/"> &lt&lt Back to main page</a>\n
</main>
        """

    with open(output_file, "w", encoding="utf-8") as final_page:
        with open("t_header.html", "r", encoding="utf-8") as f:
            final_page.write(f.read())

        final_page.write(wrapped_html)
        final_page.write("\n")

        with open("t_footer.html", "r", encoding="utf-8") as f:
            final_page.write(f.read())

    return True

# now we generate.

# create an output directory
if not os.path.exists(output_path):
    print("creating output dir")
    os.makedirs(output_path)

# create a blog subdirectory
if not os.path.exists(output_path + blog_path):
    print("creating blog dir")
    os.makedirs(output_path + blog_path)

# --- misc files ---
# stylesheet
shutil.copyfile("styles.css", output_path + "styles.css")
# favicon
shutil.copyfile("favicon.png", output_path + "favicon.png")
# rss (FIX!)
# shutil.copyfile("rss.xml", output_path + "rss.xml")
# 404
shutil.copyfile("404.html", output_path + "404.html")

# --- base files ---
print("! compiling main site pages")
for filename in glob.glob(input_path + '*.html'):
    page_name = Path(filename).stem
    
    if page_name == 'index':
        compile_base_page(input_path + "index.html", output_path + "index.html")
        continue

    if not os.path.exists(output_path + page_name):
        os.makedirs(output_path + page_name)

    if(compile_base_page(Path(filename), output_path + page_name + "/index.html")):
        print(Path(filename).name + " -> " + output_path + page_name + "/index.html")

# --- markdown blog files ---
print("! compiling markdown blog posts")
for filename in glob.glob(input_path + blog_path + '*.md'):
    page_name = Path(filename).stem

    if not os.path.exists(output_path + blog_path + page_name):
        os.makedirs(output_path + blog_path + page_name)

    if(compile_blog_page_markdown(Path(filename), output_path + blog_path + page_name + "/index.html")):
        print(Path(filename).name + " -> " + output_path + blog_path + page_name + "/index.html")

sys.exit(0)