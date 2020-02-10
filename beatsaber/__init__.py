from pathlib import Path
from moderngl_window import resources

RESOURCE_DIR = Path(__file__).parent.resolve() / 'resources'
resources.register_dir(RESOURCE_DIR)
