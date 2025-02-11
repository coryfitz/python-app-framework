import socket
import pytest
import subprocess
from .. import cli
from ..cli import is_port_in_use, find_next_available_port, run_uvicorn

def test_is_port_in_use():
    """Test if is_port_in_use correctly detects an open/closed port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 0))  # Bind to an available port
        s.listen(1)  # Start listening to properly simulate an open port
        port = s.getsockname()[1]

        assert is_port_in_use(port) is True

    assert is_port_in_use(port) is False

@pytest.fixture
def mock_is_port_in_use(mocker):
    """Mock is_port_in_use function."""
    return mocker.patch("framework.cli.is_port_in_use")

def test_find_next_available_port(mock_is_port_in_use):
    """Test find_next_available_port using pytest's mocker."""
    # Simulate port 8000 being occupied, but 8001 is free
    mock_is_port_in_use.side_effect = lambda port: port == 8000
    assert find_next_available_port(8000) == 8001

    # Simulate ports 8000 and 8001 being occupied, but 8002 is free
    mock_is_port_in_use.side_effect = lambda port: port in [8000, 8001]
    assert find_next_available_port(8000) == 8002

    # Simulate ports 8000-8002 being occupied, but 8003 is free
    mock_is_port_in_use.side_effect = lambda port: port in [8000, 8001, 8002]
    assert find_next_available_port(8000) == 8003

@pytest.fixture
def occupied_port():
    """Find a free port, bind to it, and keep it occupied until the test is done."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("localhost", 0))  # Bind to an available port
    sock.listen(1)  # Start listening to keep it occupied

    port = sock.getsockname()[1]

    yield port  # Provide the port while it's still occupied

    sock.close()  # Release the port after the test

def test_find_next_available_port_real_socket(occupied_port):
    """Test find_next_available_port using an actually occupied port."""
    next_port = find_next_available_port(occupied_port)
    assert next_port > occupied_port

def test_run_uvicorn_port_available(monkeypatch):
    """Test when the default port is available."""

    def mock_is_port_in_use(port):
        return False

    def mock_popen(cmd):
        return None  # Simulating successful process start

    def mock_webbrowser_open(url):
        return None

    monkeypatch.setattr("framework.cli.is_port_in_use", mock_is_port_in_use)
    monkeypatch.setattr("subprocess.Popen", mock_popen)
    monkeypatch.setattr("webbrowser.open", mock_webbrowser_open)

    run_uvicorn(port=8000)

def test_run_uvicorn_port_in_use_user_accepts_new_port(monkeypatch):
    """Test when the default port is in use and the user agrees to use the next available port."""

    def mock_is_port_in_use(port):
        return True

    def mock_find_next_available_port(port):
        return 8001

    def mock_input(prompt):
        return "y"

    def mock_popen(cmd):
        return None

    def mock_webbrowser_open(url):
        return None

    monkeypatch.setattr("framework.cli.is_port_in_use", mock_is_port_in_use)
    monkeypatch.setattr("framework.cli.find_next_available_port", mock_find_next_available_port)
    monkeypatch.setattr("builtins.input", mock_input)
    monkeypatch.setattr("subprocess.Popen", mock_popen)
    monkeypatch.setattr("webbrowser.open", mock_webbrowser_open)

    run_uvicorn(port=8000)

def test_run_uvicorn_port_in_use_user_declines(monkeypatch):
    """Test when the default port is in use and the user refuses to use the next available port."""

    def mock_is_port_in_use(port):
        return True

    def mock_input(prompt):
        return "n"

    popen_called = False
    browser_called = False

    def mock_popen(cmd):
        nonlocal popen_called
        popen_called = True  # Track if this was called

    def mock_webbrowser_open(url):
        nonlocal browser_called
        browser_called = True  # Track if browser was called

    monkeypatch.setattr("framework.cli.is_port_in_use", mock_is_port_in_use)
    monkeypatch.setattr("builtins.input", mock_input)
    monkeypatch.setattr("subprocess.Popen", mock_popen)
    monkeypatch.setattr("webbrowser.open", mock_webbrowser_open)

    run_uvicorn(port=8000)

    assert not popen_called, "Uvicorn should not start when the user declines to use another port."
    assert not browser_called, "Browser should not open when the user declines."

def test_run_uvicorn_popen_error(monkeypatch):
    """Test if `subprocess.Popen` raises an error."""

    def mock_is_port_in_use(port):
        return False

    def mock_popen(cmd):
        raise subprocess.CalledProcessError(1, "uvicorn")

    def mock_webbrowser_open(url):
        pytest.fail("Browser should not open")

    monkeypatch.setattr("framework.cli.is_port_in_use", mock_is_port_in_use)
    monkeypatch.setattr("subprocess.Popen", mock_popen)
    monkeypatch.setattr("webbrowser.open", mock_webbrowser_open)

    run_uvicorn(port=8000)