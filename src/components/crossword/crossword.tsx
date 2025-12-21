import { Box, Heading, HStack, Stack, VStack, Text } from "@chakra-ui/react";
import React, {FC, useEffect, useRef, useState} from "react";
import { isWithStatement } from "typescript";

type Variable = {
  i: number;
  j: number;
  direction: "ACROSS" | "DOWN";
  length: number;
  word: string;
  clue: string;
};

type CrosswordResponse = {
  ok: boolean;
  width: number;
  height: number;
  structure?: boolean[][];
  letters?: (string | null)[][];
  variables?: Variable[];
  error?: string;
};

type Props = {
  wordsPath: string;
  apiBase?: string;
}

type CellNumber = {
  row: number;
  col: number;
  number: number;
  hasAcross: boolean;
  hasDown: boolean;
}

const CrosswordView: FC<Props> = ({ wordsPath, apiBase = ""}) => {
  const [puzzle, setPuzzle] = useState<CrosswordResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const [userGrid, setUserGrid] = useState<(string | null) [][]>([]);
  const [selectedCell, setSelectedCell] = useState<{row: number; col: number} | null>(null);
  const [direction, setDirection] = useState<"ACROSS" | "DOWN">("ACROSS");

  const inputRefs = useRef<{[key: string]: HTMLInputElement | null}>({});

  useEffect(() => {
    if (!wordsPath) return;
    setLoading(true);
    setError(null);
    fetch(`${apiBase}/generate`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ words: wordsPath})
    }).then(async (res) => {
      const json = (await res.json()) as CrosswordResponse;
      if (!json.ok) {
        setError(json.error || "failed to generate");
        setPuzzle(null);
      } else {
        setPuzzle(json)
        const emptyGrid = Array.from({length: json.height}, () => 
        Array(json.width).fill(null));
        setUserGrid(emptyGrid);
      }
    }).catch((e) => {
      setError(String(e));
    }).finally(() => setLoading(false));
  }, [wordsPath, apiBase]);

  if (loading) return <div>Loading crossword...</div>;
  if (error) return <div style={{color:"red"}}> Error: {error} </div>;
  if (!puzzle) return null;

  console.log(puzzle)

  const {width, height, structure, letters} = puzzle;

  const isWhite = (r: number, c: number): boolean => {
    if (structure && structure[r] && typeof structure[r][c] === "boolean") return !!structure[r][c];
    return !!(letters && letters[r] && letters[r][c]);
  }

  const cellNumbers: CellNumber[] = [];
  let num = 1;
  for (let r = 0; r < height; r++) {
    for (let c = 0; c < width; c++) {
      if (!isWhite(r, c)) continue;
      const isAcrossStart = (c === 0 || !isWhite(r, c - 1)) && c + 1 < width && isWhite(r, c + 1);
      const isDownStart = (r == 0 || !isWhite(r - 1, c)) && r + 1 < height && isWhite(r + 1, c);

      if (isAcrossStart || isDownStart) {
        cellNumbers.push({row: r, col: c, number: num, hasAcross: isAcrossStart, hasDown: isDownStart});
        num++;
      }
    }
  }

  // CLUES
  const acrossClues: {number: number; clue: string; answer: string}[] = [];
  const downClues: {number: number; clue: string; answer: string}[] = [];

  if (puzzle.variables) {
    puzzle.variables.forEach(v => {
      const cellNum = cellNumbers.find(cn => cn.row === v.i && cn.col === v.j);
      if (cellNum) {
        const clueObj = {
          number: cellNum.number,
          clue: v.clue || `(${v.length} letters)`,
          answer: v.word
        };
        if (v.direction === "ACROSS") {
          acrossClues.push(clueObj);
        } else {
          downClues.push(clueObj);
        }
      }
    })
  }


  const handleInputChange = (r: number, c: number, value: string) => {
    const upperValue = value.toUpperCase().slice(-1);

    const newGrid = userGrid.map(row => [...row]);
    newGrid[r][c] = upperValue || null;
    setUserGrid(newGrid);

    if (upperValue) {
      moveToNextCell(r, c);
    }
  }

  const handleCellClick = (r: number, c: number) => {
    if (!isWhite(r, c)) return;

    if (selectedCell && selectedCell.row === r && selectedCell.col === c) {
      setDirection(prev => prev == "ACROSS" ? "DOWN" : "ACROSS");
    } else {
      setSelectedCell({row: r, col: c});
    }

    const key= `${r}-${c}`;
    inputRefs.current[key]?.focus();
  }

  const handleKeyDown = (r: number, c: number, e: React.KeyboardEvent) => {
    if (e.key === "ArrowRight") {
      e.preventDefault();
      setDirection("ACROSS");
      moveInDirection(r, c, 0, 1);
    } else if ((e.key === "Backspace" && !userGrid[r][c]) || e.key == "ArrowLeft") {
      e.preventDefault();
      setDirection("ACROSS");
      moveInDirection(r, c, 0, -1);
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      setDirection("DOWN");
      moveInDirection(r, c, 1, 0);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setDirection("DOWN");
      moveInDirection(r, c, -1, 0);
    }
  }

  const getCellNumber = (r: number, c: number): number | null => {
    const cell = cellNumbers.find(cn => cn.row === r && cn.col === c);
    return cell ? cell.number : null;
  }

  const moveInDirection = (r: number, c: number, dr: number, dc: number) => {
    console.log("move in direction")
    let newR = r + dr;
    let newC = c + dc;
    while (newR >= 0 && newR < height && newC >= 0 && newC < width) {
      if (isWhite(newR, newC)) {
        console.log(`selection ${newC}`)
        setSelectedCell({row: newR, col: newC});
        setTimeout(() => {
          inputRefs.current[`${newR}-${newC}`]?.focus();
        }, 0)
        return;
      }
      newR += dr;
      newC += dc;
    }
  }

  const moveToNextCell = (r: number, c: number) => {
    console.log(`move to next cell ${direction}`)
    if  (direction === "ACROSS") {
      moveInDirection(r, c, 0, 1);
    } else {
      moveInDirection(r, c, 1, 0);
    }
  }

  const isInSelectedWord = (r: number, c: number): boolean => {
    if (!selectedCell) return false;

    if (direction === "ACROSS") {
      if (r !== selectedCell.row) return false;
      let start = selectedCell.col;
      while (start > 0 && isWhite(r, start - 1)) start--;
      let end = selectedCell.col;
      while (end < width - 1 && isWhite(r, end + 1)) end++;
      return c >= start && c <= end;
    } else {
      if (c !== selectedCell.col) return false;
      let start = selectedCell.row;
      while (start > 0 && isWhite(start - 1, c)) start--;
      let end = selectedCell.row;
      while (end < height - 1 && isWhite(end + 1, c)) end++;
      return r >= start && r <= end;
    }

  }

  const checkGrid = () => {
    let correct = 0;
    let total = 0;

    for (let r = 0; r < height; r++) {
      for (let c = 0; c < width; c++) {
        if (isWhite(r, c) && letters && letters[r][c]) {
          total++;
          if (userGrid[r][c] === letters[r][c]) {
            correct++;
          }
        }
      }
    }

    console.log(correct);
  }

  const revealAnswers = () => {
    if (letters) {
      setUserGrid(letters.map(row => [...row]));
    }
  }
  const CELL_SIZE = 40;
  const DARK_GREY = "#FFEB3B";
  const LIGHT_GREY = "#E3F2FD";

  return (
    <Stack>
      <HStack>
        <Box>
          <div style={{display: "grid", gridTemplateColumns: `repeat(${width}, ${CELL_SIZE}px)`, gap:0}}>
            {Array.from({length: height}).flatMap((_, r) => 
              Array.from({length: width}).map((_, c) => {
                const white = isWhite(r, c);
                const isSelected = selectedCell?.row === r && selectedCell?.col === c;
                const inWord = isInSelectedWord(r, c);
                const cellNum = getCellNumber(r, c);
                const key = `${r}-${c}`;

                return (
                  <div key={key} onClick={() => handleCellClick(r, c)} style={{width: CELL_SIZE, height: CELL_SIZE, background: white ?
                    (isSelected ? DARK_GREY : inWord ? LIGHT_GREY : "#fff") : "#000",
                    border: white? "1px solid #000" : "none",
                    position: "relative",
                    cursor: white ? "pointer" : "default"
                  }}>
                    {white && cellNum && (
                      <span style={{position: "absolute", top: 1, left: 2, fontSize: 10, fontWeight: 700}}>
                        {cellNum}
                      </span>
                    )}
                    {white && (
                      <input ref={(el) => (inputRefs.current[key] = el)}
                      type="text" maxLength={1} value={userGrid[r]?.[c] || ""}
                      onChange={(e) => handleInputChange(r, c, e.target.value)}
                      onKeyDown={(e) => handleKeyDown(r, c, e)}
                      onClick={() => handleCellClick(r, c)}
                      style={{
                        width: "100%",
                        height: "100%",
                        border: "none",
                        textAlign: "center",
                        textTransform: "uppercase",
                        background: "transparent"
                      }}/>
                    )}


                  </div>

                )

              }))
            }
          </div>
        </Box>

        <VStack>
          <Box>
            <Heading size="sm" mb={2}>Across</Heading>
            {acrossClues.sort((a, b) => a.number - b.number).map(c => (
              <Text key={`across-${c.number}`} fontSize="sm" mb={1}>
                <strong>{c.number}.</strong> {c.clue}
              </Text>
            ))}
          </Box>

          <Box>
            <Heading size="sm" mb={2}>Down</Heading>
            {downClues.sort((a, b) => a.number - b.number).map(c => (
              <Text key={`down-${c.number}`} fontSize="sm" mb={1}>
                <strong>{c.number}.</strong> {c.clue}
              </Text>
            ))}
          </Box>
        </VStack>
      </HStack>

    </Stack>
  )

};

export default CrosswordView;

