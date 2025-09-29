#!/usr/bin/env python3
"""
Database seeding script
Run this separately to populate the database with initial data
"""

from app.services.seed_data import seed_database

if __name__ == "__main__":
    print("Starting database seeding...")
    try:
        seed_database()
        print("Database seeding completed successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        exit(1)
