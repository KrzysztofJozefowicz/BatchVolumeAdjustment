import pytest
import mp3_eq_vol.src.volume_fix.detection as detection


@pytest.fixture()
def mocked_internals(mocker):
    class mocked_Pool():

        def __init__(self,pools):
            pass
        def imap(self,funct,filenames):
            out=[ {"a":"a"},{"b":"b"},None ]
            return out
    mocker.patch('mp3_eq_vol.src.volume_fix.detection.Pool', side_effect=mocked_Pool)


class Test_Run_In_Parallel():
    def test_run_in_parallel_returns_dictionary(self,mocked_internals):
        filenames=['a','b']
        output = detection.volume_detection.run_in_parallel(filenames)
        assert type(output) == type({})
        assert output['a'] == 'a'
        assert output['b'] == 'b'

