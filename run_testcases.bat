@echo off
setlocal ENABLEDELAYEDEXPANSION

REM Build (requires make on PATH or adjust to MSVC)
make all || exit /b 1

set OUTDIR=out
if not exist "%OUTDIR%" mkdir "%OUTDIR%"

set REPORT=testcases_run_summary.md
echo # Testcases Run Summary> "%REPORT%"
echo.>> "%REPORT%"

set /a pass=0
set /a fail=0

for /r testcases %%F in (*_inputs.csv) do (
  REM Derive SCR dir and case base
  set "INCSV=%%F"
  for %%I in ("%%F") do set "DIR=%%~dpI"
  for %%I in ("%%F") do set "NAME=%%~nI"
  set "CASEBASE=!NAME:_inputs=!"
  set "GOLDEN=!DIR!!CASEBASE!_golden.csv"
  set "OUT=%OUTDIR%\!CASEBASE!_out.csv"

  echo === Running !DIR!!CASEBASE! ===

  if not exist "!GOLDEN!" (
    echo - !DIR!!CASEBASE!: MISSING GOLDEN>> "%REPORT%"
    set /a fail+=1
  ) else (
    build\ecu_app "!INCSV!" "!OUT!"
    python tools\compare_csv.py --out "!OUT!" --golden "!GOLDEN!"
    if "!ERRORLEVEL!"=="0" (
      echo - !DIR!!CASEBASE!: PASS>> "%REPORT%"
      set /a pass+=1
    ) else (
      echo - !DIR!!CASEBASE!: FAIL>> "%REPORT%"
      set /a fail+=1
    )
  )
)

echo.>> "%REPORT%"
echo passed: %pass%>> "%REPORT%"
echo failed: %fail%>> "%REPORT%"

echo Completed. Summary in %REPORT% (passed: %pass%, failed: %fail%)
endlocal
