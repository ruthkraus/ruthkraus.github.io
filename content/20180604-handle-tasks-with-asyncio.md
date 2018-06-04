Title: Get results from Asyncio tasks those were interrupted by timeout
Category: Blog
Tags: Asyncio, python3, Task, Future


So I ask myself how to do for example next thing with AsyncIO ?  

I have an ordered list of remote API's urls and need to send data to the first
of API's that can respond < 1 sec, if API can't response in 1 sec - I need to
initiate next sending to next API url in order to API's url list.    

If API responds < 1 sec I need to notify user that data was sent successfully.

If I have tasks that were initiated but were interrupted to send data ASAP to
next API url, I want finally to know their results to make some valuable 
decision - for example to notify that data was also sent there.


1. First I'll prepare simple flask app that can listen and answers for our 
requests with some data.

```python

import flask
import time

app = flask.Flask(__name__)

@app.route("/url/<int:api_id>")
def handler(api_id):
    print(f"Sleep {api_id} seconds")
    time.sleep(api_id)
    return flask.jsonify({"result":f"slept {sleep} seconds",
                          "api_id": api_id})

if __name__ == "__main__":
    app.run(debug=True, port=8001)

```

so flask app will listen on *8001* port and respond with timeout in order to 
**api_id** parameter.

2. Write code that handles my expectations: 

```python
import asyncio
import logging
import functools
import requests
import concurrent.futures


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def sync_loader(url):
    """
    Sync blocking request
    """
    logger.info(f"Sync download {url}")
    return requests.get(url).json()


async def coro_loader(url):
    """
    Runner for sync function in executor
    """
    fn = functools.partial(sync_loader, url)
    loop = asyncio.get_event_loop()
    logger.info(f"start download async {url}")
    return await loop.run_in_executor(None, fn)


async def waiter(pending_tasks):
    """
    Coroutine to wait pending tasks results 
    and display results
    """
    wait_for = 60
    while not all(map(lambda x: x.done(), pending_tasks.values())) and wait_for > 0:
        logger.info("Waiting for pending task results...")
        await asyncio.sleep(1)
        wait_for -= 1
    for api_id, task in pending_tasks.items():
        if not task.done():
            task.cancel()
            logger.warning(f"Postprocess {api_id} task was cancelled.")
            continue
        logger.info(f"Postprocess pending task api_id: {api_id}; {task.result()}")


async def download_async():
    urls = {api_id: "http://localhost:8001/url/{0}".format(api_id)
            for api_id in [3,4]}

    urls[5] = "http://localhost:8001/url/0"  # for example 5th url its a fast API

    pending_tasks = {}
    res = {}

    for api_id, url in urls.items():
        task = asyncio.Task(coro_loader(url))  # create Task from coroutine
        try: 
            # wrap asyncio.shield(task) to avoid of task cancellation
            # after 1 sec timeout
            res = await asyncio.wait_for(asyncio.shield(task), timeout=1) 
        except concurrent.futures.TimeoutError:
            # add task that was interrupted to pending task mapping
            pending_tasks[api_id] = task
            logger.info(f"Add download task for {url} to pending tasks list.")

        if not res:
            continue
        else:
            # show success message
            logger.info(f"Success with send data to {url}, in pending_tasks now"
                        f" are {len(pending_tasks)} tasks.")
            break

    loop = asyncio.get_event_loop()
    loop.create_task(waiter(pending_tasks))


loop = asyncio.get_event_loop()
loop.create_task(download_async())
loop.run_forever()

```

So code is much more clear now. I collect tasks those were interrupted to 
**waiter()** coroutine and there waiting for results.


Example of log output:

```text
(.venv) ➜  as python worker.py
INFO:__main__:start download async http://localhost:8001/url/3
INFO:__main__:Sync download http://localhost:8001/url/3
INFO:__main__:Add download task for http://localhost:8001/url/3 to pending tasks list.
INFO:__main__:start download async http://localhost:8001/url/4
INFO:__main__:Sync download http://localhost:8001/url/4
INFO:__main__:Add download task for http://localhost:8001/url/4 to pending tasks list.
INFO:__main__:start download async http://localhost:8001/url/0
INFO:__main__:Sync download http://localhost:8001/url/0
INFO:__main__:Success with send data to http://localhost:8001/url/0, in pending_tasks now are 2 tasks.
INFO:__main__:Waiting for pending task results...
INFO:__main__:Waiting for pending task results...
INFO:__main__:Waiting for pending task results...
INFO:__main__:Postprocess pending task api_id: 3; {'api_id': 3, 'result': 'slept 3 seconds'}
INFO:__main__:Postprocess pending task api_id: 4; {'api_id': 4, 'result': 'slept 4 seconds'}

```
   