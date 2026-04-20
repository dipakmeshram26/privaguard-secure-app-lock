# 🛡️ PrivaGuard: Secure Windows App & File Locker

**PrivaGuard** is an advanced, enterprise-grade security tool for Windows designed to protect your privacy by locking applications, encrypting files/folders, and monitoring system activity with AI-driven intruder detection.

![PrivaGuard Logo](assets/logo_banner.png)

## 🚀 Key Features

### 1. 🔒 Application & Process Locking
*   **Real-time Monitoring**: Detects and blocks unauthorized application launches instantly.
*   **System Tools Protection**: Automatically locks **Task Manager, CMD, and PowerShell** to prevent unauthorized system changes or app termination.
*   **Custom Passwords**: Set unique passwords for specific applications or use a global Master Password.

### 2. 📂 File & Folder Vault
*   **Secure Locking**: Uses Windows System integration to lock sensitive folders and files.
*   **Stealth Mode**: Folders become inaccessible and hidden from the standard file explorer until unlocked.

### 3. 📸 AI Intruder Detection
*   **Webcam Capture**: Stealthily captures a photo of anyone attempting to access locked apps with an incorrect password (after 3 failed attempts).
*   **Email Alerts**: Sends instant security notifications with intruder photos to your verified email address.

### 4. 🛡️ Ultimate Persistence (Anti-Kill)
*   **Guardian Process**: A secondary watchdog process (**WinSysCheck**) ensures that the main security engine is never terminated. If killed, it restarts within 1-2 seconds.
*   **High-Priority Startup**: Integrated with Windows Task Scheduler for instant, forceful startup upon user logon.

### 5. 📊 Security Audit Logs
*   **Detailed Records**: Keeps a local history of all security events, failed login attempts, and evidence captured.
*   **Tamper-Proof**: Logs require the Master Password to be viewed or cleared.

---

## 🛠️ Requirements

- **Operating System**: Windows 10 or 11
- **Hardware**: 
  - Integrated or External Webcam (for Intruder Detection)
  - Internet Connection (for Email Alerts)
- **Software**:
  - Python 3.10+ (if running from source)

## 📦 Dependencies

Install the required libraries using pip:
```bash
pip install customtkinter psutil opencv-python pillow pillow_heif cryptography
```

## 🚀 Installation & Usage

1. **Clone the Repo**:
   ```bash
   git clone https://github.com/yourusername/privaguard-secure-app-lock.git
   ```
2. **Run the App**:
   ```bash
   python main.py
   ```
3. **Build Executables**:
   Run the PyInstaller specs to generate `.exe` files:
   ```bash
   pyinstaller --noconfirm AppLocker.spec
   ```

---

## 🔐 Security & Privacy
*   **Local Storage**: All passwords and configurations are stored locally on your machine using SHA-256 hashing.
*   **No Data Collection**: We do not store any of your data, photos, or passwords on our servers.

## ⚖️ License
This project is licensed under the **MIT License**.

---
*Developed with ❤️ for Privacy & Security.*
