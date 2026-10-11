#!/usr/bin/env python3

from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os


BIND_ADDRESS = "10.10.10.100"
PORT = 8000

WEB_ROOT = (
    Path.home()
    / "linux-lab"
    / "provisioning"
    / "kickstart"
    / "http-root"
)


def main():
    if not WEB_ROOT.is_dir():
        raise FileNotFoundError(
            f"HTTP root does not exist: {WEB_ROOT}"
        )

    os.chdir(WEB_ROOT)

    server = ThreadingHTTPServer(
        (BIND_ADDRESS, PORT),
        SimpleHTTPRequestHandler,
    )

    print("RHEL Kickstart provisioning server")
    print(f"Root: {WEB_ROOT}")
    print(f"URL:  http://{BIND_ADDRESS}:{PORT}/")
    print()
    print("Available Kickstarts:")

    ks_dir = WEB_ROOT / "ks"

    for file in sorted(ks_dir.glob("*.cfg")):
        print(
            f"  http://{BIND_ADDRESS}:{PORT}/ks/{file.name}"
        )

    print()
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nStopping provisioning server.")

    finally:
        server.server_close()


if __name__ == "__main__":
    main()
