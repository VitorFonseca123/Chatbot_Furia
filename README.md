# Configurar ambiente
pip install virtualenv
python -m venv venv
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
venv\Scripts\activate
pip install -r requirements.txt
