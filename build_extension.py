import json
import shutil
import subprocess
import sys
from pathlib import Path


def transpile_with_transcrypt(source: Path, output: Path, workdir: Path) -> None:
    """
    Use Transcrypt to transpile Python to JavaScript.
    - Requires `pip install transcrypt`.
    - Generates __target__/logic.js which we copy to content.js.
    """
    transcrypt_bin = shutil.which("transcrypt")
    if not transcrypt_bin:
        candidates = [Path.home() / ".local" / "bin" / "transcrypt"]
        for candidate in candidates:
            if candidate.exists():
                transcrypt_bin = str(candidate)
                break
    if not transcrypt_bin:
        raise RuntimeError(
            "Transcrypt CLI not found. Ensure `~/.local/bin` is on PATH or install with "
            "`pip install --user transcrypt`."
        )

    # Run transcrypt to generate JS into __target__/
    subprocess.run(
        [transcrypt_bin, "-b", "-m", "-n", str(source.name)],
        check=True,
        cwd=workdir,
    )

    generated = workdir / "__target__" / f"{source.stem}.js"
    if not generated.exists():
        raise FileNotFoundError(f"Expected generated file not found: {generated}")

    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(generated, output)


def build_extension() -> Path:
    """
    Build the Chrome extension by transpiling Python (Transcrypt) to JS.
    """
    base_dir = Path(__file__).parent
    ext_dir = base_dir / "simple_ext"
    ext_dir.mkdir(exist_ok=True)

    source_py = base_dir / "logic.py"
    if not source_py.exists():
        raise FileNotFoundError(
            "logic.py not found. Add your Python logic there (RapydScript syntax)."
        )

    content_js = ext_dir / "content.js"
    transpile_with_transcrypt(source_py, content_js, base_dir)

    manifest = {
        "manifest_version": 3,
        "name": "Python via Transcrypt",
        "version": "1.3.0",
        "description": "Chrome extension logic written in Python, transpiled via Transcrypt.",
        "permissions": [],
        "host_permissions": ["<all_urls>"],
        "content_scripts": [
            {
                "matches": ["<all_urls>"],
                "js": ["content.js"],
                "run_at": "document_idle",
            }
        ],
    }

    (ext_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))

    return ext_dir


if __name__ == "__main__":
    try:
        built_dir = build_extension()
        print(f"Extension built at: {built_dir.resolve()}")
    except Exception as exc:  # keep surface simple for CLI
        sys.stderr.write(f"Build failed: {exc}\n")
        sys.exit(1)

