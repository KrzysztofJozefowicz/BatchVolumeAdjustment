import pytest
import mp3_eq_vol.src.volume_fix.analysis as analysis
import mp3_eq_vol.src.volume_fix.detection as detection
from pathlib import Path

class Test_Analysis_E2E():
    @classmethod
    def prepare_song_list(self):
        current_path = Path(__file__).parent.absolute()
        test_data_input_folder = Path.joinpath(current_path, "test_data", "test_input")
        song_1 = str(Path.joinpath(test_data_input_folder ,"file_example_MP3_1MG.mp3"))
        song_2 = str(Path.joinpath(test_data_input_folder ,"file_example_MP3_700KB_broken_file.mp3"))
        song_3 = str(Path.joinpath(test_data_input_folder, "SoundHelix-Song-1.mp3"))

        test_data_subfolder=str(Path.joinpath(test_data_input_folder ,'subfolder'))
        return { '3_songs':[song_1,song_2,song_3],'song_1':song_1, 'song_2':song_2, 'song_3':song_3, 'test_data_input_folder' :test_data_input_folder, 'test_data_subfolder':test_data_subfolder}


    def test_analysis_E2E(self):
        song_list = Test_Analysis_E2E.prepare_song_list()
        list_of_songs_with_sound_values = detection.volume_detection.analyse_volume_from_files(song_list['3_songs'])
        max_volume=analysis.volume_analysis.find_max_max_volume(list_of_songs_with_sound_values)

        songs_offsets=analysis.volume_analysis.find_volume_offset_based_on_max_max_volume(max_volume,list_of_songs_with_sound_values)
        assert songs_offsets[song_list['song_1']] == 0.2
        assert songs_offsets[song_list['song_2']] == None
        assert songs_offsets[song_list['song_3']] == 0


