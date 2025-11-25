import { useMemo, useState } from "react";

export type MethodsMap = Record<string, (...args: any[]) => any>;

export default function useMethods<S extends Record<string, any>, M extends MethodsMap>(
  factory: (s: S) => M,
  initialState: S
): [S, M] {
  const [state, setState] = useState<S>(initialState);

  const methods = useMemo(() => {
    const sample = factory(initialState);
    const names = Object.keys(sample);
    const bound = {} as M;

    for (const name of names) {
      (bound as any)[name] = (...args: any[]) => {
        setState(prev => {
          const draft = JSON.parse(JSON.stringify(prev)) as S;
          const fns = factory(draft);
          ;(fns as any)[name](...args);
          return draft;
        });
      };
    }
    return bound;
  }, [factory, initialState]);

  return [state, methods];
}