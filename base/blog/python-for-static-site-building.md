---
title: "Python for static site building"
date: December 29, 2025
---

> I wish my posts would stop being meta commentary about developing the 
> site... but I think this is at least slightly better than being a glorified 
> changelog.

I hate needless complexity.

I started my blog using Svelte / SvelteKit and found it to be easy to start
with! But over time, I found it somewhat unwieldly for my use case.
I don't want to rely on a JavaScript runtime like Node.js to build my site,
since all I'm doing is serving JS-free text-only content.

Once I examined what my needs were, I realized that all I need is a 
script that glues HTML files. Header to content, content to footer. That's it.

So I wrote that. I used Python, both for its excellent package ecosystem and
its (relative) portability. I could easily edit and build my site on my Android
phone! I considered C since I've been writing a lot of that lately, but besides
the ugly implementation I'd probably end up writing, things like Markdown parsing
and code highlighting would be a massive burden for me.

Python has tons of ways to make it easy to compile simple sites like mine. I
use:

 - `mistune` for Markdown content parsing
 - `python-frontmatter` for Markdown frontmatter parsing
 - and sooon enough, `pygments` for code highlighting

Far from the 100~ Node modules that get imported as soon as you initialize
even a more lightweight static site generator like 11ty. My site repository shrunk
from 180 megabytes to **78 kilobytes**!