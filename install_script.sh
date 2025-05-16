#!/bin/bash

# Installation script for EXIF_GENESIS

echo "Installing EXIF_GENESIS..."

# Define the installation directory
INSTALL_DIR="/usr/local/bin"
CONFIG_DIR="$HOME/.exif_genesis"

# Create the config directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

# Define required packages
REQUIRED_PACKAGES=("python3" "pip3")

# Check for required packages
for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! command -v "$package" &> /dev/null; then
        echo "Error: $package is required but not installed."
        echo "Please install $package and try again."
        exit 1
    fi
done

# Install required Python packages
echo "Installing required Python packages..."
pip3 install pillow tabulate colorama --user

# Copy the main script to the installation directory
echo "Copying EXIF_GENESIS to $INSTALL_DIR..."
if [ -f "./exif_genesis.py" ]; then
    cp "./exif_genesis.py" "$INSTALL_DIR/exif_genesis"
    chmod +x "$INSTALL_DIR/exif_genesis"
else
    echo "Error: exif_genesis.py not found in the current directory."
    exit 1
fi

# Create the launcher script
cat > "$INSTALL_DIR/exif_gen" << 'EOF'
#!/bin/bash

# EXIF_GENESIS launcher script
exif_genesis "$@"
EOF

chmod +x "$INSTALL_DIR/exif_gen"

# Create the shell function in ~/.bashrc or ~/.zshrc
SHELL_CONFIG=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
else
    echo "Warning: Couldn't find .zshrc or .bashrc. You'll need to manually add the shell function."
fi

if [ -n "$SHELL_CONFIG" ]; then
    echo "Adding shell function to $SHELL_CONFIG..."
    echo "" >> "$SHELL_CONFIG"
    echo "# EXIF_GENESIS shell function" >> "$SHELL_CONFIG"
    echo "exif_gen() {" >> "$SHELL_CONFIG"
    echo "    /usr/local/bin/exif_gen \"\$@\"" >> "$SHELL_CONFIG"
    echo "}" >> "$SHELL_CONFIG"
fi

echo "Installation complete!"
echo ""
echo "To use EXIF_GENESIS, either:"
echo "  1. Open a new terminal window and run 'exif_gen'"
echo "  2. Or, in this window, run 'source $SHELL_CONFIG' and then 'exif_gen'"
echo ""
echo "Examples:"
echo "  exif_gen path/to/image.jpg                # Interactive mode"
echo "  exif_gen -d path/to/image.jpg             # Display EXIF data"
echo "  exif_gen -e path/to/image.jpg             # Edit EXIF data"
echo "  exif_gen -x -o output.txt image.jpg       # Export EXIF data to text file"
echo "  exif_gen -j -o output.json image.jpg      # Export EXIF data to JSON file"
