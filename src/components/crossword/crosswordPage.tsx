import CrosswordView from "./crossword";

export default function CrosswordPage() {
  return (
    <CrosswordView structurePath="data/structure0.txt" wordsPath="data/words0.txt" cluesPath="data/clues.json" apiBase="http://localhost:8801"/>
  );
}