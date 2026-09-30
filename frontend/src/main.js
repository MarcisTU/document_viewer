import "./style.css";


// Mūsu FastAPI backend adrese
const API_URL = "http://127.0.0.1:8081/api/v1/documents";

// globāla dokumentu masīva instance
let documents = [];
let sortField = "creation_date";
let sortDirection = "desc";


const searchInput = document.querySelector("#search");
const categorySelect = document.querySelector("#category");
const importanceSelect = document.querySelector("#importance");
const fileTypeSelect = document.querySelector("#file-type");
const activeSelect = document.querySelector("#active");
const refreshButton = document.querySelector("#refresh");
const tableBody = document.querySelector("#documents");
const statusElement = document.querySelector("#status");
const emptyElement = document.querySelector("#empty");


async function fetchDocuments() {
    showLoading();

    try {
        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error(`API returned ${response.status}`);
        }

        documents = await response.json();

        populateFilters();
        renderDocuments();
    } catch (error) {
        console.error(error);

        statusElement.innerHTML = `
            <div class="error">
                Neizdevās ielādēt dokumentus no backend API.
                Pārbaudiet, vai FastAPI serveris darbojas.
            </div>
        `;

        tableBody.innerHTML = "";
    }
}


function populateFilters() {
    populateSelect(
        categorySelect,
        documents.map(document => document.category)
    );

    populateSelect(
        importanceSelect,
        documents.map(document => document.importance)
    );

    populateSelect(
        fileTypeSelect,
        documents.map(document => document.file_type)
    );
}


function populateSelect(select, values) {
    const uniqueValues = [...new Set(values)].sort();

    const currentValue = select.value;

    // Keep the first "all" option.
    select.innerHTML = select.options[0].outerHTML;

    for (const value of uniqueValues) {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        select.appendChild(option);
    }

    if (uniqueValues.includes(currentValue)) {
        select.value = currentValue;
    }
}


function getFilteredDocuments() {
    const search = searchInput.value.toLowerCase().trim();
    const category = categorySelect.value;
    const importance = importanceSelect.value;
    const fileType = fileTypeSelect.value;
    const active = activeSelect.value;

    return documents.filter(document => {
        const matchesSearch =
            !search ||
            document.name.toLowerCase().includes(search) ||
            document.description.toLowerCase().includes(search);

        const matchesCategory =
            !category || document.category === category;

        const matchesImportance =
            !importance || document.importance === importance;

        const matchesFileType =
            !fileType || document.file_type === fileType;

        const matchesActive =
            !active ||
            String(document.is_active) === active;

        return (
            matchesSearch &&
            matchesCategory &&
            matchesImportance &&
            matchesFileType &&
            matchesActive
        );
    });
}


function sortDocuments(documentsToSort) {
    return [...documentsToSort].sort((a, b) => {
        let valueA = a[sortField];
        let valueB = b[sortField];

        if (valueA === valueB) {
            return 0;
        }

        if (valueA === null || valueA === undefined) {
            return 1;
        }

        if (valueB === null || valueB === undefined) {
            return -1;
        }

        if (typeof valueA === "string") {
            valueA = valueA.toLowerCase();
            valueB = valueB.toLowerCase();
        }

        let result;

        if (valueA < valueB) {
            result = -1;
        } else {
            result = 1;
        }

        return sortDirection === "asc" ? result : -result;
    });
}


function renderDocuments() {
    const filteredDocuments = getFilteredDocuments();
    const sortedDocuments = sortDocuments(filteredDocuments);

    tableBody.innerHTML = "";

    for (const doc of sortedDocuments) {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>
                <a
                    href="${escapeHtml(doc.url)}"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    ${escapeHtml(doc.name)}
                </a>

                <div class="description">
                    ${escapeHtml(doc.description)}
                </div>
            </td>
            <td>${escapeHtml(doc.responsible_unit)}</td>
            <td>${formatDate(doc.creation_date)}</td>
            <td>${escapeHtml(doc.file_type)}</td>
            <td>${doc.reading_time_minutes} min</td>
            <td>${escapeHtml(doc.importance)}</td>
            <td>${escapeHtml(doc.category)}</td>
            <td>
                <span class="status ${document.is_active ? "active" : "inactive"}">
                    ${doc.is_active == "jā" ? "Aktīvs" : "Neaktīvs"}
                </span>
            </td>
        `;

        tableBody.appendChild(row);
    }
    
    // neatrastu dokumentu ziņojuma slēdzis
    emptyElement.classList.toggle(
        "hidden",
        sortedDocuments.length !== 0
    );

    // Izvada statusa paziņojumu par paraugu skaitu virs tabulas
    statusElement.innerHTML = `
        <span>
            Tiek rādīti ${sortedDocuments.length} no ${documents.length} dokumentiem
        </span>
    `;

    updateSortIndicators();
}


function updateSortIndicators() {
    document.querySelectorAll("th[data-sort]").forEach(th => {
        const field = th.dataset.sort;

        th.classList.remove("sort-asc", "sort-desc");

        if (field === sortField) {
            th.classList.add(
                sortDirection === "asc"
                    ? "sort-asc"
                    : "sort-desc"
            );
        }
    });
}


function formatDate(dateString) {
    const date = new Date(`${dateString}T00:00:00`);

    return new Intl.DateTimeFormat("lv-LV").format(date);
}


function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = String(value);
    return div.innerHTML;
}


function showLoading() {
    statusElement.innerHTML = `
        <div class="loading">
            Ielādē dokumentus...
        </div>
    `;
}


function resetFilters() {
    searchInput.value = "";
    categorySelect.value = "";
    importanceSelect.value = "";
    fileTypeSelect.value = "";
    activeSelect.value = "";

    sortField = "creation_date";
    sortDirection = "desc";
}


// Uzspiežot uz kolonas nosaukuma var to sakārtot augošā/dilstošā secībā
document.querySelectorAll("th[data-sort]").forEach(th => {
    th.addEventListener("click", () => {
        const field = th.dataset.sort;

        if (sortField === field) {
            sortDirection =
                sortDirection === "asc"
                    ? "desc"
                    : "asc";
        } else {
            sortField = field;
            sortDirection = "asc";
        }

        renderDocuments();
    });
});


[
    searchInput,
    categorySelect,
    importanceSelect,
    fileTypeSelect,
    activeSelect
].forEach(element => {
    element.addEventListener("input", renderDocuments);
    element.addEventListener("change", renderDocuments);
});


// Notīra filtrus un atjauno sākotnējo dokumentu skatu
refreshButton.addEventListener("click", () => {
    resetFilters();
    fetchDocuments();
});

fetchDocuments();