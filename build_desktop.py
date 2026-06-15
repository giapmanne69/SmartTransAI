import subprocess
import os
import sys
import shutil

def run_command(command, cwd=None):
    print(f"Executing: {command} (cwd: {cwd})")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
    for line in iter(process.stdout.readline, b''):
        sys.stdout.write(line.decode('utf-8', errors='ignore'))
    process.stdout.close()
    return_code = process.wait()
    if return_code != 0:
        print(f"Command failed with exit code: {return_code}")
        sys.exit(return_code)

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(project_root, "frontend")
    backend_dir = os.path.join(project_root, "backend")
    
    # 1. Build the React frontend
    print("\n--- 1. XÂY DỰNG GIAO DIỆN REACT FRONTEND ---")
    run_command("npm install", cwd=frontend_dir)
    run_command("npm run build", cwd=frontend_dir)
    
    # Check if build output exists
    dist_dir = os.path.join(frontend_dir, "dist")
    if not os.path.exists(dist_dir):
        print("Lỗi: Không tìm thấy thư mục 'dist' sau khi build frontend.")
        sys.exit(1)
        
    print("Xây dựng frontend thành công!")

    # 2. Setup python packaging libraries
    print("\n--- 2. CÀI ĐẶT THƯ VIỆN ĐÓNG GÓI ---")
    run_command("pip install pyinstaller pyarmor", cwd=backend_dir)
    
    # 3. Build single executable using PyArmor + PyInstaller
    # We will use PyArmor to obfuscate and then bundle it
    print("\n--- 3. ĐÓNG GÓI BACKEND BẰNG PYARMOR & PYINSTALLER ---")
    
    # Define build output path
    dist_output_dir = os.path.join(project_root, "dist_desktop")
    if os.path.exists(dist_output_dir):
        shutil.rmtree(dist_output_dir)
    os.makedirs(dist_output_dir, exist_ok=True)
    
    # We use pyarmor to obfuscate the backend/app code first,
    # then package it with pyinstaller.
    # PyArmor command to pack:
    # "pyarmor pack -e 'pyinstaller options' script"
    # To include our React frontend dist in the build so FastAPI can serve it, 
    # we need to copy it into the executable data.
    # Also, we include uvicorn/fastapi metadata which is needed for runtime.
    pyinstaller_options = (
        f" --noconfirm"
        f" --clean"
        f" --name=SmartTransAI"
        f" --add-data=\"{dist_dir};frontend/dist\""
        f" --copy-metadata fastapi"
        f" --copy-metadata uvicorn"
        f" --copy-metadata langchain-core"
        f" --copy-metadata langchain-openai"
        f" --copy-metadata langgraph"
        f" --distpath=\"{dist_output_dir}\""
        f" --workpath=\"{os.path.join(project_root, 'build_temp')}\""
    )
    
    entrypoint = os.path.join(backend_dir, "app", "main.py")
    pack_command = f"pyarmor pack {pyinstaller_options} \"{entrypoint}\""
    
    run_command(pack_command, cwd=backend_dir)
    
    print("\n--- HOÀN THÀNH ---")
    print(f"Ứng dụng đã được đóng gói thành công!")
    print(f"File chạy (.exe) nằm tại: {os.path.join(dist_output_dir, 'SmartTransAI.exe')}")
    print("\nHướng dẫn chạy ứng dụng:")
    print("1. Đảm bảo Ollama đã được bật và mô hình Llama-3 đã được tải.")
    print("2. Chạy file 'SmartTransAI.exe'.")
    print("3. Mở trình duyệt web truy cập 'http://localhost:8000' để trải nghiệm (nếu không chạy trực tiếp dưới dạng GUI).")

if __name__ == "__main__":
    main()
