import os
import json
import shutil

from typing import Optional
from mesh.storage import Storage

_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'database')

_BULLPEN_DIR = os.path.join(_DB_DIR, 'bullpen')


def _database_file():
    # the first cdb file will be the database file
    for dir_path, _, file_names in os.walk(_DB_DIR):
        file_names[:] = [f for f in file_names if not f.startswith('.')]
        f = next(iter(file_names), None)
        return os.path.join(dir_path, f)
    return None


class LocalStorage(Storage):

    def load(self) -> Optional[dict]:
        db_file = _database_file()
        if db_file:
            with open(db_file, 'r') as f:
                return json.loads(f.read())
        return None

    def swap(self, profile: str) -> Optional[dict]:
        target = os.path.join(_BULLPEN_DIR, profile)
        if not os.path.exists(target):
            raise Exception('LocalStorage: target file not found')

        # move the database file to bullpen
        db_file = _database_file()
        if db_file:
            shutil.move(db_file, os.path.join(_BULLPEN_DIR, os.path.basename(db_file)))

        # make the target profile as database
        shutil.move(target, os.path.join(_DB_DIR, profile))

        return self.load()

    def save(self, data: dict) -> bool:
        # save to the first cdb file
        db_file = _database_file()
        if db_file:
            with open(db_file, '+w') as f:
                f.write(json.dumps(data, sort_keys=False, indent=2))
                return True
        return False
