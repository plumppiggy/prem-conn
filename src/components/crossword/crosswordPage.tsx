import CrosswordView from "./crossword";

export default function CrosswordPage() {
  return (
    <CrosswordView wordsPath="data/words2-filled.txt" apiBase="http://localhost:8801"/>
  );
}