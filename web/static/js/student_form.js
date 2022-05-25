function addStudentForm() {
    function addInputBox(object, inputBoxName, labeltext) {
        let inputBox = document.createElement("div")
        inputBox.className = "input-box"
        let inputLine = document.createElement("input")
        inputLine.type = "text"
        inputLine.placeholder = " "
        inputLine.name = inputBoxName
        inputLine.autocomplete = "off"
        inputBox.appendChild(inputLine)
        let tmpLabel = document.createElement("label")
        tmpLabel.appendChild(document.createTextNode(labeltext))
        inputBox.appendChild(tmpLabel)
        object.appendChild(inputBox)
    }


    let studentsID = document.getElementsByClassName("menu")[0]
    let lastStudentNum = studentsID.children[studentsID.children.length - 2].textContent
    if(lastStudentNum == "4") 
        return
    let curStudentNum = `${parseInt(lastStudentNum) + 1}`
    let newMenuItem = document.createElement("a");
    newMenuItem.href="#win-project"
    newMenuItem.className = "student-num"
    newMenuItem.appendChild(document.createTextNode(curStudentNum))
    studentsID.insertBefore(newMenuItem, studentsID.children[studentsID.children.length - 1])
    newMenuItem.onclick = function() {setActive(this)}

    let newStudentForm = document.createElement("div")
    newStudentForm.id = "student-" + curStudentNum

    if(curStudentNum == "4") 
        document.getElementById("new-student").style.display = "none"
 
    let header = document.createElement("div")
    header.className = "up"
    let headerP = document.createElement("p")
    headerP.className = "num"
    headerP.appendChild(document.createTextNode("Студент "))
    let numHolder = document.createElement("span")
    numHolder.appendChild(document.createTextNode(curStudentNum))
    headerP.appendChild(numHolder)
    header.appendChild(headerP)

    let delButton = document.createElement("button")
    delButton.className = "delete"
    let delButtonI = document.createElement("i")
    delButtonI.className = "fas fa-trash-alt"
    delButton.appendChild(delButtonI)
    header.appendChild(delButton)
    delButton.addEventListener('click', deleteStudent)

    newStudentForm.appendChild(header)

    let fio = document.createElement("div")
    fio.className = "FIO"
    addInputBox(fio, "stud-surname-" + curStudentNum, "Фамилия")
    addInputBox(fio, "stud-name-" + curStudentNum, "Имя")
    addInputBox(fio, "stud-patronymic-" + curStudentNum, "Отчество")
    newStudentForm.appendChild(fio)

    let study = document.createElement("div")
    study.className = "study"
    addInputBox(study, "stud-group-" + curStudentNum, "Группа")
    addInputBox(study, "stud-edu-" + curStudentNum, "Форма обучения")
    newStudentForm.appendChild(study)

    let social = document.createElement("div")
    social.className = "social"
    addInputBox(social, "stud-vk-" + curStudentNum, "VK")
    addInputBox(social, "stud-git-" + curStudentNum, "GitHub")
    newStudentForm.appendChild(social)

    let parent = document.getElementsByClassName("students")[0]
    parent.appendChild(newStudentForm)
}


function deleteStudent(el) {
    el.preventDefault()
    document.getElementById("new-student").style.display = ""
    let curStudent = el.target
    let students = document.getElementsByClassName("students")[0]

    while (!curStudent.id.includes("student-"))
        curStudent = curStudent.parentElement

    let curStudentNum = parseInt(curStudent.id.slice(-1))
    let parent = curStudent.parentElement
    let menuItems = document.getElementsByClassName("student-num")
    setActive(menuItems[curStudentNum - 2])
    document.getElementsByClassName("menu")[0].removeChild(menuItems[menuItems.length - 1])
    parent.removeChild(curStudent)

    for (let i = 1; i + curStudentNum <= students.childElementCount + 1; i++) {
        let changingStudent = document.getElementById("student-" + `${i + curStudentNum}`)
        changingStudent.id = "student-" + `${i + curStudentNum - 1}`
        let headerP = changingStudent.getElementsByClassName("num")[0]
        headerP.removeChild(headerP.getElementsByTagName("span")[0])
        let tmpSpan = document.createElement("span")
        tmpSpan.appendChild(document.createTextNode(`${i + curStudentNum - 1}`))
        headerP.appendChild(tmpSpan)
        for (let childID = 1; childID < 4; childID++) {
            let child = changingStudent.children[childID]
            for (let j of child.getElementsByClassName("input-box")){
                let curInputLine = j.getElementsByTagName("input")[0]
                curInputLine.name = curInputLine.name.slice(0, (curInputLine.name.length - 1)) 
                                    + `${i + curStudentNum - 1}`
            }
        }
    }
}


function setActive(el) {
    let prevActive = document.getElementsByClassName("active")[0]
    let curActiveNum = el.textContent
    if (curActiveNum == prevActive.id.slice(-1))
        return
    document.getElementsByClassName("active-num")[0].classList.remove("active-num")
    document.getElementsByClassName("student-num")[curActiveNum - 1].classList.add("active-num")
    prevActive.className = "non-active"
    let curActive = document.getElementById("student-" + curActiveNum)
    curActive.className = "active"
}
