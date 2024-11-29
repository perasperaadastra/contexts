import pathlib

import yaml

def merge_yaml_files(input_directory, output_file, comment=None):
    """
    Merges all YAML files in the specified directory into a single YAML file.

    This function traverses the given input directory recursively, searching for
    all files with a `.yaml` or `.yml` extension. It loads the contents of these
    files and merges them into a single dictionary. The merged data is then written
    to the specified output file. If a comment is provided, it will be added at
    the top of the output YAML file.

    Parameters:
    -----------
    input_directory : pathlib.Path or str
        The path to the directory containing YAML files to merge.
    output_file : pathlib.Path or str
        The path where the merged YAML file will be saved.
    comment : str (optional)
        A comment to add at the top of the output YAML file.
        Defaults to None, which means no comment will be added.

    Raises:
    -------
    FileNotFoundError:
        If the input directory does not exist.
    yaml.YAMLError:
        If there is an error reading any of the YAML files.

    Example:
    --------
    >>> merge_yaml_files(
    ...    'path/to/yaml/files',
    ...    'merged_output.yaml',
    ...    comment='This is a merged YAML configuration',
    ... )

    Note:
    -----
    The merged data will overwrite any existing content in the output file.
    """
    if isinstance(input_directory, str):
        input_directory = pathlib.Path(input_directory)

    merged_data = {}

    for root, _, files in input_directory.walk():
        for file_name in files:
            file_path = root / file_name
            if ".yaml" in file_path.suffixes or ".yml" in file_path.suffixes:
                with open(file_path, mode='r') as f:
                    try:
                        data = yaml.safe_load(f)
                        merged_data = {**merged_data, **data}
                    except yaml.YAMLError as e:
                        print(f"Error reading {file_path}: {e}")

    with open(output_file, mode='w') as outfile:
        if comment is not None:
            outfile.write(f"# {comment}\n")
        yaml.dump(merged_data, outfile, default_flow_style=False, allow_unicode=True)


if __name__ == "__main__":
    input_dir = "data"
    output_file = "merged-contexts-metadata.yaml"
    comment = "This is the automatically merged metadata. Please do not modify it directly."
    merge_yaml_files(input_dir, output_file, comment)
    print(f"Merged YAML files into {output_file}")
