// let fs = require('fs');
// let EventEmitter = require('events');
// let eve = new EventEmitter();
// let html = {};
// eve.on('ready',function(key,value){
//   html[key] = value;
//   if(Object.keys(html).length==2){
//     console.log(html);
//   }
// });
// function render(){
//   fs.readFile('template.txt','utf8',function(err,template){
//     eve.emit('ready','template',template);
//   })
//   fs.readFile('data.txt','utf8',function(err,data){
//     eve.emit('ready','data',data);
//   })
// }
// render();

let fs = require('fs');

let after = function(times,callback){
  let result = {};
  return function(key,value){
    result[key] = value;
    if(Object.keys(result).length==times){
      callback(result);
    }
  }
}
let done = after(2,function(result){
  console.log(result);
});

function render(){
  fs.readFile('template.txt','utf8',function(err,template){
    done('template',template);
  })
  fs.readFile('data.txt','utf8',function(err,data){
    done('data',data);
  })
}
render();