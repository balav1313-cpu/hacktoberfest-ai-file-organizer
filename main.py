import argparse
import json
import shutil
import urllib.request
import urllib.error
from pathlib import Path

MODEL = "gemma3:1b"
CATEGORIES = [
    "Study", "Images", "Documents", "Videos",
    "Audio", "Archives", "Code", "Other"
]


def classify_file(filename: str) -> str:
    """Classify a filename using a locally running Ollama model."""
    prompt = (
        "Classify the following filename into exactly one of these categories: "
        + ", ".join(CATEGORIES)
        + ". Filename: " + filename
        + ". Reply with only the category name."
    )

    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }).encode("utf-8")

    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(
            "Could not connect to Ollama. Start Ollama and check that "
            f"the model '{MODEL}' is installed. Details: {exc}"
        ) from exc

    answer = result.get("response", "").strip()
    for category in CATEGORIES:
        if answer.casefold() == category.casefold():
            return category

    return "Other"


def organize_files(folder: Path, apply_changes: bool) -> None:
    folder = folder.expanduser().resolve()

    if not folder.is_dir():
        raise SystemExit(f"Error: folder does not exist: {folder}")

    files = sorted(
        item for item in folder.iterdir()
        if item.is_file()
    )

    if not files:
        print(f"No files found in: {folder}")
        return

    print("\nAI File Organizer")
    print(f"Folder: {folder}")
    print(f"Mode: {'APPLY CHANGES' if apply_changes else 'PREVIEW ONLY'}")
    print("-" * 50)

    for file_path in files:
        try:
            category = classify_file(file_path.name)
            destination_folder = folder / category
            destination = destination_folder / file_path.name
            print(f"{file_path.name} -> {category}/")

            if apply_changes:
                destination_folder.mkdir(exist_ok=True)

                # Never overwrite an existing file.
                if destination.exists():
                    print("  Skipped: destination already exists.")
                    continue

                shutil.move(str(file_path), str(destination))

        except Exception as error:
            print(f"Could not process {file_path.name}: {error}")

    if apply_changes:
        print("\nFinished organizing files.")
    else:
        print("\nPreview only: no files were moved.")
        print("Review the results, then rerun with --apply to move files.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Organize files using a local Ollama AI model."
    )
    parser.add_argument(
        "--folder",
        default="./sample_files",
        help="Folder to organize (default: ./sample_files)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually move files; without this option, only preview",
    )
    args = parser.parse_args()
    organize_files(Path(args.folder), args.apply)


if __name__ == "__main__":
    main()
