import mp3_eq_vol.valume_detection as volume_detection

def find_song_with_max_mean_volume(volume_analysis):
    max=None
    file=None
    for song in volume_analysis:
        if max == None:
            file=song
            max=volume_analysis[song]["mean_volume"]
        else:
            if volume_analysis[song]["mean_volume"] > max:
                file=song
                max = volume_analysis[song]["mean_volume"]
    return file

def find_song_with_max_max_volume(volume_analysis):
    max=None
    file=None
    for song in volume_analysis:
        if max == None:
            file=song
            max=volume_analysis[song]["max_volume"]
        else:
            if volume_analysis[song]["max_volume"] > max:
                file=song
                max = volume_analysis[song]["max_volume"]
    return file

def find_volume_offset_based_on_max_max_volume(max_max_volume,volume_analysis):
    volume_offset={}
    for song in volume_analysis:
        if max_max_volume>volume_analysis[song]["max_volume"]:
            volume_gain=max_max_volume-volume_analysis[song]["max_volume"]
            volume_offset[song] = volume_gain
        else:
            volume_offset[song] = 0
    return volume_offset


