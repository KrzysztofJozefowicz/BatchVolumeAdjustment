import argparse
import sys
import os
current_path=os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,os.path.join(current_path,'../../..'))
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
        print("Running volume adjustment:")
        run_async.run_concurent_async(set_volume_commands,tasks_names)
        print("Done volume adjustment, files unser:"+output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir',required=True, help="output dir")
    my_parser = parser.add_mutually_exclusive_group()
    my_parser.add_argument('--paths', nargs='*', help='path to files/folder to detect volume stats')
    my_parser.add_argument('--file', dest="file", nargs=1,
                           help='path to file that holds paths to detect volume stats')
    parser.parse_args()
    args = parser.parse_args()
    if args.paths is None and args.file is None:
        print("There should be either --path or --file parameter provided.")
        exit(-1)
    if os.path.isdir(args.output_dir) == False:
        print("Output dir "+args.output_dir+" does not exist.")
        exit(-1)
    else:
        mypath = args.paths if args.paths != None else args.file[0]
        song_list=volume_detection.volume_detection.detect_volume_from_files(mypath)
        song_max_volume= volume_analysis.volume_analysis.find_max_max_volume(song_list)
        offset_list= volume_analysis.volume_analysis.find_volume_offset_based_on_max_max_volume(song_max_volume, song_list)
        Adjustment.set_volume(song_list, offset_list, args.output_dir)
