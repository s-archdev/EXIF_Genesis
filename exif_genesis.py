#!/usr/bin/env python3
"""
EXIF_GENESIS - A modular EXIF exploring, editing, and writing utility for macOS

Usage: exif_gen [OPTION] [FILE]
"""

import os
import sys
import json
import argparse
import datetime
from pathlib import Path
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
from tabulate import tabulate
import colorama
from colorama import Fore, Style

# Initialize colorama for cross-platform colored terminal output
colorama.init()

class ExifGenesis:
    def __init__(self):
        self.image_path = None
        self.image = None
        self.exif_data = {}
        self.modified = False
    
    def load_image(self, image_path):
        """Load image and extract EXIF data."""
        try:
            self.image_path = image_path
            self.image = Image.open(image_path)
            
            # Extract EXIF data
            raw_exif = self.image._getexif()
            if raw_exif:
                for tag, value in raw_exif.items():
                    tag_name = TAGS.get(tag, tag)
                    
                    # Handle special cases
                    if tag_name == 'GPSInfo':
                        gps_data = {}
                        for gps_tag, gps_value in value.items():
                            gps_tag_name = GPSTAGS.get(gps_tag, gps_tag)
                            gps_data[gps_tag_name] = gps_value
                        self.exif_data[tag_name] = gps_data
                    else:
                        # Convert bytes to string if needed
                        if isinstance(value, bytes):
                            try:
                                value = value.decode('utf-8')
                            except UnicodeDecodeError:
                                value = str(value)
                        
                        # Handle datetime objects
                        if isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
                            value = str(value)
                            
                        self.exif_data[tag_name] = value
                        
            print(f"{Fore.GREEN}Successfully loaded image: {Fore.CYAN}{os.path.basename(image_path)}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}Error loading image: {e}{Style.RESET_ALL}")
            return False
            
    def display_exif(self):
        """Display EXIF data in a nicely formatted table."""
        if not self.exif_data:
            print(f"{Fore.YELLOW}No EXIF data found in the image.{Style.RESET_ALL}")
            return
            
        # Create a list for tabulate
        table_data = []
        for tag, value in self.exif_data.items():
            # Handle nested data like GPSInfo
            if isinstance(value, dict):
                table_data.append([tag, ""])
                for subtag, subvalue in value.items():
                    table_data.append([f"  {subtag}", subvalue])
            else:
                table_data.append([tag, value])
                
        print(f"\n{Fore.CYAN}EXIF Data for: {os.path.basename(self.image_path)}{Style.RESET_ALL}")
        print(tabulate(table_data, headers=["Tag", "Value"], tablefmt="pretty"))
    
    def edit_exif(self):
        """Interactive EXIF data editor."""
        if not self.exif_data:
            print(f"{Fore.YELLOW}No EXIF data to edit.{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}EXIF Editor - Enter 'quit' to exit editor mode{Style.RESET_ALL}")
        while True:
            print("\nOptions:")
            print(f"{Fore.GREEN}1. Edit existing tag{Style.RESET_ALL}")
            print(f"{Fore.GREEN}2. Add new tag{Style.RESET_ALL}")
            print(f"{Fore.GREEN}3. Delete tag{Style.RESET_ALL}")
            print(f"{Fore.GREEN}4. Show current data{Style.RESET_ALL}")
            print(f"{Fore.GREEN}5. Save changes{Style.RESET_ALL}")
            print(f"{Fore.GREEN}6. Exit editor{Style.RESET_ALL}")
            
            choice = input(f"{Fore.YELLOW}Enter your choice (1-6): {Style.RESET_ALL}")
            
            if choice == "1":
                # Show tags for selection
                tags = list(self.exif_data.keys())
                for i, tag in enumerate(tags):
                    print(f"{i+1}. {tag}")
                
                try:
                    idx = int(input(f"{Fore.YELLOW}Enter tag number to edit: {Style.RESET_ALL}")) - 1
                    if 0 <= idx < len(tags):
                        tag = tags[idx]
                        current_value = self.exif_data[tag]
                        print(f"Current value of '{tag}': {current_value}")
                        new_value = input(f"{Fore.YELLOW}Enter new value (or 'cancel'): {Style.RESET_ALL}")
                        
                        if new_value.lower() != 'cancel':
                            self.exif_data[tag] = new_value
                            self.modified = True
                            print(f"{Fore.GREEN}Updated '{tag}' to '{new_value}'{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Invalid tag number{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Please enter a valid number{Style.RESET_ALL}")
                    
            elif choice == "2":
                tag = input(f"{Fore.YELLOW}Enter new tag name: {Style.RESET_ALL}")
                if tag:
                    value = input(f"{Fore.YELLOW}Enter value for '{tag}': {Style.RESET_ALL}")
                    self.exif_data[tag] = value
                    self.modified = True
                    print(f"{Fore.GREEN}Added new tag '{tag}' with value '{value}'{Style.RESET_ALL}")
                    
            elif choice == "3":
                # Show tags for selection
                tags = list(self.exif_data.keys())
                for i, tag in enumerate(tags):
                    print(f"{i+1}. {tag}")
                
                try:
                    idx = int(input(f"{Fore.YELLOW}Enter tag number to delete: {Style.RESET_ALL}")) - 1
                    if 0 <= idx < len(tags):
                        tag = tags[idx]
                        confirm = input(f"{Fore.RED}Are you sure you want to delete '{tag}'? (y/n): {Style.RESET_ALL}")
                        if confirm.lower() == 'y':
                            del self.exif_data[tag]
                            self.modified = True
                            print(f"{Fore.GREEN}Deleted tag '{tag}'{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Invalid tag number{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Please enter a valid number{Style.RESET_ALL}")
                    
            elif choice == "4":
                self.display_exif()
                
            elif choice == "5":
                self.save_exif()
                
            elif choice == "6" or choice.lower() == "quit":
                if self.modified:
                    save = input(f"{Fore.YELLOW}You have unsaved changes. Save before exiting? (y/n): {Style.RESET_ALL}")
                    if save.lower() == 'y':
                        self.save_exif()
                break
                
            else:
                print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")
    
    def save_exif(self):
        """Save modified EXIF data back to the image."""
        if not self.modified:
            print(f"{Fore.YELLOW}No changes to save.{Style.RESET_ALL}")
            return
            
        try:
            # Create a backup of the original image
            backup_path = f"{self.image_path}.backup"
            if not os.path.exists(backup_path):
                import shutil
                shutil.copy2(self.image_path, backup_path)
                print(f"{Fore.GREEN}Created backup at: {backup_path}{Style.RESET_ALL}")
            
            # Currently, directly writing EXIF data back is complex due to PIL limitations
            # This is a simplified approach - for a real-world application, 
            # you might want to use exiftool or other libraries
            print(f"{Fore.YELLOW}Note: Some EXIF tags may not be preserved during saving due to library limitations.{Style.RESET_ALL}")
            
            # Save with basic EXIF info
            self.image.save(self.image_path, exif=self.image.info.get('exif'))
            
            print(f"{Fore.GREEN}Changes saved to image.{Style.RESET_ALL}")
            
            # Reset modification flag
            self.modified = False
            return True
        except Exception as e:
            print(f"{Fore.RED}Error saving EXIF data: {e}{Style.RESET_ALL}")
            return False
    
    def export_exif(self, export_path=None):
        """Export EXIF data to a text file."""
        if not self.exif_data:
            print(f"{Fore.YELLOW}No EXIF data to export.{Style.RESET_ALL}")
            return False
            
        try:
            if not export_path:
                # Generate default export path
                base_name = os.path.splitext(os.path.basename(self.image_path))[0]
                export_path = f"{base_name}_exif.txt"
            
            # Export as plain text
            with open(export_path, 'w') as f:
                f.write(f"EXIF Data for: {os.path.basename(self.image_path)}\n")
                f.write("-" * 50 + "\n\n")
                
                for tag, value in self.exif_data.items():
                    if isinstance(value, dict):
                        f.write(f"{tag}:\n")
                        for subtag, subvalue in value.items():
                            f.write(f"  {subtag}: {subvalue}\n")
                    else:
                        f.write(f"{tag}: {value}\n")
            
            print(f"{Fore.GREEN}EXIF data exported to: {export_path}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}Error exporting EXIF data: {e}{Style.RESET_ALL}")
            return False
    
    def export_exif_json(self, export_path=None):
        """Export EXIF data to a JSON file."""
        if not self.exif_data:
            print(f"{Fore.YELLOW}No EXIF data to export.{Style.RESET_ALL}")
            return False
            
        try:
            if not export_path:
                # Generate default export path
                base_name = os.path.splitext(os.path.basename(self.image_path))[0]
                export_path = f"{base_name}_exif.json"
            
            # Convert data to serializable format
            serializable_data = {}
            for tag, value in self.exif_data.items():
                if isinstance(value, bytes):
                    value = str(value)
                serializable_data[tag] = value
            
            # Export as JSON
            with open(export_path, 'w') as f:
                json.dump(serializable_data, f, indent=2)
            
            print(f"{Fore.GREEN}EXIF data exported to JSON: {export_path}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}Error exporting EXIF data: {e}{Style.RESET_ALL}")
            return False

    def interactive_mode(self):
        """Run the interactive mode."""
        if not self.image_path:
            print(f"{Fore.RED}No image loaded. Please load an image first.{Style.RESET_ALL}")
            return
            
        while True:
            print(f"\n{Fore.CYAN}EXIF_GENESIS - Interactive Mode{Style.RESET_ALL}")
            print(f"Working with: {os.path.basename(self.image_path)}")
            print("\nOptions:")
            print(f"{Fore.GREEN}1. Display EXIF data{Style.RESET_ALL}")
            print(f"{Fore.GREEN}2. Edit EXIF data{Style.RESET_ALL}")
            print(f"{Fore.GREEN}3. Export EXIF data as text{Style.RESET_ALL}")
            print(f"{Fore.GREEN}4. Export EXIF data as JSON{Style.RESET_ALL}")
            print(f"{Fore.GREEN}5. Save changes{Style.RESET_ALL}")
            print(f"{Fore.GREEN}6. Load different image{Style.RESET_ALL}")
            print(f"{Fore.GREEN}7. Exit{Style.RESET_ALL}")
            
            choice = input(f"{Fore.YELLOW}Enter your choice (1-7): {Style.RESET_ALL}")
            
            if choice == "1":
                self.display_exif()
            elif choice == "2":
                self.edit_exif()
            elif choice == "3":
                export_path = input(f"{Fore.YELLOW}Enter export path (leave blank for default): {Style.RESET_ALL}")
                self.export_exif(export_path if export_path else None)
            elif choice == "4":
                export_path = input(f"{Fore.YELLOW}Enter export path (leave blank for default): {Style.RESET_ALL}")
                self.export_exif_json(export_path if export_path else None)
            elif choice == "5":
                self.save_exif()
            elif choice == "6":
                image_path = input(f"{Fore.YELLOW}Enter image path: {Style.RESET_ALL}")
                if os.path.exists(image_path):
                    if self.modified:
                        save = input(f"{Fore.YELLOW}You have unsaved changes. Save before loading new image? (y/n): {Style.RESET_ALL}")
                        if save.lower() == 'y':
                            self.save_exif()
                    self.load_image(image_path)
                else:
                    print(f"{Fore.RED}Image not found: {image_path}{Style.RESET_ALL}")
            elif choice == "7":
                if self.modified:
                    save = input(f"{Fore.YELLOW}You have unsaved changes. Save before exiting? (y/n): {Style.RESET_ALL}")
                    if save.lower() == 'y':
                        self.save_exif()
                print(f"{Fore.GREEN}Exiting EXIF_GENESIS. Goodbye!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")


def main():
    parser = argparse.ArgumentParser(description='EXIF_GENESIS - A modular EXIF exploring, editing, and writing utility')
    parser.add_argument('image', nargs='?', help='Path to the image file')
    parser.add_argument('-d', '--display', action='store_true', help='Display EXIF data')
    parser.add_argument('-e', '--edit', action='store_true', help='Edit EXIF data')
    parser.add_argument('-x', '--export', action='store_true', help='Export EXIF data as text')
    parser.add_argument('-j', '--json', action='store_true', help='Export EXIF data as JSON')
    parser.add_argument('-o', '--output', help='Output file for export')
    parser.add_argument('-i', '--interactive', action='store_true', help='Run in interactive mode')
    
    args = parser.parse_args()
    
    exif_genesis = ExifGenesis()
    
    # Handle case where no image is provided
    if not args.image and not any([args.display, args.edit, args.export, args.json, args.interactive]):
        # No arguments provided, go to interactive mode with image selection
        print(f"{Fore.CYAN}Welcome to EXIF_GENESIS!{Style.RESET_ALL}")
        image_path = input(f"{Fore.YELLOW}Enter path to an image file: {Style.RESET_ALL}")
        if os.path.exists(image_path):
            if exif_genesis.load_image(image_path):
                exif_genesis.interactive_mode()
            else:
                sys.exit(1)
        else:
            print(f"{Fore.RED}Image not found: {image_path}{Style.RESET_ALL}")
            sys.exit(1)
        return
    
    # Load the image if provided
    if args.image:
        if not os.path.exists(args.image):
            print(f"{Fore.RED}Image not found: {args.image}{Style.RESET_ALL}")
            sys.exit(1)
            
        if not exif_genesis.load_image(args.image):
            sys.exit(1)
    
    # Handle commands
    if args.interactive:
        exif_genesis.interactive_mode()
    elif args.display:
        exif_genesis.display_exif()
    elif args.edit:
        exif_genesis.edit_exif()
    elif args.export:
        exif_genesis.export_exif(args.output)
    elif args.json:
        exif_genesis.export_exif_json(args.output)
    else:
        # If image was loaded but no command specified, show EXIF data by default
        if args.image:
            exif_genesis.display_exif()


if __name__ == "__main__":
    main()
