import pytest
from core import code_executor

code = """
# declare main function
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
result = f'''<<RESULT>>{output_json}<<RESULT>>'''
print(result)

"""

def test_run_python():
    ret = code_executor._run_python_code_in_process(code)
    print(ret)
