async function puxar_api() {
    await axios.get("http://localhost:8002/api/v1/personagens").then((response) => {
        const personagens = response.data;
        const container = document.getElementById("personagens-container");
        personagens.forEach(element => {
            const personagemDiv = document.createElement('div');
            personagemDiv.classList.add('personagem');
            personagemDiv.innerHTML = `
            <h2>${element.nome}</h2>
            <p>${element.idade}</p>
            <p>${element.genero}</p>
            <p>${element.especie}</p>
            <p>${element.foto}</p>
            `;
            container.appendChild(personagemDiv);
        });
    })
}

puxar_api()