

from mp3_eq_vol.src.volume_fix.run_async import run_async
from os import listdir
from os.path import isfile, join, isdir
import re

class volume_detection():


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
    def get_files(cls,mypath) -> []:
        if isfile(mypath)  and mypath[-3:]=="mp3" :
            return [mypath]
        elif isdir(mypath):
            return [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f)) and f[-3:]=="mp3" ]
        else:
            raise FileNotFoundError('Input file or folder not found:'+mypath)


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
    def analyse_volume_from_files(cls,path) ->{}:
        files = cls.get_files(path)
        return cls.get_volume_from_mp3(files)



if __name__ == "__main__":
    mypath = 'C:\\pycharm\\mp3_eq_vol\\origin\\'

    out=volume_detection.analyse_volume_from_files(mypath)
    for key in out:
        print(key)
        print(out[key])

#         print (key,out[key]["mean_volume"],out[key]["max_volume"])

    