export type Group = {
  category: string;
  items: string[];
  difficulty: 1 | 2 | 3 | 4;
}

export type Options = {
  groups: Group[];
}

export type State = {
  complete: Group[];
  incomplete: Group[];
  items: string[];
  activeItems: string[];
  mistakes: number;
  wiggleItems: string[];
}

export const difficultyColours = (difficulty: 1 | 2 | 3 | 4): string => {
  return {
    1 : '#f0da4d',
    2 : '#4df05a',
    3 : '#427bf5',
    4 : '#8e4df0',
  }[difficulty];
};

export const chunk = <T, >(list: T[], size: number): T[][] => {
  const chunkCount = Math.ceil(list.length / size);
  return new Array(chunkCount).fill(null).map((_c: null, i: number) => {
    return list.slice(i * size, i * size + size);
  })
};

export const shuffle = <T,>(list: T[]): T[] => {
  return list.sort(() => 0.5 - Math.random());
};





