import os
import signal
import subprocess
import time
import pytest
from webtest import TestApp
from apibase.app import setup_app

@pytest.fixture
def app():
    from oslo_config import cfg
    from oslo_db import options
    from apibase.db import api
    
    # Configure DB for tests
    options.set_defaults(cfg.CONF, connection='sqlite:///:memory:')
    api.setup_db()
    
    return setup_app()

@pytest.fixture
def webapp(app):
    # Valid token by default to keep existing TDD tests Green
    tapp = TestApp(app)
    # webtest mapping: Header 'X-Auth-Token' -> Environ 'HTTP_X_AUTH_TOKEN'
    tapp.extra_environ = {'HTTP_X_AUTH_TOKEN': 'SECRET_TOKEN'}
    return tapp
@pytest.fixture(scope="session")
def api_server():
    """Start the API server in a background process."""
    from apibase.db import models
    from apibase.db import api as db_api
    from oslo_config import cfg
    from oslo_db import options
    from sqlalchemy import create_engine

    db_path = os.path.abspath("test_e2e.db")
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Initialize the DB schema explicitly using a fresh engine
    connection_url = f"sqlite:///{db_path}"
    engine = create_engine(connection_url)
    models.Base.metadata.create_all(engine)
    engine.dispose()

    env = os.environ.copy()
    env["PYTHONPATH"] = f".:{env.get('PYTHONPATH', '')}"
    env["APIBASE_DB_CONNECTION"] = connection_url
    
    # Start gunicorn
    process = subprocess.Popen(
        ["gunicorn", "--bind", "127.0.0.1:8081", "apibase.app:application"],
        env=env,
        preexec_fn=os.setsid
    )
    
    # Wait for server to start
    time.sleep(2)
    
    yield "http://127.0.0.1:8081"
    
    # Shutdown
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    except ProcessLookupError:
        pass
        
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture(scope="session")
def gui_server():
    """Start a simple HTTP server to serve the GUI."""
    gui_path = os.path.abspath("public")
    process = subprocess.Popen(
        ["python3", "-m", "http.server", "3001"],
        cwd=gui_path,
        preexec_fn=os.setsid
    )
    
    time.sleep(1)
    
    yield "http://127.0.0.1:3001"
    
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
