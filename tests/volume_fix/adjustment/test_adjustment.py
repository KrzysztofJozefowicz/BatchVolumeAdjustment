import pytest
import mp3_eq_vol.src.volume_fix.adjustment as adjustment

class Tests_Adjustments_SetVolume():
    def test_set_volume(self,mocker):
        run_parallel_stub = mocker.stub()
        mocker.patch('mp3_eq_vol.src.volume_fix.run_async.run_async.run_concurent_async', side_effect=run_parallel_stub)
        song_list=["file_1.mp3","file_2.mp3"]
        output_dir="test"
        song_offset={"file_1.mp3":0, "file_2.mp3":0}
        adjustment.Adjustment.set_volume(song_list,song_offset,output_dir)
        called_args = run_parallel_stub.call_args_list
        number_of_arguments=len(called_args[0][0])
        elements_in_set_volume_commands=called_args[0][0][0]
        elements_in_task_names=called_args[0][0][1]
        assert number_of_arguments == 2
        assert len(elements_in_set_volume_commands)== 2
        assert len(elements_in_task_names) == 2
        assert elements_in_task_names == ["file_1.mp3","file_2.mp3"]

