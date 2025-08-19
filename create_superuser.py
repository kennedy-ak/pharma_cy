#!/usr/bin/env python
import os
import sys
import django
from getpass import getpass

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharma_cy.settings')
django.setup()

from app.models import User

def create_superuser():
    print("=== Pharmacy Management System - Create Superuser ===\n")
    
    # Get username
    while True:
        username = input("Enter username: ").strip()
        if username:
            if User.objects.filter(username=username).exists():
                print(f"User '{username}' already exists. Please choose a different username.")
                continue
            break
        print("Username cannot be empty.")
    
    # Get email
    email = input("Enter email address (optional): ").strip()
    
    # Get password
    while True:
        password = getpass("Enter password: ")
        password_confirm = getpass("Confirm password: ")
        
        if password != password_confirm:
            print("Passwords don't match. Please try again.")
            continue
            
        if len(password) < 6:
            print("Password must be at least 6 characters long.")
            continue
            
        break
    
    # Get phone number
    phone_number = input("Enter phone number (optional): ").strip()
    
    try:
        # Create superuser
        user = User.objects.create_user(
            username=username,
            email=email or f"{username}@pharmacy.com",
            password=password,
            phone_number=phone_number or None,
            role='admin',
            is_staff=True,
            is_superuser=True
        )
        
        print(f"\n✓ Superuser '{username}' created successfully!")
        print(f"  Email: {user.email}")
        print(f"  Role: Administrator")
        print(f"  Phone: {user.phone_number or 'Not provided'}")
        print("\nYou can now:")
        print("  1. Access Django Admin at: http://127.0.0.1:8000/admin/")
        print("  2. Login to the system at: http://127.0.0.1:8000/login/")
        print("  3. Create reception users through Django Admin")
        
    except Exception as e:
        print(f"\nError creating superuser: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    try:
        create_superuser()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")