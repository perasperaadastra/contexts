import pathlib
import shutil


def prepare_language_data(language_file_location):
    with open(language_file_location, mode="r") as file_object:
        language_data = file_object.read()
    language_data = language_data.replace("\n\n", "\n")
    language_data = "\n".join(language_data.split("\n")[:-1])
    return language_data


def prepare_languages(language_dir, language_s=None):
    if language_s is None:
        language_s = []
    if isinstance(language_s, str):
        language_s = [language_s]
    languages = []
    for language_file_location in language_dir.iterdir():
        if language_file_location.is_file():
            if ".txt" == language_file_location.suffix:
                if language_s == [] or \
                   language_file_location.stem in language_s:
                    language_data = prepare_language_data(language_file_location)
                    languages.append((language_file_location.stem, language_data))
    return languages


def prepare_context_data(context_data_location):
    with open(context_data_location, mode="r") as file_object:
        data = file_object.read()
    nr_obj = len(data.split("\n")[:-1])
    nr_attr = len(data.split("\n")[0])
    return data, nr_obj, nr_attr


def build_burmeister(context_data, language_data):
    data, nr_obj, nr_attr = context_data
    burmeister = f"B\n\n{nr_obj}\n{nr_attr}\n\n{language_data}\n{data}"
    return burmeister


def prepare_context(context_dir, dest_dir, language_s=None):
    languages = prepare_languages(context_dir / "languages", language_s)
    context_data = prepare_context_data(context_dir / "data.context")
    for language_code, language in languages:
        burmeister_context = build_burmeister(context_data, language)
        with open(dest_dir / f"{context_dir.stem}_{language_code}.cxt", mode="w") as file_object:
            file_object.write(burmeister_context)


def prepare_contexts(src_dir, dest_dir, language_s=None):
    if isinstance(src_dir, str):
        src_dir = pathlib.Path(src_dir)

    if isinstance(dest_dir, str):
        dest_dir = pathlib.Path(dest_dir)

    for file_or_dir in sorted(src_dir.iterdir()):
        if file_or_dir.is_dir():
            prepare_context(file_or_dir, dest_dir, language_s=language_s)


if __name__ == "__main__":
    src_dir = "data"
    dest_dir = "contexts/"
    prepare_contexts(src_dir, dest_dir)
    print(f"Prepared contexts in {dest_dir}")
