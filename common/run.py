from dataclasses import dataclass
from dataclasses_json import dataclass_json
from subprocess import run

from typing import List
from enum import Enum

@dataclass_json
@dataclass 
class View:
  name: str
  rect: List[float]
  children: List[View]


  def validate():
    assert len(rect) == 4
    for c in children:
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

  def format_cli() -> str:
    return "%.2f %.2f %.2f %.2f" % (wlo, hlo, whi, hhi)

@dataclass
class MockRun:
  timeout: int
  loc_type: LocalType
  glob_type: GlobalType
  glob_spec: GlobalSpec
  examples: List[View]
  input_fname: str
  output_fname: str

  def gen_run_cmd(self) -> (str, List[str]):
    prefix = 'mockdown run'
    opts = ['-pb', self.wlo, self.hlo, self.whi, self.hhi, '-pm', self.glob_type, '--timeout', str(self.timeout), '--learning-method', self.loc_type, input_fname, output_fname]
    return (prefix, opts)

  def write_to_input(self):
    with open(self.input_fname, 'w') as ifile:
      print('{ "examples": ')


def run_bench(parent: BenchSchema, local: FocusSchema, timeout: int = timeout_length):
  with open('benches.json') as script_file:
    script_config = json.load(script_file)
  p_key, local_key = parent.script_key, local.script_key

  print(f"Running bench {p_key}, {local_key}")

  script_data = script_config[p_key][local_key]
  if 'width' in script_data and 'height' in script_data:
    with open(output_dir + 'bench-%s.log' % local.script_key, 'w') as bench_out:
      run(['./bench.sh', p_key, local_key, 'hier', '--timeout', str(timeout), '--loclearn', 'bayesian'], stdout=bench_out, stderr=bench_out)
    print(f"Finished.")
    return parse_result_from_file(output_dir + 'bench-%s.log' % local.script_key, local.script_key)
  else:
    print('error: bad auto-mock script entry')
    print(parent)
    print(local)
    raise Exception()