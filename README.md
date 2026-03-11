# AQI Forecast (Streamlit)

Simple Streamlit app that fetches PM2.5 estimates and forecasts AQI using Prophet.

## Prerequisites
- Python 3.8+ (3.10 recommended)
- Git (optional)

Note: On Windows, installing `prophet` can require a compiler or `conda` prebuilt packages. See the Troubleshooting section below.

## Create virtual environment (Windows — PowerShell)

```powershell
python -m venv .venv
\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

## Create virtual environment (Windows — CMD)

```cmd
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

## Run the app (Streamlit)

From the project root (with the venv activated):

```powershell
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

Alternatively (explicit venv), run:

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

## Stop the app
- In the terminal where Streamlit is running press `Ctrl+C`.

## Troubleshooting
- If `pip install -r requirements.txt` fails on `prophet`, try one of:
  - Use conda (recommended on Windows):

```bash
conda create -n aqi python=3.10
conda activate aqi
conda install -c conda-forge prophet
pip install -r requirements.txt  # install remaining packages
```

  - Or install prerequisites before `prophet`:

```powershell
python -m pip install wheel setuptools cython
python -m pip install pystan==2.19.1.1
python -m pip install prophet
```

- If PowerShell blocks script activation, enable it for the current user:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## Files
- `app.py`: Streamlit application entrypoint
- `requirements.txt`: Python dependencies

## Next steps
- If you want, I can:
  - Confirm the Streamlit background process logs and print the terminal output.
  - Modify `requirements.txt` to prefer `conda`-friendly packages.

--


