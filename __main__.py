import markdown2
import sys
import os
import re

mark = markdown2.Markdown()

src = os.path.dirname(os.path.realpath(__file__))+"/src/"
dst = os.path.dirname(os.path.realpath(__file__))+"/dst/"
with open("template.html","r") as f:
    template = f.read()

documentlist = []
namelist = []

for root, subdirs, files in os.walk(src):
    for file in files:
        fpath = os.path.join(root, file)
        with open(fpath,"r") as f:
            rawmarkdown = f.read()
            if(rawmarkdown[0:2] != "# "):
                raise SyntaxError(".md file must begin with a # marked title!")
            documentlist.append(fpath[len(src):].replace(".md",".html").replace("\\","/"))
            namelist.append(rawmarkdown[2:].split("\n",1)[0])
template = template.replace("@DOCUMENTLIST",str(documentlist)).replace("@NAMELIST",str(namelist))
for root, subdirs, files in os.walk(src):
    if(not os.path.exists(dst+root[len(src):])):
        os.mkdir(dst+root[len(src):])
    for file in files:
        fpath = os.path.join(root, file)
        with open(fpath,"r") as f:
            with open(dst+fpath[len(src):].replace(".md",".html"), "w") as r:
                converted = mark.convert(f.read())
                links = re.findall(r'\[\[.+\]\]', converted)
                for link in links:
                    converted = converted.replace(link, "<a href=\""+link[2:-2]+".html\">"+link[2:-2].split("/")[-1]+"</a>")
                r.write(template.replace("@CONTENT",converted))