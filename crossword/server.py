from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any

import uvicorn
import json 

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
 structure: str
 words: str
 output: Optional[str] = None

@app.post("/generate")
def generate(req: CrosswordGenerateRequest) -> Dict[str, Any]:
  try: 
    cw = Crossword(req.structure, req.words)
    creator = CrosswordCreator(cw)
    assignment = creator.solve()
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
  if assignment is None:
    return {"ok": False, "error": "no solution"}

  letters = creator.letter_grid(assignment)

  vars = []
  for var, word in assignment.items():
    vars.append({
      "i": var.i,
      "j": var.j,
      "direction": "DOWN" if var.direction == var.DOWN else "ACROSS",
      "length": var.length,
      "word": word
    })

  return {
    "ok": True,
    "width": cw.width,
    "height": cw.height,
    "structure": cw.structure,
    "letters": letters,
    "variables": vars
  }

if __name__ == "__main__":
  uvicorn.run(app, host="127.0.0.1", port=8801, reload=True)

