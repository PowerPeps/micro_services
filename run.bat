@echo off

echo ================================================
echo  == Lancement des Microservices et du Client ==
echo ================================================

:: Lancer le microservice des stocks
start cmd /k "python microservice_stocks.py"

:: Lancer le microservice des emprunts
start cmd /k "python microservice_emprunts.py"

:: Lancer le microservice des retours
start cmd /k "python microservice_retours.py"

:: Lancer l'API
start cmd /k "python ui_api.py"

:: Lancer l'interface client
:: start cmd /k "python interface_client.py"

echo Tous les services ont été démarrés dans des terminaux distincts.
pause