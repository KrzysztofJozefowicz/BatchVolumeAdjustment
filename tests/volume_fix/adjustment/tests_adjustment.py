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
    run_parallel_stub=mocker.stub()
    mocker.patch('mp3_eq_vol.src.volume_fix.adjustment.Adjustment.run_in_parallel',side_effect=run_parallel_stub)

class Tests_Adjustments_SetVolume():
    def test_set_volume(self,mocker):
        run_parallel_stub = mocker.stub()
        mocker.patch('mp3_eq_vol.src.volume_fix.adjustment.Adjustment.run_in_parallel', side_effect=run_parallel_stub)
        song_list=songs_details("only_one_song")
        output_dir="test"
        import os
        song_offset={"file_1.mp3":0}
        expected_args =([song, song_offset[song], os.path.join(output_dir, os.path.split(song)[-1])] for song in song_list)

        adjustment.Adjustment.set_volume(song_list,song_offset,output_dir)
        called_args = run_parallel_stub.call_args_list
        for call in called_args:
            args, kwargs = call
            for arg in args:
                assert list(expected_args) == list(arg)

