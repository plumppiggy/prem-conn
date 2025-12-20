import React, {FC, useEffect, useState} from "react";

type Variable = {
  i: number;
  j: number;
  direction: "ACROSS" | "DOWN";
  length: number;
  word: string;
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
  structurePath: string;
  wordsPath: string;
  apiBase?: string;
}

const CrosswordView: FC<Props> = ({structurePath, wordsPath, apiBase = ""}) => {
  const [puzzle, setPuzzle] = useState<CrosswordResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!structurePath || !wordsPath) return;
    setLoading(true);
    setError(null);
    fetch(`${apiBase}/generate`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({structure: structurePath, words: wordsPath})
    }).then(async (res) => {
      const json = (await res.json()) as CrosswordResponse;
      if (!json.ok) {
        setError(json.error || "failed to generate");
        setPuzzle(null);
      } else {
        setPuzzle(json)
      }
    }).catch((e) => {
      setError(String(e));
    }).finally(() => setLoading(false));
  }, [structurePath, wordsPath, apiBase]);

  if (loading) return <div>Loading crossword...</div>;
  if (error) return <div style={{color:"red"}}> Error: {error} </div>;
  if (!puzzle) return null;

  return (
    <div>
      Hello
    </div>
  )

};

export default CrosswordView;

