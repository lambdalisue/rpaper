import * as list from '../list';


describe('range', () => {
  it('it returns [0, 1, 2, 3, 4] for range(5)', () => {
    let result = list.range(5);
    expect(result).toEqual([0, 1, 2, 3, 4]);
  });
});

describe('sum', () => {
  it('it returns 10 for sum([0, 1, 2, 3, 4])', () => {
    let result = list.sum([0, 1, 2, 3, 4]);
    expect(result).toEqual(10);
  });
});
