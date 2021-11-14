from pathlib import Path, PurePath


def load_fixture(name: str) -> str:
    file_path = PurePath(Path(__file__).parent, "fixtures", name)
    return Path(file_path).read_text()
