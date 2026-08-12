---
title: The second redesign
date: August 11, 2026
---

Just made a site style update. I took some inspiration from the look of the
[Bear](https://bearblog.dev/) home page and then copied the colors from my favorite
programming color scheme [Alabaster](https://github.com/tonsky/sublime-scheme-alabaster)!

I think it looks pretty now.

Also took the time to integrate `pygments` into my build script, and thanks
to Alabaster's conservative use of colors, I only need to add a few extra
lines of rules onto my stylesheet for my ideal syntax highlighting:

```css
/* not too many bytes... */
.c,.cm { color: #AA3731 }
.nf { color: #325CC0 }
.s { color: #448C27 }
.mi, .mh { color: #7A3E9D }
.se { color: #777 }
```

Unfortunately, it does bloat the final rendered HTML with a bunch of `<span>` tags
that end up being styled the same, but I see it as fair tradeoff for the time being.
