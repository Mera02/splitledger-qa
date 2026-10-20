import os
import subprocess
from pathlib import Path

import pytest


QA_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = QA_ROOT.parent / "splitledger"
BACKEND_DIR = APP_ROOT / "backend"

if os.name == "nt":
    APP_PYTHON = (
        APP_ROOT
        / ".venv"
        / "Scripts"
        / "python.exe"
    )
else:
    APP_PYTHON = (
        APP_ROOT
        / ".venv"
        / "bin"
        / "python"
    )


@pytest.fixture
def run_cli(tmp_path):
    database_path = tmp_path / "cli-qa.db"

    environment = os.environ.copy()

    environment["SPLITLEDGER_DB_PATH"] = str(
        database_path
    )

    def _run(*arguments):
        return subprocess.run(
            [
                str(APP_PYTHON),
                "-m",
                "app.cli",
                *map(str, arguments),
            ],
            cwd=BACKEND_DIR,
            env=environment,
            capture_output=True,
            text=True,
        )

    return _run