"""
Rehash seed user passwords from SHA-256 to bcrypt.

Run once after Phase 4 is deployed:
    python scripts/rehash_users.py

All seed users receive the default password: NovaTech@2024
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.database.connection import SessionLocal
from app.models import User

DEFAULT_PASSWORD = "NovaTech@2024"


def main() -> None:
    db: Session = SessionLocal()
    try:
        users = db.query(User).all()
        hashed = hash_password(DEFAULT_PASSWORD)
        for user in users:
            user.hashed_password = hashed
        db.commit()
        print(f"Rehashed passwords for {len(users)} user(s).")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
