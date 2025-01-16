# dify-sandbox-py
## Introduction
The Python version of the dify sandbox addresses the following issues:

- The official version of dify-sandbox includes system call restriction features, which make many libraries unusable after installation. For secure and controllable internal environments, such restrictions are unnecessary.
- Additional dependencies are installed at startup, slowing down the startup process.
- The health check interface may lack graceful shutdown handling.
- Performance issues in multi-process mode. (For example, with 10 concurrent requests, if all your requests involve slow HTTP calls, new requests may be blocked and eventually time out after 15 seconds.)

To address these issues, a Python-based sandbox was developed, compatible with the official dify-sandbox API, with the following modifications:

- Multi-threading instead of multi-processing: Threads have lower overhead. The default MAX_WORKERS has been increased to 50.
- Multi-process startup with Uvicorn: The number of processes matches the number of CPU cores. For a 4-core system, the total concurrency increases to 200 (compared to a fixed 10 in the previous version).
- Enhanced metrics and logging: Added a metrics endpoint and additional log outputs to facilitate issue diagnosis.


## Test
```bash
pip install pytest

# 运行所有的单元测试
pytest

# 运行指定的单元测试文件
pytest tests/test_executor.py

# 运行指定的单元测试方法
pytest tests/test_executor.py::test_run_python
```

## 压测
```python
import asyncio
import httpx

# URL and headers
url = "http://localhost:8194/v1/sandbox/run"
headers = {
    "X-Api-Key": "dify-sandbox",
    "Content-Type": "application/json",
}
# Data payload
data = {
    "language": "python3",
    "code": """
# declare main function
import httpx
def main(arg1: str, arg2: str) -> dict:
    return {
        "result": arg1 + arg2,
    }

import json
from base64 import b64decode

# decode and prepare input dict
inputs_obj = json.loads(b64decode('eyJhcmcxIjogImhlbGxvICIsICJhcmcyIjogIndvcmxkIn0=').decode('utf-8'))

# execute main function
output_obj = main(**inputs_obj)

# convert output to json and print
output_json = json.dumps(output_obj, indent=4)
result = f'<<RESULT>>{output_json}<<RESULT>>'
print(result)
"""
}

async def send_request():
    """Send a single HTTP POST request."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            print(f"Response: {response.status_code} {response.text}")
        except Exception as e:
            print(f"Error: {e}")

async def main():
    tasks = []
    for _ in range(200):
        tasks.append(send_request())
        
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

```
