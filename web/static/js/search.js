function updateProjectList() {
    
    function countMatches(project, name) {
        let counter = 0
        splitedRequest.forEach(requestPart => {
            counter += name.toLowerCase().includes(requestPart.toLowerCase())
        })
        if (counter == splitedRequest.length && project["year"].includes(curYear) && ( curTag in project["tags"] || curTag == "Все тэги"))
            if (!(showingProjects.includes(project)))
                showingProjects.push(project)
    }
    let request = document.getElementsByTagName("input")[0].value
    let splitedRequest = request.split(/(?:,| )+/)
    let curTag = document.getElementsByName('tag-select')[0].value
    let curYear = document.getElementsByName('year-select')[0].value
    let showingProjects = []

    allProjects.forEach(project => {
        countMatches(project, project["projectName"])
        project["students"].forEach(studentName => {
            countMatches(project, studentName)
        })
    })

    let projectList = document.createElement("div")
    projectList.className = "main-part"
    for (let curProject  of showingProjects) {
        let project = document.createElement("div");
        project.className = "project";

        let projectName = document.createElement("a");
        projectName.appendChild(document.createTextNode(curProject["projectName"]))
        projectName.href = "/review/" + curProject["repo"]
        project.appendChild(projectName)

        let students = document.createElement("p")
        students.className = "names"
        for (let curStudent of curProject["students"]) {
            let tmp = curProject["students"][curProject["students"].length - 1] != curStudent ? ", " : " "
            let student = document.createElement("span")
            student.appendChild(document.createTextNode(curStudent + tmp))
            students.appendChild(student)
        }
        project.appendChild(students)

        let repo = document.createElement("p")
        repo.className = "git"
        repo.appendChild(document.createTextNode(curProject["repo"]))

        project.appendChild(repo)

        let tags = document.createElement("div")
        tags.className = "tags"
        for (let curTag in curProject["tags"]) {
            let tag = document.createElement("div")
            tag.className = "tag"
            tag.style = `background: ${curProject["tags"][curTag]["bgColor"]}; color: ${curProject["tags"][curTag]["txtColor"]}`
            tag.appendChild(document.createTextNode(curTag))
            tags.appendChild(tag)
        }
        project.appendChild(tags)
        projectList.appendChild(project)
    }
    let oldNumSpan = document.getElementById("found-amount")
    let newNumSpan = document.createElement("span")
    newNumSpan.appendChild(document.createTextNode(`${showingProjects.length}`))
    newNumSpan.id = "found-amount"
    spanParent = document.getElementsByClassName("text-found")[0]
    spanParent.replaceChild(newNumSpan, oldNumSpan)
    let oldProjectList = document.getElementsByClassName("main-part")[0]
    let studentsParent = document.getElementsByClassName("workspace")[0]
    studentsParent.replaceChild(projectList, oldProjectList)

    let checkbox = document.getElementById("main-year-group")
    if (mainYear != curYear) {
        if (checkbox.hasAttribute("disabled"))
            checkbox.removeAttribute("disabled")
            checkbox.checked = false
            checkbox.onclick = function () {
                checkbox.setAttribute("disabled", "disabled")
                checkbox.setAttribute("checked", "checked")
                mainYear = curYear
                $.ajax({
                    url: '/api/mainyeargroup',
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    data: {
                        'group_id': $("#year-select")[0].selectedOptions[0].id.slice(10)
                    },
                    success: null,
                    error: () => {location.reload()}
                })
        }
    }
    else {
        checkbox.setAttribute("disabled", "disabled")
        checkbox.checked = true
    }


}

document.getElementsByTagName("input")[0].addEventListener('keyup', event => {
    updateProjectList()
})

let mainYear = document.getElementsByName('year-select')[0].value
