import pinggy
import dotenv

def create_tunnel(address:str="127.0.0.1:11434"):
    try:
        # Create tunnels
        tunnel = pinggy.start_tunnel(forwardto=address)

        # Print tunnel to screen
        print(f"Successfully created a public link: {tunnel.urls[0]}")
        dotenv.set_key(".env","OLLAMA_BASE_URL",tunnel.urls[0])
        print("Tunnel is running")
        # Keep the process running to maintain the tunnel connection
        tunnel.wait()

    except Exception as e:
        print(f"Error in creating a tunnel: {e}")

if __name__ == "__main__":
    create_tunnel()