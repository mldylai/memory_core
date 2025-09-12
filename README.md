# Memory Core
An interactive voice/memory simulation.

### Dependencies
Run the following to setup dependencies:
```bash
eval $(poetry env activate) # activate poetry env
poetry install # install dependencies
```
### API Key
In the project folder, generate an .env file:
```bash
touch .env
```
in the .env file, write:
```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
save the file and run the following:
```bash
echo ".env" >> .gitignore
```
### Quick Start
In one terminal run:
```bash
cd memory_core/backend/app
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```
In another terminal run:
```bash
cd memory_core/frontend/public
python3 -m http.server 3000
```