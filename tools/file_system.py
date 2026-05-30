# file_system.py
# Virtual File System — agents use this to save and read their work.
# It is just a Python dictionary stored inside LangGraph state.
# Key = filename,  Value = content string


def write_file(virtual_files: dict, filename: str, content: str) -> dict:
    """Save content to a virtual file. Returns updated dict."""
    virtual_files[filename] = content
    return virtual_files


def read_file(virtual_files: dict, filename: str) -> str:
    """Read one file. Returns empty string if file does not exist."""
    return virtual_files.get(filename, "")


def list_files(virtual_files: dict) -> list:
    """List all saved filenames."""
    return list(virtual_files.keys())


def read_all_files(virtual_files: dict) -> str:
    """Read every file and combine into one big string for the synthesizer."""
    if not virtual_files:
        return "No files found."
    combined = ""
    for filename, content in virtual_files.items():
        combined += f"\n\n=== {filename} ===\n{content}"
    return combined.strip()
