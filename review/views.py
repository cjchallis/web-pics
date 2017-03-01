from review.models import PicFile

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
import os
PIC_ROOT = os.path.join("/", "home", "pi", "tdd", "web_pics", "review",
                        "static") 
STATUS = {"keep": "Saved",
          "delete": "To Delete",
          "Unreviewed": "Unreviewed"
         }

def view_dir(request, empty, path):
    if path is None:
        path = ''
    contents = os.listdir(os.path.join(PIC_ROOT, path))
    dirs = [c + '/' for c in contents
            if os.path.isdir(os.path.join(PIC_ROOT, path, c))]
    dirs.sort()
    pics = [c for c in contents
            if os.path.isfile(os.path.join(PIC_ROOT, path, c))]
    pics.sort()
    link = '<a href="{0}">{1}</a>'
    dirs_pics = dirs + pics
    entries = [link.format(e, e) for e in dirs_pics]
    args = {"entries": entries}
    return render(request, 'home.html', args)
   

def view_img(request, nodepath):
    try:
        pf = PicFile.objects.get(path = nodepath)
    except ObjectDoesNotExist:
        pf = PicFile()
        pf.status = 'Unreviewed'
        pf.save()
    status = pf.status
    img = os.path.split(nodepath)[1]
    return render(request, 'img.html', {'path': nodepath,
                                        'img': img,
                                        'status': STATUS[status]
                                       })


def nxt(request, nodepath):
    path, node = os.path.split(nodepath)
    contents = os.listdir(os.path.join(PIC_ROOT, path))
    dirs = [c + '/' for c in contents
            if os.path.isdir(os.path.join(PIC_ROOT, path, c))]
    dirs.sort()
    pics = [c for c in contents
            if os.path.isfile(os.path.join(PIC_ROOT, path, c))]
    pics.sort()
    current = pics.index(node)
    nxt = pics[(current + 1) % len(pics)]
    return redirect("/{0}/{1}".format(path, nxt))


def prev(request, nodepath):
    path, node = os.path.split(nodepath)
    contents = os.listdir(os.path.join(PIC_ROOT, path))
    dirs = [c + '/' for c in contents
            if os.path.isdir(os.path.join(PIC_ROOT, path, c))]
    dirs.sort()
    pics = [c for c in contents
            if os.path.isfile(os.path.join(PIC_ROOT, path, c))]
    pics.sort()
    current = pics.index(node)
    nxt = pics[(current - 1) % len(pics)]
    return redirect("/{0}/{1}".format(path, nxt))


def modify(request, nodepath, mod):
    querySet = PicFile.objects.filter(path=nodepath)
    if not querySet:
        pic = PicFile()
        pic.path = nodepath
    else:
        pic = querySet[0]
    pic.status = mod
    pic.save()
    return redirect("/" + nodepath)

