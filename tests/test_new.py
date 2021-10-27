from fossil_cli import new
import logging
log = logging.getLogger(__name__)
from pathlib import Path

def test_new(invoke):
    invoke(new, '--name test --filename .fossil --readme README.md')
    
    assert log.warning(Path.cwd())