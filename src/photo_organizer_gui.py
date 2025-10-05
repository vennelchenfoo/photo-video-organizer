import os
import sys
import shutil
import hashlib
import imagehash
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import cv2
import numpy as np
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import time
import calendar

class MediaOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo & Video Organizer")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        
        # Set app icon if needed
        # self.root.iconbitmap("path/to/icon.ico")
        
        self.setup_ui()
        
        # Initialize variables
        self.source_dir = ""
        self.target_dir = ""
        self.is_processing = False
        self.stats = {
            "total_files": 0,
            "organized_photos": 0,
            "organized_videos": 0,
            "duplicates": 0,
            "errors": 0
        }
        
        # Month names for folder organization
        self.month_names = {
            1: "01-January", 2: "02-February", 3: "03-March", 4: "04-April",
            5: "05-May", 6: "06-June", 7: "07-July", 8: "08-August",
            9: "09-September", 10: "10-October", 11: "11-November", 12: "12-December",
            0: "00-Unknown"  # For cases where month can't be determined
        }
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="AI Photo & Video Organizer", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Description
        description = "This tool will scan your photos and videos, organize them by year/month, and identify duplicates."
        desc_label = ttk.Label(main_frame, text=description, wraplength=600)
        desc_label.pack(pady=(0, 20))
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Directories", padding=10)
        input_frame.pack(fill=tk.X, pady=10)
        
        # Source directory
        source_frame = ttk.Frame(input_frame)
        source_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(source_frame, text="Source Directory:").pack(side=tk.LEFT, padx=(0, 10))
        self.source_entry = ttk.Entry(source_frame, width=50)
        self.source_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(source_frame, text="Browse...", command=self.browse_source).pack(side=tk.LEFT)
        
        # Target directory
        target_frame = ttk.Frame(input_frame)
        target_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(target_frame, text="Target Directory:").pack(side=tk.LEFT, padx=(0, 10))
        self.target_entry = ttk.Entry(target_frame, width=50)
        self.target_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(target_frame, text="Browse...", command=self.browse_target).pack(side=tk.LEFT)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding=10)
        options_frame.pack(fill=tk.X, pady=10)
        
        # File types frame
        file_types_frame = ttk.Frame(options_frame)
        file_types_frame.pack(fill=tk.X, pady=5, anchor=tk.W)
        
        ttk.Label(file_types_frame, text="File Types:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.include_photos_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(file_types_frame, text="Photos", variable=self.include_photos_var).pack(side=tk.LEFT, padx=5)
        
        self.include_videos_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(file_types_frame, text="Videos", variable=self.include_videos_var).pack(side=tk.LEFT, padx=5)
        
        # Organization options
        org_frame = ttk.Frame(options_frame)
        org_frame.pack(fill=tk.X, pady=5, anchor=tk.W)
        
        ttk.Label(org_frame, text="Organize by:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.organize_by_year_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(org_frame, text="Year", variable=self.organize_by_year_var).pack(side=tk.LEFT, padx=5)
        
        self.organize_by_month_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(org_frame, text="Month", variable=self.organize_by_month_var).pack(side=tk.LEFT, padx=5)
        
        # Duplicate detection
        self.find_duplicates_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Find Duplicates", variable=self.find_duplicates_var).pack(anchor=tk.W)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding=10)
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        status_label.pack(anchor=tk.W)
        
        # Stats frame
        self.stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding=10)
        self.stats_frame.pack(fill=tk.X, pady=10)
        
        self.stats_text = tk.Text(self.stats_frame, height=7, width=50, state=tk.DISABLED)
        self.stats_text.pack(fill=tk.X)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        self.start_button = ttk.Button(button_frame, text="Start Processing", command=self.start_processing)
        self.start_button.pack(side=tk.RIGHT, padx=5)
        
        self.cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel_processing, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def browse_source(self):
        directory = filedialog.askdirectory(title="Select Source Directory")
        if directory:
            self.source_dir = directory
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, directory)
    
    def browse_target(self):
        directory = filedialog.askdirectory(title="Select Target Directory")
        if directory:
            self.target_dir = directory
            self.target_entry.delete(0, tk.END)
            self.target_entry.insert(0, directory)
    
    def start_processing(self):
        # Get directories from entry fields (in case they were typed in)
        self.source_dir = self.source_entry.get()
        self.target_dir = self.target_entry.get()
        
        # Validate inputs
        if not self.source_dir or not os.path.exists(self.source_dir):
            messagebox.showerror("Error", "Please select a valid source directory.")
            return
        
        if not self.target_dir:
            messagebox.showerror("Error", "Please select a target directory.")
            return
        
        # Check if at least one file type is selected
        if not self.include_photos_var.get() and not self.include_videos_var.get():
            messagebox.showerror("Error", "Please select at least one file type to process.")
            return
        
        # Check if at least year or month organization is selected
        if not self.organize_by_year_var.get() and not self.organize_by_month_var.get():
            messagebox.showerror("Error", "Please select at least one organization method.")
            return
        
        # Create target directory if it doesn't exist
        if not os.path.exists(self.target_dir):
            try:
                os.makedirs(self.target_dir)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create target directory: {e}")
                return
        
        # Start processing in a separate thread
        self.is_processing = True
        self.cancel_requested = False
        
        # Update UI
        self.start_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        self.status_var.set("Scanning files...")
        self.progress_var.set(0)
        
        # Reset stats
        self.stats = {
            "total_files": 0,
            "organized_photos": 0,
            "organized_videos": 0,
            "duplicates": 0,
            "errors": 0
        }
        self.update_stats_display()
        
        # Start processing thread
        self.processing_thread = threading.Thread(target=self.process_media)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
        # Start a timer to update the UI
        self.root.after(100, self.check_progress)
    
    def cancel_processing(self):
        if self.is_processing:
            self.cancel_requested = True
            self.status_var.set("Canceling...")
    
    def check_progress(self):
        if self.is_processing:
            self.update_stats_display()
            self.root.after(100, self.check_progress)
        else:
            # Processing completed or was canceled
            self.start_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED)
            
            if not self.cancel_requested:
                self.status_var.set("Processing completed!")
                messagebox.showinfo("Complete", f"Media organization complete!\n\n"
                                  f"Processed: {self.stats['total_files']} files\n"
                                  f"Organized Photos: {self.stats['organized_photos']} files\n"
                                  f"Organized Videos: {self.stats['organized_videos']} files\n"
                                  f"Duplicates: {self.stats['duplicates']} files\n"
                                  f"Errors: {self.stats['errors']} files")
            else:
                self.status_var.set("Processing canceled")
    
    def update_stats_display(self):
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, f"Total files scanned: {self.stats['total_files']}\n")
        self.stats_text.insert(tk.END, f"Photos organized: {self.stats['organized_photos']}\n")
        self.stats_text.insert(tk.END, f"Videos organized: {self.stats['organized_videos']}\n")
        self.stats_text.insert(tk.END, f"Duplicates found: {self.stats['duplicates']}\n")
        self.stats_text.insert(tk.END, f"Errors encountered: {self.stats['errors']}\n")
        self.stats_text.config(state=tk.DISABLED)
    
    def get_media_date(self, file_path, is_video=False):
        """Extract date from image EXIF data, video metadata, or use file modification date as fallback."""
        try:
            if is_video:
                # Try to get date from video metadata using OpenCV
                cap = cv2.VideoCapture(file_path)
                if cap.isOpened():
                    # Some video formats might store creation time
                    # This is a basic approach - more advanced video metadata extraction
                    # would require additional libraries like ffmpeg-python or pymediainfo
                    cap.release()
                    
                    # For now, fall back to file modification time for videos
                    mod_time = os.path.getmtime(file_path)
                    dt = datetime.fromtimestamp(mod_time)
                    return dt.year, dt.month
            else:
                # Try to get date from EXIF data for images
                with Image.open(file_path) as img:
                    exif_data = img._getexif()
                    if exif_data:
                        for tag_id, value in exif_data.items():
                            tag = TAGS.get(tag_id, tag_id)
                            if tag == 'DateTimeOriginal':
                                # Parse EXIF date format (YYYY:MM:DD HH:MM:SS)
                                date_str = value
                                dt = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                                return dt.year, dt.month
        except Exception as e:
            pass
        
        # Fallback to file modification time
        try:
            mod_time = os.path.getmtime(file_path)
            dt = datetime.fromtimestamp(mod_time)
            return dt.year, dt.month
        except:
            # If all else fails, return Unknown
            return "Unknown", 0
    
    def compute_media_hash(self, file_path, is_video=False):
        """Compute hash for an image or video."""
        try:
            if is_video:
                # For videos, we'll use a combination of file size and a sample of frames
                file_size = os.path.getsize(file_path)
                
                # Extract a few frames for comparison
                cap = cv2.VideoCapture(file_path)
                if not cap.isOpened():
                    return None
                
                # Get video properties
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                duration = total_frames / fps if fps > 0 else 0
                
                # Sample frames at different points
                sample_points = [0.1, 0.5, 0.9]  # 10%, 50%, 90% of video
                frames_data = []
                
                for point in sample_points:
                    if duration > 0:
                        # Set position to percentage of video
                        target_frame = int(total_frames * point)
                        cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
                        
                        ret, frame = cap.read()
                        if ret:
                            # Resize frame to small size for faster hashing
                            small_frame = cv2.resize(frame, (32, 32))
                            # Convert to grayscale
                            gray_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
                            # Add frame data to our collection
                            frames_data.append(gray_frame.tobytes())
                
                cap.release()
                
                # Create a hash from the combination of file size and frame data
                hasher = hashlib.md5()
                hasher.update(str(file_size).encode())
                for frame_data in frames_data:
                    hasher.update(frame_data)
                
                return hasher.hexdigest()
            else:
                # For images, use perceptual hash
                with Image.open(file_path) as img:
                    # Convert to consistent format for hashing
                    img = img.convert("RGB")
                    # Calculate perceptual hash - robust against minor changes
                    return str(imagehash.phash(img))
        except Exception as e:
            # Return None if we can't process the file
            return None

    def is_valid_media(self, file_path):
        """Check if file is a valid image or video."""
        # Get file extension
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # Define valid extensions
        valid_image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
        valid_video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.3gp']
        
        # Check if it's an image file
        if self.include_photos_var.get() and file_ext in valid_image_extensions:
            try:
                with Image.open(file_path) as img:
                    # Try to verify the image
                    img.verify()
                return "image"
            except:
                return False
        
        # Check if it's a video file
        if self.include_videos_var.get() and file_ext in valid_video_extensions:
            try:
                # Try to open video file using OpenCV
                cap = cv2.VideoCapture(file_path)
                if cap.isOpened():
                    cap.release()
                    return "video"
                return False
            except:
                return False
        
        return False
    
    def get_target_directory(self, year, month, media_type):
        """Create and return the target directory path based on organization options."""
        target_dir = self.target_dir
        
        # Organize by year if enabled
        if self.organize_by_year_var.get():
            target_dir = os.path.join(target_dir, str(year))
        
        # Organize by month if enabled
        if self.organize_by_month_var.get() and month > 0:
            month_name = self.month_names.get(month, "00-Unknown")
            target_dir = os.path.join(target_dir, month_name)
        
        # Create media type subdirectory
        if media_type == "video":
            target_dir = os.path.join(target_dir, "Videos")
        else:
            target_dir = os.path.join(target_dir, "Photos")
        
        # Create directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        
        return target_dir
    
    def process_media(self):
        """Process photos and videos in a separate thread."""
        try:
            # Create duplicates directory if needed
            duplicates_dir = os.path.join(self.target_dir, "Duplicates")
            if self.find_duplicates_var.get() and not os.path.exists(duplicates_dir):
                os.makedirs(duplicates_dir)
            
            # First, count total files to set up progress bar
            total_media_files = 0
            for root, _, files in os.walk(self.source_dir):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    if self.is_valid_media(file_path):
                        total_media_files += 1
            
            # Dictionary to store hashes and corresponding file paths
            hash_dict = {}
            # Track which files have been copied
            processed_files = set()
            
            # Walk through the source directory
            files_processed = 0
            for root, _, files in os.walk(self.source_dir):
                for filename in files:
                    if self.cancel_requested:
                        self.is_processing = False
                        return
                    
                    file_path = os.path.join(root, filename)
                    
                    # Skip if not a valid media file
                    media_type = self.is_valid_media(file_path)
                    if not media_type:
                        continue
                    
                    self.stats["total_files"] += 1
                    files_processed += 1
                    
                    # Update progress
                    if total_media_files > 0:
                        progress = (files_processed / total_media_files) * 100
                        self.progress_var.set(progress)
                        self.status_var.set(f"Processing file {files_processed} of {total_media_files}")
                    
                    try:
                        is_video = (media_type == "video")
                        
                        # Get year and month from media file
                        year, month = self.get_media_date(file_path, is_video)
                        
                        # Get target directory based on organization options
                        target_dir = self.get_target_directory(year, month, media_type)
                        
                        # Find duplicates if enabled
                        if self.find_duplicates_var.get():
                            # Compute media hash
                            media_hash = self.compute_media_hash(file_path, is_video)
                            if media_hash is None:
                                self.stats["errors"] += 1
                                continue
                            
                            # Check for duplicates
                            if media_hash in hash_dict:
                                # This is a duplicate
                                self.stats["duplicates"] += 1
                                duplicate_path = os.path.join(duplicates_dir, filename)
                                
                                # Ensure we don't overwrite existing files in the duplicates folder
                                if os.path.exists(duplicate_path):
                                    base, ext = os.path.splitext(filename)
                                    duplicate_path = os.path.join(duplicates_dir, f"{base}_dup_{self.stats['duplicates']}{ext}")
                                
                                # Copy to duplicates folder
                                shutil.copy2(file_path, duplicate_path)
                            else:
                                # New media file, store its hash
                                hash_dict[media_hash] = file_path
                                
                                # Copy to target directory if not already processed
                                if file_path not in processed_files:
                                    target_path = os.path.join(target_dir, filename)
                                    
                                    # Ensure we don't overwrite existing files
                                    if os.path.exists(target_path):
                                        base, ext = os.path.splitext(filename)
                                        target_path = os.path.join(target_dir, f"{base}_{hash(file_path)}{ext}")
                                    
                                    shutil.copy2(file_path, target_path)
                                    processed_files.add(file_path)
                                    
                                    if is_video:
                                        self.stats["organized_videos"] += 1
                                    else:
                                        self.stats["organized_photos"] += 1
                        else:
                            # Just organize without duplicate detection
                            target_path = os.path.join(target_dir, filename)
                            
                            # Ensure we don't overwrite existing files
                            if os.path.exists(target_path):
                                base, ext = os.path.splitext(filename)
                                target_path = os.path.join(target_dir, f"{base}_{hash(file_path)}{ext}")
                            
                            shutil.copy2(file_path, target_path)
                            
                            if is_video:
                                self.stats["organized_videos"] += 1
                            else:
                                self.stats["organized_photos"] += 1
                            
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
                        self.stats["errors"] += 1
            
            # Processing completed
            self.progress_var.set(100)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during processing: {e}")
        
        finally:
            self.is_processing = False

def main():
    root = tk.Tk()
    app = MediaOrganizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
