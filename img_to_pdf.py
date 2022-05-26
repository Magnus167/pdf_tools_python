import img2pdf, glob, os
from tqdm import tqdm

def main(input_folder='./out_imgs', output_folder='./imgs_as_pdfs'):
    os.makedirs(output_folder, exist_ok=True)
    for img in tqdm(glob.glob(input_folder + '/*.png')):
        with open(img, 'rb') as fImg:
            pdf = img2pdf.convert(fImg)
            imgName = img.split('\\')[-1]
            with open(f'{output_folder}/{imgName[:-4]}.pdf', 'wb') as fPdf:
                fPdf.write(pdf)
main()