

from mp3_eq_vol.src.volume_fix.run_async import run_async
from os import listdir
from os.path import isfile, join, isdir
import re

class volume_detection():
    allowed_file_extensions=set(["mp3"])

    @classmethod
    def get_volume_from_mp3(cls, files):

        cmd_list=[]
        for file in files:
            cmd = ['ffmpeg', '-i', file, '-af', "volumedetect", '-f', 'null', '/dev/null']
            cmd_list.append(cmd)

        results = run_async.run_concurent_async(cmd_list,files)
        out = {}
        for output in results:
            for key in output:
                out[key] = cls.get_details_from_ffmpeg_output(output[key])
                #out key = filename
                #out value: {mean_volume:[float], max_volume: [float]}
        return out



    @classmethod
    def get_files(cls,*file_paths) -> []:
        files=[]
        for path in file_paths:
            if isfile(path)  and path[-3:] in cls.allowed_file_extensions:
                files.append(path)

            elif isdir(path):
                for f in listdir(path):
                    if isfile(join(path, f)) and f[-3:] in cls.allowed_file_extensions:
                        files.append(join(path, f))

            else:
                raise FileNotFoundError('Input file or folder not found: '+path)
        return list(set(files))


    @classmethod
    def get_details_from_ffmpeg_output(cls,ffmpeg_output) -> {}:
        output={}
        try:
            output["mean_volume"]=float(re.search("mean_volume:\s(.*)\sdB",ffmpeg_output)[1])
        except:
            return None
        try:
            output["max_volume"] =float( re.search("max_volume:\s(.*)\sdB", ffmpeg_output)[1])
        except:
            return None
        return(output)

    @classmethod
    def analyse_volume_from_files(cls,*paths) ->{}:
        files = cls.get_files(*paths)
        return cls.get_volume_from_mp3(files)



if __name__ == "__main__":
    mypath = 'C:\\pycharm\\mp3_eq_vol\\origin\\'

    out=volume_detection.analyse_volume_from_files([mypath])
    for key in out:
        print(key)
        print(out[key])

#         print (key,out[key]["mean_volume"],out[key]["max_volume"])

    