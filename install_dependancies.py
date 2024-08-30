import os
import subprocess

def run_command_in_cmd(command, base_directory=None, new_window=False):
    if base_directory is None:
        base_directory = os.path.join(os.path.expanduser('~'), 'Desktop')
    
    if base_directory:
        os.chdir(base_directory)
        
        if new_window:
            # Use 'start' with 'cmd' to open a new window
            cmd = f'start cmd /K "{command}"'
        else:
            # Execute in the same window
            cmd = f'cmd /C "{command}"'
            
        try:
            process = subprocess.Popen(cmd, shell=True)
            process.communicate(timeout=600)  # 10 minutes timeout
        except subprocess.TimeoutExpired:
            process.kill()
            raise

def install():
    command = "pip install pygame"
    run_command_in_cmd(command, new_window=True)

if __name__ == '__main__':
    install()
