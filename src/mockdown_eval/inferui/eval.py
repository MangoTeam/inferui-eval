from .ast import *
from .parse import load_iui
import numpy as np
from ..common.run import *

from yaml import safe_load
from pathlib import Path

def summary_stats():
  layouts = load_iui()
  sizes = np.array([len(l.renderings[0].boxes) for l in layouts])
  print('Total & Mean & Median & 25 & 75')
  total = len(layouts)
  mean = np.mean(sizes)
  median = np.median(sizes)
  lower = np.quantile(sizes, 0.25)
  upper = np.quantile(sizes, 0.75)
  outstr = ' & '.join([str(x) for x in [total, mean, median, lower, upper]])
  print(outstr)


def rend_to_gspec(x: List[Rendering]) -> GlobalSpec:
  heights = [rend.resolution.height for rend in x]
  widths = [rend.resolution.height for rend in x]

  return GlobalSpec(min(heights), max(heights), min(widths), max(widths))



def IUI2Mock(x: Layout, num_examples: int = 2) -> Tuple[MockRun, View]:
  x.validate()

  if num_examples > len(x.renderings) - 1:
    print('warning: training example included in IUI experiment')
  
  timeout = 60
  loc_type = LocalType.BAYESIAN
  glob_type = GlobalType.HIER
  glob_spec = rend_to_gspec(x.renderings)

  examples = [rend.to_view() for rend in x.renderings]

  inp_fname = 'tmp/' + str(x.id) + "_input.json"
  out_fname = 'tmp/' + str(x.id) + "_output.json"

  return MockRun(timeout, loc_type, glob_type, glob_spec, examples[0:num_examples], inp_fname, out_fname), examples[-1]


def formatMR(test: View, id: int, mr: MockRun, synth_time: float) -> str:
  encoding_fname = 'tmp/automock.json'

  # if 'output_fname' in mr:
  Path(mr.output_fname).touch()
  with open(mr.output_fname, 'r') as constraint_file:
    # print(constraint_file.readlines())
    # constraint_file.
    if len(constraint_file.readlines()) > 0:
      constraint_file.seek(0)
      automock_obj = json.load(constraint_file)
      automock_obj['timeout'] = False
    else:
      automock_obj = {"timeout": True, "constraints": []}


    automock_obj['example'] = test.to_dict()
    automock_obj['synthTime'] = synth_time
    automock_obj['id'] = id

    # print('encoding: ')
    # print(automock_obj)
  
    
  with open(encoding_fname, 'w') as inter_file:
    # inter_file.
    print(json.JSONEncoder().encode(automock_obj), file=inter_file)

  return encoding_fname

def run_automock_iui(automock_json_path: str):
  result = run(['npm', 'run-script', '--prefix', '../auto-mock', 'iui', '--', '--path', '../mockdown-inferui-eval/' + automock_json_path], capture_output=True, universal_newlines=True)
  # print('automock iui output:')
  # print(result.stdout)
  # return safe_load(' '.join(result.stdout.split('\n')[4:-1]))


# currently not used
def evaluate_summary(x): 

  values = x.items()
  total = len(values)
  correct = 0
  for id, result in values:
    if result['timeout']:
      continue

    if result['accuracy'] == 1:
      correct += 1

  print('correct', correct)
  print('total', total)


def main(): 
  layouts = load_iui()
  results = {}

  for layout in layouts:
    print('starting layout', layout.id)
    mock_run, test_example = IUI2Mock(layout, 1)
    synth_time = mock_run.run_cmd()
    auto_json = formatMR(test_example, layout.id, mock_run, synth_time)
    # auto_json = 'tmp/automock.json'
    results[layout.id] = run_automock_iui(auto_json)

  print('finished!')

  # evaluate_summary(results)
  
  with open('tmp/aggregate_results.json', 'w') as aggregates:
    print(json.JSONEncoder().encode(results), file=aggregates)

if __name__ == "__main__":
  main()
