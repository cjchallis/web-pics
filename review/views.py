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
        pf = PicFile.objects.get(path=path, name=name)
    except ObjectDoesNotExist:
        if os.path.isfile(os.path.join(PIC_ROOT, path, name)):
            pf = PicFile()
            pf.status = 'UN'
            pf.path = path
            pf.name = name
            pf.save()
        else:
            pf = None
    return pf


def get_contents(path):
    contents = os.listdir(os.path.join(PIC_ROOT, path))
    dirs = [c + '/' for c in contents
            if os.path.isdir(os.path.join(PIC_ROOT, path, c))]
    dirs.sort()
    pics = [p for p in contents
            if os.path.isfile(os.path.join(PIC_ROOT, path, p))]
    pics.sort()
    return pics, dirs

def view_dir(request, path):
    if path is None:
        path = ''
    pics, dirs = get_contents(path)
    # initializes PicFile for new images
    for p in pics:
        get_picfile(path, p)
    up = "/{0}/".format(os.path.split(path)[0])
    if up == "//":
        up = "/"
    text = ["/.."]
    ref = [up]
    text.extend(dirs)
    ref.extend(dirs)
    entries = zip(ref, text)
    PicFormSet = modelformset_factory(PicFile, form=PicForm, max_num = 0)
    if request.method == 'POST':
        formset = PicFormSet(request.POST, request.FILES)
        for form in formset:
            if form.is_valid():
                form.save()
    else:
        formset = PicFormSet(queryset=PicFile.objects.filter(path=path))
    return render(request, 'dir.html', 
                  {
                      "path": path,
                      "entries": entries,
                      "formset": formset
                  })


def home(request):
    return render(request, 'home.html')


def run_del(request):
    to_del = PicFile.objects.filter(status="DL")
    for f in to_del:
        os.remove(os.path.join(PIC_ROOT, f.path, f.name))
        f.delete()
    return redirect('/deletion_list')


def del_list(request):
    to_del = PicFile.objects.filter(status="DL")
    entries = [os.path.join(f.path, f.name) for f in to_del]
    return render(request, 'del_list.html', {"entries": entries})


def chatbooks(request):
    chat = PicFile.objects.filter(status="CH")
    entries = [os.path.join(f.path, f.name) for f in chat]
    return render(request, 'chatbooks.html', {"entries": entries})


def view_img(request, nodepath):
    if not os.path.isfile(os.path.join(PIC_ROOT, nodepath)):
        return render(request, 'not_found.html', {'url': nodepath}) 
    path, node = os.path.split(nodepath)
    pf = get_picfile(path, node)
    status = pf.status
    return render(request, 'img.html', {'path': nodepath,
                                        'img': node,
                                        'folder': path,
                                        'status': STATUS[status]
                                       })


def nxt(request, nodepath):
    path, node = os.path.split(nodepath)
    pics, dirs = get_contents(path)
    current = pics.index(node)
    nxt = pics[(current + 1) % len(pics)]
    return redirect("/{0}/{1}".format(path, nxt))


def prev(request, nodepath):
    path, node = os.path.split(nodepath)
    pics, dirs = get_contents(path)
    current = pics.index(node)
    nxt = pics[(current - 1) % len(pics)]
    return redirect("/{0}/{1}".format(path, nxt))


def modify(request, nodepath, mod):
    path, node = os.path.split(nodepath)
    querySet = PicFile.objects.filter(path=path, name=node)
    if not querySet:
        pic = PicFile()
        pic.path = path
        pic.name = node
    else:
        pic = querySet[0]
    pic.status = mod
    pic.save()
    return redirect("/" + nodepath)

