from review.models import PicFile
from review.forms import PicForm

from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from copy import copy
import datetime
import os
import pandas as pd

cur_path = os.path.realpath(__file__)
review = os.path.split(cur_path)[0]
web_pics = os.path.split(review)[0]
PIC_ROOT = os.path.join(web_pics, "review", "static", "review", "pics")
VID_ROOT = os.path.join(web_pics, "review", "static", "review", "videos")
PIC_EXT = [".jpg", ".png", ".bmp"]
VID_EXT = [".mp4", ".mov"]

STATUS = {PicFile.KEEP: "Saved",
          PicFile.DELETE: "To Delete",
          PicFile.UNREVIEWED: "Unreviewed",
          PicFile.CHATBOOKS: "In Chatbooks"
         }

def get_picfile(path, name, root):
    try:
        pf = PicFile.objects.get(path=path, name=name)
    except ObjectDoesNotExist:
        file_path = os.path.join(root, path, name)
        if os.path.isfile(file_path):
            pf = PicFile()
            pf.status = 'UN'
            pf.path = path
            pf.name = name
            filename, ext = os.path.splitext(name)
            if ext in PIC_EXT:
                pf.filetype = PicFile.IMAGE 
            elif ext in VID_EXT:
                pf.filetype = PicFile.VIDEO
                pf.thumbnail = os.path.join("static", "review", "thumbnails",
                                            path, filename + ".jpg")
                thm_path = os.path.join(web_pics, "review", pf.thumbnail)
                if not os.path.isfile(thm_path):
                    os.system(
                        "ffmpeg -ss 00:00:00 -i {0} -frames:v 1 {1}".format(
                        file_path, thm_path)
                    )

            pf.save()
        else:
            pf = None
    return pf


def make_top_path(nodepath):
    npath = os.path.normpath(nodepath)
    comps = npath.split(os.sep)
    top_refs = []
    for i in range(0, len(comps)):
        top_refs.append("/" + "/".join(comps[:i+1]) + "/")
    #top_refs[-1] = top_refs[-1][:-1]
    top_path = zip(comps, top_refs)
    top_path = ["<a href='{0}'>{1}</a>".format(c, r) for r,c in top_path]
    return top_path


def count_files(path, root):
    if path == "/":
        return sum([len(files) for r, d, files, in os.walk(root)])
    return sum([len(files) for r, d, files,
                in os.walk(os.path.join(root, path))])


def get_contents(path, root):
    contents = os.listdir(os.path.join(root, path))
    dirs = [c + '/' for c in contents
            if os.path.isdir(os.path.join(root, path, c))]
    dirs.sort()
    pics = [p for p in contents
            if os.path.isfile(os.path.join(root, path, p))]
    pics.sort()
    return pics, dirs


def view_dir(request, path):
    if path is None:
        path = ''
    pics, dirs = get_contents(path, PIC_ROOT)
    # initializes PicFile for new images
    for p in pics:
        get_picfile(path, p, PIC_ROOT)
    top_path = make_top_path(os.path.join("pics", path))
    up = "/{0}/".format(os.path.split(path)[0])
    if up == "//":
        up = up_path = "/"
    else:
        up_path = up[1:]
    ref = copy(dirs)
    reviewed = PicFile.objects.filter(path__icontains=up_path)
    reviewed = reviewed.exclude(status='UN')

    counts = [str(count_files(os.path.join(path, dr), PIC_ROOT)) for dr in dirs]
    rev_cts = [reviewed.filter(path__icontains=dr[:-1]).count() for dr in dirs]

    table = list(zip(ref, rev_cts, counts))
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
                      "table": table,
                      "formset": formset,
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
    top_path = make_top_path(nodepath)
    time_stamp = os.path.getmtime(os.path.join(PIC_ROOT, nodepath))
    pic_date = datetime.datetime.fromtimestamp(time_stamp)
    year = pic_date.year
    month = pic_date.month
    day = pic_date.day
    path, node = os.path.split(nodepath)
    pf = get_picfile(path, node, PIC_ROOT)
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
    pics, dirs = get_contents(path, PIC_ROOT)
    current = pics.index(node)
    nxt = pics[(current + 1) % len(pics)]
    return redirect("/{0}/{1}".format(path, nxt))


def prev(request, nodepath):
    path, node = os.path.split(nodepath)
    pics, dirs = get_contents(path, PIC_ROOT)
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
    df = pd.read_csv(os.path.join(web_pics, "review", "static",
                                  "county_peaks2.csv"))
    df = df.loc[df['Dir'] != 'none']
    dirs = list(df['Dir'])
    peaks = df['Peak']
    files = []
    for i in range(len(dirs)):
        files.append([os.path.join("static", "mountains", dirs[i], f)
            for f in os.listdir(os.path.join(web_pics, "review", "static",
                                             "mountains", dirs[i]))])
    return render(request, 'testing.html', {"entries": zip(peaks, dirs, files)})


def video(request, nodepath):
    if not os.path.isfile(os.path.join(VID_ROOT, nodepath)):
        return render(request, 'not_found.html', {'url': nodepath}) 
    top_path = make_top_path(nodepath)
    return render(request, 'mov.html')

