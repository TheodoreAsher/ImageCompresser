import os
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
import math
import webbrowser

class ImageCompressor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Compressor v1.0")
        self.root.geometry("400x350")  # Adjusted height for compact layout
        
        # UI Elements
        self.label = Label(root, text="Image Compressor v1.0", font=("Arial", 16))
        self.label.pack(pady=10)
        
        self.select_button = Button(root, text="Select Image(s)", command=self.select_files)
        self.select_button.pack(pady=10)
        
        self.compress_button = Button(root, text="Compress", command=self.compress_images, state=DISABLED)
        self.compress_button.pack(pady=10)
        
        self.status_label = Label(root, text="")
        self.status_label.pack(pady=10)
        
        # Frame for social buttons (to place them in one row)
        self.social_frame = Frame(root)
        self.social_frame.pack(pady=5)
        

        
        # GitHub Button (Smaller)
        self.github_button = Button(self.social_frame, text="GitHub", 
                                  command=lambda: webbrowser.open("https://github.com/TheodoreAsher"),
                                  bg="#333333", fg="white", 
                                  font=("Arial", 8), width=8, height=1)
        self.github_button.pack(side=LEFT, padx=5)
        
        # LinkedIn Button (Smaller)
        self.linkedin_button = Button(self.social_frame, text="LinkedIn", 
                                    command=lambda: webbrowser.open("https://www.linkedin.com/in/muhammad-ahsan-171519229/"),
                                    bg="#0077B5", fg="white", 
                                    font=("Arial", 8), width=8, height=1)
        self.linkedin_button.pack(side=LEFT, padx=5)

        # Footer Label
        self.footer_label = Label(root, text="Developed by Ahsan", font=("Arial", 8))
        self.footer_label.pack(pady=10)

        # Footer Link

        
        self.files = []

    def select_files(self):
        self.files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff")],
        )
        if self.files:
            self.status_label.config(text=f"Selected {len(self.files)} image(s)")
            self.compress_button.config(state=NORMAL)
        else:
            self.status_label.config(text="No images selected")
            self.compress_button.config(state=DISABLED)

    def compress_image(self, input_path, output_path, target_size_mb=1):
        """Compress image to target size in MB while maintaining quality"""
        try:
            # Convert target size from MB to bytes
            target_size = target_size_mb * 1024 * 1024
            
            # Open the image
            img = Image.open(input_path)
            
            # Convert to RGB if it's RGBA
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            # Initial quality setting
            quality = 95
            step = 5
            
            # Get original file size
            original_size = os.path.getsize(input_path)
            
            # If already under target size, save with slight compression
            if original_size <= target_size:
                img.save(output_path, "JPEG", quality=95, optimize=True)
                return True
            
            # Calculate initial resize factor based on file size
            size_ratio = math.sqrt(target_size / original_size)
            new_width = int(img.width * size_ratio * 0.9)  # 0.9 for safety margin
            new_height = int(img.height * size_ratio * 0.9)
            
            # Resize image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Iterative compression
            while quality > 10:
                img.save(output_path, "JPEG", quality=quality, optimize=True)
                current_size = os.path.getsize(output_path)
                
                if current_size <= target_size:
                    return True
                
                quality -= step
            
            return False
            
        except Exception as e:
            print(f"Error compressing {input_path}: {str(e)}")
            return False

    def compress_images(self):
        if not self.files:
            messagebox.showerror("Error", "No images selected")
            return
            
        self.status_label.config(text="Compressing...")
        self.root.update()
        
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            self.status_label.config(text="Compression cancelled")
            return
            
        success_count = 0
        for file_path in self.files:
            filename = os.path.basename(file_path)
            output_path = os.path.join(output_dir, f"compressed_{filename.rsplit('.', 1)[0]}.jpg")
            
            if self.compress_image(file_path, output_path):
                success_count += 1
        
        self.status_label.config(text=f"Compressed {success_count}/{len(self.files)} images")
        messagebox.showinfo("Complete", f"Compressed {success_count} out of {len(self.files)} images")

def main():
    root = Tk()
    app = ImageCompressor(root)
    root.mainloop()

if __name__ == "__main__":
    main()