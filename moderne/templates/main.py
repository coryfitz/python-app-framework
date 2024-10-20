from psx_syntax import psx_import, packed
from moderne.conf import settings
from pathlib import Path

psx_file_path = Path(settings.BASE_DIR) / 'blog' / 'app' / 'routes' / 'index.psx'

component_name = 'Home'

@packed
def run():
    main = psx_import(psx_file_path, component_name)
    return main()

run()