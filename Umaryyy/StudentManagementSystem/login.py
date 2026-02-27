"""
Login system for the Student Management System.
Provides username-password authentication.
"""

import hashlib
from typing import Dict, Optional

class LoginSystem:
    """
    Simple login system with username-password authentication.
    
    Uses SHA-256 hashing for password storage.
    """
    
    def __init__(self):
        """Initialize the login system with default admin user."""
        self.users: Dict[str, str] = {}
        # Add default admin user (username: admin, password: admin123)
        self.add_user("admin", "admin123")
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def add_user(self, username: str, password: str) -> bool:
        """
        Add a new user with username and password.
        
        Args:
            username: Username (must be unique)
            password: Password
            
        Returns:
            True if user added successfully, False if username already exists
        """
        if not username or not password:
            raise ValueError("Username and password cannot be empty")
        
        if username in self.users:
            return False
        
        self.users[username] = self._hash_password(password)
        return True
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticate user with username and password.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            True if authentication successful, False otherwise
        """
        if username not in self.users:
            return False
        
        hashed_password = self._hash_password(password)
        return self.users[username] == hashed_password
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """
        Change user's password.
        
        Args:
            username: Username
            old_password: Current password
            new_password: New password
            
        Returns:
            True if password changed successfully, False otherwise
        """
        if not self.authenticate(username, old_password):
            return False
        
        if not new_password:
            raise ValueError("New password cannot be empty")
        
        self.users[username] = self._hash_password(new_password)
        return True
    
    def get_all_users(self) -> list:
        """Get list of all usernames."""
        return list(self.users.keys())

# Example usage and test
if __name__ == "__main__":
    login_system = LoginSystem()
    
    print("Login System Test")
    print("=" * 30)
    
    # Test default admin login
    print("Testing default admin login:")
    if login_system.authenticate("admin", "admin123"):
        print("✓ Admin login successful")
    else:
        print("✗ Admin login failed")
    
    # Test invalid login
    print("\nTesting invalid login:")
    if not login_system.authenticate("admin", "wrongpassword"):
        print("✓ Invalid password correctly rejected")
    else:
        print("✗ Invalid password accepted")
    
    # Add new user
    print("\nAdding new user 'user1' with password 'password123':")
    if login_system.add_user("user1", "password123"):
        print("✓ User 'user1' added successfully")
    else:
        print("✗ Failed to add user (username may already exist)")
    
    # Test new user login
    print("\nTesting new user login:")
    if login_system.authenticate("user1", "password123"):
        print("✓ User1 login successful")
    else:
        print("✗ User1 login failed")
    
    # Change password
    print("\nChanging password for user1:")
    if login_system.change_password("user1", "password123", "newpassword456"):
        print("✓ Password changed successfully")
    else:
        print("✗ Failed to change password")
    
    # Test new password
    print("\nTesting new password:")
    if login_system.authenticate("user1", "newpassword456"):
        print("✓ New password works")
    else:
        print("✗ New password doesn't work")
    
    print(f"\nAll users: {login_system.get_all_users()}")