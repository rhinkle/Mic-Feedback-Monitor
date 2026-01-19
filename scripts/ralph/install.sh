#!/bin/bash
set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SOURCE_DIR="$SCRIPT_DIR/skills"

# Verify skills source directory exists
if [ ! -d "$SKILLS_SOURCE_DIR" ]; then
    echo "Error: Skills directory not found at $SKILLS_SOURCE_DIR"
    exit 1
fi

# Ask user if they want a global install for skills or local project only
echo "Where would you like to install the skills?"
echo "1) Global (available system-wide)"
echo "2) Local project only"
read -p "Enter your choice (1 or 2): " INSTALL_CHOICE

case $INSTALL_CHOICE in
    1)
        SKILLS_DIR=~/.claude/skills
        echo "Installing skills globally to $SKILLS_DIR"
        ;;
    2)
        SKILLS_DIR="$(pwd)/.claude/skills"
        echo "Installing skills locally to $SKILLS_DIR"
        ;;
    *)
        echo "Invalid choice. Defaulting to local installation."
        SKILLS_DIR="$(pwd)/.claude/skills"
        ;;
esac

# Create skills directory if it doesn't exist
mkdir -p "$SKILLS_DIR"

# Track overwrite preference
OVERWRITE_ALL=false
SKIP_ALL=false

# Copy each skill from the skills source directory
for skill in "$SKILLS_SOURCE_DIR"/*; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")
        target_path="$SKILLS_DIR/$skill_name"

        # Check if skill already exists
        if [ -d "$target_path" ]; then
            if [ "$SKIP_ALL" = true ]; then
                echo "Skipping skill: $skill_name (already exists)"
                continue
            fi

            if [ "$OVERWRITE_ALL" = false ]; then
                echo ""
                echo "Skill '$skill_name' already exists at $target_path"
                echo "What would you like to do?"
                echo "1) Overwrite"
                echo "2) Skip"
                echo "3) Overwrite all existing"
                echo "4) Skip all existing"
                read -p "Enter your choice (1-4): " CONFLICT_CHOICE

                case $CONFLICT_CHOICE in
                    1)
                        echo "Overwriting skill: $skill_name"
                        rm -rf "$target_path"
                        cp -r "$skill" "$target_path"
                        ;;
                    2)
                        echo "Skipping skill: $skill_name"
                        continue
                        ;;
                    3)
                        OVERWRITE_ALL=true
                        echo "Overwriting skill: $skill_name"
                        rm -rf "$target_path"
                        cp -r "$skill" "$target_path"
                        ;;
                    4)
                        SKIP_ALL=true
                        echo "Skipping skill: $skill_name"
                        continue
                        ;;
                    *)
                        echo "Invalid choice. Skipping skill: $skill_name"
                        continue
                        ;;
                esac
            else
                echo "Overwriting skill: $skill_name"
                rm -rf "$target_path"
                cp -r "$skill" "$target_path"
            fi
        else
            echo "Installing skill: $skill_name"
            cp -r "$skill" "$target_path"
        fi
    fi
done

echo ""
echo "Installation complete."