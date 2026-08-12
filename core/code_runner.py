import subprocess
import sys

from django.conf import settings


def run_python_code(code: str) -> dict:
    timeout = getattr(settings, "CODE_RUN_TIMEOUT_SECONDS", 5)
    try:
        result = subprocess.run(
            [sys.executable, "-I", "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "timed_out": False,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "stdout": exc.stdout or "",
            "stderr": (exc.stderr or "") + f"\n[اجرا بیش از {timeout} ثانیه طول کشید و متوقف شد]",
            "timed_out": True,
            "returncode": None,
        }