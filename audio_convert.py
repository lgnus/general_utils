
import os, re
from pathlib import Path
import begin

from tqdm import tqdm
from pydub import AudioSegment

def get_audio_files(path):
    """ Obtains the list of all files ending in *mp3|wav|m4b*

    Parameters
    ----------
        path : str
            Path to the folder/file
    Returns
    -------
        sounds : array-like
            Array of paths to each file in the folder / path to unique file
    """
    # make sure it's a valid path
    path = Path(str(path))

    # if path is dir return all the files, else return the single file
    if path.is_dir():
        sounds = [f for f in path.glob('*') if re.search(r'.(mp3|wav|m4b)', f.name)]
    elif path.is_file():
        sounds = [path]
    else:
        print(f'The specified path: {path} is not a valid directory / file') 
    return sounds
    

def scale_and_save_audio(audio_path, output_path, target_dbfs=-40, convert_output=None):
    """ Scales the audio to the provided dBFS and saves the file to output_path.
    If a convert_output is provided, exports the file with the provided extension.

    Parameters
    ----------
        audio_path : str
            path to the audio file
        output_path : str
            path to output directory
        target_dbfs : float
            target volume dbfs
        convert_output : str (mp3, wav, m4b)
            file extension to convert to
    """
    # loads the audio file and scales the dbfs
    audio = AudioSegment.from_file(Path(str(audio_path)))
    dif = target_dbfs - audio.dBFS
    converted_audio = audio + dif

    # if a conversion is provided do it, else use the same as the source
    if convert_output is None:
        converted_audio.export(out_f=f'{output_path}/{audio_path.stem}.{audio_path.suffix[1:]}', format=f'{audio_path.suffix[1:]}')
    else:
        converted_audio.export(out_f=f'{output_path}/{audio_path.stem}.{convert_output}', format=convert_output)


@begin.start
@begin.convert(input_path=str, target_dbfs=float, output_path=str, convert_output=str)
def audio_convert(input_path, target_dbfs, output_path='output', convert_output='mp3'):
    """ Given an input path and a target dBFS, changes all compatible audio files in the input 
    folder (or file) to the intended dBFS. Can optionally provide an output path for the new
    audio files as well as a different file extension.

    Parameters
    ----------
        input_path : str
            path to folder with audio files or a single audio file
        target_dbfs : float
            dBFS the audio should be scaled to
        output_path : str
            path to save the new audio files
        convert_output : str
            file extension to try and convert to (mp3 by default)
    """
    # get the paths to all audio paths to convert
    audio_paths = get_audio_files(input_path)

    # create output_path if it doesn't exist yet
    os.makedirs(output_path, exist_ok=True)

    # iterate each file and convert to the desired volume
    tqdm_ = tqdm(audio_paths, total=len(audio_paths))
    for file_path in tqdm_:
        tqdm_.write(f'{file_path.name}')
        scale_and_save_audio(file_path, output_path, target_dbfs, convert_output)