export function range(start, stop, step=1) {
  if (stop === undefined) {
    stop = start;
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
