"""Stats module for Minicahe.

Tracks token savings and compression history.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class StatsTracker:
    """Track compression statistics across sessions."""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = os.path.join(str(Path.home()), ".minicahe", "stats.json")
        self.db_path = db_path
        self._ensure_db()

    def _ensure_db(self):
        """Ensure stats database file exists."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.exists(self.db_path):
            self._write_db({
                "total_original_tokens": 0,
                "total_compressed_tokens": 0,
                "total_sessions": 0,
                "total_compressions": 0,
                "sessions": [],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            })

    def _read_db(self) -> dict:
        """Read stats database."""
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _write_db(self, data: dict):
        """Write stats database."""
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def record_compression(self, original_tokens: int, compressed_tokens: int,
                           context: Optional[str] = None):
        """Record a compression event."""
        db = self._read_db()
        db["total_original_tokens"] = db.get("total_original_tokens", 0) + original_tokens
        db["total_compressed_tokens"] = db.get("total_compressed_tokens", 0) + compressed_tokens
        db["total_compressions"] = db.get("total_compressions", 0) + 1
        db["updated_at"] = datetime.now().isoformat()

        # Keep last 100 sessions
        sessions = db.get("sessions", [])
        sessions.append({
            "timestamp": datetime.now().isoformat(),
            "original_tokens": original_tokens,
            "compressed_tokens": compressed_tokens,
            "savings": original_tokens - compressed_tokens,
            "savings_pct": round((original_tokens - compressed_tokens) / original_tokens * 100, 1)
            if original_tokens > 0 else 0,
            "context": context,
        })
        if len(sessions) > 100:
            sessions = sessions[-100:]
        db["sessions"] = sessions

        self._write_db(db)

    def get_summary(self) -> dict:
        """Get summary statistics."""
        db = self._read_db()
        total_orig = db.get("total_original_tokens", 0)
        total_comp = db.get("total_compressed_tokens", 0)

        return {
            "total_compressions": db.get("total_compressions", 0),
            "total_tokens_saved": total_orig - total_comp,
            "total_tokens_original": total_orig,
            "total_tokens_compressed": total_comp,
            "overall_savings_pct": round((total_orig - total_comp) / total_orig * 100, 1)
            if total_orig > 0 else 0,
            "sessions": db.get("sessions", [])[-10:],  # Last 10 sessions
            "db_path": self.db_path,
        }
