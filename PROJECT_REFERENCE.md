# Project Reference - Dictionary using API

## Original Project Functionality (Backend Logic)
This project is a Python dictionary application that uses the public API:
`https://api.dictionaryapi.dev/api/v2/entries/en/<word>`

### Core features preserved
1. Search a word and fetch:
   - Definitions with part of speech
   - Synonyms
   - Antonyms
2. Save every successful searched word to history (`word_history.txt`)
3. View full search history
4. Clear search history
5. Error logging to `dictionary.log`
6. Text-to-speech and voice input support in desktop UI (original Tkinter app)

## Current Folder Architecture
- `backend/`
  - `Dictionary_.py` (original Tkinter desktop app logic/UI preserved)
  - `dictionary_service.py` (shared backend dictionary logic for API)
  - `api.py` (Flask API for frontend consumption)
  - `requirements.txt`
  - `word_history.txt`
- `frontend/`
  - React + Vite UI
  - Calls backend endpoints for search/history/clear history

## Backend API Contract
### `GET /api/health`
Response:
```json
{ "status": "ok" }
```

### `GET /api/search?word=<term>`
Response:
```json
{ "word": "<term>", "result": "<formatted dictionary text>" }
```

### `GET /api/history`
Response:
```json
{ "history": ["word1", "word2"] }
```

### `DELETE /api/history`
Response:
```json
{ "message": "Search history cleared successfully!" }
```

## Frontend Functionality (React)
1. Search input + search button
2. Displays dictionary result text
3. Speak/Stop (browser speech synthesis)
4. Voice input (browser speech recognition, if supported)
5. Shows search history from backend
6. Clears history using backend API

## Run Instructions
### Backend
```bash
cd backend
pip install -r requirements.txt
python api.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Then open `http://localhost:5173`.
