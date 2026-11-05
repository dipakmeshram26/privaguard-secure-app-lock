"""
PrivaGuard Process DACL Anti-Termination & Anti-Suspend Shield.
Applies native Windows Kernel Object Security (SetKernelObjectSecurity) to strip
PROCESS_TERMINATE (0x0001) and PROCESS_SUSPEND_RESUME (0x0800) from the process
Security Descriptor, preventing taskkill /F, Task Manager, and third-party tools
from terminating or freezing the application.
"""

import os
import sys
from typing import Optional

try:
    import win32api
    import win32security
    import ntsecuritycon
    import win32process
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

_IS_SHIELDED = False

# Win32 Process Access Rights constants
PROCESS_TERMINATE = 0x0001
PROCESS_SUSPEND_RESUME = 0x0800
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
SYNCHRONIZE = 0x00100000
READ_CONTROL = 0x00020000
WRITE_DAC = 0x00040000
WRITE_OWNER = 0x00080000
STANDARD_RIGHTS_REQUIRED = 0x000F0000


def harden_process_dacl(h_proc: Optional[int] = None) -> bool:
    """
    Applies custom DACL on current process handle:
    - Explicit DENY: PROCESS_TERMINATE (0x0001) to User, Admins, and World
    - Explicit DENY: PROCESS_SUSPEND_RESUME (0x0800) to User, Admins, and World
    - Explicit DENY: WRITE_DAC (0x00040000) to prevent tampering with DACL
    - Allow: Full Control to NT AUTHORITY\\SYSTEM (PrivaGuard Service)
    - Allow: Limited Query, Read Control & Synchronize to User/Admins (keeps UI smooth)
    """
    global _IS_SHIELDED
    if not WIN32_AVAILABLE:
        return False

    try:
        if h_proc is None:
            h_proc = win32api.GetCurrentProcess()

        # Query Current User Token
        tok = win32security.OpenProcessToken(h_proc, win32security.TOKEN_QUERY)
        user_sid = win32security.GetTokenInformation(tok, win32security.TokenUser)[0]

        # Resolve System, Admin, and Everyone SIDs
        system_sid = win32security.CreateWellKnownSid(win32security.WinLocalSystemSid)
        admin_sid = win32security.CreateWellKnownSid(win32security.WinBuiltinAdministratorsSid)
        world_sid = win32security.CreateWellKnownSid(win32security.WinWorldSid)

        dacl = win32security.ACL()

        # 1. Deny ACEs (In Windows NTFS/Kernel security, Deny ACEs MUST precede Allow ACEs)
        DENY_FLAGS = PROCESS_TERMINATE | PROCESS_SUSPEND_RESUME | WRITE_DAC | WRITE_OWNER
        dacl.AddAccessDeniedAce(win32security.ACL_REVISION, DENY_FLAGS, user_sid)
        dacl.AddAccessDeniedAce(win32security.ACL_REVISION, DENY_FLAGS, admin_sid)
        dacl.AddAccessDeniedAce(win32security.ACL_REVISION, DENY_FLAGS, world_sid)

        # 2. Allow SYSTEM (Our Session 0 Service) full management control
        dacl.AddAccessAllowedAce(win32security.ACL_REVISION, ntsecuritycon.GENERIC_ALL, system_sid)

        # 3. Allow Current User and Administrators safe non-terminating rights
        # (Needed so Windows DWM compositor, shell, and taskbar can query window state)
        SAFE_ALLOW_FLAGS = PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE | READ_CONTROL | 0x0400 # QUERY_INFORMATION
        dacl.AddAccessAllowedAce(win32security.ACL_REVISION, SAFE_ALLOW_FLAGS, user_sid)
        dacl.AddAccessAllowedAce(win32security.ACL_REVISION, SAFE_ALLOW_FLAGS, admin_sid)

        sd = win32security.SECURITY_DESCRIPTOR()
        sd.SetSecurityDescriptorDacl(1, dacl, 0)

        win32security.SetKernelObjectSecurity(
            h_proc,
            win32security.DACL_SECURITY_INFORMATION,
            sd
        )

        _IS_SHIELDED = True
        return True
    except Exception as e:
        return False


def restore_process_dacl(h_proc: Optional[int] = None) -> bool:
    """
    Restores standard full-control DACL so application can terminate cleanly
    during Master Password authorized exit or official uninstallation.
    """
    global _IS_SHIELDED
    if not WIN32_AVAILABLE:
        return False

    try:
        if h_proc is None:
            h_proc = win32api.GetCurrentProcess()

        tok = win32security.OpenProcessToken(h_proc, win32security.TOKEN_QUERY)
        user_sid = win32security.GetTokenInformation(tok, win32security.TokenUser)[0]
        system_sid = win32security.CreateWellKnownSid(win32security.WinLocalSystemSid)
        admin_sid = win32security.CreateWellKnownSid(win32security.WinBuiltinAdministratorsSid)

        dacl = win32security.ACL()
        dacl.AddAccessAllowedAce(win32security.ACL_REVISION, ntsecuritycon.GENERIC_ALL, user_sid)
        dacl.AddAccessAllowedAce(win32security.ACL_REVISION, ntsecuritycon.GENERIC_ALL, admin_sid)
        dacl.AddAccessAllowedAce(win32security.ACL_REVISION, ntsecuritycon.GENERIC_ALL, system_sid)

        sd = win32security.SECURITY_DESCRIPTOR()
        sd.SetSecurityDescriptorDacl(1, dacl, 0)

        win32security.SetKernelObjectSecurity(
            h_proc,
            win32security.DACL_SECURITY_INFORMATION,
            sd
        )

        _IS_SHIELDED = False
        return True
    except Exception:
        return False


def is_process_shielded() -> bool:
    """Returns True if the current process DACL anti-termination shield is active."""
    return _IS_SHIELDED
