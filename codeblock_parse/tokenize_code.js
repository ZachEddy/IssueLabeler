const {Document} = require('tree-sitter');
const js = require('tree-sitter-ruby')

// const code = process.argv[2]
// document.setLanguage(require('tree-sitter-javascript'));
// document.setInputString(code);
// document.parse();
// tokenizeTree(document.rootNode);

var parsedJSON = require('../codeblocks');
var codeblockList = parsedJSON.codeblocks
// console.log(codeblockList[2798]


// const document = new Document();
// const codeblock = codeblockList[3483][0]
// console.log(codeblock);
// document.setLanguage(require('tree-sitter-ruby'));
// document.setInputString(codeblock);
// try {
//   document.parse();
// }catch(err){
//   console.log("fsddfs");
// }
// tokes = tokenizeTree(document.rootNode, codeblock);
// console.log(tokes);

for(var i = 2500; i < codeblockList.length; i++) {
  codeblocks = codeblockList[i]
  for(var j = 0; j < codeblocks.length; j++) {
    codeblock = codeblocks[j]
    var document = new Document();
    console.log(codeblock);
    document.setInputString(codeblock)
    document.setLanguage(js);
    document.parse();
    codeblocks[j] = tokenizeTree(document.rootNode, codeblock)
    // console.log(codeblocks[j]);
  }
  console.log(i);
}

function tokenizeTree(root, code) {
  if(root == null) {
    return;
  }
  tokens = []
  nodeStack = [root]
  while(nodeStack.length != 0) {
    var node = nodeStack.pop();
    if(isLeaf(node)) {
      if(node.isNamed) {
        tokens.push(tokenizeNode(node, code));
      }
    } else {
      children = node.children;
      for(var i = 0; i < children.length; i++) {
        nodeStack.push(children[i]);
      }
    }
  }
  return tokens
}

function isLeaf(node) {
  return node.children.length == 0;
}

function tokenizeNode(node, code) {
  return code.substring(node.startIndex, node.endIndex);
}