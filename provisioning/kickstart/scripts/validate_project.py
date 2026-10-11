#!/usr/bin/env python3

import json
import subprocess
from pathlib import Path


BASE = (
    Path.home()
    / "linux-lab"
    / "provisioning"
    / "kickstart"
)

INVENTORY = BASE / "inventory" / "hosts.json"
GENERATED = BASE / "generated"


def run(command):
    result = subprocess.run(
        command,
        text=True,
        capture_output=True,
    )

    return result


def main():
    print("Project 1 validation")
    print("=" * 40)

    hosts = json.loads(
        INVENTORY.read_text(encoding="utf-8")
    )

    failures = 0

    for name in hosts:
        cfg = GENERATED / f"{name}.cfg"

        if not cfg.is_file():
            print(f"[FAIL] {name}: Kickstart missing")
            failures += 1
            continue

        result = run(
            [
                "ksvalidator",
                "-v",
                "RHEL10",
                str(cfg),
            ]
        )

        if result.returncode == 0:
            print(
                f"[PASS] {name}: "
                f"Kickstart validation successful"
            )

        else:
            print(
                f"[FAIL] {name}: "
                f"Kickstart validation failed"
            )

            print(result.stderr)
            failures += 1

    print("=" * 40)

    if failures:
        print(
            f"Validation completed with "
            f"{failures} failure(s)."
        )
        raise SystemExit(1)

    print("All generated Kickstarts passed.")


if __name__ == "__main__":
    main()
