import CrosswordView from "./crossword";

export default function CrosswordPage() {
  return (
    <CrosswordView structurePath="data/structure0.txt" wordsPath="data/words0.txt" apiBase="http://localhost:8801"/>
  );
}