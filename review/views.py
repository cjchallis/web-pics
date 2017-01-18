from django.shortcuts import render
import os

def home_page(request):
    pic_root = os.path.join("/", "home", "pi", "tdd", "web_pics", "pics")
    dirs = os.listdir(pic_root)
    dirs.sort()
    link = '<a href="{0}">{0}</a>'
    keys = ['item' + str(i) for i in range(len(dirs))]
    values = [link.format(d) for d in dirs]
    args = dict(zip(keys, values))
    return render(request, 'home.html', args) 

