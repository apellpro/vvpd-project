const userColors = ['red', 'blue', 'green', 'orange'];

let inputs = document.getElementsByName("student")
inputs.forEach(elem => {
    elem.addEventListener('click', studentSelected, true)
})

function studentSelected(event) {
    if (event.target.id === 'cancel') {
        document.body.classList.remove('user-mode')
    } else {
        document.body.classList.add('user-mode')
        drawUserCommits(event.target.id)
        drawUserDelta(event.target.id)
    }
}

async function drawUserCommits(username) {
    let commits = document.querySelector('#user-commits').getElementsByClassName('commit')
    document.querySelector('#user-commits .other-commits').remove()
    for (let i = commits.length - 1; i >= 0; i--) {
        commits[i].remove()
    }
    let data = null
    await $.ajax({
        url: '/api/getcommits',
        method: 'post',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        data: {
            'git_owner': document.querySelector('[name=git_owner]').value,
            'git_repo': document.querySelector('[name=git_repo]').value,
            'git_user': username
        },
        success: res => data = res,
    })
    if (!data) return
    for (let i = 0; i < data.length; i++) {
        if (i === 5) break
        let div = document.createElement('div')
        div.classList.add('commit')
        div.style = `--user-color: var(--${username})`
        div.innerHTML += `<span class="commit-description">${data[i]['commit']['message']}</span>`
        div.innerHTML += `<span class="commit-date">${data[i]['commit']['committer']['date']}</span>`
        document.querySelector('#user-commits').appendChild(div)
    }
    let div = document.createElement('div')
    div.classList.add('other-commits')
    if (data.length > 5) div.innerHTML += `<p>и ещё ${data.length - 5} коммитов</p>`
    document.querySelector('#user-commits').appendChild(div)
}

async function drawUserDelta(username) {
    let data = null
    await $.ajax({
        url: '/api/getuserdelta',
        method: 'post',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        data: {
            'git_owner': document.querySelector('[name=git_owner]').value,
            'git_repo': document.querySelector('[name=git_repo]').value,
            'git_user': username
        },
        success: res => data = res
    })
    if (!data) return
    document.getElementById("user-delta-plus").innerHTML = `+${data.delta_plus}`
    document.getElementById("user-delta-minus").innerHTML = data.delta_minus
}