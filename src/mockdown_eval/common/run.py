from __future__ import annotations
from timeit import timeit


from dataclasses import dataclass
from dataclasses_json import dataclass_json
from subprocess import run

from typing import List, Tuple
from enum import Enum

import json

@dataclass_json
@dataclass 
class View:
  name: str
  rect: List[float]
  children: List[View]


  def validate(self):
    assert len(self.rect) == 4
    for c in self.children:
      c.validate()

class LocalType(Enum):
  SIMPLE = "simple"
  BAYESIAN = "noisetolerant"

class GlobalType(Enum):
  NONE = "none"
  FLAT = "baseline"
  HIER = "hierarchical"

@dataclass
class GlobalSpec:
  hlo: float
  hhi: float
  wlo: float
  whi: float

  def format_cli(self) -> str:
    return "%.2f %.2f %.2f %.2f" % (self.wlo, self.hlo, self.whi, self.hhi)

@dataclass
class MockRun:
  timeout: int
  loc_type: LocalType
  glob_type: GlobalType
  glob_spec: GlobalSpec
  examples: List[View]
  input_fname: str
  output_fname: str

  def gen_run_cmd(self) -> Tuple[str, List[str]]:
    prefix = 'mockdown run'
    path_prefix = '../mockdown-inferui-eval/'
    opts = [str(x) for x in ['-pb', self.glob_spec.wlo, self.glob_spec.hlo, self.glob_spec.whi, self.glob_spec.hhi, '-pm', self.glob_type.value, '--learning-method', self.loc_type.value, path_prefix + self.input_fname, path_prefix + self.output_fname]]
    return (prefix, opts)

  def write_to_input(self):
    with open(self.input_fname, 'w') as ifile:
      examples_str = json.JSONEncoder().encode([x.to_dict() for x in self.examples])
      print('{ "examples": ' + examples_str + '}', file=ifile)

  def make_runner(self):

    with open('tmp/runner.sh', 'w') as runner:
      print('#!/bin/sh', file=runner)
      print('', file=runner)
      print('export PIPENV_PIPFILE=../mockdown/Pipfile', file=runner)
      print('LOGLEVEL=INFO', file=runner)
      pref, opts = self.gen_run_cmd()
      print(*['timeout', str(self.timeout), 'pipenv run --', pref, *opts], file=runner)

  def run_cmd(self): 
    self.write_to_input()
    self.make_runner()
    return timeit(lambda : run('tmp/runner.sh'), number=1)
