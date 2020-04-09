import mp3_eq_vol.src.volume_fix.detection as volume_detection
import mp3_eq_vol.src.volume_fix.analysis as volume_analysis
import os.path
from mp3_eq_vol.src.volume_fix.run_async import run_async



class Adjustment():

    @classmethod
    def set_volume(cls, song_list, offset_list, output_dir):

        set_volume_commands=[]
        tasks_names=[]
        for song in song_list:
            filename, offset_dB, output_filepath = song, offset_list[song], os.path.join(output_dir, os.path.split(song)[-1])
            task_command=['ffmpeg','-y', '-i', filename, '-filter:a', "volume=" + str(offset_dB) + "dB",output_filepath]
            set_volume_commands.append(task_command)
            tasks_names.append(song)
        run_async.run_concurent_async(set_volume_commands,tasks_names)


if __name__ == "__main__":
    output_dir='C:\pycharm\mp3_eq_vol\out'
    mypath = 'C:\pycharm\mp3_eq_vol\origin'

    song_list=volume_detection.volume_detection.analyse_volume_from_files(mypath)
    #for song in song_list:
    #    print (song,song_list[song]["mean_volume"],song_list[song]["max_volume"])
    #print("max  mean volume")
    #print(volume_analysis.volume_analysis.find_max_mean_volume(song_list))
    #print("max max volume")
    song_max_volume= volume_analysis.volume_analysis.find_max_max_volume(song_list)
    #print(song_max_volume)
    #maximum_volume=song_list[song]["max_volume"]
    offset_list= volume_analysis.volume_analysis.find_volume_offset_based_on_max_max_volume(song_max_volume, song_list)
    #Adjustment.set_volume(song_list,offset_list,output_dir)
    Adjustment.set_volume(song_list, offset_list, output_dir)
