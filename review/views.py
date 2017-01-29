from django.shortcuts import render
import os
PIC_ROOT = os.path.join("/", "home", "pi", "tdd", "web_pics", "pics") 

def home_page(request):
    dirs = os.listdir(PIC_ROOT)
    dirs.sort()
    link = '<a href="{0}">{0}</a>'
    entries = [link.format(d) for d in dirs]
    args = {"entries": entries}
    return render(request, 'home.html', args) 

def view_dir(request, empty, path):
    if path is None:
        path = ''
    contents = os.listdir(os.path.join(PIC_ROOT, path))
    print(os.path.join(PIC_ROOT, path))
    dirs = [c + '/' for c in contents
            if os.path.isdir(os.path.join(PIC_ROOT, path, c))]
    dirs.sort()
    pics = [c for c in contents
            if os.path.isfile(os.path.join(PIC_ROOT, path, c))]
    pics.sort()
    link = '<a href="{0}">{1}</a>'
    dirs_pics = dirs + pics
    entries = [link.format(e, e) for e in dirs_pics]
    print(entries)
    args = {"entries": entries}
    return render(request, 'home.html', args)
   
