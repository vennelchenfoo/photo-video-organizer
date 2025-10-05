# 📸 Photo & Video Organizer

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

*A Python desktop app that automatically organizes photos and videos by date and finds duplicates*

**Built with AI assistance in under an hour! 🚀**

</div>

---

## 💡 The Story Behind This Project

My wife had two external hard drives filled with thousands of photos and videos from years of family memories—all mixed up in different folders with no organization. Finding a specific photo by date was nearly impossible, and she was spending hours manually searching through files.

One evening, she asked: *"Can you help me organize these photos by year and month so I can actually find things?"*

This was my first real experience with **"vibe coding"**—I had some Python knowledge from freelancing gigs but wasn't fluent. With the help of an LLM (Claude), I turned this problem into a working solution in about an hour. The result? **A tool that saved her countless hours** and made our family photo library actually usable.

**The best part?** Anyone with basic Python knowledge and access to AI can build practical solutions like this. You don't need to be a coding expert—you just need a real problem to solve.

---

## ✨ What It Does

- 📅 **Organizes by Date**: Automatically sorts photos and videos into `Year/Month/` folders
- 🔍 **Finds Duplicates**: Uses smart algorithms to detect duplicate files (even with different names!)
- 📊 **Shows Progress**: Real-time progress bar and statistics
- 🖼️ **Handles Both**: Works with photos (EXIF data) and videos (metadata)
- 💾 **Safe**: Copies files instead of moving them—your originals stay untouched

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher ([Download here](https://www.python.org/downloads/))
- Basic command line knowledge

### Installation

**1. Download or Clone:**
```bash
git clone https://github.com/vennelchenfoo/photo-video-organizer.git
cd photo-video-organizer
```

**2. Create Virtual Environment:**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install Requirements:**
```bash
pip install -r requirements.txt
```

**4. Run the App:**
```bash
python src/photo_organizer_gui.py
```

---

## 💻 How to Use

1. **Select Source Folder**: Click "Browse" and choose the messy folder
2. **Select Target Folder**: Choose where organized files should go
3. **Pick Options**:
   - ☑️ Photos and/or Videos
   - ☑️ Organize by Year and/or Month
   - ☑️ Find Duplicates (optional)
4. **Click "Start Processing"**: Watch it work!
5. **Check Results**: Your files are now organized by date!

### Example Output

```
target_folder/
├── 2022/
│   ├── 01-January/
│   │   ├── Photos/
│   │   └── Videos/
│   └── 02-February/
│       ├── Photos/
│       └── Videos/
├── 2023/
│   └── ...
├── Unknown/  ← Files without date info
└── Duplicates/  ← Duplicate files for review
```

---

## 🔧 Technical Details

**Built with:**
- **Pillow**: Image processing and EXIF data
- **OpenCV**: Video handling
- **imagehash**: Perceptual image hashing for duplicates
- **tkinter**: GUI (built into Python)

**Supported formats:**
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`
- **Videos**: `.mp4`, `.avi`, `.mov`, `.mkv`, `.wmv`, `.flv`, `.webm`, `.m4v`, `.3gp`

**How duplicate detection works:**
- **Photos**: Perceptual hashing (finds similar images even if slightly different)
- **Videos**: Samples frames at 10%, 50%, 90% and compares them

---

## 📸 Screenshots

### Main Interface
*[Screenshot will be added here]*

### Organized Results
*[Screenshot will be added here]*

---

## ⚠️ Important Notes

✅ **Non-destructive**: Files are **copied**, not moved or deleted  
✅ **No overwrites**: Duplicate names get renamed automatically  
✅ **Cancel anytime**: Safe to stop mid-process  

⚡ **Tips:**
- Test with a small folder first (50-100 files)
- Duplicate detection is slower for videos
- Always review the `Duplicates/` folder before deleting
- Make sure you have enough disk space (doubles your file size)

---

## 🤔 Why This Matters

This project shows that **you don't need to be a coding expert to solve real problems**. With AI assistance and some basic programming knowledge, you can:

- Build practical tools in hours, not days
- Solve problems that would take manual work for weeks
- Learn by doing, not just reading tutorials

**The future of coding isn't about memorizing syntax—it's about solving problems and knowing how to work with AI tools.**

---

## 🗺️ Future Ideas

Want to improve this? Here are some ideas:

- [ ] Add undo functionality
- [ ] Support RAW image formats
- [ ] Organize by GPS location
- [ ] Export organization report (PDF)
- [ ] Batch rename files by date
- [ ] Create standalone executable (no Python needed)

Feel free to fork and experiment!

---

## 📄 License

MIT License - Feel free to use this for your own projects!

---

## 👤 About Me

**Vennel Chenfoo**  
Data Science & AI | Automation Enthusiast | Ethical Tech Advocate

*Turning advocacy into algorithms — building AI and automation with purpose, empathy, and impact.*

- 🎓 Studying Data Science & AI at WBS Coding School
- 📍 Based in Lüneburg, Germany
- 🤖 Building automation tools with n8n, Python, and AI
- 🌏 Passionate about ethical, accessible tech for social good
- 🏃 Sub-4h Berlin Marathon runner

**Connect with me:**
- 💼 LinkedIn: [vennelchenfoo](https://www.linkedin.com/in/vennelchenfoo/)
- 🐙 GitHub: [@vennelchenfoo](https://github.com/vennelchenfoo)

**Motto:** *keep building, always learning*

---

## 🙏 Acknowledgments

- Thanks to my wife for inspiring this project (and for being patient while testing it!)
- Built with assistance from Claude AI
- Inspired by the need to organize 10+ years of family photos

---

<div align="center">

**⭐ If this saved you time organizing your photos, consider giving it a star!**

*Built with Python and AI in under an hour*

</div>
