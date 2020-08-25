from .ast import *
from .parse import load_iui
import numpy as np

def iui_stats():
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