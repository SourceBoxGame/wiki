import markdown2
import sys
import os
import re
import shutil

mark = markdown2.Markdown()

rootpath = os.path.dirname(os.path.realpath(__file__))
src = rootpath+"/src/"
lensrc = len(src)
dst = rootpath+"/dst/"
assets = rootpath+"/assets/"
shutil.rmtree(dst)
shutil.copytree(assets,dst)
with open("template.html","r") as f:
    template = f.read()

documentlist = []
namelist = []
filetreedict = {}
filetree = ""

for root, subdirs, files in os.walk(src):
    p = filetreedict
    if root[lensrc:]:
        for x in root[lensrc:].replace("\\","/").split("/"):
            p = p.setdefault(x, {})
    p[''] = []
    for file in files:
        fpath = os.path.join(root, file)
        with open(fpath,"r") as f:
            rawmarkdown = f.read()
            if(rawmarkdown[0:2] != "# "):
                raise SyntaxError(".md file must begin with a # marked title!")
            name = rawmarkdown[2:].split("\n",1)[0]
            p[''].append([os.path.join(root[lensrc:],file.replace(".md","")).replace("\\","/"),name])
            documentlist.append("/wiki/"+fpath[len(src):].replace(".md",".html").replace("\\","/"))
            namelist.append(name)

def IterateFileTree(filedict):
    global filetree
    for key, value in filedict.items():
        if isinstance(value, dict):
            filetree += f"<li><small class=\"liicon\">+</small><b onclick=\"toggleTree(this);\">{key}</b>\n<ul class=\"nested\">\n"
            IterateFileTree(value)
            filetree += f"</ul>\n</li>\n"
        else:
            for file in value:
                filetree += f"<li><a href=\"/wiki/{file[0]}.html\">{file[1]}</a></li>\n"

IterateFileTree(filetreedict)

def FindFile(name):
    for root, subdirs, files in os.walk(src):
        if name in files:
            return os.path.join(root[lensrc:],name)
    raise SyntaxError(f"Could not find file {name}!")

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
                links = re.findall(r'\[\[[^\[^\]]+\]\]', rawmarkdown)
                for link in links:
                    if os.path.exists(os.path.join(src,link[2:-2]+".md")):
                        rawmarkdown = rawmarkdown.replace(link, "<a href=\"/wiki/"+link[2:-2]+".html\">"+link[2:-2].split("/")[-1]+"</a>")
                    else:
                        foundpath = FindFile(link[2:-2]+".md").replace(".md","").replace("\\","/")
                        rawmarkdown = rawmarkdown.replace(link, "<a href=\"/wiki/"+foundpath+".html\">"+foundpath.split("/")[-1]+"</a>")
                links = re.findall(r'\[[^\[^\]]+\]\[[^\[^\]]+\]',rawmarkdown)
                for link in links:
                    name = link[1:].split("]",1)[0]
                    href = link[1:].split("[",1)[1].split("]",1)[0]
                    if(href.startswith("http://") or href.startswith("https://")):
                        rawmarkdown = rawmarkdown.replace(link, "<a href=\""+href+"\">"+name+"</a>")
                    elif os.path.exists(os.path.join(src,href+".md")):
                        rawmarkdown = rawmarkdown.replace(link, "<a href=\"/wiki/"+href+".html\">"+name+"</a>")
                    else:
                        foundpath = FindFile(href+".md").replace(".md","").replace("\\","/")
                        rawmarkdown = rawmarkdown.replace(link, "<a href=\"/wiki/"+foundpath+".html\">"+name+"</a>")
                converted = mark.convert(rawmarkdown)
                r.write(template.replace("@CONTENT",converted).replace("@FILETREE",filetree))