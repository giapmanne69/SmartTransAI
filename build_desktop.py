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
    # Make sure we add Cargo bin path to PATH if running Rust commands
    env = os.environ.copy()
    cargo_bin = os.path.join(os.environ.get("USERPROFILE", ""), ".cargo", "bin")
    if os.path.exists(cargo_bin) and cargo_bin not in env.get("PATH", ""):
        env["PATH"] = cargo_bin + os.pathsep + env["PATH"]

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd, env=env)
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
    tauri_bin_dir = os.path.join(frontend_dir, "src-tauri", "src", "bin")
    
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
    print("\n--- 2. CÀI ĐẶT THƯ VIỆN ĐÓNG GÓI PYINSTALLER ---")
    run_command("pip install pyinstaller pyarmor", cwd=backend_dir)
    
    # Target architecture suffix required by Tauri (Windows 64-bit target default)
    target_triple = "x86_64-pc-windows-msvc"
    dest_exe = os.path.join(tauri_bin_dir, f"SmartTransAI-{target_triple}.exe")
    
    force_build = "--force-backend" in sys.argv
    
    if os.path.exists(dest_exe) and not force_build:
        print("\n--- 3 & 4. SIDECAR BINARY ĐÃ TỒN TẠI, BỎ QUA ĐÓNG GÓI PYINSTALLER ---")
        print(f"Tìm thấy sidecar tại: {dest_exe}")
        print("Sử dụng file sidecar hiện tại. Để bắt buộc build lại backend, hãy chạy lệnh: python build_desktop.py --force-backend")
    else:
        # 3. Build single executable backend using PyInstaller for Tauri Sidecar
        print("\n--- 3. ĐÓNG GÓI BACKEND FATASTPI BẰNG PYINSTALLER ---")
        
        # Clean up any existing PyInstaller dist, build folders or spec files
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
        
        # Pack backend API as single file
        pyinstaller_dist_dir = os.path.join(backend_dir, "dist")
        pack_command = (
            f"pyinstaller"
            f" --noconfirm"
            f" --clean"
            f" --name=SmartTransAI"
            f" --copy-metadata fastapi"
            f" --copy-metadata uvicorn"
            f" --copy-metadata langchain-core"
            f" --copy-metadata langchain-openai"
            f" --copy-metadata langgraph"
            f" --hidden-import passlib.handlers.sha2_crypt"
            f" --distpath=\"{pyinstaller_dist_dir}\""
            f" --workpath=\"{build_temp_dir}\""
            f" --onefile"
            f" \"{entrypoint}\""
        )
        
        run_command(pack_command, cwd=backend_dir)
        
        # 4. Copy backend executable to Tauri sidecar folder with target triple
        print("\n--- 4. CẤU HÌNH SIDECAR CHO TAURI APP ---")
        os.makedirs(tauri_bin_dir, exist_ok=True)
        
        src_exe = os.path.join(pyinstaller_dist_dir, "SmartTransAI.exe")
        
        if not os.path.exists(src_exe):
            print("Lỗi: Không tìm thấy file chạy backend sau khi build PyInstaller.")
            sys.exit(1)
            
        print(f"Copying backend sidecar: {src_exe} -> {dest_exe}")
        shutil.copy2(src_exe, dest_exe)
    
    # Ensure sidecar is also copied to target/release folder to prevent WiX/light.exe from failing
    target_release_dir = os.path.join(frontend_dir, "src-tauri", "target", "release")
    os.makedirs(target_release_dir, exist_ok=True)
    target_release_exe = os.path.join(target_release_dir, f"SmartTransAI-{target_triple}.exe")
    print(f"Manually copying sidecar to target/release to ensure WiX compatibility: {dest_exe} -> {target_release_exe}")
    shutil.copy2(dest_exe, target_release_exe)

    # 5. Build Tauri Desktop Installer
    print("\n--- 5. BIÊN DỊCH VÀ ĐÓNG GÓI TAURI DESKTOP APPLICATION ---")
    # Force install Tauri CLI v1 if not present to match the v1 Rust project dependencies and schema
    tauri_cli_path = os.path.join(frontend_dir, "node_modules", "@tauri-apps", "cli")
    if os.path.exists(tauri_cli_path):
        print("Tauri CLI is already installed, skipping npm install to avoid file locks.")
    else:
        print("Ensuring Tauri CLI v1 dependency is installed...")
        run_command("npm install -D @tauri-apps/cli@^1", cwd=frontend_dir)

    # Execute Tauri Release Build
    run_command("npx tauri build", cwd=frontend_dir)
    
    # Clean up temporary files
    try:
        if os.path.exists(build_temp_dir):
            shutil.rmtree(build_temp_dir)
        if os.path.exists(pyinstaller_dist_dir):
            shutil.rmtree(pyinstaller_dist_dir)
    except Exception as e:
        print(f"Temporary files cleanup warning: {str(e)}")
    
    print("\n--- HOÀN THÀNH ---")
    print("Ứng dụng Desktop đã được đóng gói thành công cùng Sidecar Backend!")
    print(f"Các gói cài đặt (.msi / .exe) nằm tại thư mục:")
    print(f"  {os.path.join(frontend_dir, 'src-tauri', 'target', 'release', 'bundle')}")

if __name__ == "__main__":
    main()
