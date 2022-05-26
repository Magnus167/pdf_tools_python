import numpy as np
import PIL.Image as Image
import pdf2image
import sys, os, glob, math
from tqdm import tqdm
from joblib import Parallel, delayed


def get_files(path, ext='pdf'):
    rChar = '/' if sys.platform == 'posix' else '\\'
    return [f.split(rChar)[-1] for f in glob.glob(path + '/*.' + ext.lower())]

def pdf_to_images(pdf_path):
    pages = pdf2image.convert_from_path(pdf_path, dpi=450, fmt='png')
    # for pg in range(len(pages)):
    #     pages[pg].save('out_imgs/' + str(pg) + '.png')
    return [pg for pg in pages]

def save_np_arr_as_img(np_arr, base_filename, index, max_page_count=-1):
    fName = base_filename + '-' + str(index)
    if max_page_count > 0:
        if len(str(index)) < len(str(max_page_count)):
                fName = base_filename + '-' + '0'*(len(str(max_page_count))-len(str(index))) + str(index)

    Image.fromarray(np.uint8(np_arr)).save(fName + '.png')
    return True

def iterate_over_rows(img_np_arr):
    gRows = [row for row in range(img_np_arr.shape[0]-1) if (np.array_equal(img_np_arr[row], img_np_arr[row+1]))]
    gCols = [col for col in range(img_np_arr.shape[1]-1) if (np.array_equal(img_np_arr[:, col], img_np_arr[:, col+1]))]
    new_arr = np.delete(img_np_arr, gRows, axis=0)
    new_arr = np.delete(new_arr, gCols, axis=1)
    return new_arr


def convert(pdfs_path='./pdf_files', out_path='./out_imgs'):
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    files_list = get_files(pdfs_path, 'pdf')
    for pdfFile in tqdm(files_list):
        # outFile = out_path + '/' + pdfFile[:-4] + '.png'
        outFile = out_path + '/' + pdfFile[:-4] 
        images = pdf_to_images(pdfs_path + '/' + pdfFile)
        imgs_count = len(images)
        processed_imgs = Parallel(n_jobs=1, pre_dispatch='n_jobs')(delayed(save_np_arr_as_img)(iterate_over_rows(np.array(images[img].copy())), outFile,img, imgs_count) for img in tqdm(range(len(images))))


    return True

convert('./pdf_files', './out_imgs')


# from joblib import Parallel, delayed
# processed = Parallel(n_jobs=1, pre_dispatch='3*8')(delayed(function)(data) for data in tqdm(data_list))
