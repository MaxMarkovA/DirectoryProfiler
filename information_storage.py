# Max Markov 01.26.2023

from __future__ import annotations
from typing import Optional
from dataclasses import dataclass


@dataclass
class Directory:
    """Directory-related collected information"""
    id: int
    name: str
    parent: Optional[Directory]


@dataclass
class File:
    """File-related collected information"""
    id: int
    name: str
    last_modified: float
    access_rights: str
    content_hash: bytes
    directory: Directory
