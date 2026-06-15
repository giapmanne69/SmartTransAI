import subprocess
import os
import sys
import shutil

# Configure stdout and stderr to use UTF-8 to prevent encoding crashes on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def run_command(command, cwd=None):
    print(f"Executing: {command} (cwd: {cwd})")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
    for line in iter(process.stdout.readline, b''):
        # Decode using utf-8 and ignore errors, then write
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
    node_modules_dir = os.path.join(frontend_dir, "node_modules")
    if not os.path.exists(node_modules_dir):
        run_command("npm install", cwd=frontend_dir)
    else:
        print("node_modules đã tồn tại, bỏ qua bước cài đặt npm install.")
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
    
    # 3. Build single executable using Pure PyInstaller (Solution A)
    print("\n--- 3. ĐÓNG GÓI BACKEND BẰNG PYINSTALLER THUẦN TÚY ---")
    
    # Define build output path
    dist_output_dir = os.path.join(project_root, "dist_desktop")
    if os.path.exists(dist_output_dir):
        shutil.rmtree(dist_output_dir)
    os.makedirs(dist_output_dir, exist_ok=True)
    
    # Clean up any existing PyInstaller dist, build folders or spec files in backend/root to avoid conflict
    for folder in ["dist", "build", "run_desktop.spec", "SmartTransAI.spec"]:
        p = os.path.join(backend_dir, folder)
        if os.path.exists(p):
            try:
                if os.path.isdir(p):
                    shutil.rmtree(p)
                else:
                    os.remove(p)
            except Exception as e:
                print(f"Pre-cleanup warning for {folder}: {str(e)}")
                
    build_temp_dir = os.path.join(project_root, "build_temp")
    if os.path.exists(build_temp_dir):
        shutil.rmtree(build_temp_dir)

    entrypoint = os.path.join(backend_dir, "run_desktop.py")
    
    # Run PyInstaller command directly
    pack_command = (
        f"pyinstaller"
        f" --noconfirm"
        f" --clean"
        f" --name=SmartTransAI"
        f" --add-data=\"{dist_dir};frontend/dist\""
        f" --copy-metadata fastapi"
        f" --copy-metadata uvicorn"
        f" --copy-metadata langchain-core"
        f" --copy-metadata langchain-openai"
        f" --copy-metadata langgraph"
        f" --hidden-import passlib.handlers.sha2_crypt"
        f" --distpath=\"{dist_output_dir}\""
        f" --workpath=\"{build_temp_dir}\""
        f" --onefile"
        f" \"{entrypoint}\""
    )
    
    run_command(pack_command, cwd=backend_dir)
    
    # Clean up temporary files in root or backend
    try:
        for spec in ["SmartTransAI.spec", "run_desktop.spec"]:
            for path_dir in [backend_dir, project_root]:
                spec_path = os.path.join(path_dir, spec)
                if os.path.exists(spec_path):
                    os.remove(spec_path)
        
        if os.path.exists(build_temp_dir):
            shutil.rmtree(build_temp_dir)
    except Exception as e:
        print(f"Temporary files cleanup warning: {str(e)}")
    
    print("\n--- HOÀN THÀNH ---")
    print(f"Ứng dụng đã được đóng gói thành công!")
    print(f"File chạy (.exe) nằm tại: {os.path.join(dist_output_dir, 'SmartTransAI.exe')}")
    print("\nHướng dẫn chạy ứng dụng:")
    print("1. Đảm bảo Ollama đã được bật và mô hình Llama-3 đã được tải.")
    print("2. Chạy file 'SmartTransAI.exe'.")
    print("3. Mở trình duyệt web truy cập 'http://localhost:8000' để trải nghiệm (nếu không chạy trực tiếp dưới dạng GUI).")

if __name__ == "__main__":
    main()
