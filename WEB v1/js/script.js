const canvas = document.getElementById("graph");
const ctx = canvas.getContext("2d");
const form = document.getElementById("function-form");
const inputX = document.getElementById("function-x");
const inputY = document.getElementById("function-y");
const heartButton = document.getElementById("heart-button");

const bounds = {
  xMin: -18,
  xMax: 18,
  yMin: -18,
  yMax: 18,
};

let heartPath = null;

const toCanvas = (x, y) => {
  const xNorm = (x - bounds.xMin) / (bounds.xMax - bounds.xMin);
  const yNorm = (y - bounds.yMin) / (bounds.yMax - bounds.yMin);
  return {
    x: xNorm * canvas.width,
    y: canvas.height - yNorm * canvas.height,
  };
};

const drawBackground = () => {
  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "rgba(255, 255, 255, 0.1)";
  ctx.lineWidth = 1;

  const step = 3;
  ctx.beginPath();
  for (let x = Math.ceil(bounds.xMin / step) * step; x <= bounds.xMax; x += step) {
    const pos = toCanvas(x, 0).x;
    ctx.moveTo(pos, 0);
    ctx.lineTo(pos, canvas.height);
  }
  for (let y = Math.ceil(bounds.yMin / step) * step; y <= bounds.yMax; y += step) {
    const pos = toCanvas(0, y).y;
    ctx.moveTo(0, pos);
    ctx.lineTo(canvas.width, pos);
  }
  ctx.stroke();

  ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  const axisY = toCanvas(0, 0).y;
  const axisX = toCanvas(0, 0).x;
  ctx.moveTo(0, axisY);
  ctx.lineTo(canvas.width, axisY);
  ctx.moveTo(axisX, 0);
  ctx.lineTo(axisX, canvas.height);
  ctx.stroke();
};

const drawPath = (path, color = "#fff") => {
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
  ctx.stroke(path);
};

const renderHeart = () => {
  drawBackground();
  const path = new Path2D();
  const total = 400;
  for (let i = 0; i <= total; i += 1) {
    const t = (i / total) * Math.PI * 2;
    const x = 16 * Math.pow(Math.sin(t), 3);
    const y =
      13 * Math.cos(t) -
      5 * Math.cos(2 * t) -
      2 * Math.cos(3 * t) -
      Math.cos(4 * t);
    const point = toCanvas(x, y);
    if (i === 0) {
      path.moveTo(point.x, point.y);
    } else {
      path.lineTo(point.x, point.y);
    }
  }
  drawPath(path);
  heartPath = path;
};

const normalizeExpression = (raw, variable) => {
  let expr = raw.trim();
  if (!expr) return expr;

  expr = expr.replace(/\^/g, "**");
  const powerPattern = new RegExp(`\\b${variable}(\\d+(?:\\.\\d+)?)\\b`, "gi");
  expr = expr.replace(powerPattern, (_, power) => `Math.pow(${variable}, ${power})`);
  const implicitVarPattern = new RegExp(`(\\d)(${variable})`, "gi");
  expr = expr.replace(implicitVarPattern, "$1*$2");
  expr = expr.replace(/(\d)(\()/g, "$1*(");
  const beforeOpen = new RegExp(`([${variable}0-9\\)])\\(`, "g");
  expr = expr.replace(beforeOpen, "$1*(");
  const afterClose = new RegExp(`\\)([${variable}0-9])`, "g");
  expr = expr.replace(afterClose, ")*$1");
  expr = expr.replace(/\bpi\b/gi, "PI");

  return expr;
};

const plotFunction = (expression, variable, color) => {
  const normalized = normalizeExpression(expression, variable);
  let fn;
  try {
    fn = new Function(variable, `with (Math) { return ${normalized}; }`);
    void fn(0);
  } catch (error) {
    throw new Error("could not be parsed");
  }

  const path = new Path2D();
  const sampleCount = canvas.width;
  const min = variable === "x" ? bounds.xMin : bounds.yMin;
  const max = variable === "x" ? bounds.xMax : bounds.yMax;
  const step = (max - min) / sampleCount;

  let started = false;
  let drawnPoints = 0;

  for (let i = 0; i <= sampleCount; i += 1) {
    const independent = min + i * step;
    let dependent;
    try {
      dependent = fn(independent);
    } catch (error) {
      started = false;
      continue;
    }

    if (!Number.isFinite(dependent)) {
      started = false;
      continue;
    }

    const point =
      variable === "x"
        ? toCanvas(independent, dependent)
        : toCanvas(dependent, independent);

    if (!started) {
      path.moveTo(point.x, point.y);
      started = true;
    } else {
      path.lineTo(point.x, point.y);
    }

    drawnPoints += 1;
  }

  if (drawnPoints === 0) {
    throw new Error("returned no values in range");
  }

  drawPath(path, color);
  heartPath = null;
};

const showError = (message) => {
  canvas.dataset.error = message;
  canvas.classList.remove("error");
  void canvas.offsetWidth;
  canvas.classList.add("error");
};

const clearError = () => {
  canvas.classList.remove("error");
  delete canvas.dataset.error;
};

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const rawFx = inputX.value.trim();
  const rawFy = inputY.value.trim();
  clearError();

  const fxHeart = rawFx && rawFx.toLowerCase() === "heart";
  const fyHeart = rawFy && rawFy.toLowerCase() === "heart";

  if ((!rawFx && !rawFy) || fxHeart || fyHeart) {
    inputX.value = "heart";
    inputY.value = "";
    renderHeart();
    return;
  }

  drawBackground();

  let plotted = false;
  const errors = [];

  if (rawFx) {
    try {
      plotFunction(rawFx, "x", "#ffffff");
      plotted = true;
    } catch (error) {
      errors.push(`f(x) ${error.message}`);
    }
  }

  if (rawFy) {
    try {
      plotFunction(rawFy, "y", "#ff4f6b");
      plotted = true;
    } catch (error) {
      errors.push(`f(y) ${error.message}`);
    }
  }

  if (!plotted) {
    renderHeart();
  }

  if (errors.length) {
    showError(errors.join("  •  "));
  }
});

canvas.addEventListener("click", (event) => {
  const rect = canvas.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;

  if (heartPath && ctx.isPointInPath(heartPath, x, y)) {
    canvas.classList.remove("pulse");
    void canvas.offsetWidth;
    canvas.classList.add("pulse");
  }
});

if (heartButton) {
  heartButton.addEventListener("click", () => {
    inputX.value = "heart";
    inputY.value = "";
    clearError();
    renderHeart();
    inputX.focus();
  });
}

renderHeart();
