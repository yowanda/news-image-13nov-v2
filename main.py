"""news-image-01 entry: copy the bundled world-news image to /output/entry.png.

Standard library only, no network. The entry image (entry.png, shipped
beside this file) is copied to the output directory and verified
byte-for-byte before the program reports success.
"""

import hashlib
import os
import shutil
import sys


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(output_dir, "entry.png")

    if not os.path.isfile(source):
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1

    os.makedirs(output_dir, exist_ok=True)
    shutil.copyfile(source, target)

    source_hash = sha256_of(source)
    target_hash = sha256_of(target)
    if source_hash != target_hash:
        print(
            "error: verification failed: /output/entry.png differs from "
            "entry.png ({} != {})".format(source_hash, target_hash),
            file=sys.stderr,
        )
        return 1

    print(
        "ok: wrote {} ({} bytes, sha256 {})".format(
            target, os.path.getsize(target), target_hash
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
