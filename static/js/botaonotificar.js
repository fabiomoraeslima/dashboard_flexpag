function normalizarCliente(clienteId) {
    // Enviar uma requisição AJAX para o servidor Flask
    fetch('/normalizar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cliente_id: clienteId })
    })
    .then(response => {
        if (response.ok) {
            // Cliente notificado com sucesso, atualize o status do botão
            document.getElementById('notificarBtn' + clienteId).innerText = 'Notificar';
            document.getElementById('notificarBtn' + clienteId).disabled = false;
        } else {
            throw new Error('Erro ao normalizar o cliente.');
        }
    })
}


function notificarCliente(clienteId, farol) {
    // Verificar se o farol é "red" e o botão ainda não está desativado
    if (farol === 'red' && !document.getElementById('notificarBtn' + clienteId).disabled) {
        // Enviar uma requisição AJAX para o servidor Flask
        fetch('/notificar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cliente_id: clienteId })
        })
        .then(response => {
            if (response.ok) {
                // Cliente notificado com sucesso, atualize o status do botão
                document.getElementById('notificarBtn' + clienteId).innerText = 'Notificado';
                document.getElementById('notificarBtn' + clienteId).disabled = true;
            } else {
                throw new Error('Erro ao notificar o cliente.');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao notificar o cliente.');
        });
    } else {
        // Se o farol não for "red" ou o botão já estiver desativado, exibir mensagem informando que o cliente já está notificado
        fetch('/normalizar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cliente_id: clienteId })
        })

        alert('Notificar somente clientes com Status vermelho!!');
    }
}

function limparNotificacoes() {
    // Enviar uma requisição AJAX para o servidor Flask
    fetch('/limparNotificacoes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify()
    })
    .then(response => {
        if (response.ok) {
          location.reload(); // recarrega a página após o comando ser executado
        } else {
          console.error('Erro ao executar o comando');
        }
      })
      .catch(error => {
        console.error('Erro ao executar o comando:', error);
      });
}

function confirmarAcao() {
    if (confirm("Deseja mesmo limpar todas as notificações?")) {
        // Ação a ser executada se o usuário clicar em "OK"
        limparNotificacoes()
        console.log("Ação confirmada!");
    } else {
        // Ação a ser executada se o usuário clicar em "Cancelar"
        console.log("Ação cancelada.");
    }
}    
