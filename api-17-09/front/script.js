// async function puxando_api() {
//     const response = await fetch("http://localhost:8001/api/v1/bandas");
//     const data = await response.json();
//     return data;
// }

// async function mostrar_banda() {
//     const bandas = await puxando_api();
//     const container = document.getElementById("bandas-container");

//     bandas.forEach(element => {
//         const bandaDiv = document.createElement('div');
//         bandaDiv.classList.add('banda');
//         bandaDiv.innerHTML = `
//         <h2>${banda.nome}</h2>
//         <p>${banda.qtd_integrantes}</p>
//         <p>${banda.tipo_musical}</p>
//         `;

//         container.appendChild(bandaDiv);
//     });
// }

async function puxar_api() {
    await axios.get("http://localhost:8002/api/v1/bandas").then((response) => {
        const bandas = response.data;
        const container = document.getElementById("bandas-container");
        bandas.forEach(element => {
            const bandaDiv = document.createElement('div');
            bandaDiv.classList.add('banda');
            bandaDiv.innerHTML = `
            <h2>${element.nome}</h2>
            <p>${element.qtd_integrantes}</p>
            <p>${element.tipo_musical}</p>
            `;
            container.appendChild(bandaDiv);
        });
    })
}

puxar_api()