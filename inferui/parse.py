from arpeggio.cleanpeg import ParserPEG
from arpeggio import PTNodeVisitor, visit_parse_tree

from .ast import *

grammar = """
int = r'[0-9]+'
box = '[' int ',' int ',' int ',' int ']'
resolution = '[' int ',' int ']'
rendering = '{' '"resolution":' resolution ',' '"views":' '[' box (',' box)* ']' '}'
layout = '{' '"screens":' '[' rendering (',' rendering)* ']' ',' '"id":' '"' int '"' '}'
layouts = layout*
"""

class IUIVisitor(PTNodeVisitor):
  def visit_int(self, node, children) -> int:
    return int(node.value)

  def visit_box(self, node, children) -> Box:
    assert len(children) == 4
    return Box(*children)
  
  def visit_resolution(self, node, children) -> Resolution:
    assert len(children) == 2
    return Resolution(*children)

  def visit_rendering(self, node, children):
    # print(children)
    # assert len(children) == 3
    for box in children[1:]:
      assert isinstance(box, Box)
    return Rendering(resolution=children[0], boxes=children[1:])

  def visit_layout(self, node, children):
    # print(children)
    return Layout(renderings=children[0:-1], id=children[-1])

  def visit_layouts(self, node, children):
    return children

    




int_test = "1232"
int_parser = ParserPEG(grammar, "int")
int_tree = int_parser.parse(int_test)
int_result = visit_parse_tree(int_tree, IUIVisitor())

box_test = "[12, 125,27,       3       ]"
box_parser = ParserPEG(grammar, "box")
box_tree = box_parser.parse(box_test)
box_result = visit_parse_tree(box_tree, IUIVisitor())

rendering_test = """
{
      "resolution": [
        1400,
        2520
      ],
      "views": [
        [
          0,
          0,
          1400,
          2328
        ],
        [
          0,
          96,
          1400,
          2328
        ],
        [
          64,
          592,
          1336,
          1832
        ],
        [
          64,
          2124,
          1336,
          2200
        ],
        [
          0,
          928,
          1400,
          1496
        ],
        [
          0,
          928,
          1400,
          1208
        ],
        [
          0,
          1216,
          1400,
          1496
        ],
        [
          0,
          0,
          1400,
          96
        ]
      ]
    }
"""
rendering_parser = ParserPEG(grammar, "rendering")
rendering_tree = rendering_parser.parse(rendering_test)
rendering_result = visit_parse_tree(rendering_tree, IUIVisitor())

layout_test = ' { "screens": [' + ','.join([rendering_test, rendering_test, rendering_test]) + '], "id": "42" }'
layout_parser = ParserPEG(grammar, "layout")
layout_tree = layout_parser.parse(layout_test)
layout_result = visit_parse_tree(layout_tree, IUIVisitor())

with open('inferui/inferui.json', 'r') as data:
  iui_str = data.read()

def load_iui() -> List[Layout]:
  parser = ParserPEG(grammar, "layouts")
  parsed = parser.parse(iui_str)
  return visit_parse_tree(parsed, IUIVisitor())
