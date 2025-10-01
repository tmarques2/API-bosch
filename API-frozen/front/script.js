const apiUrl = 'http://localhost:8002/api/v1/personagens/'; // ajuste se necessário
const form = document.getElementById('personagemForm');
const messageDiv = document.getElementById('message');
const listDiv = document.getElementById('list');

let editId = null; // Armazena o ID do personagem em edição

// Função para listar personagens
async function listarPersonagens() {
    listDiv.innerHTML = '';
    try {
        const res = await fetch(apiUrl);
        const personagens = await res.json();
        personagens.forEach(p => {
            const div = document.createElement('div');
            div.classList.add('personagem-item');

            div.innerHTML = `
                <div style="display:flex; align-items:center;">
                    ${p.foto ? `<img src="${p.foto}" alt="${p.nome}">` : ''}
                    <strong>${p.nome}</strong> - ${p.idade} anos - ${p.genero} - ${p.especie}
                </div>
                <div class="actions">
                    <button onclick="editarPersonagem(${p.id}, '${p.nome}', ${p.idade}, '${p.genero}', '${p.especie}', '${p.foto || ''}')">Editar</button>
                    <button onclick="deletarPersonagem(${p.id})">Excluir</button>
                </div>
            `;
            listDiv.appendChild(div);
        });
    } catch (err) {
        console.error(err);
        messageDiv.textContent = 'Erro ao carregar personagens.';
        messageDiv.style.color = 'red';
    }
}

// Função para cadastrar ou atualizar personagem
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const personagemData = {
        nome: document.getElementById('nome').value,
        idade: parseInt(document.getElementById('idade').value),
        genero: document.getElementById('genero').value,
        especie: document.getElementById('especie').value,
        foto: document.getElementById('foto').value || null
    };

    try {
        let res;
        if (editId) {
            // Atualizando personagem existente
            res = await fetch(apiUrl + editId, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(personagemData)
            });
        } else {
            // Cadastrando novo personagem
            res = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(personagemData)
            });
        }

        if (res.ok) {
            messageDiv.textContent = editId ? 'Personagem atualizado com sucesso!' : 'Personagem cadastrado com sucesso!';
            messageDiv.style.color = 'green';
            form.reset();
            editId = null;
            form.querySelector('button[type="submit"]').textContent = 'Cadastrar Personagem';
            listarPersonagens();
        } else {
            const error = await res.json();
            messageDiv.textContent = 'Erro: ' + (error.detail || 'Não foi possível salvar.');
            messageDiv.style.color = 'red';
        }
    } catch (err) {
        console.error(err);
        messageDiv.textContent = 'Erro de conexão com a API.';
        messageDiv.style.color = 'red';
    }
});

// Função para deletar personagem
async function deletarPersonagem(id) {
    if (!confirm('Deseja realmente excluir este personagem?')) return;
    try {
        const res = await fetch(apiUrl + id, { method: 'DELETE' });
        if (res.status === 204) {
            messageDiv.textContent = 'Personagem excluído com sucesso!';
            messageDiv.style.color = 'green';
            listarPersonagens();
        } else {
            const error = await res.json();
            messageDiv.textContent = 'Erro: ' + (error.detail || 'Não foi possível excluir.');
            messageDiv.style.color = 'red';
        }
    } catch (err) {
        console.error(err);
        messageDiv.textContent = 'Erro de conexão com a API.';
        messageDiv.style.color = 'red';
    }
}

// Função para preencher o formulário com os dados do personagem para edição
function editarPersonagem(id, nome, idade, genero, especie, foto) {
    editId = id;
    document.getElementById('nome').value = nome;
    document.getElementById('idade').value = idade;
    document.getElementById('genero').value = genero;
    document.getElementById('especie').value = especie;
    document.getElementById('foto').value = foto;

    form.querySelector('button[type="submit"]').textContent = 'Atualizar Personagem';
}

// Listar personagens ao carregar a página
listarPersonagens();
