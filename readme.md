# EXIF_GENESIS

A modular terminal-based EXIF exploring, editing, and writing utility for macOS.

## Features

- View EXIF metadata from images in a nice, formatted display
- Edit, add, or delete EXIF tags interactively
- Export EXIF data as text or JSON files
- User-friendly terminal interface with color highlighting
- Simple command-line options for quick operations
- Interactive mode for comprehensive EXIF management

## Installation

1. Clone this repository or download the source files:

```
git clone https://github.com/yourusername/exif_genesis.git
cd exif_genesis
```

2. Run the installation script:

```
chmod +x install.sh
./install.sh
```

The installation script will:
- Install required Python packages (Pillow, tabulate, colorama)
- Copy the main script to /usr/local/bin
- Create the necessary command aliases
- Set up the shell function for the `exif_gen:` command

## Usage

### Basic Commands

```
exif_gen path/to/image.jpg                # Interactive mode
exif_gen -d path/to/image.jpg             # Display EXIF data
exif_gen -e path/to/image.jpg             # Edit EXIF data
exif_gen -x -o output.txt image.jpg       # Export EXIF data to text file
exif_gen -j -o output.json image.jpg      # Export EXIF data to JSON file
```

### Interactive Mode

Running `exif_gen` with just an image path will start the interactive mode, which provides a menu-driven interface for:

1. Displaying EXIF data
2. Editing EXIF metadata
3. Exporting EXIF data as text
4. Exporting EXIF data as JSON
5. Saving changes
6. Loading a different image
7. Exiting the program

### Command-line Options

```
  -h, --help            Show help message and exit
  -d, --display         Display EXIF data
  -e, --edit            Edit EXIF data
  -x, --export          Export EXIF data as text
  -j, --json            Export EXIF data as JSON
  -o OUTPUT, --output OUTPUT
                        Output file for export
  -i, --interactive     Run in interactive mode
```

## Requirements

- macOS
- Python 3.6+
- Pillow (Python Imaging Library)
- tabulate (for formatted tables)
- colorama (for colored terminal output)

## Limitations

- Some EXIF tags might not be preserved when saving changes due to limitations in the PIL library
- The tool creates backups of original images before modifying them

## License

MIT License
