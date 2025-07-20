#!/bin/bash
set -e

# Move to the directory where install.sh is located
cd "$(dirname "$0")"
echo "Starting installation of passman..."

# Step 1: Check Python 3
if ! command -v python3 &>/dev/null; then
    echo "Python3 is not installed. Please install it before proceeding."
    exit 1
fi

echo "Python version: $(python3 --version)"

# Step 2: Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    if ! python3 -m venv venv; then
        echo "Failed to create virtual environment. You may need to install the python3-venv package:"
        echo "  sudo apt install python3-venv"
        exit 1
    fi
else
    echo "Virtual environment already exists."
fi

# Step 3: Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "Virtual environment activated."
else
    echo "Failed to find venv/bin/activate. Aborting."
    exit 1
fi

# Step 4: Upgrade pip and install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Dependencies installed."
else
    echo "requirements.txt not found. Skipping dependency installation."
fi

# Step 5: Create launcher script to run passman
PROJECT_DIR="$PWD"

cat << EOF > run_passman.sh
#!/bin/bash
cd "$PROJECT_DIR"
source venv/bin/activate
python3 main.py "\$@"
EOF

chmod +x run_passman.sh

# Step 6: Create global symlink
sudo ln -sf "$PROJECT_DIR/run_passman.sh" /usr/local/bin/passman


# create some required files and folder
touch config/.env
mkdir logs 

echo "Installation complete."
echo "You can now run the application from anywhere using the command: passman"
