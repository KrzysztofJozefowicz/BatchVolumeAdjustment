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


class Test_Find_Song_With_Max_Max_Volume():
    def test_multiple_songs_multiple_values_(self):
        out=analysis.volume_analysis.find_song_with_max_max_volume(songs_details("multiple_songs_multiple_values"))
        assert out == 'file_1.mp3'

    def test_mutliple_songs_equal_values(self):
        out = analysis.volume_analysis.find_song_with_max_max_volume(songs_details("multiple_songs_equal_values"))
        assert out == 'file_1.mp3'

    def test_one_song(self):
        out = analysis.volume_analysis.find_song_with_max_max_volume(songs_details("only_one_song"))
        assert out == 'file_1.mp3'

    def test_no_max_volume(self):
        with pytest.raises(ValueError):
           analysis.volume_analysis.find_song_with_max_max_volume(songs_details("only_one_song_no_max_volume"))

    def test_empty_song_list(self):
        with pytest.raises(ValueError):
            analysis.volume_analysis.find_song_with_max_max_volume(songs_details("empty_song_list"))


class Test_Find_Song_With_Max_Mean_Volume():
    def test_multiple_songs_multiple_values_(self):
        out=analysis.volume_analysis.find_song_with_max_mean_volume(songs_details("multiple_songs_multiple_values"))
        assert out == 'file_1.mp3'

    def test_mutliple_songs_equal_values(self):
        out = analysis.volume_analysis.find_song_with_max_mean_volume(songs_details("multiple_songs_equal_values"))
        assert out == 'file_1.mp3'

    def test_one_song(self):
        out = analysis.volume_analysis.find_song_with_max_mean_volume(songs_details("only_one_song"))
        assert out == 'file_1.mp3'

    def test_no_mean_volume(self):
        with pytest.raises(ValueError):
           analysis.volume_analysis.find_song_with_max_mean_volume(songs_details("only_one_song_no_mean_volume"))

    def test_empty_song_list(self):
        with pytest.raises(ValueError):
            analysis.volume_analysis.find_song_with_max_mean_volume(songs_details("empty_song_list"))

class Test_Find_Volume_Offset_Based_On_Max_Max_Volume():
    def test_get_volume_offset_based_on_max_max_volume(self):
        
        songs_offsets=analysis.volume_analysis.find_volume_offset_based_on_max_max_volume(1,songs_details("multiple_songs_multiple_values"))
        assert songs_offsets["file_0.mp3"] == 1
        assert songs_offsets["file_1.mp3"] == 0
        assert songs_offsets["file_2.mp3"] == 2
