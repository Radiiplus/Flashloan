import os
import subprocess

def run_scripts():
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Run req.py in the 'modules' folder
    req_script_path = os.path.join(script_directory, 'modules', 'req.py')
    subprocess.run(['python3', req_script_path])

    # Change permissions on run.sh in the same folder (without running it)
    run_script_path = os.path.join(script_directory, 'run')
    subprocess.run(['chmod', '+x', run_script_path])

if __name__ == "__main__":
    run_scripts()
