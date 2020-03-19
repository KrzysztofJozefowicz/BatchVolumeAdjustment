import pytest
import mp3_eq_vol.src.volume_fix.detection as detection



def test_get_details_from_ffmpeg_output_with_correct_output():
    correct_output='''  Duration: 00:09:12.26, start: 0.023021, bitrate: 135 kb/s
    Stream #0:0: Audio: mp3, 48000 Hz, stereo, fltp, 135 kb/s
    Metadata:
      encoder         : Lavc58.48
Stream mapping:
  Stream #0:0 -> #0:0 (mp3 (mp3float) -> pcm_s16le (native))
Press [q] to stop, [?] for help
Output #0, null, to '/dev/null':
  Metadata:
    encoder         : Lavf58.26.101
    Stream #0:0: Audio: pcm_s16le, 48000 Hz, stereo, s16, 1536 kb/s
    Metadata:
      encoder         : Lavc58.48.100 pcm_s16le
size=N/A time=00:09:12.22 bitrate=N/A speed= 173x
video:0kB audio:103543kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: unknown
[Parsed_volumedetect_0 @ 000001fd0b2cb180] n_samples: 53013944
[Parsed_volumedetect_0 @ 000001fd0b2cb180] mean_volume: -9.7 dB
[Parsed_volumedetect_0 @ 000001fd0b2cb180] max_volume: 0.0 dB
[Parsed_volumedetect_0 @ 000001fd0b2cb180] histogram_0db: 641384'''
    output=detection.volume_detection.get_details_from_ffmpeg_output(correct_output)
    assert output == {"mean_volume" : -9.7 ,"max_volume" : 0.0 }

def test_get_details_from_ffmpeg_output_with_missing_volumes_output():
    missing_volume_output = '''  Duration: 00:09:12.26, start: 0.023021, bitrate: 135 kb/s
        Stream #0:0: Audio: mp3, 48000 Hz, stereo, fltp, 135 kb/s
        Metadata:
          encoder         : Lavc58.48
    Stream mapping:
      Stream #0:0 -> #0:0 (mp3 (mp3float) -> pcm_s16le (native))
    Press [q] to stop, [?] for help
    Output #0, null, to '/dev/null':
      Metadata:
        encoder         : Lavf58.26.101
        Stream #0:0: Audio: pcm_s16le, 48000 Hz, stereo, s16, 1536 kb/s
        Metadata:
          encoder         : Lavc58.48.100 pcm_s16le
    size=N/A time=00:09:12.22 bitrate=N/A speed= 173x
    video:0kB audio:103543kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: unknown'''
    output = detection.volume_detection.get_details_from_ffmpeg_output(missing_volume_output)
    assert output == {"max_volume":None,"mean_volume":None }