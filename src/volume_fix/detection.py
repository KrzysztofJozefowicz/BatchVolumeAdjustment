
import subprocess
from multiprocessing.dummy import Pool
import re

from os import listdir
from os.path import isfile, join, isdir

class volume_detection():
    @classmethod
    def get_files(cls,mypath) -> []:
        if isfile(mypath)  and mypath[-3:]=="mp3" :
            return [mypath]
        elif isdir(mypath):
            return [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f)) and f[-3:]=="mp3" ]
        else:
            raise FileNotFoundError

    @classmethod
    def get_volume_from_mp3(cls,filename) -> {}:
        ffmpeg_args=['ffmpeg',  '-i' ,"FILE_PATH_HERE", '-af' ,"volumedetect",  '-f', 'null', '/dev/null']
        ffmpeg_args[2]=filename
        output=subprocess.check_output(ffmpeg_args,stderr=subprocess.STDOUT)
        tmp={}
        tmp[filename]=cls.get_details_from_ffmpeg_output(output.decode("utf-8"))
        return tmp

    @classmethod
    def run_in_parallel(cls,filenames) -> {}:
        out={}
        number_of_processes=5
        p = Pool(number_of_processes)  # specify number of concurrent processes

        for output in p.imap(cls.get_volume_from_mp3, filenames):  # provide filenames
             for key in output:
                 out[key]=output[key]
        return out

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
            output["max_volume"] = None
        return(output)

    @classmethod
    def analyse_volume_from_files(cls,path) ->{}:
        files = cls.get_files(path)
        return cls.run_in_parallel(files)



if __name__ == "__main__":
    mypath = 'C:\\pycharm\\mp3_eq_vol\\origin\\'

    out=volume_detection.analyse_volume_from_files(mypath)
    # for key in out:
    #     print (key,out[key]["mean_volume"],out[key]["max_volume"])

    