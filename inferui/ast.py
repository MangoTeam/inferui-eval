from dataclasses import dataclass

from typing import List

@dataclass
class Box:
  left: int
  top: int
  right: int
  bottom: int

@dataclass
class Resolution:
  width: int
  height: int

@dataclass
class Rendering:
  resolution: Resolution
  boxes: List[Box]

@dataclass
class Layout:
  id: int
  renderings: List[Rendering]

