from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import os
import glob

import uvicorn
import json 
import random

from crossword import *
from generate import CrosswordCreator

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

class CrosswordGenerateRequest(BaseModel):
 words: str
 output: Optional[str] = None

STRUCTURES_DIR = "structures"
CLUES_FILE = "data/words2_clues.json"

CACHE_DIR = "crossword_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def get_files(directory: str, pattern: str) -> list:
  pattern = os.path.join(directory, pattern)
  files = sorted(glob.glob(pattern))
  return files

def get_structure():
  structures = get_files("data/structures", "*.txt")
  idx = datetime.now().weekday() % len(structures)
  return structures[idx]

def get_seed() -> int: 
  today = datetime.now().strftime("%Y%m%d")
  return int(today)

def get_cache_path(seed: int) -> str:
  return os.path.join(CACHE_DIR, f"crossword_{seed}.json")

def load_from_cache(seed: int) -> Optional[Dict[str, Any]]:
  path = get_cache_path(seed)
  if os.path.exists(path):
    with open(path) as f:
      return json.load(f)
  return None

def save_to_cache(seed: int, data: Dict[str, Any]) -> None:
  seed = get_seed()
  cached = get_cache_path(seed)
  with open(cached, "w") as f:
    json.dump(data, f)



@app.post("/generate")
def generate(req: CrosswordGenerateRequest) -> Dict[str, Any]:
  seed = get_seed()
  # cached = load_from_cache(seed)
  # if cached is not None:
  #   return cached

  structure = get_structure()
  
  random.seed(seed)
  try: 
    cw = Crossword(structure, req.words)
    creator = CrosswordCreator(cw)
    assignment = creator.solve()
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
  if assignment is None:
    return {"ok": False, "error": "no solution"}
  
  clue_map: Dict[str, str] = {}
  try: 
    with open(CLUES_FILE) as f:
      clue_map = json.load(f)
      clue_map = {k.upper(): v for k, v in clue_map.items()}
  except Exception as e:
    print(f"Warning: could not load clues from {CLUES_FILE}: {e}")

  letters = creator.letter_grid(assignment)

  vars = []
  for var, word in assignment.items():
    vars.append({
      "i": var.i,
      "j": var.j,
      "direction": "DOWN" if var.direction == var.DOWN else "ACROSS",
      "length": var.length,
      "word": word,
      "clue": clue_map.get(word.upper(), f"Clue not found Lol, try ur best xoxo {word}")
    })

  puzzle = {
    "ok": True,
    "width": cw.width,
    "height": cw.height,
    "structure": cw.structure,
    "letters": letters,
    "variables": vars
  }

  save_to_cache(seed, puzzle)

  return puzzle

if __name__ == "__main__":
  uvicorn.run(app, host="127.0.0.1", port=8801, reload=True)

