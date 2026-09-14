from pathlib import Path
import tempfile
import unittest
from runtime import atomic_json
from app import prepare,verify

class UsbTests(unittest.TestCase):
    def test_integrity(self):
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/'prestige-demo';source.mkdir();atomic_json(source/'metadata.json',{'version':'0.1.0'});(source/'app.py').write_text('print(1)')
            result=prepare(Path(d)/'usb',[source]);root=Path(result['root']);self.assertTrue(verify(root)['ok'])
            (root/'Tools/prestige-demo/app.py').write_text('changed');self.assertFalse(verify(root)['ok'])
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            prepare(d,[])
            with self.assertRaises(FileExistsError):prepare(d,[])
