

import re
import asyncio
from os import listdir
from os.path import isfile, join, isdir

class volume_detection():
    number_of_concurrent_processes = 3

    @classmethod
    def get_volume_from_mp3_async(cls, files):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        loop = asyncio.get_event_loop()
        semaphore = asyncio.Semaphore(cls.number_of_concurrent_processes)
        async_tasks = (cls.run_as_async(file, semaphore) for file in files)
        all_tasks = asyncio.gather(*async_tasks)
        results = loop.run_until_complete(all_tasks)
        loop.close()
        out = {}
        for output in results:
            for key in output:
                out[key] = output[key]
        return out

    @classmethod
    async def run_as_async(cls, filename, semaphore):
        async with semaphore:
            ffmpeg_args = ['ffmpeg', '-i', "FILE_PATH_HERE", '-af', "volumedetect", '-f', 'null', '/dev/null']
            ffmpeg_args[2] = filename
            proc = await asyncio.create_subprocess_exec(*ffmpeg_args, stdout=asyncio.subprocess.PIPE,
                                                        stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
            output = cls.get_details_from_ffmpeg_output(stderr.decode("utf-8"))
            return {filename: output}

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
        return cls.get_volume_from_mp3_async(files)



if __name__ == "__main__":
    mypath = 'C:\\pycharm\\mp3_eq_vol\\origin\\'

    out=volume_detection.analyse_volume_from_files(mypath)
    # for key in out:
    #     print (key,out[key]["mean_volume"],out[key]["max_volume"])

    