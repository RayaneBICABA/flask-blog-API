#!/usr/bin/env python3
"""
Management script for Flask Blog API
Handles database migrations, user creation, and other administrative tasks
"""

import os
import sys
from flask.cli import FlaskGroup
from app import create_app
from app.models import db, User
from app.controllers.userController import create_admin_user
from app.utils.passwordHash import hash_password

app = create_app()
cli = FlaskGroup(app)

@cli.command("init-db")
def init_db():
    """Initialize the database with tables"""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

@cli.command("create-admin")
def create_admin():
    """Create an admin user"""
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    
    with app.app_context():
        try:
            admin = create_admin_user(username, email, password)
            print(f"Admin user '{admin.username}' created successfully!")
        except Exception as e:
            print(f"Error creating admin user: {e}")

@cli.command("migrate")
def migrate():
    """Run database migrations"""
    os.system("alembic upgrade head")
    print("Migrations completed successfully!")

@cli.command("migrate-create")
def migrate_create():
    """Create a new migration"""
    message = input("Enter migration message: ")
    os.system(f"alembic revision --autogenerate -m '{message}'")
    print("Migration created successfully!")

@cli.command("migrate-rollback")
def migrate_rollback():
    """Rollback the last migration"""
    os.system("alembic downgrade -1")
    print("Migration rolled back successfully!")

@cli.command("migrate-history")
def migrate_history():
    """Show migration history"""
    os.system("alembic history")

@cli.command("reset-db")
def reset_db():
    """Reset the database (WARNING: This will delete all data)"""
    confirm = input("Are you sure you want to reset the database? This will delete ALL data! (yes/no): ")
    if confirm.lower() == 'yes':
        with app.app_context():
            db.drop_all()
            db.create_all()
            print("Database reset successfully!")
    else:
        print("Database reset cancelled.")

@cli.command("list-users")
def list_users():
    """List all users"""
    with app.app_context():
        users = User.query.all()
        if users:
            print("\nUsers:")
            print("-" * 50)
            for user in users:
                print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Role: {user.role}")
        else:
            print("No users found.")

if __name__ == '__main__':
    cli() 