let canvas = document.getElementById('impact-circle');
let ctx = canvas.getContext('2d');

const pi = Math.PI;

let countSum = 0;
for (let i = 0; i < counts.length; i++)
    countSum += counts[i];


function drawPie (f) {
    ctx.beginPath();
    ctx.moveTo(100, 100);
    ctx.arc(100,100,101, 0, 2 * pi);
    ctx.fillStyle = 'white';
    ctx.fill();
    let lastAngle = -pi / 2;
    for (let i = 0; i < counts.length; i++) {
        let newAngle = lastAngle + ((2 * pi / countSum) * counts[i] * f);
        ctx.beginPath();
        ctx.moveTo(100, 100);
        ctx.arc(100, 100, 100, lastAngle, newAngle, false);
        ctx.fillStyle = userColors[i];
        ctx.fill();
        lastAngle = newAngle;
        ctx.closePath();
    }
    ctx.beginPath();
    ctx.moveTo(100, 100);
    ctx.arc(100,100,60, 0, 2 * pi);
    ctx.fillStyle = 'white';
    ctx.fill();
    if (f < 1) {
        setTimeout(() => {drawPie(f+0.02)}, 3);
    }
}

drawPie(0.02)

