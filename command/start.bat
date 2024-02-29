@echo off
cd C:\projetos\Projeto_Oficial_Dashboard_v3
start /B cmd /c "C:\projetos\Projeto_Oficial_Dashboard_v3\venv\Scripts\activate.bat && waitress-serve --host=10.155.0.239 --port=80 app:app"
timeout /nobreak /t 10 >nul