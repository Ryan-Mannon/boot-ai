import os

def get_file_content(working_directory: str, file_path: str) -> str:

    try:

        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

        if not os.path.isfile(target_dir):
            raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')


        #Read the file and return its contents as a string

        MAX_CHARS = 10_000

        with open(target_dir, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    

    except Exception as e:
        return(f"Error: {e}")

    return file_content_string