from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.config_service import ConfigService


def main() -> int:
    config_service = ConfigService(PROJECT_ROOT / "config")

    try:
        config = config_service.load_all()
        result = config_service.validate_all(config)
    except Exception as exc:
        print("Configuration check: ERROR")
        print(f"- {exc}")
        return 1

    if result.is_valid:
        print("Configuration check: OK")
        return 0

    print("Configuration check: ERRORS")
    for error in result.errors:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
