@echo off
REM -----------------------------
REM Run PyTorch Docker container
REM -----------------------------

echo ===============================================
echo   Environnement PyTorch - Demarrage
echo ===============================================
echo.

echo [1/3] Chargement de l'image Docker depuis pytorch_image.tar...
echo       (cela peut prendre plusieurs minutes, ne fermez pas cette fenetre)
docker load -i pytorch_image.tar
if errorlevel 1 (
    echo.
    echo [ERREUR] Echec du chargement de l'image Docker.
    echo          Verifiez que Docker Desktop est bien demarre.
    echo.
    pause
    exit /b 1
)
echo       Image chargee avec succes.
echo.

echo [2/3] Preparation du dossier de travail (volume)...
set "VOLUME=%~dp0volume"
if not exist "%VOLUME%" (
    mkdir "%VOLUME%"
    echo       Dossier "volume" cree.
) else (
    echo       Dossier "volume" deja present.
)
REM Convert Windows path to Docker-friendly format (forward slashes)
set "DOCKER_VOLUME=%VOLUME:\=/%"
echo.

echo [3/3] Lancement du conteneur pytorch2...
REM 8889 = Jupyter, 11434 = Ollama, 8080 = Open-WebUI
docker run -dit --name pytorch2 ^
  -p 8889:8889 -p 11434:11434 -p 8080:8080 ^
  -v "%DOCKER_VOLUME%:/workdir/volume" ^
  pytorch:latest
if errorlevel 1 (
    echo.
    echo [ERREUR] Le conteneur n'a pas pu demarrer.
    echo          Il existe peut-etre deja un conteneur nomme "pytorch2".
    echo          Supprimez-le avec :  docker rm -f pytorch2
    echo.
    pause
    exit /b 1
)
echo.

echo ===============================================
echo   Conteneur demarre !
echo ===============================================
echo.
echo   Patientez 1 a 2 minutes le temps que les services
echo   se lancent (Ollama, Open-WebUI, Jupyter), puis ouvrez :
echo.
echo     - Jupyter Notebook : http://localhost:8889
echo     - Open-WebUI       : http://localhost:8080
echo     - Ollama (API)     : http://localhost:11434
echo.
echo   Pour suivre le demarrage des services :
echo     docker logs -f pytorch2
echo.
echo ===============================================
echo.
echo Appuyez sur une touche pour fermer cette fenetre...
pause >nul
