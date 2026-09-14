import json
import tempfile
import unittest
from pathlib import Path
from app import prepare,verify
from update import update,rollback


class UpdateTests(unittest.TestCase):
    def fixture(self,root):
        source=root/'prestige-fixture';source.mkdir()
        (source/'metadata.json').write_text(json.dumps({'version':'0.1.0'}))
        (source/'app.py').write_text('old')
        usb=Path(prepare(root/'usb',[source])['root'])
        (source/'app.py').write_text('new')
        (source/'metadata.json').write_text(json.dumps({'version':'0.2.0'}))
        return source,usb

    def test_update_preserves_reports_and_rollback(self):
        with tempfile.TemporaryDirectory() as temporary:
            source,usb=self.fixture(Path(temporary))
            report=usb/'Tools/prestige-fixture/reports/diagnostic.json';report.write_text('private fixture')
            self.assertFalse(update(usb,[source],prepare)['executed'])
            self.assertEqual((usb/'Tools/prestige-fixture/app.py').read_text(),'old')
            result=update(usb,[source],prepare,True)
            self.assertEqual(report.read_text(),'private fixture')
            self.assertEqual((usb/'Tools/prestige-fixture/app.py').read_text(),'new')
            self.assertTrue(verify(usb)['ok'])
            rollback(result['rollback'],True)
            self.assertEqual((usb/'Tools/prestige-fixture/app.py').read_text(),'old')
            self.assertTrue(verify(usb)['ok'])

    def test_user_modified_code_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            source,usb=self.fixture(Path(temporary))
            (usb/'Tools/prestige-fixture/app.py').write_text('custom')
            with self.assertRaises(ValueError):update(usb,[source],prepare,True)
            self.assertEqual((usb/'Tools/prestige-fixture/app.py').read_text(),'custom')

    def test_changed_new_version_blocks_rollback(self):
        with tempfile.TemporaryDirectory() as temporary:
            source,usb=self.fixture(Path(temporary));result=update(usb,[source],prepare,True)
            (usb/'Tools/prestige-fixture/app.py').write_text('custom after update')
            with self.assertRaises(ValueError):rollback(result['rollback'],True)
