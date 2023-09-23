import markdown2
import sys
import os
import re
import shutil

mark = markdown2.Markdown()

src = os.path.dirname(os.path.realpath(__file__))+"/src/"
dst = os.path.dirname(os.path.realpath(__file__))+"/dst/"
shutil.rmtree(dst)
os.mkdir(dst)
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
            documentlist.append("/wiki/"+fpath[len(src):].replace(".md",".html").replace("\\","/"))
            namelist.append(rawmarkdown[2:].split("\n",1)[0])
template = template.replace("@DOCUMENTLIST",str(documentlist)).replace("@NAMELIST",str(namelist))
for root, subdirs, files in os.walk(src):
    if(not os.path.exists(dst+root[len(src):])):
        os.mkdir(dst+root[len(src):])
    for file in files:
        fpath = os.path.join(root, file)
        with open(fpath,"r") as f:
            with open(dst+fpath[len(src):].replace(".md",".html"), "w") as r:
                rawmarkdown = f.read().replace("\r\n","\n")
                smalls = re.findall(r"^\S+\n[(    )\t]",rawmarkdown,re.MULTILINE)
                for small in smalls:
                    smallstring = small.strip()
                    whitespace = small[len(smallstring):]
                    rawmarkdown = rawmarkdown.replace(small, "<small style=\"position:relative; top:16px;\">"+smallstring+"</small>\n"+whitespace)
                converted = mark.convert(rawmarkdown)
                links = re.findall(r'\[\[.+\]\]', converted)
                for link in links:
                    converted = converted.replace(link, "<a href=\"/wiki/"+link[2:-2]+".html\">"+link[2:-2].split("/")[-1]+"</a>")
                links = re.findall(r'\[.+\]\[.+\]',converted)
                for link in links:
                    name = link[1:].split("]",1)[0]
                    href = link[1:].split("[",1)[1].split("]",1)[0]
                    converted = converted.replace(link, "<a href=\"/wiki/"+href+".html\">"+name+"</a>")
                r.write(template.replace("@CONTENT",converted))