from dataclasses import dataclass
from ..common.run import View

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

  def to_view(self) -> View:
    kids: List[View] = []
    for i,box in enumerate(self.boxes):
      child = View(name="child_%d" % i, rect=list(map(float, [box.left, box.top, box.right, box.bottom])))
      kids.append(child)
    return View(name="root", rect=[0.0, 0.0, float(self.resolution.width), float(self.resolution.height)])

@dataclass
class Layout:
  id: int
  renderings: List[Rendering]


