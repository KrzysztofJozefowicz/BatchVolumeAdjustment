import pytest
import os
import mp3_eq_vol.src.volume_fix.analysis as volume_analysis
import mp3_eq_vol.src.volume_fix.detection as volume_detection
import mp3_eq_vol.src.volume_fix.adjustment as volume_adjustment
from pathlib import Path




class Test_Adjustment_E2E():
    @classmethod
    def prepare_song_list(self):
        current_path = Path(__file__).parent.absolute()
        test_data_input_folder = Path.joinpath(current_path, "test_data", "test_input")
        test_data_output_folder = Path.joinpath(current_path, "test_data", "test_output")
        song_1 = str(Path.joinpath(test_data_input_folder ,"file_example_MP3_1MG.mp3"))
        song_2 = str(Path.joinpath(test_data_input_folder ,"file_example_MP3_700KB_broken_file.mp3"))
        song_3 = str(Path.joinpath(test_data_input_folder, "SoundHelix-Song-1.mp3"))

        test_data_subfolder=str(Path.joinpath(test_data_input_folder ,'subfolder'))
        return { '3_songs':[song_1,song_2,song_3],'song_1':song_1, 'song_2':song_2, 'song_3':song_3, 'test_data_input_folder' :test_data_input_folder, 'test_data_subfolder':test_data_subfolder,'test_data_output_folder':test_data_output_folder}


    def test_adjustment_E2E_files_list(self):
        setup = Test_Adjustment_E2E.prepare_song_list()
        song_list = volume_detection.volume_detection.analyse_volume_from_files(setup['3_songs'])
        song_max_volume = volume_analysis.volume_analysis.find_max_max_volume(song_list)
        offset_list = volume_analysis.volume_analysis.find_volume_offset_based_on_max_max_volume(song_max_volume,
                                                                                                 song_list)
        volume_adjustment.Adjustment.set_volume(song_list, offset_list, setup['test_data_output_folder'])
        post_adjustment_song_list=volume_detection.volume_detection.analyse_volume_from_files([setup['test_data_output_folder']])

        file_list_to_delete=[f for f in os.listdir(setup["test_data_output_folder"])]
        for f in file_list_to_delete:
            os.remove(os.path.join(setup["test_data_output_folder"],f))


