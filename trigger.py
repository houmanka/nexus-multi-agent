import asyncio
import uuid

from temporalio.client import Client
from temporalio.envconfig import ClientConfig

from config import Config
from workflow.activity.sample_activity import SampleInput

TASK_QUEUE = "sample-task-queue"


async def main():
    connect_config = ClientConfig.load_client_connect_config()
    connect_config.setdefault("target_host", "localhost:7233")
    conf = Config()

    client = await Client.connect(**connect_config)
    result = await client.execute_workflow(
        "SampleWorkflow",
        SampleInput(name="Temporal"),
        id=f"sample-workflow-{uuid.uuid4()}",
        task_queue=conf.task_queue,
    )
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
