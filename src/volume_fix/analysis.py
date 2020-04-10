class volume_analysis():
    song_with_max_max_volume = None
    song_with_max_mean_volume = None

    @classmethod
    def find_max_mean_volume(cls,volume_analysis) -> float:

        if volume_analysis == None or len(volume_analysis) == 0:
            raise ValueError("List of songs to analyse empty")

        try:
            return max(x["mean_volume"] for x in volume_analysis.values())
        except:
            raise ValueError("Key 'mean_volume' not found in one of the song list",volume_analysis)



    @classmethod
    def find_max_max_volume(cls,volume_analysis) -> float:

        if volume_analysis == None or len(volume_analysis) == 0:
            raise ValueError("Empty list of songs to analyse")

        try:
            max_values=[]
            for entry in volume_analysis:
                if volume_analysis[entry]["max_volume"] is not None and "max_volume" in volume_analysis[entry].keys():
                    max_values.append(volume_analysis[entry]["max_volume"])
            return max(max_values)
        except:
            raise ValueError("Key 'max_volume' not found in one of the song list", volume_analysis)

    @classmethod
    def find_volume_offset_based_on_max_max_volume(cls,max_max_volume,volume_analysis) -> dict:
        volume_offset={}

        for song in volume_analysis:
            if volume_analysis[song]["max_volume"] != None:
                if max_max_volume>volume_analysis[song]["max_volume"]:
                    volume_gain=max_max_volume-volume_analysis[song]["max_volume"]
                    volume_offset[song] = volume_gain
                else:
                    volume_offset[song] = 0
            else:
                volume_offset[song] = None

        return volume_offset


