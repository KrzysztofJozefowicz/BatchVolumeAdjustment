class volume_analysis():
    song_with_max_max_volume = None
    song_with_max_mean_volume = None

    @classmethod
    def find_max_mean_volume(cls,volume_analysis) -> float:
        max=None

        if volume_analysis == None or len(volume_analysis) == 0:
            raise ValueError("List of songs to analyse empty")

        for song in volume_analysis:
            try:
                if max == None:

                    max=volume_analysis[song]["mean_volume"]
                else:
                    if volume_analysis[song]["mean_volume"] > max:

                        max = volume_analysis[song]["mean_volume"]
            except:
                raise ValueError("Key 'mean_volume' not found in ", song)
        return max

    @classmethod
    def find_max_max_volume(cls,volume_analysis) -> float:
        max=None
        if volume_analysis == None or len(volume_analysis) == 0:
            raise ValueError("List of songs to analyse empty")

        for song in volume_analysis:
            try:
                if max == None:
                    max=volume_analysis[song]["max_volume"]
                else:
                    if volume_analysis[song]["max_volume"] > max:
                        max = volume_analysis[song]["max_volume"]
            except:
                raise ValueError("Key 'max_volume' not found in ",song)
        return max


    @classmethod
    def find_volume_offset_based_on_max_max_volume(cls,max_max_volume,volume_analysis) -> dict:
        volume_offset={}

        for song in volume_analysis:
            if max_max_volume>volume_analysis[song]["max_volume"]:
                volume_gain=max_max_volume-volume_analysis[song]["max_volume"]
                volume_offset[song] = volume_gain
            else:
                volume_offset[song] = 0
        return volume_offset


