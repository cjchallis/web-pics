import os

cur_path = os.path.split(os.path.realpath(__file__))[0]
pic_root = os.path.join(cur_path, "static", "review", "pics")
thumb_root = os.path.join(cur_path, "static", "review", "thumbnails")


pic_ext = [".png", ".jpg", ".bmp", ".gif"]

for subdir, dirs, files in os.walk(pic_root):
    sub = os.path.relpath(subdir, pic_root)
    for f in files:
        if os.path.splitext(f)[1].lower() in pic_ext:
            thumb = os.path.join(thumb_root, sub, f)
            pic = os.path.join(pic_root, sub, f)
            if not os.path.exists(thumb):
                d = os.path.join(thumb_root, sub)
                if not os.path.exists(d):
                    os.mkdir(d)
                os.system("convert -thumbnail 300 '{0}' '{1}'".format(pic, thumb))

