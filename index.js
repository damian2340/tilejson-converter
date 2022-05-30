const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");
const uriToRelative = (uri) =>
  path.relative("./", path.join("./MESH 2021/L15/LR", uri));
const jsonPath = uriToRelative("./6359_6158_-001_lv15_0.json");

let rootTranslation

const readFileAsync = (jsonPath) =>
  new Promise((resolve, reject) => {
    fs.readFile(jsonPath, "utf8", (err, data) => {
      if (err) {
        reject(err);
        return;
      }

      resolve(data);
    });
  });

const readExternalChildren = async (uri) => {
  const filePath = uriToRelative(uri);
  const exists = fs.existsSync(filePath);
  console.log({ filePath, exists })
  return exists
    ? await readFileAsync(filePath)
        .then((data) => JSON.parse(data))
        .then((data) => data.root.children)
    : [];
};

const convert = (transform, typeTransform) => {
  if(typeTransform === 'root') {
    rootTranslation = transform.slice(12, 15)
    console.log({ rootTranslation })
  }
  return new Promise((resolve) => {
    console.log({typeTransform, transform})
    const pyProcess = spawn("python3", [
      "tileset_transform.py",
      typeTransform,
      ...rootTranslation,
      ...transform,
    ]);
    pyProcess.stdout.on("data", function (data) {
      console.log({typeTransform})
      const converted = JSON.parse(data)//.replace(/(\d)\s+([\d|-])/gm, '$1, $2'));
      console.log({ typeTransform, converted })
      resolve(converted)
    });
  });
};

const processChild = async (
  { transform, children, content, geometricError, boundingVolume: { box }, refine, ...otherChild },
  typeTransform, file
) => {
  const { uri } = content;
  console.log({ uri });
  const transformed = transform
    ? await convert(transform, typeTransform)
    : undefined;

  const internalChildrenPromised = children
    ? children
        .filter(({ content: { uri } }) => uri?.endsWith(".b3dm"))
        .map((child) => processChild(child, 'child'))
    : [];

  const externalChildrenPromised = children
    ? children
        .filter(({ content: { uri } }) => uri?.endsWith("NR/6361_6158_-1_lv8_group_0_0.json"))
        .flatMap(async ({ content: { uri } }) =>
          await Promise.all((await readExternalChildren(uri))
            .flatMap((child) =>
              processChild(child, 'child')
          ))
        )
    : [];

  const childrenPromised = [
    internalChildrenPromised,
    externalChildrenPromised,
  ].flat(50);

  const childrenProcessed = childrenPromised.length
    ? (await Promise.all(childrenPromised)).flat(50)
    : undefined;

  const result = {
    ...otherChild,
    geometricError: geometricError,
    transform: transformed,
    children: childrenProcessed,
    content: {
      uri: uriToRelative(uri),
    },
    boundingVolume: {
      box: await convert(box, 'bounding')//[0, 0, 0, 20000, 0, 0, 0, 20000, 0, 0, 0, 20000],
    },
    refine
  };

  return result;
};

/// Process root json
(async () =>
  await readFileAsync(jsonPath)
    .then((data) => JSON.parse(data))
    .then(async ({ root, ...otherTileset }) => ({
      ...otherTileset,
      root: await processChild(root, 'root'),
    }))
    .then((data) => JSON.stringify(data))
    .then((data) => {
      fs.writeFileSync("tileset.json", data);
    })
    .catch((error) => console.log({ error })))();
