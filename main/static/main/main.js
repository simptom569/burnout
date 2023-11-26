function getCategory(chance){
    if (chance >= 0 && chance <= 40) {
        return 'low-risk';
    } else if (chance > 40 && chance <= 70) {
        return 'medium-risk';
    } else if (chance > 70 && chance <= 100) {
        return 'high-risk';
    }
}

const employeesData = []

$.ajax({
    url: "",
    type: 'GET',
    success: function(html){
        employees = html.response;
        for (const employee of employees){
            const category = getCategory(parseFloat(employee.chance));
            employeesData.push({ id: employee.id, name: employee.name, category, chance: parseFloat(employee.chance) });
        }
    }
})

let originalRowsOrder;

function copyRows(container) {
    return Array.from(container.children).map(row => row.cloneNode(true));
}

function showCategory(category) {
    const categoriesContainer = document.getElementById('categories');
    const employeesContainer = document.getElementById('employees');
    const employeesListContainer = document.getElementById('employeesList');

    employeesListContainer.innerHTML = '';

    originalRowsOrder = copyRows(employeesListContainer);

    var table = document.getElementById("table_cat");
    table.classList.add(category);

    var button = document.getElementById("backButton");
    button.classList.add(category+"_button");

    employeesData.forEach(employee => {
        if (employee.category === category) {
            const row = document.createElement('tr');
            row.innerHTML = `<td><a href="user/${employee.id}">${employee.name}</a></td><td>${employee.chance}%</td>`;
            employeesListContainer.appendChild(row);
        }
    });
    
    const backButton = document.getElementById('backButton');

    if (!sortButton) {
        sortButton = document.createElement('button_sort');
        sortButton.setAttribute("id", "button_sort")
        sortButton.textContent = 'Сортировать';
        sortButton.classList.add(category+"_button");
        sortButton.onclick = function () {
            sortTable();
        };

        if (backButton) {
            backButton.parentNode.insertBefore(sortButton, backButton.nextSibling);
        }
    }
    else {
        sortButton.classList.add(category+"_button");
    }

    categoriesContainer.style.display = 'none';
    employeesContainer.style.display = 'block';

    backButton.onclick = function () {
        goBack(category);
    };
}

function goBack(category) {
    const categoriesContainer = document.getElementById('categories');
    const employeesContainer = document.getElementById('employees');
    const employeesListContainer = document.getElementById('employeesList');

    categoriesContainer.style.display = 'block';
    employeesContainer.style.display = 'none';

    employeesListContainer.innerHTML = '';

    originalRowsOrder.forEach(row => employeesListContainer.appendChild(row));

    var table = document.getElementById("table_cat");
    table.classList.remove(category);

    var button = document.getElementById("backButton");
    button.classList.remove(category+"_button");

    var sort_butt = document.getElementById("button_sort");
    sort_butt.classList.remove(category+"_button");
}

function sortTable() {
    const table = document.querySelector("table");
    const table1 = document.getElementById('employeesList');
    const rows = Array.from(table.rows).slice(1);

    const sortedRows = rows.sort((a, b) => {
        const x = parseFloat(a.cells[1].innerHTML);
        const y = parseFloat(b.cells[1].innerHTML);

        return x - y;
    });

    if (table.classList.contains('sorted')) {
        sortedRows.reverse();
        table.classList.remove('sorted');
    } else {
        table.classList.add('sorted');
    }

    sortedRows.forEach(row => table1.appendChild(row));
}

let sortButton;