from review.models import PicFile
from review.forms import PicForm

from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
import datetime
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


def count_files(path):
    if path == "/":
        return sum([len(files) for r, d, files, in os.walk(PIC_ROOT)])
    return sum([len(files) for r, d, files,
                in os.walk(os.path.join(PIC_ROOT, path))])


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
    npath = os.path.normpath(path)
    comps = npath.split(os.sep)
    top_refs = []
    for i in range(0, len(comps)):
        top_refs.append("/" + "/".join(comps[:i+1]) + "/")
    top_path = zip(comps, top_refs)
    top_path = ["<a href='{0}'>{1}</a>".format(c, r) for r,c in top_path]
    #top_path = ["{0}{1}".format(c, r) for r,c in top_path]
    if up == "//":
        up = "/"
    text = []
    ref = []
    text.extend(dirs)
    ref.extend(dirs)
    if up == "/":
        up_path = "/"
    else:
        up_path = up[1:]
    counts = []
    reviewed = PicFile.objects.filter(path__icontains=up_path)
    reviewed = reviewed.exclude(status='UN')
    rev_counts = []
    table = list()
    for q in reviewed:
        print(q.path + '/' + q.name)
    for dr in dirs:
        print(dr[:-1])
        counts.append(count_files(os.path.join(path, dr)))
        rev_counts.append(reviewed.filter(path__icontains=dr[:-1]).count())
        print(reviewed.filter(path__icontains=dr))
    for i in range(0, len(text)):
        table.append([text[i], str(rev_counts[i]), str(counts[i])])
    entries = zip(ref, table)
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
                      "top_path": top_path,
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
    npath = os.path.normpath(nodepath)
    comps = npath.split(os.sep)
    top_refs = []
    for i in range(0, len(comps)):
        top_refs.append("/" + "/".join(comps[:i+1]) + "/")
    top_refs[-1] = top_refs[-1][:len(top_refs[-1])-1]
    top_path = zip(comps, top_refs)
    top_path = ["<a href='{0}'>{1}</a>".format(c, r) for r,c in top_path]
    time_stamp = os.path.getmtime(os.path.join(PIC_ROOT, nodepath))
    pic_date = datetime.datetime.fromtimestamp(time_stamp)
    year = pic_date.year
    month = pic_date.month
    day = pic_date.day
    path, node = os.path.split(nodepath)
    pf = get_picfile(path, node)
    status = pf.status
    PicFormSet = modelformset_factory(PicFile, form=PicForm, max_num = 0)
    if request.method == 'POST':
        formset = PicFormSet(request.POST, request.FILES)
        for form in formset:
            if form.is_valid():
                form.save()
    else:
        formset = PicFormSet(
            #queryset=PicFile.objects.filter(path=path)
            queryset=PicFile.objects.filter(path=path).filter(name=node)
        )
    return render(request, 'img.html', {'top_path': top_path,
                                        'path': nodepath,
                                        'img': node,
                                        'folder': path,
                                        'status': STATUS[status],
                                        'formset': formset,
                                        'year': year,
                                        'month': month,
                                        'day': day
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


def testing(request):
    return render(request, 'testing.html')


def video(request):
    return render(request, 'mov.html')

