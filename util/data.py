from util import const


def get_audio_path(filename: str):
    return const.AUDIO_PATH + filename


def read_string(filename: str):
    """
    Reads a file from the data directory or its subdirectories and returns it as a string.

    Args:
        filename: Name of the file that should be read, can contain slashes for subdirectories

    Returns:
        Content of the file as string.
    """
    with open("data/" + filename, "r") as file:
        return file.read()
