import mp3_eq_vol.src.volume_fix.detection as volume_detection
import mp3_eq_vol.src.volume_fix.analysis as volume_analysis
import os.path
from subprocess import Popen , PIPE
from multiprocessing.dummy import Pool




def set_volume(song_list,offset_list,output_dir):
    #set_volume_args=[]
    set_volume_args = ([song,offset_list[song], os.path.join(output_dir,os.path.split(song)[-1])] for song in song_list)
    # for song in song_list:
    #     filename=os.path.split(song)[-1]
    #     set_volume_args.append([song, offset_list[song], os.path.join(output_dir,filename)])
    run_in_parallel(set_volume_args)

def set_volume_to_mp3(args):
        filename , offset_dB, output_filepath = args[0],args[1],args[2],
        ffmpeg_args=['ffmpeg',  '-i' ,"FILE_PATH_HERE", '-filter:a' ,"volume="+str(offset_dB)+"dB", output_filepath ]
        ffmpeg_args[2]=filename
        p = Popen(ffmpeg_args, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        print(stdout)
        print(stderr)



def run_in_parallel(set_volume_args):
        print("running paralel")
        print(set_volume_args)

        number_of_processes=5
        p = Pool(number_of_processes)  # specify number of concurrent processes
        for output in p.imap(set_volume_to_mp3, set_volume_args):
            pass

if __name__ == "__main__":
    output_dir='C:\pycharm\mp3_eq_vol\output'
    mypath = 'C:\pycharm\mp3_eq_vol\mp3'

    song_list=volume_detection.volume_detection.analyse_volume_from_files(mypath)
    for song in song_list:
        print (song,song_list[song]["mean_volume"],song_list[song]["max_volume"])
    print("max  mean volume")
    print(volume_analysis.find_song_with_max_mean_volume(song_list))
    print("max max volume")
    song_max_volume= volume_analysis.find_song_with_max_max_volume(song_list)
    print(song_max_volume)
    maximum_volume=song_list[song]["max_volume"]
    offset_list= volume_analysis.find_volume_offset_based_on_max_max_volume(maximum_volume, song_list)
    set_volume(song_list,offset_list,output_dir)
