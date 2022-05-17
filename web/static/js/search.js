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
    let oldProjectList = document.getElementsByClassName("main-part")[0]
    let parent = document.getElementsByClassName("workspace")[0]
    parent.replaceChild(projectList, oldProjectList)
}

document.getElementsByTagName("input")[0].addEventListener('keyup', event => {
    updateProjectList()
})
