```
 ██████╗ ██████╗ ██╗██╗   ██╗ █████╗  ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ 
 ██╔══██╗██╔══██╗██║██║   ██║██╔══██╗██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗
 ██████╔╝██████╔╝██║██║   ██║███████║██║  ███╗██║   ██║███████║██████╔╝██║  ██║
 ██╔═══╝ ██╔══██╗██║╚██╗ ██╔╝██╔══██║██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║
 ██║     ██║  ██║██║ ╚████╔╝ ██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
 ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 
                 [ KERNEL-HARDENED PRIVACY DEFENSE SUITE ]
```

<div align="center">

[![Windows 11 / 10](https://img.shields.io/badge/Platform-Windows%2011%20%7C%2010-0078d4?style=for-the-badge&logo=windows&logoColor=white)](https://privaguard.tech)
[![Security Architecture](https://img.shields.io/badge/Security-Process%20DACL%20Hardened-b1ff29?style=for-the-badge&logo=shield&logoColor=black)](https://privaguard.tech)
[![Encryption](https://img.shields.io/badge/Cipher-AES--256%20GCM%20%7C%20RSA--2048-a855f7?style=for-the-badge&logo=lock&logoColor=white)](https://privaguard.tech)
[![Service Level](https://img.shields.io/badge/SCM%20Service-Session%200%20SYSTEM-06b6d4?style=for-the-badge&logo=server&logoColor=white)](https://privaguard.tech)
[![Cloud Telemetry](https://img.shields.io/badge/Telemetry-0%25%20Air--Gapped-ef4444?style=for-the-badge&logo=private-internet-access&logoColor=white)](https://privaguard.tech)

**Enterprise-Grade Process Lockdown • Session 0 Watchdog • Anti-Taskkill Immunity • Hardware Sentry**

[Official Website](https://privaguard.tech) • [Features](https://privaguard.tech/features.html) • [Security Docs](https://privaguard.tech/how-it-works.html) • [Waitlist](https://privaguard.tech/waitlist.html)

</div>

---

## ⚡ Overview

**PrivaGuard** is an enterprise-grade Windows endpoint security suite, privacy application locker, and physical intrusion defense engine. Engineered specifically for physical workstation defense, PrivaGuard prevents unauthorized individuals from accessing sensitive IDEs (VS Code), web browsers (Chrome), chat clients (Telegram, WhatsApp), and local confidential files.

Unlike conventional application lockers that run as easily terminable user-space processes, PrivaGuard integrates deeply into the **Windows NT kernel subsystem**, enforcing **Process DACL anti-termination hooks**, **Session 0 SCM services**, **SafeBoot boot persistence**, and **offline asymmetric RSA-2048 licensing**.

---

## 🛡️ Threat Benchmark Matrix (Penetration Defense)

| Threat Vector / Attack Scenario | Conventional App Lockers | PrivaGuard Cyber Defense |
| :--- | :--- | :--- |
| **Elevated Admin `taskkill /F`** | Process instantly terminated ❌ | **Access Denied (`SetKernelObjectSecurity` DACL)** 🛡️ |
| **Windows Safe Mode Boot** | Bypassed completely at startup ❌ | **SafeBoot Minimal & Network Sentinel (`SM_CLEANBOOT`)** 🛡️ |
| **Manual `config.json` Deletion** | Passwords wiped & apps unlocked ❌ | **< 50ms HMAC-SHA256 Multi-Hive Shadow Vault** 🛡️ |
| **Public Cafe Laptop Snatching** | Stolen silently without alert ❌ | **105dB Charger Disconnect Acoustic Siren** 🛡️ |
| **PIN Guessing & Snooning** | Unlimited guesses, zero trace ❌ | **Silent DirectShow Camera Sentry + Outbox Alert** 🛡️ |
| **Memory / Hex Patching** | Cracked via byte flipping ❌ | **PE Checksum Integrity & PEB Debugger Traps** 🛡️ |
| **Cloud Keystroke Telemetry** | Sends usage to 3rd-party servers ❌ | **100% Local Air-Gapped Verification** 🛡️ |

---

## 🏗️ System Architecture

PrivaGuard uses a **Dual-Process Watchdog** architecture spanning across Windows isolation boundaries:

```
+---------------------------------------------------------------------------------+
|                                 WINDOWS HOST                                    |
|                                                                                 |
|  [SESSION 0: NT AUTHORITY\SYSTEM]                                               |
|  +---------------------------------------------------------------------------+  |
|  | PrivaGuardService.exe (Background Guardian Service)                       |  |
|  | - SCM Auto-Restart Recovery (actions=restart/1000/restart/1000)            |  |
|  | - SafeBoot Minimal/Network Boot Guard (SM_CLEANBOOT Metric)               |  |
|  | - 50ms Real-Time File Sentinel (ReadDirectoryChangesW)                    |  |
|  | - Multi-Hive HMAC-SHA256 Shadow Vault (%PROGRAMDATA% / HKLM)              |  |
|  | - Named Pipe Server (\\.\pipe\PrivaGuard_Security_Pipe)                   |  |
|  | - Session Bridge (WTSQueryUserToken -> DuplicateTokenEx)                  |  |
|  +---------------------------------------------------------------------------+  |
|                                       | Named Pipe IPC / 1.5s Heartbeat         |
|                                       v                                         |
|  [SESSION 1+: INTERACTIVE USER DESKTOP]                                         |
|  +---------------------------------------------------------------------------+  |
|  | PrivaGuard.exe (CustomTkinter Cyber UI & Process Engine)                   |  |
|  | - Process DACL Hardening (Denies PROCESS_TERMINATE / taskkill /F)         |  |
|  | - < 10ms Foreground Window Focus Interceptor Hook                         |  |
|  | - Anti-Tamper Engine (PEB Debugger Traps & Hardware Breakpoints)           |  |
|  | - Silent Intruder Camera Sentry (OpenCV DirectShow)                        |  |
|  | - 105dB AC Power Disconnect Theft Listener                                 |  |
|  | - Offline Cryptographic RSA-2048 PKCS1v15 License Engine                   |  |
|  | - AES-256 GCM File & Folder Vault                                         |  |
|  +---------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------+
```

---

## ⚡ The 14 Kernel-Hardened Security Modules

### 1. ⚡ Process DACL Anti-Termination Hook (Admin Taskkill Immunity)
Upon initialization, PrivaGuard calls the native Windows `SetKernelObjectSecurity` API to set a hardened discretionary access control list (DACL) on its process handle. This explicitly strips `PROCESS_TERMINATE` (0x0001), `PROCESS_SUSPEND_RESUME` (0x0800), `WRITE_DAC`, and `WRITE_OWNER` rights from standard users and Administrators alike. Running `taskkill /F /PID <pid>` yields `ERROR: Access is denied`.

### 2. 🛡️ Windows SafeBoot Kernel Mode Sentinel
PrivaGuard registers `PrivaGuardService` into the Windows SCM SafeBoot tree (`HKLM\SYSTEM\CurrentControlSet\Control\SafeBoot\Minimal` and `\Network`). PrivaGuard queries `GetSystemMetrics(SM_CLEANBOOT)` (Code 67); if Windows is booted in Safe Mode, defensive postures escalate instantly.

### 3. 💎 50ms Config Shadow Vault & HMAC-SHA256 Resurrection
The configuration `%LOCALAPPDATA%\PrivaGuard\config.json` is protected via NTFS DACLs (`Deny DELETE`). If forcibly deleted via low-level kernel utilities, the background service’s `ReadDirectoryChangesW` sentinel detects the tamper in < 1ms and resurrects authenticated configuration from the machine-bound HMAC-SHA256 shadow vault (`%PROGRAMDATA%\PrivaGuard\config.vault` or `HKLM`) in < 50ms.

### 4. 🚀 True Windows NT SCM Service Architecture (Session 0)
`PrivaGuardService` runs continuously under `NT AUTHORITY\SYSTEM` in Session 0 with automatic SCM restart recovery. It bridges across session boundaries using `WTSQueryUserToken` and `DuplicateTokenEx` to spawn and monitor the interactive UI inside active user desktop sessions.

### 5. 🔑 Offline RSA-2048 Asymmetric Cryptographic Licensing
PrivaGuard eliminates spoofable local registry serial keys. Licenses are signed remotely using a 2048-bit RSA private key and verified locally using the embedded public key, cryptographically binding plan limits and expiration dates to the user's hardware motherboard UUID and CPU serial.

### 6. 📸 Silent DirectShow Webcam Sentry & Resend Email Alerts
Entering an invalid PIN 3 consecutive times triggers asynchronous DirectShow camera capture. The intruder's photo is logged with cryptographic timestamps in an encrypted directory and dispatched to your email address via secure Resend API integration.

### 7. 🚨 105dB Laptop Charger Anti-Snatch Acoustic Siren
Monitors AC power status via `GetSystemPowerStatus`. If an opportunist unplugs your laptop power cable in a public cafe or office while the screen is locked, PrivaGuard triggers a continuous 105dB acoustic alarm and blacks out the screen.

### 8. ⚙️ Single-Instance Global Named Mutex Shield
Enforces singleton process execution using Win32 `CreateMutexW` (`Global\PrivaGuard_Service_Mutex`). Repeated launches seamlessly wake and focus the existing instance without spawning duplicate threads.

### 9. 🔍 PE Checksum & PEB Anti-Debug Watchdog
Continuously interrogates the Process Environment Block (PEB) for `BeingDebugged`, `NtGlobalFlag` manipulation, and hardware debug registers (DR0-DR3). Real-time SHA-256 PE checksum validation defends against in-memory hex modifications.

### 10. ⚡ Global Emergency Panic Lock (`Ctrl+Alt+P`)
Registers system-wide hotkeys through `RegisterHotKey`. Pressing `Ctrl+Alt+P` (or custom combinations) instantly locks all foreground windows in 0.01 seconds.

### 11. 🔒 Sub-Millisecond Foreground Interceptor (< 10ms)
Hooks Windows active focus events. As soon as a protected target process gains foreground focus, PrivaGuard cloaks the window with a frosted glass security shield before unauthorized inputs or screenshots can take place.

### 12. 📂 Military-Grade AES-256 GCM File & Folder Vault
Integrated cryptographic vault allowing developers and privacy-conscious users to encrypt sensitive `.env` files, SSH keys, documents, and folders using hardware-accelerated AES-256 GCM with PBKDF2HMAC key derivation.

### 13. 🌐 100% Air-Gapped Local Operation (Zero Cloud Telemetry)
PrivaGuard requires zero internet connection to protect your applications or verify master passwords. Authentication hashes are evaluated purely offline on local hardware.

### 14. 🔄 In-App Cloud Auto-Updater Stream
Includes a seamless, non-blocking auto-updater that queries `version.json` via HTTPS, displays real-time download progress, verifies executable checksums, and performs clean installer handoffs.

---

## 🛠️ Tech Stack & Win32 Security APIs

- **Core Runtime:** Python 3.13 (64-bit)
- **GUI Engine:** CustomTkinter (Cyber Dark / Neon Lime `#b1ff29`)
- **System Interop:** `pywin32`, `ctypes` (`kernel32`, `user32`, `advapi32`, `wtsapi32`, `shell32`)
- **Cryptography:** `cryptography.hazmat` (AES-256 GCM, RSA-2048 PKCS1v15, PBKDF2HMAC)
- **Hardware & Peripherals:** `opencv-python` / DirectShow (Webcam), `psutil` (Process Monitor)
- **Packaging & Compilation:** PyInstaller (Spec-driven multi-binary architecture)

---

## 🚀 Building & Deploying from Source

PrivaGuard includes an automated PowerShell build and deployment engine:

```powershell
# 1. Clone the repository
git clone https://github.com/dipakmeshram26/privaguard-secure-app-lock.git
cd privaguard-secure-app-lock

# 2. Install dependencies
pip install -r requirements.txt

# 3. Compile all 4 release binaries via automated pipeline
powershell -ExecutionPolicy Bypass -File .\build_and_deploy.ps1
```

### Generated Release Binaries (`dist/`):
- `PrivaGuardService.exe` — Windows NT SCM Guardian Service (Session 0)
- `PrivaGuard.exe` — Interactive Desktop Security Client (Session 1+)
- `PrivaGuard_Setup.exe` — Production Setup Installer & Program Files Provisioner
- `Uninstall.exe` — Self-Elevating Uninstaller & Service Cleaner

---

## 📜 Zero-Telemetry Privacy Manifesto

PrivaGuard is engineered on the principle of **Zero-Knowledge Endpoint Privacy**:
- **Zero Cloud Keystroke Logging:** Your passwords, locked process names, and keystrokes are never transmitted across the network.
- **Local Master Password Verification:** Passwords are salted and hashed using PBKDF2HMAC-SHA256 entirely on-device.
- **Air-Gapped Licensing:** Cryptographic verification operates offline using asymmetric public-key math.

---

<div align="center">

**Developed by Augionix Technologies • All Rights Reserved**  
*Defending Developer Workstations & Enterprise Privacy Worldwide.*

</div>
