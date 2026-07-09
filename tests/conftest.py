import pytest
from temporalio.testing import WorkflowEnvironment


@pytest.fixture(scope="session")
async def workflow_env():
    env = await WorkflowEnvironment.start_time_skipping()
    yield env
    await env.shutdown()
