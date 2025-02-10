import socket
from .. import cli
from ..cli import is_port_in_use

def test_is_port_in_use():
    print('hello world')
    """Test if is_port_in_use correctly detects an open/closed port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 0))  # Bind to an available port
        s.listen(1)  # Start listening to properly simulate an open port
        port = s.getsockname()[1]

        assert is_port_in_use(port) is True

    assert is_port_in_use(port) is False