const main = require("./output.js");

function runFunctionWithArgs(jsonArgs) {
  try {
    const args = JSON.parse(jsonArgs);

    if (!Array.isArray(args)) {
      throw new Error("Arguments must be an array.");
    }

    const result = main(...args);
    console.log(result);
    process.exit(0);
  } catch (e) {
    console.error(e.stack || e);
    process.exit(1);
  }
}

const jsonArgs = process.argv[2];

runFunctionWithArgs(jsonArgs);
