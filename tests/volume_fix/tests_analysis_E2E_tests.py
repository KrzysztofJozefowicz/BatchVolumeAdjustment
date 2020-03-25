import pytest
import mp3_eq_vol.src.volume_fix.analysis as analysis

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

class Test_Analysis_E2E():
    def test_analysis_E2E(self):
        song_list=songs_details("multiple_songs_multiple_values")
        song_with_max_volume=analysis.volume_analysis.find_song_with_max_max_volume(songs_details("multiple_songs_multiple_values"))
        max_max_volume=song_list[song_with_max_volume]["max_volume"]
        songs_offsets=analysis.volume_analysis.find_volume_offset_based_on_max_max_volume(max_max_volume,songs_details("multiple_songs_multiple_values"))
        assert songs_offsets["file_0.mp3"] == 1
        assert songs_offsets["file_1.mp3"] == 0
        assert songs_offsets["file_2.mp3"] == 2
