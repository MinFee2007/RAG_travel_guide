import subprocess

if __name__ == "__main__":
    app_path = "application/app.py"
    subprocess.run(["streamlit","run",app_path])