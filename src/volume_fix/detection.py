
import sys
from os.path import isfile, join, isdir, dirname
import os
current_path=dirname(os.path.realpath(__file__))
sys.path.insert(0,os.path.join(current_path,'../../..'))
from mp3_eq_vol.src.volume_fix.run_async import run_async
from os import walk
import re
import argparse

class volume_detection():
    allowed_file_extensions=set(["mp3"])

    @classmethod
    def get_volume_from_mp3(cls, files):

        cmd_list=[]
        for file in files:
            cmd = ['ffmpeg', '-i', file, '-af', "volumedetect", '-f', 'null', '/dev/null']
            cmd_list.append(cmd)

        print("Running volume detection:")
        results = run_async.run_concurent_async(cmd_list,files)
        print("Done volume detection.")
        out = {}
        for output in results:
            for key in output:
                out[key] = cls.get_details_from_ffmpeg_output(output[key])
        return out



    @classmethod
    def get_files(cls,*file_paths) -> []:
        files=[]
        for path in file_paths:
            if isfile(path)  and path[-3:] in cls.allowed_file_extensions:
                files.append(path)

            elif isdir(path):
                for (dirpath, dirnames, filenames) in walk(path):
                    for f in filenames:
                        if isfile(join(dirpath, f)) and f[-3:] in cls.allowed_file_extensions:
                            files.append(join(dirpath, f))

            else:
                raise FileNotFoundError('Input file or folder not found: '+path)
        return list(set(files))


    @classmethod
    def get_details_from_ffmpeg_output(cls,ffmpeg_output) -> {}:
        output={}
        try:
            output["mean_volume"]=float(re.search("mean_volume:\s(.*)\sdB",ffmpeg_output)[1])
        except:
            output["mean_volume"]=None
        try:
            output["max_volume"] =float( re.search("max_volume:\s(.*)\sdB", ffmpeg_output)[1])
        except:
            output["max_volume"]=None
        return(output)

    @classmethod
    def sanitize_input_paths(cls,input_param):

        if type(input_param) is list:
            return input_param

        if isfile(input_param) and input_param[-3:] == "txt":
            with open(input_param, 'r') as text_file:
                return [line.strip() for line in text_file]
        else:
            return [input_param]

    @classmethod
    def detect_volume_from_files(cls, paths) ->{}:
        paths=cls.sanitize_input_paths(paths)
        files = cls.get_files(*paths)
        return cls.get_volume_from_mp3(files)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    my_parser = parser.add_mutually_exclusive_group()
    my_parser.add_argument('--paths' ,nargs='*', help='path to files/folder to detect volume stats')
    my_parser.add_argument('--file',dest="file", nargs=1,
                        help='path to file that holds paths to detect volume stats')
    parser.parse_args()
    args = parser.parse_args()
    if args.paths is None and args.file is None:
        print("There should be either --path or --file parameter provided.")
        exit(-1)
    mypath=args.paths if args.paths is not None else args.file[0]
    if mypath != None:
        detected_volumes=volume_detection.detect_volume_from_files(mypath)
        for file in detected_volumes:
            print(file,'max volume:',detected_volumes[file]["max_volume"],'mean volume:',detected_volumes[file]["mean_volume"])
