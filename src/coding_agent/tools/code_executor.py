import os
from sandbox_fusion import set_endpoint, run_code_async, RunCodeRequest, RunCodeResponse

set_endpoint(os.getenv("SANDBOX_FUSION_ENDPOINT", "http://localhost:7777"))


async def execute_code(
    code: str, language: str = "python", timeout: float = 60
) -> RunCodeResponse:
    run_code_request = RunCodeRequest(
        code=code,
        language=language,
        timeout=timeout,
    )
    return await run_code_async(run_code_request)
