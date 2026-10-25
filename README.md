# AI File Organizer

A beginner-friendly Python project that uses a locally running open-weight AI model to suggest categories for files.

## Features

- Uses Gemma through Ollama.
- Suggests categories based on filenames.
- Preview mode is the default; files are not moved unless `--apply` is supplied.
- Does not overwrite an existing file in a destination category.
- Uses Python's standard library; no pip packages are required.

## Categories

`Study`, `Images`, `Documents`, `Videos`, `Audio`, `Archives`, `Code`, and `Other`.

## Requirements

- Python 3
- [Ollama](https://ollama.com/download/linux)
- The `gemma3:1b` model

## Setup on Linux

Install Python and Git if needed:

```bash
sudo apt update
sudo apt install -y python3 git
```

Install Ollama using its official instructions: https://ollama.com/download/linux

Download the model:

```bash
ollama pull gemma3:1b
```

Check that the model is installed:

```bash
ollama list
```

## Run the project

Clone the repository or open this project folder, then run:

```bash
python3 main.py
```

By default, the program previews the files in `sample_files/`. It does not move them.

To test it, add a few sample files to `sample_files/`. Empty placeholder files are okay for filename classification.

After reviewing the preview, apply the changes:

```bash
python3 main.py --apply
```

To preview a different folder:

```bash
python3 main.py --folder "/path/to/your/folder"
```

To organize that folder after reviewing the preview:

```bash
python3 main.py --folder "/path/to/your/folder" --apply
```

## How it works

1. Python reads filenames in the selected folder.
2. It sends each filename to the local Ollama API.
3. Gemma suggests one category.
4. The program displays the proposed category.
5. Files are moved only when `--apply` is provided.

## Privacy

This program sends filenames to the Ollama service running on your computer. It does not call a cloud AI API. Avoid using it on sensitive files unless you understand the information contained in their filenames.

## Limitations

- Classification can be incorrect because it is based on filenames, not full document contents.
- Ollama must be installed and running, and the model must be downloaded.
- Review the preview before applying changes.
- The program only checks files directly inside the selected folder; it does not recursively process subfolders.

## Project status

Educational beginner project created for learning Python, local AI, and Git/GitHub workflows.

## License

MIT. See [LICENSE](LICENSE).
