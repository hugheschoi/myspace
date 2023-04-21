const digits = [9];
var plusOne = function(digits) {
  const n = digits.length;
  for(let i = n - 1; i >=0; i--) {
      if (digits[i] === 9) {
          digits[i] = 0;
      } else {
          digits[i] += 1
          return digits;
      }    
  }
  digits.unshift(1);
  return digits;
};

plusOne(digits)
console.log(digits);