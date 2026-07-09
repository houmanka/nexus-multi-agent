import asyncio
from concurrent.futures import ThreadPoolExecutor

from temporalio.client import Client
from temporalio.envconfig import ClientConfig
from temporalio.worker import Worker

from config import Config
from workflow.activity.sample_activity import HelloActivity
from workflow.sample_workflow import SampleWorkflow


async def main():
    connect_config = ClientConfig.load_client_connect_config()
    connect_config.setdefault("target_host", "localhost:7233")

    conf = Config()

    hello_activity = HelloActivity()

    client = await Client.connect(**connect_config)
    worker = Worker(
        client,
        task_queue=conf.task_queue,
        activities=[hello_activity.say_hello],
        workflows=[SampleWorkflow],
        activity_executor=ThreadPoolExecutor(5),
    )
    print("worker running...", end="", flush=True)
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())