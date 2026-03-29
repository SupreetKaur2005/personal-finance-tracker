import subprocess
import sys
import time
import os

def wait_for_backend(url="http://localhost:8000", timeout=30):
    """Wait for backend to be ready"""
    import requests
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{url}/health")
            if response.status_code == 200:
                print("✅ Backend is ready!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        
        time.sleep(1)
    
    raise TimeoutError("Backend took too long to start")

def generate_sdk():
    """Generate Python SDK from OpenAPI spec"""
    print("🔄 Generating Python SDK...")
    
    # Wait for backend
    wait_for_backend()
    
    cmd = [
        "openapi-generator-cli", "generate",
        "-i", "http://localhost:8000/openapi.json",
        "-g", "python",
        "-o", "../finance_sdk",
        "--additional-properties", "packageName=finance_sdk",
        "--additional-properties", "projectName=finance-sdk"
    ]
    
    try:
        subprocess.run(cmd, check=True, shell=True)
        print("✅ SDK generated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to generate SDK: {e}")
        print("\nAlternative: Install openapi-generator-cli globally:")
        print("npm install -g @openapitools/openapi-generator-cli")
        sys.exit(1)

if __name__ == "__main__":
    generate_sdk()
