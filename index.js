const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");

const folderPath = "MESH 2021";

const readTileSet = (filePath) => {
  return new Promise((resolve, reject) => {
    fs.readFile(filePath, "utf8", (err, data) => {
      if (err) {
        reject(err);
        return;
      }

      resolve(data);
    });
  });
};

const processTileset = (tilesset) => {
  const { root, children } = tilesset;
  const newTransform = [];
  const newChildren
  if (root.transform) {
    console.log("convert", root.transform);
    newTransform.push(1, 2, 3, 4);
    tilesset.transform = newTransform;
  }
  tilesset.children = children?.map(({ child }) => {
    
  })

  return { tilesset, wasConverted: !!newTransform.length };
};

const replaceFile = (filePath, tileset) => {
  console.log({ filePath, tileset });
};

const processRecursive = (filePath) => {
  console.log(`Processing ${filePath}`);
  readTileSet(filePath)
    .then((data) => JSON.parse(data))
    .then(processTileset)
    .then(({ wasConverted, tilesset }) => {
      if (wasConverted) {
        replaceFile(filePath, tilesset);
      }
      tilesset.root.children
        ?.map(({ content }) => content.uri)
        .filter((uri) => uri?.endsWith(".json"))
        .forEach((uri) => {
          const dirname = path.dirname(filePath);
          const nextPath = path.resolve(dirname, uri);
          console.log(`processRecursive(${nextPath})`);
          processRecursive(nextPath);
        });
    });
};

processRecursive(`${folderPath}/tileset.json`);
// const pyProcess = spawn("python3", ["pythonFunction.py", 3, 6]);
// pyProcess.stdout.on("data", function (data) {
//   // convert Buffer object to Float
//   const value = parseFloat(data);
//   console.log(value);
// });
