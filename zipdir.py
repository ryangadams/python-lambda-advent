import shutil
import sys

if __name__ == "__main__":
    target_directory = sys.argv[1]

    shutil.make_archive(
        f"{target_directory}/{target_directory}", "zip", target_directory
    )
