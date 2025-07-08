import sys
import os
import shutil
import tempfile
import subprocess
import re
import html
from PyQt6 import uic
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                             QInputDialog, QMessageBox, QComboBox,
                             QDialog, QVBoxLayout, QLabel,
                             QDialogButtonBox, QGroupBox, QPushButton)
from PyQt6.QtCore import QProcess, Qt
from PyQt6.QtGui import QTextCursor, QPixmap

# Function to clear ANSI escape codes
def clean_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

# To define UI file ingredients as string
UI_STRING = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>1024</width>
    <height>768</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Rom Builder</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QPushButton" name="pushButton_4">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>20</y>
      <width>221</width>
      <height>45</height>
     </rect>
    </property>
    <property name="text">
     <string>Select Rom Source Folder</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_3">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>75</y>
      <width>221</width>
      <height>45</height>
     </rect>
    </property>
    <property name="text">
     <string>Add Device Manifest</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_5">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>130</y>
      <width>221</width>
      <height>45</height>
     </rect>
    </property>
    <property name="text">
     <string>Sync Selected Rom Source</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_6">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>185</y>
      <width>221</width>
      <height>45</height>
     </rect>
    </property>
    <property name="text">
     <string>Add Build Sign Keys</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_envsetup">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>240</y>
      <width>221</width>
      <height>45</height>
     </rect>
    </property>
    <property name="text">
     <string>Source Environment Setup</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_lunch">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>295</y>
      <width>221</width>
      <height>45</height>
     </rect>
    </property>
    <property name="text">
     <string>Lunch Device Before Build</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_build">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>350</y>
      <width>221</width>
      <height>45</height>
     </rect>
    </property>
    <property name="text">
     <string>Start Build Process</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_7">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>405</y>
      <width>221</width>
      <height>45</height>
     </rect>
    </property>
    <property name="text">
     <string>Look at Rom Source Folder</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_8">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>460</y>
      <width>221</width>
      <height>45</height>
     </rect>
    </property>
    <property name="text">
     <string>Look at Output Folder</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_2">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>515</y>
      <width>221</width>
      <height>45</height>
     </rect>
    </property>
    <property name="text">
     <string>Save log.txt For Debug</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_9">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>570</y>
      <width>110</width>
      <height>35</height>
     </rect>
    </property>
    <property name="text">
     <string>Stop Execution</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_10">
    <property name="geometry">
     <rect>
      <x>125</x>
      <y>570</y>
      <width>110</width>
      <height>35</height>
     </rect>
    </property>
    <property name="text">
     <string>Clear Output</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_quit">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>615</y>
      <width>110</width>
      <height>35</height>
     </rect>
    </property>
    <property name="text">
     <string>Quit</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_about">
    <property name="geometry">
     <rect>
      <x>125</x>
      <y>615</y>
      <width>110</width>
      <height>35</height>
     </rect>
    </property>
    <property name="text">
     <string>About</string>
    </property>
   </widget>
   <widget class="QLabel" name="iconLabel">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>655</y>
      <width>221</width>
      <height>64</height>
     </rect>
    </property>
    <property name="text">
     <string/>
    </property>
    <property name="alignment">
     <set>Qt::AlignCenter</set>
    </property>
   </widget>
   <widget class="QTextBrowser" name="textBrowser">
    <property name="geometry">
     <rect>
      <x>241</x>
      <y>20</y>
      <width>773</width>
      <height>708</height>
     </rect>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>1024</width>
     <height>19</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""

class RomVersionDialog(QDialog):
    """Spesific dialog for select rom and its version"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select ROM Version")
        self.setGeometry(100, 100, 300, 150)
        
        layout = QVBoxLayout()
        
        # ROM version selection box
        group_box = QGroupBox("Select ROM Version")
        group_layout = QVBoxLayout()
        
        self.combo = QComboBox()
        versions = [
            "Custom...",
            "AxionAOSP 15 QPR1",
            "AxionAOSP 15 QPR2",
            "crDroid 14.0",
            "crDroid 15.0",
            "InfinityX 15 QPR2",
            "LineageOS 20",
            "LineageOS 21",
            "LineageOS 22.1",
            "LineageOS 22.2",
            "LineageOS 23.0",
            "Matrixx 15 QPR2",
            "MistOS 3.5",
            "RisingOS 6.3",
            "RisingOS 7.1"
        ]
        self.combo.addItems(versions)
        self.combo.setCurrentIndex(9)  # Predefined selection
        
        group_layout.addWidget(self.combo)
        group_box.setLayout(group_layout)
        
        layout.addWidget(group_box)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
    
    def get_selected_version(self):
        return self.combo.currentText()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # To create temporary .ui file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ui") as tmp_file:
            tmp_file.write(UI_STRING.encode())
            tmp_file_path = tmp_file.name
        
        # To load .ui file
        uic.loadUi(tmp_file_path, self)
        os.unlink(tmp_file_path)  # Temporary file deletion
        
        # Remove logo and set text instead
        self.iconLabel.setText("<b>PyQT Rom Builder</b>")
        self.iconLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Optionally, you can set a larger font size or color if desired
        # font = self.iconLabel.font()
        # font.setPointSize(16)
        # self.iconLabel.setFont(font)
        
        # Connect button signals
        self.pushButton_4.clicked.connect(self.select_rom_source)        # Select Rom Source Folder
        self.pushButton_3.clicked.connect(self.add_repositories)         # Add Device Manifest
        self.pushButton_5.clicked.connect(self.initialize_selected_repo) # Sync Selected Repo
        self.pushButton_6.clicked.connect(self.add_signing_keys)         # Add Signing Keys
        self.pushButton_7.clicked.connect(self.look_at_rom_source)       # Look at Rom Source Folder
        self.pushButton_8.clicked.connect(self.look_at_output)           # Look at Output
        self.pushButton_2.clicked.connect(self.save_log_file)            # Get log.txt
        self.pushButton_9.clicked.connect(self.stop_process)             # Stop Executed Command
        self.pushButton_10.clicked.connect(self.clear_output)            # Clear Terminal Output
        
        # New build process buttons
        self.pushButton_envsetup.clicked.connect(self.source_environment)
        self.pushButton_lunch.clicked.connect(self.lunch_device)
        self.pushButton_build.clicked.connect(self.start_build)
        self.pushButton_quit.clicked.connect(self.quit_app)              # Quit application
        self.pushButton_about.clicked.connect(self.show_about_dialog)
        
        # QProcess for managing processes
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.process.readyRead.connect(self.handle_output)
        self.process.finished.connect(self.process_finished)
        
        # Variables
        self.rom_source_dir = ""
        self.rom_version = ""
        self.device_codename = ""  # To just store device codename
        self.lunch_target = ""     # To store full lunch target
        self.threads = 8           # Default build threads
        self.log_file = ""
        self.raw_log_buffer = []   # To get raw log output

    def start_persistent_shell(self):
        if self.process.state() == QProcess.Running:
            self.process.kill()
            self.process.waitForFinished()
        
        self.process.setWorkingDirectory(self.rom_source_dir)
        self.process.start("bash")
        if not self.process.waitForStarted():
            self.append_text("Failed to start shell process.", color='red')

    def handle_output(self):
        data = self.process.readAll()
        text = bytes(data).decode('utf-8', 'ignore')
        self.raw_log_buffer.append(text)
        clean_text = clean_ansi_codes(text)
        self.append_text(clean_text)

    def process_finished(self, exit_code, exit_status):
        if exit_code == 0:
            self.append_text("\n✅ Process completed successfully!\n")
        else:
            self.append_text(f"\n❌ Process failed with exit code {exit_code}\n")
            # To save automatically log file if build fails
            self.save_log_file(automatic=True)

    def append_text(self, text, color=None):
        """To insert text into the screen without HTML tags"""
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)

        if color:
            text = html.escape(text)
            cursor.insertHtml(f"<font color='{color}'>{text}</font><br>")
            self.textBrowser.setTextCursor(cursor)
            self.textBrowser.ensureCursorVisible()
            return

        text = text.replace('\r\n', '\n')
        if '\r' in text:
            parts = text.split('\r')
            for i, part in enumerate(parts):
                if not part and i != len(parts) -1 :
                    cursor.movePosition(QTextCursor.StartOfBlock)
                    cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
                    cursor.removeSelectedText()
                    continue

                if i > 0 or text.startswith('\r'):
                    cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.MoveAnchor)
                    cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
                    cursor.removeSelectedText()

                part_html = html.escape(part).replace('\n', '<br>')
                cursor.insertHtml(part_html)
        else:
            cursor.insertHtml(html.escape(text).replace('\n', '<br>'))
        
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def select_rom_source(self):
        # Rom folder selection
        dir_path = QFileDialog.getExistingDirectory(self, "Select ROM Source Directory")
        if not dir_path:
            return
            
        self.rom_source_dir = dir_path
        
        # To add information messages
        self.append_text(f"ROM Source: {dir_path}\n")
        
        # Start the persistent shell
        self.start_persistent_shell()
        
        # If there is a .repo directory in the folder, assume it has already been initialized
        if os.path.exists(os.path.join(dir_path, ".repo")):
            self.append_text("Rom source already initialized.\n\n")
            return
            
        # Version selection to initialize 
        version_dialog = RomVersionDialog(self)
        if version_dialog.exec_() == QDialog.Accepted:
            self.rom_version = version_dialog.get_selected_version()
            self.append_text(f"Selected Version: {self.rom_version}\n")
            
            repo_command = ""
            if self.rom_version == "Custom...":
                command, ok = QInputDialog.getText(self, "Custom Repo Init", "Enter the full repo init command:")
                if ok and command:
                    repo_command = command
                else:
                    self.append_text("Custom ROM initialization canceled\n", color='orange')
                    return
            else:
                repo_command = self.get_repo_init_command()
            
            # To run repo init
            if repo_command:
                self.append_text(f"$ {repo_command}", color='yellow')
                self.raw_log_buffer.append(f"$ {repo_command}\n")
                self.run_command(repo_command)
        else:
            self.append_text("ROM initialization canceled\n", color='orange')

    def initialize_selected_repo(self):
        if not self.rom_source_dir:
            QMessageBox.warning(self, "Warning", "Please select ROM source directory first!")
            return
            
        if not os.path.exists(os.path.join(self.rom_source_dir, ".repo")):
            QMessageBox.warning(self, "Warning", "Repository not initialized. Please select ROM source first!")
            return

        user_command = "repo sync --force-sync"
        internal_command = ""

        # Check for unbuffer, which is more reliable for forcing interactive output
        if shutil.which("unbuffer"):
            internal_command = f"unbuffer {user_command}"
        elif shutil.which("stdbuf"):
            # Fallback to stdbuf if unbuffer is not available
            internal_command = f"stdbuf -oL {user_command}"
            self.append_text(
                "Warning: 'unbuffer' not found. Falling back to 'stdbuf'. "
                "For best results, please install the 'expect' package.", 
                color='orange'
            )
        else:
            # If neither is available, run the command directly
            internal_command = user_command
            self.append_text(
                "Warning: 'unbuffer' and 'stdbuf' not found. "
                "Real-time progress updates may not be available.", 
                color='orange'
            )
            
        # To run repo sync
        self.append_text(f"$ {user_command}", color='yellow')
        self.raw_log_buffer.append(f"$ {user_command}\n")
        self.run_command(internal_command)

    def get_repo_init_command(self):
        """Returns the repo init command according to the ROM version"""
        version = self.rom_version.lower()
        
        ####################################################
        # REPO INIT COMMANDS ACCORDING TO ROM VERSIONS
        ####################################################
        if "lineageos" in version:
            if "20" in version:
                return "repo init -u https://github.com/LineageOS/android.git -b lineage-20 --git-lfs --depth=1"
            elif "21" in version:
                return "repo init -u https://github.com/LineageOS/android.git -b lineage-21 --git-lfs --depth=1"
            elif "22.1" in version:
                return "repo init -u https://github.com/LineageOS/android.git -b lineage-22.1 --git-lfs --depth=1"
            elif "22.2" in version:
                return "repo init -u https://github.com/LineageOS/android.git -b lineage-22.2 --git-lfs --depth=1"
            elif "23.0" in version:
                return "repo init -u https://github.com/LineageOS/android.git -b lineage-23.0 --git-lfs --depth=1"
        
        elif "crdroid" in version:
            if "14.0" in version:
                return "repo init -u https://github.com/crdroidandroid/android.git -b 14.0 --git-lfs --depth=1"
            elif "15.0" in version:
                return "repo init -u https://github.com/crdroidandroid/android.git -b 15.0 --git-lfs --depth=1"
        
        elif "axionaosp" in version:
            if "15 qpr1" in version:
                return "repo init -u https://github.com/AxionAOSP/android.git -b lineage-22.1 --git-lfs --depth=1"
            elif "15 qpr2" in version:
                return "repo init -u https://github.com/AxionAOSP/android.git -b lineage-22.2 --git-lfs --depth=1"
        
        elif "risingos" in version:
            if "6.3" in version:
                return "repo init -u https://github.com/RisingOS-Revived/android -b fifteen --git-lfs --depth=1"
            elif "7.1" in version:
                return "repo init -u https://github.com/RisingOS-Revived/android -b qpr2 --git-lfs --depth=1"
         
        elif "mistos" in version:
            if "3.5" in version:
                return "repo init -u https://github.com/Project-Mist-OS/manifest -b vic --git-lfs --depth=1"
        
        elif "matrixx" in version:
            if "15 qpr2" in version:
                return "repo init -u https://github.com/ProjectMatrixx/android.git -b 15.0 --git-lfs --depth=1"
        
        elif "infinityx" in version:
            if "15 qpr2" in version:
                return "repo init -u https://github.com/ProjectInfinity-X/android.git -b 15 --git-lfs --depth=1"

        # Predefined initialization command
        return "repo init -u https://github.com/LineageOS/android.git -b lineage-22.2 --git-lfs --depth=1"

    def add_repositories(self):
        if not self.rom_source_dir:
            QMessageBox.warning(self, "Warning", "Please select ROM source directory first!")
            return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select local_manifest.xml", 
            "", 
            "XML Files (*.xml)"
        )
        
        if file_path:
            # To create .repo/local_manifests folder for dt's
            local_manifests_dir = os.path.join(self.rom_source_dir, ".repo", "local_manifests")
            os.makedirs(local_manifests_dir, exist_ok=True)
            
            # Get original filename instead of renaming
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(local_manifests_dir, file_name)

            # Copy manifest into folder
            shutil.copy(file_path, dest_path)
            
            self.append_text(f"{file_name} copied to: {dest_path}\n")

    def add_signing_keys(self):
        if not self.rom_source_dir:
            QMessageBox.warning(self, "Warning", "Please select ROM source directory first!")
            return
        
        dir_path = QFileDialog.getExistingDirectory(self, "Select Sign Keys Directory")
        if dir_path:
            # Target folder: rom_source/vendor/
            dest_dir = os.path.join(self.rom_source_dir, "vendor")
   
            # To copy keys
            try:
                # Get selected folder name
                keys_folder_name = os.path.basename(dir_path)
                target_keys_dir = os.path.join(dest_dir, keys_folder_name)
                
                # Delete previous keys (if any)
                if os.path.exists(target_keys_dir):
                    shutil.rmtree(target_keys_dir)
                
                # Paste new keys
                shutil.copytree(dir_path, target_keys_dir)
                
                self.append_text(f"Signing keys copied to: {target_keys_dir}\n")
                QMessageBox.information(self, "Success", "Sign keys added successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to copy signing keys:\n{str(e)}")

    def source_environment(self):
        if not self.rom_source_dir:
            QMessageBox.warning(self, "Warning", "Please select ROM source directory first!")
            return
        
        command = ". build/envsetup.sh"
        self.append_text(f"$ {command}", color='yellow')
        self.raw_log_buffer.append(f"$ {command}\n")
        self.run_command(command)

    def lunch_device(self):
        if not self.rom_source_dir:
            QMessageBox.warning(self, "Warning", "Please select ROM source directory first!")
            return

        device, ok = QInputDialog.getText(self, "Device Selection", 
                                        "Enter lunch device name and build type (e.g. lineage_munch-bp1a-userdebug):",
                                        text=self.lunch_target)
        if not ok or not device:
            return
        
        self.lunch_target = device
        
        # Extract device codename for output folder (lineage_munch-userdebug -> munch)
        if '_' in device:
            self.device_codename = device.split('_')[1].split('-')[0]
        else:
            self.device_codename = device.split('-')[0]
        
        self.append_text(f"Lunch target set to: {self.lunch_target}\n")
        self.append_text(f"Device codename set to: {self.device_codename}\n")

        # Run the lunch command
        command = f"lunch {self.lunch_target}"
        self.append_text(f"$ {command}", color='yellow')
        self.raw_log_buffer.append(f"$ {command}\n")
        self.run_command(command)

    def start_build(self):
        if not self.rom_source_dir:
            QMessageBox.warning(self, "Warning", "Please select ROM source directory first!")
            return
        
        if not self.lunch_target:
            QMessageBox.warning(self, "Warning", "Please set a lunch target first!")
            return
        
        # To define j paramater count for compile
        threads, ok = QInputDialog.getInt(self, "Build Threads", 
                                        "Number of build threads (j parameter):", 
                                        self.threads, 1, 128, 1)
        if not ok:
            return
        
        self.threads = threads
        
        # Run the build commands
        m_command = f"m bacon otatools target-files-package -j{self.threads}"
        
        # To logging text
        self.append_text(f"$ {m_command}", color='yellow')
        
        # Add commands to raw log file
        self.raw_log_buffer.append(f"$ {m_command}\n")
        
        # Run command
        self.run_command(m_command)

    def run_command(self, command):
        if self.process.state() != QProcess.Running:
            QMessageBox.warning(self, "Warning", "Shell is not running. Please select a ROM source directory first.")
            return

        # Write command to the shell
        self.process.write(f"{command}\n".encode('utf-8'))

    def save_log_file(self, automatic=False):
        if not self.raw_log_buffer:
            QMessageBox.information(self, "Information", "No log data to save!")
            return
            
        # To automate save log file if get error
        if automatic:
            log_file = os.path.join(os.getcwd(), "build_log.txt")
            try:
                with open(log_file, "w") as f:
                    f.write("".join(self.raw_log_buffer))
                self.append_text(f"\nLog automatically saved to: {log_file}\n")
            except Exception as e:
                self.append_text(f"\n<font color='red'>Failed to save log: {str(e)}</font>\n")
            return
            
        # Save log file to a spesific destination if user clicks button
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save Log File", 
            "build_log.txt", 
            "Text Files (*.txt)"
        )
        
        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write("".join(self.raw_log_buffer))
                QMessageBox.information(self, "Log Saved", 
                                      f"Log file saved as:\n{file_path}")
                self.append_text(f"\nLog saved to: {file_path}\n")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save log:\n{str(e)}")
                self.append_text(f"\n<font color='red'>Failed to save log: {str(e)}</font>\n")
    
    def look_at_rom_source(self):
        """Open ROM source folder in file manager"""
        if not self.rom_source_dir:
            QMessageBox.warning(self, "Warning", "No ROM source directory selected!")
            return
        
        # Check platform for file manager
        try:
            if sys.platform == "darwin": #MacOS shi
                subprocess.run(["open", self.rom_source_dir])
            else:  # Linux and unix-like systems
                subprocess.run(["xdg-open", self.rom_source_dir])
            self.append_text(f"\nOpened ROM source folder: {self.rom_source_dir}\n")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open folder:\n{str(e)}")
    
    def look_at_output(self):
        """Open the compile output folder in the file manager"""
        if not self.rom_source_dir:
            QMessageBox.warning(self, "Warning", "No ROM source directory selected!")
            return
        
        if not self.device_codename:
            QMessageBox.warning(self, "Warning", "Device codename not set! Please run a build first.")
            return
        
        # Create output folder path (use only device codename)
        output_path = os.path.join(
            self.rom_source_dir, 
            "out", 
            "target", 
            "product", 
            self.device_codename
        )
        
        if not os.path.exists(output_path):
            QMessageBox.warning(self, "Warning", f"Output directory not found:\n{output_path}")
            return
        
        # Check platform for file manager
        try:
            if sys.platform == "darwin": #MacOS shi
                subprocess.run(["open", output_path])
            else:  # Linux and unix-like systems
                subprocess.run(["xdg-open", output_path])
            self.append_text(f"\nOpened output folder: {output_path}\n")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open folder:\n{str(e)}")

    def show_about_dialog(self):
        """Shows an about dialog for the application"""
        QMessageBox.about(self, "About Rom Builder",
                      "<b>Rom Builder v1.1</b><br><br>"
                      "This application helps to build custom Android ROMs.<br><br>"
                      "Source code available on <a href='https://github.com/efeisot/pyqt-aosp-rom-builder'>GitHub</a>.<br><br>"
                      "Developed by efeisot and licenced with AGPLv3")

    def stop_process(self):
        """Stop running process"""
        if self.process.state() == QProcess.Running:
            self.process.terminate()
            self.process.waitForFinished(3000) # Wait 3 secs
            if self.process.state() == QProcess.Running:
                self.process.kill() # If still running kill it
                self.process.waitForFinished()
            self.append_text("\n❌ Process stopped by user.\n", color='orange')
            
    def clear_output(self):
        """Clear the output text browser"""
        self.textBrowser.clear()

    def quit_app(self):
        """Quit the application"""
        QApplication.instance().quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
