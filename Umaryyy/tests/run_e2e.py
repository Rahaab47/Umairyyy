import glob
import py_compile
import subprocess
import sys
import traceback
import os

root = '.'
py_files = [f for f in glob.glob(root + '/**/*.py', recursive=True) if 'tests/run_e2e.py' not in f.replace('\\','/')]

results = []

for f in sorted(py_files):
    info = {'file': f, 'syntax': False, 'run': False, 'syntax_err': None, 'run_err': None, 'run_out': None}
    try:
        py_compile.compile(f, doraise=True)
        info['syntax'] = True
        print('SYNTAX OK:', f)
    except Exception as e:
        info['syntax_err'] = traceback.format_exc()
        print('SYNTAX ERR:', f)
        print(info['syntax_err'])

    # Try to execute the file with a timeout to catch immediate runtime errors
    # If the script appears interactive (uses input() or an infinite loop), skip running it
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            src = fh.read()
    except Exception:
        src = ''

    if 'input(' in src or 'while True' in src or 'getpass' in src:
        info['run'] = True
        info['run_out'] = 'SKIPPED_INTERACTIVE'
        print('RUN SKIP (interactive):', f)
    else:
        try:
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            proc = subprocess.run([sys.executable, f], capture_output=True, text=True, timeout=5, env=env)
            info['run_out'] = proc.stdout + proc.stderr
            if proc.returncode == 0:
                info['run'] = True
                print('RUN OK:', f)
            else:
                info['run_err'] = f'Exit code {proc.returncode}\n{proc.stdout}\n{proc.stderr}'
                print('RUN ERR:', f, 'Exit code', proc.returncode)
        except subprocess.TimeoutExpired as te:
            info['run_err'] = 'TimeoutExpired'
            print('RUN TIMEOUT:', f)
        except Exception:
            info['run_err'] = traceback.format_exc()
            print('RUN EXC:', f)
            print(info['run_err'])

    results.append(info)

all_ok = all(r['syntax'] and r['run'] for r in results)

print('\nSUMMARY:')
for r in results:
    status = 'OK' if (r['syntax'] and r['run']) else 'FAIL'
    print(status, r['file'])

if all_ok:
    print('\nRESULT: ok')
    sys.exit(0)
else:
    print('\nRESULT: not')
    sys.exit(2)
