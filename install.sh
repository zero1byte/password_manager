#!/bin/bash
set -e

cd "$(dirname "$0")"

# Run setup
bash setup.sh

# Make run_myapp.sh executable
chmod +x run.sh

# Create global symlink (replaces any existing one)
sudo ln -sf "$PWD/run.sh" /usr/local/bin/passman

echo "✅ Installed successfully. Now run your app anywhere with: passman"
