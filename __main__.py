import markdown2
import sys
import os
import re
import shutil

mark = markdown2.Markdown(extras={"tables":True,"fenced-code-blocks":None,"code-friendly":True,"break-on-newline":True})

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
        if file.endswith(".embed.md"):
            continue
        fpath = os.path.join(root, file)
        with open(fpath,"r") as f:
            rawmarkdown = f.read()
            if(rawmarkdown[0:2] != "# "):
                raise SyntaxError(".md file must begin with a # marked title!")
            name = rawmarkdown[2:].split("\n",1)[0]
            p[''].append([os.path.join(root[lensrc:],file.replace(".md","")).replace("\\","/"),name])
            documentlist.append("/wiki/"+fpath[len(src):].replace(".md",".html").replace("\\","/"))
            namelist.append(name)

def IterateFileTree(filedict,path,parentexpanded):
    global filetree
    currentfile = path[1:].replace(".md","")
    for key, value in filedict.items():
        if isinstance(value, dict):
            classname = "nested"
            expandicon = "+"
            expanded = False
            if "/"+key+"/" in path and parentexpanded:
                classname += " active"
                expandicon = "-"
                expanded = True
            
            filetree += f"<li class=\"sidebar\"><small class=\"liicon\">{expandicon}</small><span onmousedown=\"toggleTree(this);\" onmouseleave=\"unPress(this);\" onmouseup=\"unPress(this);\"><span onmousedown=\"Press(this);\" onmouseleave=\"unPress(this);\" onmouseup=\"unPress(this);\">{key}</span></span>\n<ul class=\"sidebar {classname}\">\n"
            IterateFileTree(value,path,expanded)
            filetree += f"</ul>\n</li>\n"
        else:
            for file in value:
                if file[0] == currentfile:
                    filetree += f"<li class=\"sidebar\"><b>{file[1]}</b></li>\n"
                else:
                    filetree += f"<li class=\"sidebar\"><a href=\"/wiki/{file[0]}.html\">{file[1]}</a></li>\n"

def FindFile(name):
    for root, subdirs, files in os.walk(src):
        if name in files:
            return os.path.join(root[lensrc:],name)
    raise SyntaxError(f"Could not find file {name}!")

def ConvertToHtml(fpath):
    with open(fpath,"r") as f:
        rawmarkdown = f.read().replace("\r\n","\n")
        smalls = re.findall(r"^\$\_SMALL\s[\s\S]+\s\_\$$",rawmarkdown,re.MULTILINE)
        for small in smalls:
            rawmarkdown = rawmarkdown.replace(small, "<small style=\"position:relative; top:8px;\">"+small[2:-2]+"</small>")
        frames = re.findall(r"^\$_FRAME\s[\S\s]+\s_\$$",rawmarkdown,re.MULTILINE)
        for frame in frames:
            framed_string = frame[8:-3]
            rawmarkdown = rawmarkdown.replace(frame,f"<div class=\"framed\"><div class=\"framed\">{framed_string}</div></div>")
        links = re.findall(r'\[\[[^\[^\]]+\]\]', rawmarkdown)
        for link in links:
            if os.path.exists(os.path.join(src,link[2:-2]+".md")):
                rawmarkdown = rawmarkdown.replace(link, "<a href=\"/wiki/"+link[2:-2]+".html\">"+link[2:-2].split("/")[-1]+"</a>")
            else:
                foundpath = FindFile(link[2:-2]+".md").replace(".md","").replace("\\","/")
                rawmarkdown = rawmarkdown.replace(link, "<a href=\"/wiki/"+foundpath+".html\">"+foundpath.split("/")[-1]+"</a>")
        embeds = re.findall(r'\{\{[^\{^\}]+\}\}', rawmarkdown)
        for embed in embeds:
            if os.path.exists(os.path.join(src,embed[2:-2]+".embed.md")):
                rawmarkdown = rawmarkdown.replace(embed, ConvertToHtml(src+embed[2:-2]+".embed.md"))
            else:
                foundpath = FindFile(embed[2:-2]+".embed.md").replace("\\","/")
                rawmarkdown = rawmarkdown.replace(embed, ConvertToHtml(src+foundpath))
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
        return converted
        

template = template.replace("@DOCUMENTLIST",str(documentlist)).replace("@NAMELIST",str(namelist))

for root, subdirs, files in os.walk(src):
    if(not os.path.exists(dst+root[len(src):])):
        os.mkdir(dst+root[lensrc:])
    for file in files:
        if file.endswith(".embed.md"):
            continue
        fpath = os.path.join(root, file)
        filetree = ""
        IterateFileTree(filetreedict,"/"+os.path.join(root[lensrc:], file).replace("\\","/"), True)
        with open(dst+fpath[len(src):].replace(".md",".html"), "w") as r:
            converted = ConvertToHtml(fpath)
            r.write(template.replace("@CONTENT",converted).replace("@FILETREE",filetree))