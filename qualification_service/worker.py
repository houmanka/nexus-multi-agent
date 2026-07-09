import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from qualification_service.activity import calculate_ltv
from qualification_service.const import QUALIFICATION_NAMESPACE, QUALIFICATION_TASK_QUEUE
from qualification_service.handler import QualificationServiceHandler
from qualification_service.workflow import QualificationServiceWorkflow


async def main():
    client = await Client.connect("localhost:7233", namespace=QUALIFICATION_NAMESPACE)
    worker = Worker(
        client=client,
        task_queue=QUALIFICATION_TASK_QUEUE,
        workflows=[QualificationServiceWorkflow],
        activities=[calculate_ltv],
        nexus_service_handlers=[QualificationServiceHandler()],
    )
    print(f"[qualification-team] worker running on namespace '{QUALIFICATION_NAMESPACE}'...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())