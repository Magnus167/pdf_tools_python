from merge_pdf import merge
import glob, os
output_file, in_folder = 'merged_files.pdf', './imgs_as_pdfs/'
files_list=glob.glob(in_folder+'/*.pdf')
# if output_file exists, delete it
if os.path.exists(output_file):
    input('Output file exists. Press Enter to delete it and continue; or Ctrl+C to exit.')
    os.remove(output_file)
merge.Merge(output_file, debug= True).merge_file_list(files_list)
# input(" >> Press Enter to Exit. Lol. Enter to exit. HAHAHAHA >>")