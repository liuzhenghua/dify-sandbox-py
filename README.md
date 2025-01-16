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