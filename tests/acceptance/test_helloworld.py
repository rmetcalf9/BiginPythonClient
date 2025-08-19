import sys
print(sys.path)
import BiginPythonClient


def test_helloworld():
    assert BiginPythonClient.hello_world() == 'Hello'
