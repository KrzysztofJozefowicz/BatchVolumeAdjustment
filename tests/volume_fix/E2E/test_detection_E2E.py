import mp3_eq_vol.src.volume_fix.detection as detection

import pytest
from pathlib import Path

class Test_Detection_E2E():

    @classmethod
    def prepare_song_list(self):
        current_path = Path(__file__).parent.absolute()
        test_data_input_folder = Path.joinpath(current_path, "test_data", "test_input")
        song_1 = str(Path.joinpath(test_data_input_folder ,"file_example_MP3_1MG.mp3"))
        song_2 = str(Path.joinpath(test_data_input_folder ,"file_example_MP3_700KB_broken_file.mp3"))
        song_3 = str(Path.joinpath(test_data_input_folder , "SoundHelix-Song-1.mp3"))
        test_data_subfolder=str(Path.joinpath(test_data_input_folder ,'subfolder'))
        return { '3_songs':[song_1,song_2,song_3],'song_1':song_1, 'song_2':song_2, 'song_3':song_3, 'test_data_input_folder' :test_data_input_folder, 'test_data_subfolder':test_data_subfolder}


    def test_list_of_files(self):
        song_list=Test_Detection_E2E.prepare_song_list()
        output = detection.volume_detection.analyse_volume_from_files(*song_list['3_songs'])

        assert type(output) == type({})
        assert output[song_list['song_1']].keys() == set(['mean_volume', 'max_volume'])
        assert output[song_list['song_1']]['mean_volume'] == -16.4
        assert output[song_list['song_1']]['max_volume'] == -0.2
        assert output[song_list['song_2']] == {'max_volume': None, 'mean_volume': None}

        assert output[song_list['song_3']].keys() == set(['mean_volume', 'max_volume'])
        assert output[song_list['song_3']]['mean_volume'] == -10.4
        assert output[song_list['song_3']]['max_volume'] == 0.0

    def test_list_of_folders(self):
        song_list=Test_Detection_E2E.prepare_song_list()
        output = detection.volume_detection.analyse_volume_from_files(*[song_list["test_data_input_folder"]])

        assert type(output) == type({})
        assert len(output) == 3
        assert output[song_list['song_1']].keys() == set(['mean_volume', 'max_volume'])
        assert output[song_list['song_1']]['mean_volume'] == -16.4
        assert output[song_list['song_1']]['max_volume'] == -0.2
        assert output[song_list['song_2']] == {'max_volume': None, 'mean_volume': None}

        assert output[song_list['song_3']].keys() == set(['mean_volume', 'max_volume'])
        assert output[song_list['song_3']]['mean_volume'] == -10.4
        assert output[song_list['song_3']]['max_volume'] == 0.0


