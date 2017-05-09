from review.models import PicFile
from review.forms import PicForm

from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
import os

cur_path = os.path.realpath(__file__)
review = os.path.split(cur_path)[0]
web_pics = os.path.split(review)[0]
PIC_ROOT = os.path.join(web_pics, "review", "static")

STATUS = {PicFile.KEEP: "Saved",
          PicFile.DELETE: "To Delete",
          PicFile.UNREVIEWED: "Unreviewed",
          PicFile.CHATBOOKS: "In Chatbooks"
         }

def get_picfile(path, name):
    try:
        pf = PicFile.objects.get(path=path, name=node)
    except ObjectDoesNotExist:
        pf = PicFile()
        pf.status = 'UN'
        pf.path = path
        pf.name = node
        pf.save()
    return pf


def test_forms(request, path):
    if path is None:
        path = ''
    contents = os.listdir(os.path.join(PIC_ROOT, path))
    dirs = [c + '/' for c in contents
            if os.path.isdir(os.path.join(PIC_ROOT, path, c))]
    dirs.sort()
    link = '<a href="{0}">{1}</a>'
    up = os.path.split(path)[0]
    if up == "":
        entries = ['<a href="/">/..</a>']
    else:
        entries = ['<a href="/{0}/">/..</a>'.format(up)]
    entries.extend([link.format(d, d) for d in dirs])
    relpath = path 
    abspath = os.path.join(PIC_ROOT, relpath)
    pics = [p for p in os.listdir(abspath)
            if os.path.isfile(os.path.join(abspath, p))]
    for p in pics:
        get_picfile(path, p)
    PicFormSet = modelformset_factory(PicFile, form=PicForm, max_num = 0)
    if request.method == 'POST':
        formset = PicFormSet(request.POST, request.FILES)
        for form in formset:
            if form.is_valid():
                form.save()
    else:
        formset = PicFormSet(
            queryset=PicFile.objects.filter(path=relpath))
    return render(request, 'test_forms.html', 
                  {
                      "entries": entries,
                      "formset": formset
                  })


def home(request):
    return render(request, 'home.html')


def run_del(request):
    to_del = PicFile.objects.filter(status="DL")
    for f in to_del:
        os.remove(os.path.join(PIC_ROOT, f.path))
        f.delete()
    return redirect('/deletion_list')


def del_list(request):
    to_del = PicFile.objects.filter(status="delete")
    entries = [f.path for f in to_del]
    args = {"entries": entries}
    return render(request, 'del_list.html', args)


def view_dir(request, path):
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
    up = os.path.split(path)[0]
    if up == "":
        entries = ['<a href="/">/..</a>']
    else:
        entries = ['<a href="/{0}/">/..</a>'.format(up)]
    # dirs_pics = dirs + pics
    dirs_pics = dirs
    entries.extend([link.format(e, e) for e in dirs_pics])
    pic_paths = [os.path.join(path, p) for p in pics]
    args = {"entries": entries, "pics": pics, "path": path}
    return render(request, 'dir.html', args)
   

def view_img(request, nodepath):
    path, node = os.path.split(nodepath)
    try:
        pf = PicFile.objects.get(path=path, name=node)
    except ObjectDoesNotExist:
        pf = PicFile()
        pf.status = 'UN'
        pf.path = path
        pf.name = node
        pf.save()
    status = pf.status
    return render(request, 'img.html', {'path': nodepath,
                                        'img': node,
                                        'folder': path,
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

