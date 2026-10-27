import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function":{
        "name": "run_python_file",
        "description": "Execute a Python file with optional command-line arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the Python file to execute",
                },
                "args": {
                    "type": "array",
                    "description": "Optional command-line arguments to pass to the script",
                    "items": {
                        "type": "string",
                        "description": "A single argument string",
                    },  
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:

        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]
        if args != None:
            command.extend(args)
        
        sub_process = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, timeout=30)
        process_string = ""    

        if sub_process.returncode != 0:
            process_string += f"Process exited with code {sub_process.returncode}"
        if sub_process.stdout == "" and sub_process.stderr == "":
            process_string += "No output produced"
        if sub_process.stdout != "":
            process_string += f"STDOUT: {sub_process.stdout}"
        if sub_process.stderr != "":
            process_string += f"STDERR: {sub_process.stderr}"
        
    except Exception as e:
        return (f"Error: {e}")

    return process_string