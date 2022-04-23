const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");

const jsonPath =
  `./MESH 2021/L15/LR/6359_6158_-001_lv15_0.json`;

const convert = (transform) => {
  return new Promise((resolve) => {
    const pyProcess = spawn("python3", [
      "transformaciones.py",
      ...transform.slice(12, 15),
    ]);
    pyProcess.stdout.on("data", function (data) {
      const converted = JSON.parse(data);
      resolve(converted);
    });
  });
};
const processChild = async ({
  transform,
  children,
  content: { uri },
  ...otherChild
}, rootTransform) => {
  return {
    ...otherChild,
    transform: transform && (rootTransform ? await convert(transform) : transform),
    children:
      children &&
      (await Promise.all(
        children
          .filter(({ content: { uri } }) => uri?.indexOf("b3dm") > 0)
          .map(processChild)
      )),
    content: {
      uri: path.join("./MESH 2021/L15/LR", uri),
    },
    boundingVolume: {
      box: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    },
  };
};

/// Process root json
new Promise((resolve, reject) => {
  fs.readFile(jsonPath, "utf8", (err, data) => {
    if (err) {
      reject(err);
      return;
    }

    resolve(data);
  });
})
  .then((data) => JSON.parse(data))
  .then(async ({ root, ...otherTileset }) => {
    return {
      ...otherTileset,
      root: await processChild(root, true),
    };
  })
  .then((data) => JSON.stringify(data))
  .then((data) => {
    fs.writeFileSync("tileset.json", data);
  });

  /*

convert([
  1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0,
  2739735.055245, -4476943.731842, -3611192.317842, 1.0
]).then(console.log)
  [
      0.95317991371353, -0.332138445861544, 0.4795188785373789, 0,
      -3.571763283578787e-17, -0.9186528552536825, -0.6363043151938046, 0,
      0.5833132109708019, 0.5427404852366688, -0.7835717667144457, 0,
      -6515835.74298203, -4123865.6167859375, -224.24348250683397, 1
    ],
  */

    // -10207.48265475841, 12015.938291085713, -6367876.548935372, 1