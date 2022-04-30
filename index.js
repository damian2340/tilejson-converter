const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");

const jsonPath = `./MESH 2021/L15/LR/6359_6158_-001_lv15_0.json`;

const convert = (transform, rootTransform) => {
  return new Promise((resolve) => {
    const pyProcess = spawn("python3", [
      "transformaciones.py",
      ...transform.slice(12, 15),
      rootTransform,
    ]);
    pyProcess.stdout.on("data", function (data) {
      const converted = JSON.parse(data);
      resolve(
        rootTransform
          ? [
              ...converted.slice(0, 13),
              converted[13] - 16000,
              converted[14],
              converted[15],
            ]
          : converted
      );
    });
  });
};
const processChild = async (
  { transform, children, content, geometricError, ...otherChild },
  rootTransform
) => {
  const { uri } = content;
  const transformed = transform
    ? await convert(transform, rootTransform)
    : undefined;
  const childrenPromised = children
    ? children
        .filter(({ content: { uri } }) => uri?.indexOf("b3dm") > 0)
        .map((child) => processChild(child, false))
    : [];

  /*
  for (child of childrenPromised) {
    console.log({child})
    const data = await processChild(child, false);
    childrenPromised.push(data);
  }
  */

  const childrenProcessed = childrenPromised.length
    ? await Promise.all(childrenPromised)
    : undefined;
  const result = {
    ...otherChild,
    geometricError: geometricError, // && geometricError / 10.0,
    transform: transformed,
    children: childrenProcessed,
    content: {
      uri: path.relative("./", path.join("./MESH 2021/L15/LR", uri)),
      // path.relative(
      //   "/Users/lopez/Code/kan/tilejson-converter",
      //   path.resolve("./MESH 2021/L15/LR", uri)
      // ),
    },
    boundingVolume: {
      box: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    },
  };

  return result;
};

/// Process root json
(async () =>
  await new Promise((resolve, reject) => {
    fs.readFile(jsonPath, "utf8", (err, data) => {
      if (err) {
        reject(err);
        return;
      }

      resolve(data);
    });
  })
    .then((data) => JSON.parse(data))
    .then(async ({ root, ...otherTileset }) => ({
      ...otherTileset,
      root: await processChild(root, true),
    }))
    .then((data) => JSON.stringify(data))
    .then((data) => {
      fs.writeFileSync("tileset.json", data);
    })
    .catch((error) => console.log({ error })))();
