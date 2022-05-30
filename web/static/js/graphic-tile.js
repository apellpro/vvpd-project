let gCanvas = document.getElementById('graphic')
let gCtx = gCanvas.getContext('2d')

let graphHeight = 150
let graphWidth = 500

let basicHeight = graphHeight / (Math.max.apply(null, weekCounts) + 3)
let basicWidth = 500 / weekCounts.length

function drawGraph() {
    let startX = (gCanvas.clientWidth - graphWidth) / 2 + basicWidth / 2

    gCtx.beginPath()
    gCtx.moveTo((gCanvas.clientWidth - graphWidth) / 2, graphHeight + 35)
    gCtx.lineTo((gCanvas.clientWidth - graphWidth) / 2 + graphWidth, graphHeight + 35)
    gCtx.fillStyle = 'grey'
    gCtx.lineWidth = 1
    gCtx.stroke()
    gCtx.closePath()

    gCtx.beginPath()
    gCtx.moveTo(startX, graphHeight - basicHeight * weekCounts[0])
    gCtx.font = "14px sans-serif"
    gCtx.textAlign = "center"
    gCtx.fillStyle = 'black'
    gCtx.lineWidth = 3
    gCtx.fillText(`${weekCounts[0]}`, startX, graphHeight + 25)
    let textPos = -1
    for (let i = 1; i < weekCounts.length; i++) {
        gCtx.lineTo(startX + basicWidth * i,
            graphHeight - basicHeight * weekCounts[i]
        )
        gCtx.stroke()

        if (weekCounts[i] > weekCounts[i - 1]) textPos = 1;
        else if (weekCounts[i] < weekCounts[i - 1]) textPos = -1;
        gCtx.fillText(`${weekCounts[i]}`,
            startX + basicWidth * i,
            graphHeight + 25
        )
        var date = new Date();
        var delta = 1 - date.getDay();
        date.setDate(date.getDate() - 7 + delta)
        gCtx.fillText(`${date.getDay()}.${date.getMonth()}`,
            startX + basicWidth * i,
            graphHeight + 45
        )
    }
    gCtx.closePath()
}

drawGraph()