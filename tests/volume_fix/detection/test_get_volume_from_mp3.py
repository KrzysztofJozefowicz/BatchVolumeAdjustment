import pytest

from _pytest import monkeypatch
import mp3_eq_vol.src.volume_fix.detection as detection

import pytest

@pytest.fixture()
def mocked_internals(mocker):
    def return_output_from_subprocess_mocked(ffmpeg_args, stderr):
        return "".encode("utf-8")
    def get_details_from_ffmpeg_output_mocked(input):
        return {"mean_volume":0 , "max_volume":10}

    mocker.patch('mp3_eq_vol.src.volume_fix.detection.subprocess.check_output', side_effect=return_output_from_subprocess_mocked)
    mocker.patch('mp3_eq_vol.src.volume_fix.detection.volume_detection.get_details_from_ffmpeg_output',side_effect=get_details_from_ffmpeg_output_mocked)


def test_get_volume_from_mp3_check_keys(mocked_internals):
    filename = "my_file"
    out = detection.volume_detection.get_volume_from_mp3(filename)
    assert out["my_file"].keys() == set(["mean_volume","max_volume"])

def test_get_volume_from_mp3_check_values(mocked_internals):
    filename="my_file"
    out = detection.volume_detection.get_volume_from_mp3(filename)
    assert out["my_file"] == {"mean_volume":0 , "max_volume":10}
