import os
import pecan
from oslo_config import cfg

# Define oslo.config options if needed (example)
opt_group = cfg.OptGroup(name='api', title='API Options')
api_opts = [
    cfg.StrOpt('host_ip', default='0.0.0.0', help='The IP address to bind to.'),
    cfg.IntOpt('port', default=8080, help='The port to bind to.'),
]

CONF = cfg.CONF
CONF.register_group(opt_group)
CONF.register_opts(api_opts, group=opt_group)

def get_pecan_config():
    # In a professional setup, we find config from etc/apibase
    # We look relative to the root of the project
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = os.path.join(root_dir, 'etc', 'apibase', 'config.py')
    return pecan.configuration.conf_from_file(filename)

def setup_app(config=None):
    if not config:
        config = get_pecan_config()

    # Setup logging
    from oslo_log import log as logging
    from oslo_config import cfg
    logging.register_options(cfg.CONF)
    logging.setup(cfg.CONF, 'apibase')

    # Register hooks
    from apibase.common import hooks
    app_hooks = [hooks.ErrorHook(), hooks.CorsHook()]

    app = pecan.make_app(
        config.app.root,
        static_root=config.app.static_root,
        template_path=config.app.template_path,
        debug=config.app.debug,
        hooks=app_hooks,
        force_canonical=getattr(config.app, 'force_canonical', True)
    )
    
    # Wrap with Keystone-compatible middleware
    from apibase.middleware import FakeAuthMiddleware
    app = FakeAuthMiddleware(app)
    
    return app

# WSGI Application for Gunicorn
application = setup_app()
