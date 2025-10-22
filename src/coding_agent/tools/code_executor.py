import os
from sandbox_fusion import set_endpoint, run_code_async, RunCodeRequest, RunCodeResponse

set_endpoint(os.getenv("SANDBOX_FUSION_ENDPOINT", "http://localhost:7777"))


async def execute_code(
    code: str, language: str = "python", timeout: float = 60
) -> RunCodeResponse:
    """
    Execute code in a sandboxed environment

    This function runs code safely in an isolated environment, capturing stdout,
    stderr, and return values. It's useful for testing generated code, debugging,
    and validating solutions.

    Args:
        code: The source code to execute. Should be a complete, runnable program.
        language: Programming language of the code. Defaults to "python".
                 Supported languages depend on Sandbox Fusion configuration.
        timeout: Maximum execution time in seconds. Defaults to 60 seconds.
                Execution will be terminated if it exceeds this limit.

    Returns:
        RunCodeResponse: Response object containing:
            - status: RunStatus ("Success", "Failed", or "SandboxError")
            - message: Response message with details
            - compile_result: Object with compilation details:
                - status: "Finished", "Error", or "TimeLimitExceeded"
                - execution_time: Compilation time in seconds
                - return_code: Compiler return code
                - stdout: Compiler standard output
                - stderr: Compiler standard error
            - run_result: Object with execution details:
                - status: "Finished", "Error", or "TimeLimitExceeded"
                - execution_time: Execution time in seconds
                - return_code: Program return code (0 for success)
                - stdout: Program standard output
                - stderr: Program standard error
            - executor_pod_name: Name of the executor environment
            - files: Dictionary mapping file paths to their contents

    Raises:
        Exception: If the sandbox service is unavailable or request fails.

    Example:
        >>> code = '''
        ... def add(a, b):
        ...     return a + b
        ... print(add(2, 3))
        ... '''
        >>> response = await execute_code(code)
        >>> print(response.run_result.stdout)
        5
        >>> print(response.run_result.return_code)
        0
        >>> print(response.status)
        Success

    Note:
        - Requires Sandbox Fusion service at SANDBOX_FUSION_ENDPOINT
        - Default endpoint: http://localhost:7777 (configurable via env var)
        - For Python, no compilation occurs (compile_result will be empty)
        - Access execution output via response.run_result.stdout/stderr
    """
    run_code_request = RunCodeRequest(
        code=code,
        language=language,
        timeout=timeout,
    )
    return await run_code_async(run_code_request)


if __name__ == "__main__":
    import asyncio

    sample_code = """
def add(a, b):
    return a + b
result = add(2, 3)
print(result)
"""
    response = asyncio.run(execute_code(sample_code))
    print("Output:", response)
