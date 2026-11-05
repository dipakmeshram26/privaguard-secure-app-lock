import os
import ctypes
import string
import random
import json
import shutil

class FileLocker:
    def __init__(self):
        self._aplk_ext = ".aplk"
        self._folder_clsid = ".{91523423-8824-4f62-1025-a4d1f2345123}" # AppLocker Custom Folder CLSID
        local_app = os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))
        self._vault_dir = os.path.join(local_app, "PrivaGuard", "Vault")
        if not os.path.exists(self._vault_dir) and os.path.exists(os.path.join(local_app, "AppLocker", "Vault")):
            self._vault_dir = os.path.join(local_app, "AppLocker", "Vault")
        os.makedirs(self._vault_dir, exist_ok=True)
        # Hide vault directory
        self._apply_hidden_attrs(os.path.dirname(self._vault_dir), hide=True) # Hide PrivaGuard folder

    def _apply_hidden_attrs(self, path: str, hide: bool):
        if not os.path.exists(path): return
        hidden_system = 0x02 | 0x04
        current_attributes = ctypes.windll.kernel32.GetFileAttributesW(path)
        if current_attributes != -1:
            if hide:
                new_attributes = current_attributes | hidden_system
            else:
                new_attributes = current_attributes & ~hidden_system
            ctypes.windll.kernel32.SetFileAttributesW(path, new_attributes)

    def _get_random_id(self, length=8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def lock_item(self, target_path: str, is_folder: bool) -> tuple[bool, str]:
        """Locks an item by moving it to the central Vault and creating a placeholder in its place."""
        if not os.path.exists(target_path):
            return False, ""
            
        try:
            base_name = os.path.basename(target_path).rstrip('/')
            vault_name = f"{base_name}_{self._get_random_id()}"
            vault_target_path = os.path.join(self._vault_dir, vault_name)
            
            # 1. Move to Vault
            shutil.move(target_path, vault_target_path)
            self._apply_hidden_attrs(vault_target_path, hide=True)
            
            placeholder_path = ""
            pointer_data = {
                "original_path": target_path,
                "vault_path": vault_target_path,
                "is_folder": is_folder
            }

            # UNIVERSAL Wrapper logic (Files and Folders are now both locked as .aplk FILES)
            placeholder_path = target_path + self._aplk_ext
            with open(placeholder_path, 'w') as f:
                json.dump(pointer_data, f)
            
            # Apply hidden attribute to the wrapper file? 
            # No, keep it visible but maybe make it 'ReadOnly' or 'System' if we want to be fancy.
            # Keeping it simple REG_SZ association is enough.
                
            return True, placeholder_path
        except Exception as e:
            print(f"Error locking item: {e}")
            return False, ""

    def unlock_item(self, placeholder_path: str) -> tuple[bool, str]:
        """Unlocks item given the placeholder path, moving it back from the Vault."""
        try:
            print(f"DEBUG: Unlocking {placeholder_path}")
            if not os.path.exists(placeholder_path):
                print(f"DEBUG: Placeholder {placeholder_path} NOT FOUND")
                return False, ""
                
            # Unified File-based lock detection
            with open(placeholder_path, 'r') as f:
                data = json.load(f)
                
            if not data: 
                print("DEBUG: No metadata found in placeholder")
                return False, ""
                
            vault_path = data.get("vault_path")
            original_path = data.get("original_path")
            
            print(f"DEBUG: Original path: {original_path}")
            print(f"DEBUG: Vault path: {vault_path}")

            if not vault_path or not os.path.exists(vault_path):
                print("DEBUG: Vault path missing!")
                return False, ""
                
            # 1. Unhide
            self._apply_hidden_attrs(vault_path, hide=False)
            
            # 2. Move back to original location
            original_path = original_path.rstrip('\\').rstrip('/')
            
            if os.path.exists(original_path):
                 print(f"DEBUG: Target {original_path} ALREADY EXISTS. Cleaning up...")
                 if os.path.isdir(original_path): shutil.rmtree(original_path)
                 else: os.remove(original_path)
                 
            print(f"DEBUG: Moving {vault_path} -> {original_path}")
            shutil.move(vault_path, original_path)
            
            # 3. Clean up placeholder file
            print(f"DEBUG: Cleaning up placeholder {placeholder_path}")
            os.remove(placeholder_path)
            
            return True, original_path
        except Exception as e:
             print(f"Error unlocking item: {e}")
             import traceback
             traceback.print_exc()
             return False, ""
