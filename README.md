![rombuilder](https://github.com/user-attachments/assets/13b4be04-5607-43cd-b905-23bbb0f36221)

# ROM Builder GUI 🧱🛠️

**ROM Builder** is a PyQt5-based graphical tool that simplifies the Android ROM building process.  
It lets you sync repositories, add local manifests, configure signing keys, and compile ROMs — all through an easy-to-use GUI.

![image](https://github.com/user-attachments/assets/91062123-f34f-4065-af63-a62e452c1023)

[Video preview](https://t.me/munch_chat/64288)
---

## 🚀 Features

- 📂 Select and manage ROM source directory
- 🔁 `repo init` and `repo sync` with one click
- 📦 Add `device.xml` to `.repo/local_manifests/`
- 🔐 Add signing keys to the correct vendor path
- ⚙️ Automate build commands (`envsetup`, `lunch`, `m`)
- 📄 Live terminal log viewer with color output
- 🧾 Export logs as `build_log.txt`
- 📁 Open source and output folders directly

---

## 🛠️ Requirements (for development)

If you want to run or modify the source code:

- Python 3.6+
- PyQt5

Install dependencies:

```bash
pip install PyQt5
```
Run the application:
```bash
python3 rom_builder.py
```

## 📦 Download
You don't need Python or dependencies to use ROM Builder.
Just download the prebuilt AppImage from Releases:

👉 [Download ROM Builder AppImage](https://github.com/Efeisot/pyqt-aosp-rom-builder/releases/download/v1.1/ROM_Builder-x86_64.AppImage)

Make it executable and run:

```bash
chmod +x rom_builder-x86_64.AppImage
./rom_builder-x86_64.AppImage
```

## ✅ Supported ROMs
- LineageOS 20 / 21 / 22.1 / 22.2
- crDroid 14.0 / 15.0
- AxionAOSP 15 QPR1 / QPR2
- RisingOS 7.0 / 7.1
- MistOS 3.5

## 🧱 Credits
- Deepseek: For entire script, without it, i couldn't have done this project in less than 3-4 hours
- Chatgpt: For README.md structure
- Me: For some fixes in script and README.md, translations of comments in script, and application icon design. Also, the idea came to my mind, don't worry, I'm not as lazy as you think, I'm even lazier :D

Feel free to suggest your contributions and fork the project. There are probably a lot of things missing from this project.
