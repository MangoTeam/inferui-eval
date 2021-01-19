This evaluation assumes that `mockdown` and `auto-mock` are a level above this root (i.e. at `..`).
Also, it uses a `tmp/` directory for temporary files and saves the directory in version control
with a `.gitignore` file.

To run:

1. `pipenv shell`
2.  python3 -c "from  src.mockdown_eval.inferui.eval import main; main()"

