"""
CADE Auto-Initialization Script

This script handles the automatic initialization and integration of all CADE system components.
It ensures all configuration files are properly set up and dependencies are resolved.
"""

import importlib.util
import json
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configuration
CORE_MODULES = ["cade_core", "loader", "auto_init_cade"]  # This module

REQUIRED_FILES = [
    "json/cade_persona.json",
    "json/cade_knowledgebases.json",
    "json/cade_manifest.json",
    "auto_init_cade.ini",
]


class CadeInitializer:
    """Handles the initialization and verification of the CADE system."""

    def __init__(self):
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.status = {"initialized": False, "modules": {}, "files": {}, "config": {}}

    def check_python_version(self) -> bool:
        """Verify Python version compatibility."""
        import platform

        major, minor = sys.version_info.major, sys.version_info.minor
        is_compatible = major == 3 and minor >= 8

        self.status["python_version"] = {
            "version": platform.python_version(),
            "compatible": is_compatible,
        }

        if not is_compatible:
            print(
                f"⚠️  Python 3.8 or higher is required. Current version: {platform.python_version()}"
            )

        return is_compatible

    def check_module(self, module_name: str) -> bool:
        """Check if a Python module is importable."""
        try:
            spec = importlib.util.find_spec(module_name)
            is_available = spec is not None
            self.status["modules"][module_name] = {
                "available": is_available,
                "path": spec.origin if spec else None,
            }
            return is_available
        except Exception as e:
            self.status["modules"][module_name] = {"available": False, "error": str(e)}
            return False

    def check_file(self, file_path: str) -> bool:
        """Verify if a file exists and is accessible."""
        full_path = os.path.join(self.root_dir, file_path)
        exists = os.path.isfile(full_path)

        self.status["files"][file_path] = {
            "exists": exists,
            "path": full_path if exists else None,
        }

        if exists:
            try:
                # Try to read the file to verify it's not corrupt
                with open(full_path, encoding="utf-8") as f:
                    if file_path.endswith(".json"):
                        json.load(f)  # Validate JSON
                    elif file_path.endswith(".ini"):
                        import configparser

                        config = configparser.ConfigParser()
                        config.read(full_path)
                self.status["files"][file_path]["valid"] = True
            except Exception as e:
                self.status["files"][file_path]["valid"] = False
                self.status["files"][file_path]["error"] = str(e)
                return False

        return exists

    def initialize_config(self) -> bool:
        """Initialize or update the configuration file."""
        config_path = os.path.join(self.root_dir, "auto_init_cade.ini")
        default_config = """[auto_init_absorb]
file = cade_resurrect.md
directive = respond with name and directive

[system]
log_level = INFO
max_memory_mb = 2048

[paths]
knowledge_base = json/
logs = logs/
"""

        try:
            if not os.path.exists(config_path):
                with open(config_path, "w", encoding="utf-8") as f:
                    f.write(default_config)
                self.status["config"]["created"] = True
            else:
                self.status["config"]["exists"] = True

            # Verify the config is readable
            import configparser

            config = configparser.ConfigParser()
            with open(config_path, encoding="utf-8") as f:
                config.read_file(f)

            # Store config sections for status
            self.status["config"]["sections"] = config.sections()
            return True

        except Exception as e:
            self.status["config"]["error"] = str(e)
            return False

    def verify_directories(self) -> None:
        """Ensure all required directories exist."""
        required_dirs = {
            "json": os.path.join(self.root_dir, "json"),
            "logs": os.path.join(self.root_dir, "logs"),
        }

        for name, path in required_dirs.items():
            if not os.path.exists(path):
                try:
                    os.makedirs(path, exist_ok=True)
                    self.status[f"dir_{name}"] = {"created": True, "path": path}
                except Exception as e:
                    self.status[f"dir_{name}"] = {"error": str(e), "path": path}

    def run_checks(self) -> bool:
        """Run all initialization checks."""
        # Check Python version first
        if not self.check_python_version():
            return False

        # Check required modules
        all_modules_ok = all(self.check_module(module) for module in CORE_MODULES)

        # Check required files
        all_files_ok = all(self.check_file(f) for f in REQUIRED_FILES)

        # Initialize config if needed
        config_ok = self.initialize_config()

        # Ensure directories exist
        self.verify_directories()

        # Update overall status
        self.status["initialized"] = all_modules_ok and all_files_ok and config_ok

        return self.status["initialized"]

    def generate_report(self) -> str:
        """Generate a human-readable status report."""
        report = ["🔍 CADE System Initialization Report\n"]

        # Python version
        py_info = self.status.get("python_version", {})
        py_status = "✅" if py_info.get("compatible", False) else "❌"
        report.append(
            f"{py_status} Python {py_info.get('version', 'unknown')} (Requires 3.8+)\n"
        )

        # Modules
        report.append("📦 Core Modules:")
        for name, info in self.status.get("modules", {}).items():
            status = "✅" if info.get("available") else "❌"
            report.append(f"  {status} {name}")
            if "error" in info:
                report.append(f"     Error: {info['error']}")

        # Files
        report.append("\n📄 Required Files:")
        for name, info in self.status.get("files", {}).items():
            status = "✅" if info.get("exists") else "❌"
            report.append(f"  {status} {name}")
            if "error" in info:
                report.append(f"     Error: {info['error']}")

        # Config
        report.append("\n⚙️  Configuration:")
        if "config" in self.status:
            if "error" in self.status["config"]:
                report.append(f"  ❌ Error: {self.status['config']['error']}")
            else:
                sections = self.status["config"].get("sections", [])
                status = "✅" if sections else "⚠️"
                report.append(
                    f"  {status} Config initialized with sections: {', '.join(sections) if sections else 'None'}"
                )

        # Final status
        if self.status.get("initialized"):
            report.append("\n✨ CADE System is ready to use!")
        else:
            report.append(
                "\n❌ Initialization completed with errors. Please check the report above."
            )

        return "\n".join(report)


def main():
    """Main entry point for the auto-initialization script."""
    print("🚀 Starting CADE System Auto-Initialization...\n")

    initializer = CadeInitializer()
    success = initializer.run_checks()

    # Print the report
    print(initializer.generate_report())

    # If running as a script, exit with appropriate status
    if __name__ == "__main__":
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
