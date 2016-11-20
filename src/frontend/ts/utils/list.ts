export function range(start: number, stop?: number, step: number=1): Array<number> {
  if (stop === undefined) {
    stop = start - 1;
    start = 0;
  }
  if (start === undefined) {
    throw new TypeError("'start' argument is required.");
  }
  let size = (stop - start) / step;
  let arr = new Array(size);
  let i = 0;
  while (start <= stop) {
    arr[i++] = start;
    start += step;
  }
  return arr;
}

export function sum<T extends string | number>(arr: Array<T>): T;
export function sum(arr) {
    return arr.reduce(function(prev, current, i, arr) {
        return prev+current;
    });
}
