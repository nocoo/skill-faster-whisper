#!/usr/bin/env python3
"""
Install script for faster-whisper skill
Copies the skill to ~/.claude/skills/ for Claude Code to discover
"""

import os
import sys
import shutil
from pathlib import Path


def main():
    # Get paths
    current_dir = Path.cwd()
    skill_name = "faster-whisper"
    target_dir = Path.home() / ".claude" / "skills" / skill_name

    print(f"📦 Installing {skill_name} skill...")
    print(f"   From: {current_dir}")
    print(f"   To:   {target_dir}")
    print()

    # Create target directory
    target_dir.mkdir(parents=True, exist_ok=True)

    # Files to copy (excluding install script itself)
    files_to_copy = [
        "SKILL.md",
        "README.md",
        "LICENSE",
        "requirements.txt",
        "skill.json",
        "scripts",
    ]

    # Copy files
    for item in files_to_copy:
        src = current_dir / item
        dst = target_dir / item

        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"   ✅ Copied: {item}/")
        elif src.exists():
            shutil.copy2(src, dst)
            print(f"   ✅ Copied: {item}")
        else:
            print(f"   ⚠️  Skipped: {item} (not found)")

    # Make scripts executable
    scripts_dir = target_dir / "scripts"
    if scripts_dir.exists():
        for script in ["run.py", "setup_environment.py", "transcribe.py"]:
            script_path = scripts_dir / script
            if script_path.exists():
                script_path.chmod(0o755)

    print()
    print("✅ Installation complete!")
    print()
    print(f"🚀 You can now use the skill:")
    print(f"   python {target_dir.name}/scripts/run.py transcribe.py audio.mp3 --language zh")
    print()
    print(f"   Or from anywhere:")
    print(f"   python ~/.claude/skills/{target_dir.name}/scripts/run.py transcribe.py audio.mp3")


if __name__ == "__main__":
    main()
