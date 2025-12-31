#!/usr/bin/env python3

import os
import glob
import shutil
import io
import datetime
from pathlib import Path
import mistune, frontmatter
from xml.etree.ElementTree import Element, SubElement, tostring, indent

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

# this is all-in-one and regenerates the markdown content so there's
# room for potential refactoring here
def compile_rss_feed(output_file):
    root = Element("rss")
    root.attrib = {
        "version": "2.0",
        "xmlns:atom": "http://www.w3.org/2005/Atom"
    }

    # channel and its required children:
    channel = SubElement(root, "channel")
    title = SubElement(channel, "title")
    link = SubElement(channel, "link")
    description = SubElement(channel, "description")
    copyright = SubElement(channel, "copyright")
    language = SubElement(channel, "language")
    build_date = SubElement(channel, "lastBuildDate")
    atom_link = SubElement(channel, "atom:link")

    # image for the feed
    image = SubElement(channel, "image")
    image_link = SubElement(image, "link")
    image_title = SubElement(image, "title")
    image_url = SubElement(image, "url")
    image_height = SubElement(image, "height")
    image_width = SubElement(image, "width")

    # set the channel's properties
    title.text = "MechanicalRuby"
    link.text = "https://mechanicalruby.com"
    description.text = "Posts from MechanicalRuby's blog"
    copyright.text = "MechanicalRuby (c) 2025, CC BY-SA 4.0"
    language.text = "en-us"
    build_date.text = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
    atom_link.attrib = {
        "href": "http://mechanicalruby.com/rss.xml",
        "rel":  "self",
        "type": "application/rss+xml"
    }

    # set the image's properties
    image_link.text = "https://mechanicalruby.com"
    image_title.text = "MechanicalRuby"
    image_url.text = "https://mechanicalruby.com/favicon.png"
    image_height.text = "32"
    image_width.text = "32"

    # render html for every blog post
    for filename in glob.glob(input_path + blog_path + '*.md'):
        item = SubElement(channel, "item")
        item_title = SubElement(item, "title")
        item_date = SubElement(item, "pubdate")
        item_link = SubElement(item, "link")
        item_guid = SubElement(item, "guid")
        item_desc = SubElement(item, "description")

        # these files should already be validated
        obj = frontmatter.load(Path(filename))
        rendered_html = mistune.html(obj.content)

        item_title.text = obj["title"]
        item_link.text = "https://mechanicalruby.com/" + blog_path + Path(filename).stem + "/"
        item_guid.text = item_link.text
        item_desc.text = f"<![CDATA[{rendered_html}]]>"

        # handle the date. format example: January 1, 2025
        dt = datetime.datetime.strptime(obj["date"], "%B %d, %Y") # %H:%M for 24 hr time after
        output_date = dt.strftime("%a, %d %b %Y %H:%M:%S")
        item_date.text = output_date

    with open(output_file,'wb') as feed:
        indent(root, "    ")
        feed.write(tostring(root))

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

# --- misc files ---
# stylesheet
shutil.copyfile("styles.css", output_path + "styles.css")
# favicon
shutil.copyfile("favicon.png", output_path + "favicon.png")
# 404
shutil.copyfile("404.html", output_path + "404.html")
# rss
print("! compiling rss feed")
if(compile_rss_feed(output_path + "rss.xml")):
    print("rss -> " + output_path + "rss.xml")