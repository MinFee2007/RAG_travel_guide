import os, subprocess, requests, time, dotenv

from tunnel import create_tunnel

def start_AI_server():
    # Load environment variable
    dotenv.load_dotenv()

    # Make a copy of OS environment
    env = os.environ.copy()

    # localhost:11434 instead of 127.0.0.1:11434 to bypass the host header check for loopback
    env["OLLAMA_HOST"] = "0.0.0.0:11434"

    # Allow all origins/tunnels to connect (important)
    env["OLLAMA_ORIGINS"] = "*"

    # Separate log file for Ollama
    log = open("tmp/ollama.log", "w")

    # Run ollama serve command
    process = subprocess.Popen(["ollama", "serve"], env=env, stdout=log, stderr=subprocess.STDOUT)

    # Check connection for 30 times each 1s (30s in total)
    for _ in range(30):
        try:
            if requests.get("http://127.0.0.1:11434/api/tags", timeout=2).ok:
                break
        except requests.RequestException:
            pass
        time.sleep(1)
    else:
        raise RuntimeError("Ollama did not start. Check tmp/ollama.log")

    # Connect successfully
    print("Ollama is running on localhost:11434")
    create_tunnel("127.0.0.1:11434")

if __name__ == "__main__":
    start_AI_server()
