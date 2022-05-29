function deleteTag(tag) {
    if (!confirm("Вы действительно хотите удалить этот тэг?"))
        return;
    $.ajax({
        url: '/ajax/deletetag',
        method: 'post',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        data: {
            'tagId': tag.id.slice(4)
        },
        success: ()=>{location.reload()}
    })
}

function boundTag(tag) {
    $("#unbounded-tags")[0].removeChild(tag.parentNode)
    $("#bounded-tags")[0].appendChild(tag.parentNode)
    tag.classList.remove('enter')
    tag.classList.add('delete')
    tag.children[0].className = 'fa fa-times'
    tag.onclick = () => {unboundTag(tag)}
    $.ajax({
        url: '/ajax/boundtag',
        method: 'post',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        data: {
            'git_owner': document.querySelector('[name=git_owner]').value,
            'git_repo': document.querySelector('[name=git_repo]').value,
            'tagId': tag.id.slice(2)
        },
    })
}

function unboundTag(tag) {
    $("#bounded-tags")[0].removeChild(tag.parentNode)
    $("#unbounded-tags")[0].appendChild(tag.parentNode)
    tag.classList.add('enter')
    tag.classList.remove('delete')
    tag.children[0].className = 'fa fa-plus'
    tag.onclick = () => {boundTag(tag)}
    $.ajax({
        url: '/ajax/unboundtag',
        method: 'post',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        data: {
            'git_owner': document.querySelector('[name=git_owner]').value,
            'git_repo': document.querySelector('[name=git_repo]').value,
            'tagId': tag.id.slice(2)
        },
    })
}