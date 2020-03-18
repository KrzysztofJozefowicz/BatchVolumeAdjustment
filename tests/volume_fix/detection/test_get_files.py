# happy-path


#  analyse_volume_from_files -> zwraca slownik gdzie klucze to slowniki

# run_in_parallel -> dostaje liste plikow, zwraca slownik, gdzie klucze to slowniki

# get_volume_from_mp3 -dostaje sciezke do pliku, zwraca slownik

# get_details_from_ffmpeg_output -> dostaje output z ffmpeg, zwraca slownik z dwoma kluczami

# get_files -> dostaje katalog, zwrawca sciezke do plikow tylko mp3, idac rekursywnie w podkatalogach
import mp3_eq_vol.src.volume_fix.detection as detection

import pytest


@pytest.fixture()
def mocked_internals(monkeypatch):

    def is_file_mocked(file):
        if file[-3:]=='mp3' or file[-3:]=='txt':
            return True
        else:
            return False
    monkeypatch.setattr(detection, 'isfile', is_file_mocked)


@pytest.mark.parametrize("return_list_of_files,input_path,asertion",
                         [(['1.mp3','2.mp3','folder','3.txt'],'C:\\pycharm\\mp3_eq_vol\\origin\\',['C:\\pycharm\\mp3_eq_vol\\origin\\1.mp3','C:\\pycharm\\mp3_eq_vol\\origin\\2.mp3']),
                          (['1.mp3'],'C:\\pycharm\\mp3_eq_vol\\origin\\1.mp3' ,['C:\\pycharm\\mp3_eq_vol\\origin\\1.mp3']),
                          ])
def test_get_files(monkeypatch,return_list_of_files,input_path,asertion,mocked_internals):

    def return_list_files_in_dir(path):
        return(return_list_of_files)
    monkeypatch.setattr(detection, 'listdir', return_list_files_in_dir)
    assert detection.volume_detection.get_files(input_path) == asertion

@pytest.mark.parametrize("return_list_of_files,input_path",
                         [(['1.mp3'],'C:\\1.txt'),(['1.mp3'],'C:\folder')] )
def test_get_files_with_non_valid_input(monkeypatch,return_list_of_files,input_path,mocked_internals):

    def return_list_files_in_dir(path):
        return(return_list_of_files)
    monkeypatch.setattr(detection, 'listdir', return_list_files_in_dir)

    with pytest.raises(Exception):
        detection.volume_detection.get_files(input_path)