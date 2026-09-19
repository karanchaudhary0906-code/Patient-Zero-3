import os
import sys
import subprocess

def main():
    port = os.environ.get("PORT", "8000")
    host = os.environ.get("HOST", "0.0.0.0")

    # Path to virtual env python
    venv_python = os.path.join(os.path.dirname(__file__), ".venv", "Scripts", "python.exe")
    if not os.path.exists(venv_python):
        # Fallback to linux/unix style venv path
        unix_venv = os.path.join(os.path.dirname(__file__), ".venv", "bin", "python")
        venv_python = unix_venv if os.path.exists(unix_venv) else sys.executable

    # Reconfigure Windows stdout for UTF-8 compatibility
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 64)
    print("  PATIENT ZERO: THE MISSING CONTEXT (Unified Full-Stack)")
    print("  Longitudinal Patient Timeline & Sourced Insights Engine")
    print("=" * 64)
    print("  [+] FRONTEND & BACKEND MERGED ON A SINGLE SERVER:")
    print(f"      [UI]     Frontend Web UI:   http://127.0.0.1:{port}")
    print(f"      [API]    Backend REST API:  http://127.0.0.1:{port}/api")
    print(f"      [DOCS]   API Documentation: http://127.0.0.1:{port}/docs")
    print(f"      [HEALTH] Service Health:    http://127.0.0.1:{port}/api/health")
    print(f"  [+] Host: {host} | Port: {port}")
    print("=" * 64)
    print(f"  Ready! Open http://127.0.0.1:{port} in your browser.")
    print("=" * 64 + "\n")


    cmd = [venv_python, "-m", "uvicorn", "app.main:app", "--host", host, "--port", str(port)]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n[!] Server stopped by user.")

if __name__ == "__main__":
    main()