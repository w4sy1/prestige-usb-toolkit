import json
import tempfile
import unittest
from pathlib import Path
from app import prepare,verify
from update import update,rollback
from unittest.mock import patch
import shutil


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

    def test_corrupt_saved_version_does_not_replace_working_version(self):
        with tempfile.TemporaryDirectory() as temporary:
            source,usb=self.fixture(Path(temporary));result=update(usb,[source],prepare,True)
            (Path(result['rollback'])/'prestige-fixture/app.py').write_text('corrupt')
            with self.assertRaises(ValueError):rollback(result['rollback'],True)
            self.assertEqual((usb/'Tools/prestige-fixture/app.py').read_text(),'new')
            self.assertTrue(verify(usb)['ok'])

    def test_missing_saved_version_does_not_claim_rollback(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);source,usb=self.fixture(root);result=update(usb,[source],prepare,True)
            (Path(result['rollback'])/'prestige-fixture').rename(root/'displaced-fixture')
            with self.assertRaises(ValueError):rollback(result['rollback'],True)
            self.assertTrue(verify(usb)['ok'])

    def test_failed_install_can_restore_saved_version(self):
        with tempfile.TemporaryDirectory() as temporary:
            source,usb=self.fixture(Path(temporary));move=shutil.move
            def fail_install(source_path,target_path,*args,**kwargs):
                if Path(target_path)==usb/'Tools/prestige-fixture':raise OSError('fixture failure')
                return move(source_path,target_path,*args,**kwargs)
            with patch('update.shutil.move',side_effect=fail_install):
                with self.assertRaises(OSError):update(usb,[source],prepare,True)
            journal=next((usb/'Backup/Updates').iterdir())
            rollback(journal,True)
            self.assertEqual((usb/'Tools/prestige-fixture/app.py').read_text(),'old')
            self.assertTrue(verify(usb)['ok'])
