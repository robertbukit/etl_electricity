import subprocess
import sys

def run_script(script_path):
    """
    helper function to run the other python script (etl)
    """

    # Running the script as if we're type in the terminal
    result = subprocess.run([sys.executable, script_path])

    if result.returncode == 0:
        print(f"Orchestrator {script_path} successfully executed")
        return True

    else:
        print(f"Orchestrator crash in script {script_path}")
        return False


def main():
    """
    main orchestrator pipeline
    """

    #1. Execute extract code program
    if not run_script("scripts/extract.py"):
        sys.exit(1)

    #2. Execute transform code program
    if not run_script("scripts/transform.py"):
        sys.exit(1)

    #3. Execuute load code program
    if not run_script("scripts/load.py"):
        sys.exit(1)

if __name__ == "__main__":
    main()

