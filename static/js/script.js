const getTodoURL = "/api/todos"
const todos = document.querySelector(".todos")

async function getTodo() {
    const response = await fetch(getTodoURL)
    const data = await response.json()
    console.log(data)

    data.map((value) => {
        let is_checked = null
        if (value.is_done === true) {
            is_checked = "checked"
        }
        const createdDate = new Date(value.created_date)
        const lastUpdatedDate = new Date(value.last_updated_date)
        let template = `
        <div class="todo-item" data-id=${value.id}>
        <input type="checkbox" ${is_checked}>
        <a class="todo-link" href="${'/todo/' + value.id}">
        <div class="todo-title">${value.title}</div>
        <div class="todo-date">${createdDate.toLocaleDateString()}</div>
        <div class="todo-date">${lastUpdatedDate.toLocaleDateString()}</div>
        <div class="see-more">See more</div>
        </a>
        </div>
        `
        todos.innerHTML += template
    })

    const todoItems = document.querySelectorAll(".todo-item")
    todoItems.forEach((todo) => {
        const checkbox = todo.querySelector("input[type=checkbox]")
        const title = todo.querySelector(".todo-title")
        checkbox.addEventListener("click", (e) => {
            const todoID = todo.attributes["data-id"].value
            const url = `/api/todos/${todoID}/is-done`
            console.log(url)
            const response = fetch(url, {
                method: "PATCH",
                headers: {
                    'Accept': 'application/json',
                },
            })
        })
    })
}

getTodo()





// console.log(todoItems)