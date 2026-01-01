#!/usr/bin/env python3
"""
Environment Setup for Faster Whisper Skill
Manages virtual environment and dependencies automatically
Zero configuration required
"""

import os
import sys
import subprocess
import venv
from pathlib import Path


class SkillEnvironment:
    """Manages skill-specific virtual environment"""

    def __init__(self):
        # Skill directory paths
        self.skill_dir = Path(__file__).parent.parent
        self.venv_dir = self.skill_dir / ".venv"
        self.requirements_file = self.skill_dir / "requirements.txt"

        # Python executable in venv
        if os.name == 'nt':  # Windows
            self.venv_python = self.venv_dir / "Scripts" / "python.exe"
            self.venv_pip = self.venv_dir / "Scripts" / "pip.exe"
        else:  # Unix/Linux/Mac
            self.venv_python = self.venv_dir / "bin" / "python"
            self.venv_pip = self.venv_dir / "bin" / "pip"

    def ensure_venv(self) -> bool:
        """Ensure virtual environment exists and is set up"""

        # Check if we're already in the correct venv
        if self.is_in_skill_venv():
            print("✅ Already running in skill virtual environment")
            return True

        # Create venv if it doesn't exist
        if not self.venv_dir.exists():
            print(f"🔧 Creating virtual environment in {self.venv_dir.name}/")
            try:
                venv.create(self.venv_dir, with_pip=True)
                print("✅ Virtual environment created")
            except Exception as e:
                print(f"❌ Failed to create venv: {e}")
                return False

        # Install/update dependencies
        if self.requirements_file.exists():
            print("📦 Installing dependencies...")
            try:
                # Upgrade pip first
                subprocess.run(
                    [str(self.venv_pip), "install", "--upgrade", "pip"],
                    check=True,
                    capture_output=True,
                    text=True
                )

                # Install requirements
                result = subprocess.run(
                    [str(self.venv_pip), "install", "-r", str(self.requirements_file)],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print("✅ Dependencies installed (faster-whisper ready)")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install dependencies: {e}")
                print(f"   Output: {e.output if hasattr(e, 'output') else 'No output'}")
                return False
        else:
            print("⚠️ No requirements.txt found, skipping dependency installation")
            return True

    def is_in_skill_venv(self) -> bool:
        """Check if we're already running in the skill's venv"""
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            # We're in a venv, check if it's ours
            venv_path = Path(sys.prefix)
            return venv_path == self.venv_dir
        return False

    def get_python_executable(self) -> str:
        """Get the correct Python executable to use"""
        if self.venv_python.exists():
            return str(self.venv_python)
        return sys.executable


def main():
    """Main entry point for environment setup"""
    env = SkillEnvironment()

    # Default: ensure environment is set up
    if env.ensure_venv():
        print("\n✅ Environment ready!")
        print(f"   Virtual env: {env.venv_dir}")
        print(f"   Python: {env.get_python_executable()}")
        print(f"\n🚀 You can now run transcriptions:")
        print(f"   python scripts/run.py transcribe.py audio.mp3")
        print(f"   python scripts/run.py transcribe.py audio.mp3 --language zh --output result.txt")
    else:
        print("\n❌ Environment setup failed")
        return 1


if __name__ == "__main__":
    sys.exit(main() or 0)
