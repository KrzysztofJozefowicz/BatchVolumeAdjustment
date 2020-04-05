import pytest
import mp3_eq_vol.src.volume_fix.adjustment as adjustment

def songs_details(output_type):
    song_list={}
    if output_type=="multiple_songs_multiple_values":
        song_list={"file_0.mp3":{"max_volume":0 , "mean_volume": -1} ,"file_1.mp3":{"max_volume":1 , "mean_volume": 0} , "file_2.mp3":{"max_volume":-1 ,"mean_volume":-2}}

    if output_type=="multiple_songs_equal_values":
        song_list={"file_1.mp3":{"max_volume":0 , "mean_volume": 0} , "file_2.mp3":{"max_volume":0 ,"mean_volume":0}}


    if output_type=="only_one_song":
        song_list = {"file_1.mp3": {"max_volume": 0, "mean_volume": 0}}

    if output_type=="empty_song_list":
        song_list = None

    if output_type=="only_one_song_no_max_volume":
        song_list = {"file_1.mp3": {"mean_volume": 0}}

    if output_type == "only_one_song_no_mean_volume":
        song_list = {"file_1.mp3": {"max_volume": 0}}
    return song_list

@pytest.fixture()
def run_parallel(mocker):
    def run_parallel_mocked(args):
        pass
    run_parallel_stub=mocker.stub()
    mocker.patch('mp3_eq_vol.src.volume_fix.adjustment.Adjustment.run_in_parallel',side_effect=run_parallel_stub)

class Tests_Adjustments_SetVolume():
    def test_set_volume(self,mocker):
        run_parallel_stub = mocker.stub()
        mocker.patch('mp3_eq_vol.src.volume_fix.adjustment.Adjustment.run_in_parallel', side_effect=run_parallel_stub)
        song_list=songs_details("multiple_songs_multiple_values")
        adjustment.Adjustment.set_volume(song_list,0,"test")
        run_parallel_stub.assert_called_once_with()