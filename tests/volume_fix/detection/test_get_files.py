import mp3_eq_vol.src.volume_fix.detection as detection
import pytest


@pytest.fixture()
def mocked_internals(mocker):

    def is_file_mocked(file):
        if file[-3:]=='mp3' or file[-3:]=='txt':
            return True
        else:
            return False
    mocker.patch('mp3_eq_vol.src.volume_fix.detection.isfile', side_effect=is_file_mocked)

class Test_Get_Files():
    @pytest.mark.parametrize("return_list_of_files,input_path,asertion",
                             [(['1.mp3','2.mp3','folder','3.txt'],'C:\\pycharm\\mp3_eq_vol\\origin\\',['C:\\pycharm\\mp3_eq_vol\\origin\\1.mp3','C:\\pycharm\\mp3_eq_vol\\origin\\2.mp3']),
                              (['1.mp3'],'C:\\pycharm\\mp3_eq_vol\\origin\\1.mp3' ,['C:\\pycharm\\mp3_eq_vol\\origin\\1.mp3']),
                              ])
    def test_get_files(self,monkeypatch,return_list_of_files,input_path,asertion,mocked_internals):

        def return_list_files_in_dir(path):
            return(return_list_of_files)
        monkeypatch.setattr(detection, 'listdir', return_list_files_in_dir)
        assert detection.volume_detection.get_files(input_path) == asertion

    @pytest.mark.parametrize("return_list_of_files,input_path",
                             [(['1.mp3'],'C:\\1.txt'),(['1.mp3'],'C:\folder')] )
    def test_get_files_with_non_valid_input(self,monkeypatch,return_list_of_files,input_path,mocked_internals):

        def return_list_files_in_dir(path):
            return(return_list_of_files)
        monkeypatch.setattr(detection, 'listdir', return_list_files_in_dir)

        with pytest.raises(Exception):
            detection.volume_detection.get_files(input_path)