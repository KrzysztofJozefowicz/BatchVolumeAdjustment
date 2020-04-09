import asyncio

class run_async():
    number_of_concurrent_processes = 3

    @classmethod
    def set_cincurrecy(cls,number_of_concurent_runs):
        cls.number_of_concurrent_processes=int(number_of_concurent_runs)

    @classmethod
    def run_concurent_async(cls, cmd_list,task_names=None):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        loop = asyncio.get_event_loop()
        semaphore = asyncio.Semaphore(cls.number_of_concurrent_processes)
        if task_names != None:
            async_tasks = (cls.worker_run_async(cmd, task_names[cmd_list.index(cmd)], semaphore) for cmd in cmd_list)
        else:
            async_tasks = (cls.worker_run_async(cmd,cmd_list.index(cmd),semaphore) for cmd in cmd_list)
        all_tasks = asyncio.gather(*async_tasks)
        results = loop.run_until_complete(all_tasks)
        loop.close()
        return results

    @classmethod
    async def worker_run_async(cls, cmd,task_name, semaphore):
        async with semaphore:
            print("running:",task_name)
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE,
                                                        stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
            print("finished:", task_name)
            return {task_name: stderr.decode("utf-8")}

