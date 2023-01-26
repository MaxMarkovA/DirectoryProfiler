# Max Markov 01.26.2023

from __future__ import annotations
from typing import Optional
from dataclasses import dataclass


@dataclass
class Directory:
    """Directory-related collected information"""
    name: str
    parent: Optional[Directory]
    database_id: Optional[int] = None


@dataclass
class File:
    """File-related collected information"""
    name: str
    last_modified: float
    access_rights: str
    content_hash: bytes
    directory: Directory
