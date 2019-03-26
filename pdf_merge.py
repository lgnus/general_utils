import os
import re
from pathlib import Path
import begin
import fitz

__author__ = 'lgnus'


def numeric(filepath):
    """ Obtains the integer part of a string, if none, return 0

    Parameters
    ----------
        filepath : pathlib.Path
            filepath
    """
    regex_pattern = re.compile(r'\d+')
    try:
        return int(re.findall(regex_pattern, str(filepath.stem))[0])
    except:
        return 0


@begin.start
@begin.convert(input_path=str, output_path=str, filename=str)
def pdf_merger(input_path, output_path, filename='merged_file'):
    """ Creates a new pdf document that is the result of the merging
    of all the documents from the provided folder.

    Parameters
    ----------
        input_path : str
            input path to pdf files (should be a folder)
        output_path : str
            output path to folder (should be a folder)
        filename : str
            output filename
    """
    # get all pdf files from input folder and create the output folder if
    # it doesn't exist yet
    os.makedirs(output_path, exist_ok=True)
    path = Path(str(input_path))

    # create a new empty pdf, load the pdfs from folder and
    # append them to the empty document
    merged = fitz.Document()
    for pdf in sorted([file for file in path.glob('*.pdf')], key=numeric):
        merged.insertPDF(fitz.open(pdf))

    merged.save(str(Path(output_path) / f'{filename}.pdf'))
