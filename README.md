# SRTCreator

Upload audio files and get word-by-word SRT subtitle files using AssemblyAI. This is for Mike.

## Setup

### 1. Clone repo

```bash
git clone https://github.com/CLopez021/SRTCreator.git
```

### 2. Install uv

macOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows:
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. Configure API key

Add your API key to the `.env-example` file:
```bash
ASSEMBLY_AI_API_KEY=your_api_key_here
```
Get your API key from [AssemblyAI](https://www.assemblyai.com/).

### 4. Change the name of `.env-example` to `.env`

## 5. Run

```bash
uv run src/backend/main.py
```

Open http://localhost:8000 in your browser.

## Usage

1. Drag and drop an audio/video file
2. Click "Transcribe Audio"
3. Download the generated SRT file

The SRT file contains word-by-word captions with precise timestamps.

