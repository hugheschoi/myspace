function mergeArr(arr) {
  return arr.reduce((list, subList) => {
      const set = list.find(set => {
          return subList.some(str => set.has(str));
      });
      if (set) {
          subList.forEach(set.add.bind(set))
      } else {
          list.push(new Set(subList));
      }
      return list;
  }, []).map(set => [...set]);
}

const arr = [
  ['a','b','c'],
  ['a','d'],
  ['d','e'],
  ['f','g'],
  ['h','g'],
  ['i'],
];

console.log(mergeArr(arr));
