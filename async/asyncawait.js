let fs = require('fs');
function readFile(filename) {
  return new Promise(function (resolve, reject) {
    fs.readFile(filename, 'utf8', function (err, data) {
      if (err)
        reject(err);
      else
        resolve(data);
    })
  })
}

// function co(gen) {
//   let it = gen();
//   return new Promise(function (resolve, reject) {
//     !function next(lastVal) {
//       let {value, done} = it.next(lastVal);
//       if (done) {
//         resolve(value);
//       } else {
//         value.then(next, reason => reject(reason));
//       }
//     }();
//   });
// }
function read(){
  return co(function*() {
    let template = yield readFile('./asset/template.txt');
    let data = yield readFile('./asset/data.txt');
    return template + '+' + data;
  });
}
const asyncFunc = read();
asyncFunc.then(res => {
  console.log(res);
});

function co(gen) {
  const it = gen();
  return new Promise((resolve, reject) => {
    (function next(lastVal) {
      const { done, value } = it.next(lastVal);
      if (done) {
        resolve(value);
      } else {
        value.then(next, reason => reject(reason));
      }
    })();
  });
}
