import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
from PIL import Image

def str2datetime(date_str)-> dt:
    return dt.strptime(date_str, "%y%m%d")

def show_timecourse_img(
    plate_label, well, data_dir, day0="250823", wp_format=6, show_wells=None, maxcols=4
):
    day0 = str2datetime(day0)
    file_lst = sorted(list(data_dir.glob(f"{plate_label}/??????/well_*{well}.tif")))
    div_lst = [(str2datetime(path.parent.stem) - day0).days for path in file_lst]
    
    nrows = len(file_lst)//maxcols + 1
    ncols = maxcols if len(file_lst) > maxcols else len(file_lst)

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(4*ncols, 3*nrows))
    fig.subplots_adjust(wspace=0, top=0.90)
    fig.suptitle(f"{plate_label}, well:{well}")
    for i in range(ncols*nrows):
        r, c = i//ncols, i%ncols
        ax = axs[r,c] if len(file_lst)>maxcols else axs[c]
        if i < len(file_lst):
            path = file_lst[i]
            ax.set_title(f"Day:{div_lst[i]}")
            img = Image.open(path)
            img = img.resize((img.width//4, img.height//4)) # size reduction
            ax.imshow(np.array(img), cmap=plt.cm.gray)
            # ax.text(0,0,div_lst[i], va="top", c="white")
        ax.axis("off")

    plt.show()
    # return file_lst, div_lst