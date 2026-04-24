# 🛡️ PrivaGuard: The Ultimate Windows Security & Privacy Suite

**PrivaGuard** is a high-performance, enterprise-grade security application designed to provide an unbreakable layer of protection for your Windows environment. It combines process monitoring, file encryption, and AI-driven intruder detection to ensure your data stays private and your system stays tamper-proof.

![PrivaGuard Banner](assets/logo_banner.png)

---

## 🌟 Deep Feature Analysis

### 1. 🔒 Intelligent Application Locking
**How it works:**
PrivaGuard runs a high-frequency background monitor that polls the active process list every 0.3 seconds. When a user attempts to launch a "Locked App," the system intercepts the process immediately. Instead of just killing it, it suspends the process and overlays a **Secure Password Vault** UI.
*   **Process Interception**: Uses `psutil` for lightning-fast detection.
*   **Custom Per-App Passwords**: You can set different passwords for different apps (e.g., a complex one for Chrome and a simple one for Games).
*   **Fake Crash Mode**: (Optional) Instead of asking for a password, the app shows a fake "Windows has encountered an error" message to deter casual snoopers.

### 2. 📂 Stealth File & Folder Vault
**How it works:**
Our folder locker doesn't just "hide" files; it manipulates system-level attributes and permissions to make folders inaccessible to the standard Windows Explorer.
*   **Invisible Mode**: Locked folders are stripped of their directory status in the eye of the OS, making them appear as "System Protected" files that cannot be opened or deleted.
*   **No Data Loss**: Your data is never moved or modified, only the "access gates" are locked at the kernel level.

### 3. 📸 AI Intruder Capture (The Silent Guardian)
**How it works:**
If an unauthorized person attempts to access a locked app or the PrivaGuard dashboard, the system tracks failed attempts. 
*   **Threshold Trigger**: After exactly **3 failed attempts**, the system silently activates the primary webcam.
*   **Stealth Capture**: An image is captured asynchronously (without freezing the UI) and saved in an encrypted local directory.
*   **Visual Evidence**: Every log entry includes a timestamp, the targeted application, and the high-resolution photo of the intruder.

### 4. 📧 Real-Time Email Security Alerts
**How it works:**
PrivaGuard integrates with secure SMTP protocols to provide remote monitoring.
*   **Instant Notifications**: If an intruder is detected, an email is sent to your verified address within seconds.
*   **Evidence Attachment**: The intruder's photo is automatically attached to the email, allowing you to identify the culprit even if you are away from your PC.
*   **OTP Verification**: High-security actions (like changing the Master Password or Alert Email) require an OTP (One Time Password) sent to your mail.

### 5. 🛡️ Anti-Kill & Self-Protection (The "Unstoppable" Logic)
**How it works:**
This is what makes PrivaGuard better than standard lockers. It uses a **Mutual Protection Protocol**.
*   **The Guardian (WinSysCheck)**: A separate, lightweight process that monitors `AppLocker.exe`. If the main app is force-killed via Task Manager or CMD, the Guardian restarts it within 1 second.
*   **Task Manager Interception**: Since Task Manager is the primary tool used to kill security apps, PrivaGuard places an **Execution Lock** on `taskmgr.exe`. You must enter the Master Password just to open Task Manager.
*   **CMD/PowerShell Safety**: You can use terminals freely, but they cannot be used to terminate PrivaGuard processes.

### 6. 🚀 Zero-Delay Instant Startup
**How it works:**
Unlike most apps that use the Registry "Run" key (which Windows can delay for 10-20 seconds), PrivaGuard uses the **Windows Task Scheduler**.
*   **Highest Privileges**: The app launches with "System/Admin" privileges automatically at logon.
*   **Instant Protection**: The monitor starts working even before your desktop icons finish loading.

---

## 🔐 Security & Privacy
*   **Zero Data Collection**: We do not store any of your data, photos, or passwords on our servers. Everything stays on your PC.
*   **Encrypted Local Storage**: All sensitive data is stored using industry-standard hashing and encryption.

---
*Built for those who value their digital privacy.*
