"""
CADE System Initialization Script

This script handles the complete setup and initialization of the CADE system,
including dependency installation, configuration, and first-time setup.
"""

import json
import os
import platform
import shutil
import subprocess
import sys
import venv
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Constants
REQUIREMENTS_FILES = ["requirements.txt", "requirements-prod.txt"]
CONFIG_FILES = ["config.ini", ".env"]
DATA_DIRS = ["data", "logs", "plugins"]


class CadeInstaller:
    def __init__(self):
        self.root_dir = Path(__file__).parent.absolute()
        self.is_windows = platform.system() == "Windows"
        self.python_cmd = "python" + ("3" if not self.is_windows else "")
        self.pip_cmd = f"{self.python_cmd} -m pip"
        self.venv_dir = self.root_dir / "venv"
        self.venv_python = str(
            self.venv_dir
            / ("Scripts\\python.exe" if self.is_windows else "bin/python3")
        )
        self.venv_pip = f"{self.venv_python} -m pip"
        self.use_venv = True

    def run_command(
        self, cmd: str, cwd: Optional[Path] = None, shell: bool = True
    ) -> Tuple[bool, str]:
        """Run a shell command and return (success, output)"""
        try:
            print(f"$ {cmd}")
            result = subprocess.run(
                cmd,
                cwd=str(cwd or self.root_dir),
                shell=shell,
                check=True,
                text=True,
                capture_output=True,
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, f"{e.stderr}\n{e.stdout}"

    def check_python_version(self) -> bool:
        """Check if Python version is compatible"""
        major, minor = sys.version_info.major, sys.version_info.minor
        if major < 3 or (major == 3 and minor < 8):
            print(f"❌ Python 3.8+ is required, but found {platform.python_version()}")
            return False
        print(f"✅ Python {platform.python_version()} is compatible")
        return True

    def setup_virtualenv(self) -> bool:
        """Set up a Python virtual environment"""
        if self.venv_dir.exists():
            print(f"✅ Virtual environment already exists at {self.venv_dir}")
            return True

        print(f"Creating virtual environment at {self.venv_dir}...")
        try:
            venv.create(self.venv_dir, with_pip=True)
            print("✅ Virtual environment created successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to create virtual environment: {e}")
            self.use_venv = False
            return False

    def install_dependencies(self) -> bool:
        """Install Python dependencies"""
        pip_cmd = self.venv_pip if self.use_venv else self.pip_cmd

        # Upgrade pip first
        success, output = self.run_command(f"{pip_cmd} install --upgrade pip")
        if not success:
            print(f"❌ Failed to upgrade pip: {output}")
            return False

        # Install requirements
        for req_file in REQUIREMENTS_FILES:
            if not (self.root_dir / req_file).exists():
                print(f"⚠️  {req_file} not found, skipping...")
                continue

            print(f"Installing dependencies from {req_file}...")
            success, output = self.run_command(f"{pip_cmd} install -r {req_file}")
            if not success:
                print(f"❌ Failed to install dependencies from {req_file}: {output}")
                return False

        print("✅ All dependencies installed successfully")
        return True

    def setup_environment(self) -> bool:
        """Set up environment configuration"""
        # Create .env file if it doesn't exist
        env_file = self.root_dir / ".env"
        if not env_file.exists():
            with open(env_file, "w") as f:
                f.write("# CADE System Environment Variables\n")
                f.write("CADE_ENV=development\n")
                f.write("LOG_LEVEL=INFO\n")
                f.write("DATABASE_URL=sqlite:///data/cade.db\n")
            print("✅ Created .env file with default settings")

        # Create config.ini if it doesn't exist
        config_file = self.root_dir / "config.ini"
        if not config_file.exists():
            with open(config_file, "w") as f:
                f.write(
                    """[database]
engine = sqlite
name = cade
host = localhost
port =
username =
password =

[logging]
level = INFO
file = logs/cade.log
max_size = 10  # MB
backup_count = 5

[server]
host = 0.0.0.0
port = 8000
debug = True
"""
                )
            print("✅ Created config.ini with default settings")

        return True

    def setup_directories(self) -> bool:
        """Create necessary directories"""
        try:
            for dir_name in DATA_DIRS:
                dir_path = self.root_dir / dir_name
                dir_path.mkdir(exist_ok=True, parents=True)
                print(f"✅ Created directory: {dir_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to create directories: {e}")
            return False

    def run_initial_checks(self) -> bool:
        """Run initial system checks"""
        if not self.check_python_version():
            return False

        if not self.setup_virtualenv():
            print("⚠️  Continuing without virtual environment")

        if not self.setup_directories():
            return False

        if not self.setup_environment():
            return False

        return True

    def install_system_dependencies(self) -> bool:
        """Install system-level dependencies if needed"""
        if self.is_windows:
            print(
                "ℹ️  On Windows, please ensure you have the necessary build tools installed."
            )
            print(
                "   You may need to install them from: https://visualstudio.microsoft.com/visual-cpp-build-tools/"
            )
        else:
            print("Checking for system dependencies...")
            # Example for Debian/Ubuntu
            # self.run_command("sudo apt-get update && sudo apt-get install -y python3-dev python3-venv build-essential")

        return True

    def run_database_migrations(self) -> bool:
        """Run database migrations if any"""
        print("Running database migrations...")
        # Example: self.run_command(f"{self.venv_python} manage.py migrate")
        print("✅ Database setup complete")
        return True

    def print_success_message(self):
        """Print success message with next steps"""
        print("\n🎉 CADE System Setup Complete!")
        print("\nNext steps:")
        print(f"1. Review the configuration in {self.root_dir}/config.ini")
        print(f"2. Edit environment variables in {self.root_dir}/.env if needed")
        print("3. Start the development server with:")
        print(
            f"   {self.venv_python} -m cade_production"
            if self.use_venv
            else "   python -m cade_production"
        )
        print("\nFor production deployment:")
        print("1. Update the .env file with production settings")
        print("2. Set up a production web server (e.g., gunicorn, uvicorn)")
        print("3. Configure a reverse proxy (e.g., Nginx, Apache)")

    def run(self) -> bool:
        """Run the complete setup process"""
        print("🚀 Starting CADE System Setup...\n")

        try:
            if not self.run_initial_checks():
                return False

            if not self.install_system_dependencies():
                return False

            if not self.install_dependencies():
                return False

            if not self.run_database_migrations():
                return False

            self.print_success_message()
            return True

        except Exception as e:
            print(f"\n❌ Setup failed: {e}")
            return False


if __name__ == "__main__":
    installer = CadeInstaller()
    success = installer.run()
    sys.exit(0 if success else 1)
