import mp3_eq_vol.src.volume_fix.detection as detection

import pytest

@pytest.fixture()
def mocked_internals(mocker):

        def is_file_mocked(file):
            if file[-3:] == 'mp3' or file[-3:] == 'txt':
                return True
            if file[-3:] == "dir":
                return True
            else:
                return False

        def listdir_mocked(path):
            return ['fake_1.mp3','fake_2.mp3','fake_3.mp3']

        def subprocess_check_output_mocked(process_to_start,stderr=''):
            ffmpeg_output='''  Duration: 00:09:12.26, start: 0.023021, bitrate: 135 kb/s
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
            return ffmpeg_output.encode('utf-8')
        mocker.patch('mp3_eq_vol.src.volume_fix.detection.isfile', side_effect=is_file_mocked)
        mocker.patch('mp3_eq_vol.src.volume_fix.detection.isdir', side_effect=is_file_mocked)
        mocker.patch('mp3_eq_vol.src.volume_fix.detection.listdir', side_effect=listdir_mocked)

        mocker.patch('mp3_eq_vol.src.volume_fix.detection.subprocess.check_output',side_effect=subprocess_check_output_mocked)


class Test_Detection_E2E():
    def test_single_file(self,mocked_internals):
        single_file='my_fake_file.mp3'
        output = detection.volume_detection.analyse_volume_from_files(single_file)

        assert type(output) == type({})
        assert output[single_file].keys() == set(['mean_volume', 'max_volume'])
        assert output[single_file]['mean_volume'] == -9.7
        assert output[single_file]['max_volume'] == 0.0

    def test_list_of_files(self,mocked_internals):
        my_dir = 'my_fake_dir'
        output = detection.volume_detection.analyse_volume_from_files(my_dir)

        assert type(output) == type({})
        assert len(output) == 3
        assert output[my_dir+'\\fake_1.mp3'].keys() == set(['mean_volume', 'max_volume'])
        assert output[my_dir+"\\fake_2.mp3"].keys() == set(['mean_volume', 'max_volume'])
        assert output[my_dir+"\\fake_3.mp3"].keys() == set(['mean_volume', 'max_volume'])

