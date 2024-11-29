import pathlib
import shutil


def prepare_contexts(src_dir, dest_dir):
    if isinstance(src_dir, str):
        src_dir = pathlib.Path(src_dir)

    if isinstance(dest_dir, str):
        dest_dir = pathlib.Path(dest_dir)

    for file_or_dir_ in src_dir.iterdir():
        if file_or_dir_.is_dir():
            for file_or_dir in file_or_dir_.iterdir():
                if file_or_dir.is_file() and ".cxt" == file_or_dir.suffix:
                    shutil.copyfile(file_or_dir, dest_dir / file_or_dir.name)


if __name__ == "__main__":
    src_dir = "data"
    dest_dir = "contexts"
    prepare_contexts(src_dir, dest_dir)
    print(f"Prepared contexts in {dest_dir}")
