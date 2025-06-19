import sys
import os
import shutil
import tempfile
import subprocess
import re
import html
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, 
                             QInputDialog, QMessageBox, QComboBox, 
                             QDialog, QVBoxLayout, QLabel, 
                             QDialogButtonBox, QGroupBox, QPushButton)
from PyQt5.QtCore import QProcess
from PyQt5.QtGui import QTextCursor

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
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Rom Builder</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QPushButton" name="pushButton">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>370</y>
      <width>201</width>
      <height>41</height>
     </rect>
    </property>
    <property name="text">
     <string>Add Device and Start Build</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_2">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>510</y>
      <width>201</width>
      <height>41</height>
     </rect>
    </property>
    <property name="text">
     <string>Get log.txt file for debug</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_3">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>90</y>
      <width>201</width>
      <height>41</height>
     </rect>
    </property>
    <property name="text">
     <string>Add Repositories</string>
    </property>
   </widget>
   <widget class="QTextBrowser" name="textBrowser">
    <property name="geometry">
     <rect>
      <x>220</x>
      <y>20</y>
      <width>551</width>
      <height>541</height>
     </rect>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_4">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>20</y>
      <width>201</width>
      <height>41</height>
     </rect>
    </property>
    <property name="text">
     <string>Select Rom Source</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_5">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>160</y>
      <width>201</width>
      <height>41</height>
     </rect>
    </property>
    <property name="text">
     <string>Sync Selected Repo</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_6">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>230</y>
      <width>201</width>
      <height>41</height>
     </rect>
    </property>
    <property name="text">
     <string>Add Signing Keys</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_7">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>300</y>
      <width>201</width>
      <height>41</height>
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
      <y>440</y>
      <width>201</width>
      <height>41</height>
     </rect>
    </property>
    <property name="text">
     <string>Look at Output</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
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
            "LineageOS 20",
            "LineageOS 21",
            "LineageOS 22.1",
            "LineageOS 22.2",
            "crDroid   14.0",
            "crDroid   15.0",
            "AxionAOSP 15 QPR1",
            "AxionAOSP 15 QPR2",
            "RisingOS  7.0",
            "RisingOS  7.1",
            "MistOS    3.5",
        ]
        self.combo.addItems(versions)
        self.combo.setCurrentIndex(3)  # Predefined selection
        
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
        os.unlink(tmp_file_path)  # Geçici dosyayı sil
        
        # Connect button signals
        self.pushButton_4.clicked.connect(self.select_rom_source)        # Select Rom Source
        self.pushButton_3.clicked.connect(self.add_repositories)         # Add Repositories
        self.pushButton_5.clicked.connect(self.initialize_selected_repo) # Sync Selected Repo
        self.pushButton_6.clicked.connect(self.add_signing_keys)         # Add Signing Keys
        self.pushButton_7.clicked.connect(self.look_at_rom_source)       # Look at Rom Source Folder
        self.pushButton.clicked.connect(self.start_build_process)        # Add Device and Start Build
        self.pushButton_8.clicked.connect(self.look_at_output)           # Look at Output
        self.pushButton_2.clicked.connect(self.save_log_file)            # Get log.txt
        
        # QProcess for managing processes
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)
        
        # Variables
        self.rom_source_dir = ""
        self.rom_version = ""
        self.device_codename = ""  # To just store device codename
        self.log_file = ""
        self.raw_log_buffer = []   # To get raw log output

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        
        # To save raw output
        self.raw_log_buffer.append(stdout)
        
        # To clear ANSI codes 
        stdout = clean_ansi_codes(stdout)
        
        # To print logs into screen
        self.append_text(stdout)

    def handle_stderr(self):
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        
        # To save raw output
        self.raw_log_buffer.append(stderr)
        
        # To clear ANSI codes
        stderr = clean_ansi_codes(stderr)
        
        # To print logs into screen (with red color)
        self.append_text(stderr, color='red')

    def process_finished(self, exit_code, exit_status):
        if exit_code == 0:
            self.append_text("\n✅ Process completed successfully!\n")
        else:
            self.append_text(f"\n❌ Process failed with exit code {exit_code}\n")
            # To save automatically log file if build fails
            self.save_log_file(automatic=True)

    def append_text(self, text, color=None):
        """To insert text into the screen without HTML tags"""
        # Fix special characters
        text = html.escape(text)
        
        # To change new lines with <br> 
        text = text.replace('\n', '<br>')
        
        # Apply color format - CHANGE BLUE TO YELLOW
        if color == 'blue':
            color = 'yellow'  # Better visibility on dark background
        
        if color:
            text = f"<font color='{color}'>{text}</font>"
        
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertHtml(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def is_repo_available(self):
        """Check if 'repo' command is available in the system"""
        try:
            subprocess.run(["repo", "--version"], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL,
                          check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def select_rom_source(self):
        # Rom folder selection
        dir_path = QFileDialog.getExistingDirectory(self, "Select ROM Source Directory")
        if not dir_path:
            return
            
        self.rom_source_dir = dir_path
        
        # To add information messages
        self.append_text(f"ROM Source: {dir_path}\n")
        
        # If there is a .repo directory in the folder, assume it has already been initialized
        if os.path.exists(os.path.join(dir_path, ".repo")):
            self.append_text("Repository already initialized.\n\n")
            return
            
        # Version selection to initialize 
        version_dialog = RomVersionDialog(self)
        if version_dialog.exec_() == QDialog.Accepted:
            self.rom_version = version_dialog.get_selected_version()
            self.append_text(f"Selected Version: {self.rom_version}\n")
            
            # Check if repo command is available
            if not self.is_repo_available():
                QMessageBox.critical(
                    self, 
                    "Error", 
                    "'repo' command not found! Please install repo tool and ensure it's in your PATH."
                )
                return
                
            # To run repo init
            repo_command = self.get_repo_init_command()
            self.run_command(repo_command)
        else:
            self.append_text("ROM initialization canceled\n", color='orange')

    def initialize_selected_repo(self):
        if not self.rom_source_dir:
            QMessageBox.warning(self, "Warning", "Please select ROM source directory first!")
            return
            
        # To give a warning if there is no .repo directory in the folder
        if not os.path.exists(os.path.join(self.rom_source_dir, ".repo")):
            QMessageBox.warning(self, "Warning", "Repository not initialized. Please select ROM source first!")
            return
            
        # To run repo sync
        self.run_command("repo sync --force-sync")

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
            if "7.0" in version:
                return "repo init -u https://github.com/RisingOS-Revived/android -b fifteen --git-lfs --depth=1"
            elif "7.1" in version:
                return "repo init -u https://github.com/RisingOS-Revived/android -b qpr2 --git-lfs --depth=1"
         
        elif "mistos" in version:
            if "3.5" in version:
                return "repo init -u https://github.com/Project-Mist-OS/manifest -b vic --git-lfs --depth=1"
        
        # Default command if no match
        return "repo init -u https://github.com/LineageOS/android.git -b lineage-22.2 --git-lfs --depth=1"

    def add_repositories(self):
        if not self.rom_source_dir:
            QMessageBox.warning(self, "Warning", "Please select ROM source directory first!")
            return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Manifest XML File", 
            "", 
            "XML Files (*.xml)"
        )
        
        if file_path:
            # To create .repo/local_manifests folder for dt's
            local_manifests_dir = os.path.join(self.rom_source_dir, ".repo", "local_manifests")
            os.makedirs(local_manifests_dir, exist_ok=True)
            
            # Get original filename instead of renaming to "device.xml"
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(local_manifests_dir, file_name)
            
            # Copy manifest into folder
            shutil.copy(file_path, dest_path)
            
            self.append_text(f"{file_name} copied to: {dest_path}\n")

    def add_signing_keys(self):
        if not self.rom_source_dir:
            QMessageBox.warning(self, "Warning", "Please select ROM source directory first!")
            return
        
        dir_path = QFileDialog.getExistingDirectory(self, "Select Signing Keys Directory")
        if dir_path:
            # Target folder: rom_source/vendor/
            dest_dir = os.path.join(self.rom_source_dir, "vendor")
   
            # To copy keys
            try:
                # Delete previous keys (if any)
                target_keys_dir = os.path.join(dest_dir, "lineage_priv")
                if os.path.exists(target_keys_dir):
                    shutil.rmtree(target_keys_dir)
                
                # Paste new keys
                shutil.copytree(dir_path, target_keys_dir)
                
                self.append_text(f"Signing keys copied to: {target_keys_dir}\n")
                QMessageBox.information(self, "Success", "Signing keys added successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to copy signing keys:\n{str(e)}")

    def start_build_process(self):
        if not self.rom_source_dir:
            QMessageBox.warning(self, "Warning", "Please select ROM source directory first!")
            return
        
        # Device and version selection for lunch
        device, ok = QInputDialog.getText(self, "Device Selection", 
                                        "Enter lunch device name and build type (e.g. lineage_munch-bp1a-userdebug):")
        if not ok or not device:
            return
            
        # Extract device codename for output folder (lineage_munch-userdebug -> munch)
        if '_' in device:
            self.device_codename = device.split('_')[1].split('-')[0]
        else:
            self.device_codename = device.split('-')[0]
            
        # To define j paramater count for compile
        threads, ok = QInputDialog.getInt(self, "Build Threads", 
                                        "Number of build threads (j parameter):", 
                                        8, 1, 32, 1)
        if not ok:
            return
        
        # Run the build commands
        command = f". build/envsetup.sh && lunch {device} && m bacon otatools target-files-package -j{threads}"
        
        # To logging text (changed color to yellow)
        self.append_text(f"$ {command}\n", color='blue')  # Will be converted to yellow in append_text
        
        # Add commands to raw log file
        self.raw_log_buffer.append(f"$ {command}\n")
        
        # Run command
        self.run_command(command)

    def run_command(self, command):
        if not self.rom_source_dir:
            return
            
        self.process.setWorkingDirectory(self.rom_source_dir)
        
        # Check old process if it finished or not
        if self.process.state() == QProcess.Running:
            self.process.terminate()
            self.process.waitForFinished()
            
        # Log the command to the console (changed color to yellow)
        self.append_text(f"$ {command}\n", color='blue')  # Will be converted to yellow in append_text
        self.raw_log_buffer.append(f"$ {command}\n")
        
        self.process.start("bash", ["-c", command])

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
