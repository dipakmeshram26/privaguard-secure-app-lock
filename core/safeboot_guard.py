"""
PrivaGuard Windows SafeBoot Registry Guard & Boot Mode Sentinel.
Enables PrivaGuardService to run even when the machine is booted into Windows Safe Mode
(Minimal or Network) by provisioning service entries in HKLM\\SafeBoot.
Detects operating system boot mode (Normal, Safe Mode Minimal, Safe Mode with Networking)
via native Windows SM_CLEANBOOT kernel metrics.
"""

import os
import sys
import ctypes
import winreg
from typing import Tuple

SAFEBOOT_MINIMAL = r"SYSTEM\CurrentControlSet\Control\SafeBoot\Minimal\PrivaGuardService"
SAFEBOOT_NETWORK = r"SYSTEM\CurrentControlSet\Control\SafeBoot\Network\PrivaGuardService"
SERVICE_NAME = "PrivaGuardService"
SM_CLEANBOOT = 67


def get_boot_mode() -> Tuple[int, str]:
    """
    Queries Windows native SM_CLEANBOOT metric to identify current operating system boot state:
    0: Normal Boot
    1: Fail-safe Minimal (Safe Mode without Networking)
    2: Fail-safe with Network (Safe Mode with Networking)
    Returns: (boot_code, mode_name)
    """
    try:
        boot_code = ctypes.windll.user32.GetSystemMetrics(SM_CLEANBOOT)
        modes = {
            0: "Normal Boot",
            1: "Safe Mode (Minimal)",
            2: "Safe Mode with Networking"
        }
        return boot_code, modes.get(boot_code, f"Unknown ({boot_code})")
    except Exception:
        return 0, "Normal Boot"


def is_safe_mode() -> bool:
    """Returns True if the system is currently executing in any Windows Safe Mode."""
    code, _ = get_boot_mode()
    return code > 0


def install_safeboot_keys() -> bool:
    """
    Registers PrivaGuardService under Windows SafeBoot Minimal and Network branches.
    Allows continuous protection even if user reboots into Safe Mode to bypass locks.
    Fails safely without raising exceptions if running non-elevated.
    """
    success_count = 0
    for mode in ["Minimal", "Network"]:
        key_path = rf"SYSTEM\CurrentControlSet\Control\SafeBoot\{mode}\{SERVICE_NAME}"
        try:
            with winreg.CreateKeyEx(
                winreg.HKEY_LOCAL_MACHINE,
                key_path,
                0,
                winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY
            ) as k:
                winreg.SetValueEx(k, "", 0, winreg.REG_SZ, "Service")
            success_count += 1
        except Exception:
            pass

    return success_count == 2


def remove_safeboot_keys() -> bool:
    """
    Deregisters PrivaGuardService from Windows SafeBoot branches during clean uninstallation.
    """
    for mode in ["Minimal", "Network"]:
        key_path = rf"SYSTEM\CurrentControlSet\Control\SafeBoot\{mode}"
        try:
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                key_path,
                0,
                winreg.KEY_ALL_ACCESS | winreg.KEY_WOW64_64KEY
            ) as k:
                winreg.DeleteKey(k, SERVICE_NAME)
        except Exception:
            pass

    return True


def is_safeboot_registered() -> Tuple[bool, bool]:
    """Returns (is_minimal_registered, is_network_registered)."""
    minimal_ok = False
    network_ok = False

    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            SAFEBOOT_MINIMAL,
            0,
            winreg.KEY_READ | winreg.KEY_WOW64_64KEY
        ) as k:
            val, _ = winreg.QueryValueEx(k, "")
            minimal_ok = (val == "Service")
    except Exception:
        pass

    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            SAFEBOOT_NETWORK,
            0,
            winreg.KEY_READ | winreg.KEY_WOW64_64KEY
        ) as k:
            val, _ = winreg.QueryValueEx(k, "")
            network_ok = (val == "Service")
    except Exception:
        pass

    return minimal_ok, network_ok


def ensure_safeboot_keys() -> bool:
    """
    Verifies that SafeBoot keys are intact. If missing or tampered with,
    attempts to repair them immediately. Returns True if keys are active.
    """
    min_ok, net_ok = is_safeboot_registered()
    if min_ok and net_ok:
        return True
    # Attempt repair
    return install_safeboot_keys()
