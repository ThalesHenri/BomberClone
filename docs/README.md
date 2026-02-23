# 💣 TH-BOMBER v1.0b - Manual de Operação



## 📜 1. DESCRIÇÃO DO SISTEMA
O **TH-BOMBER** é uma solução de entretenimento tático baseada em simulação de combate com explosivos. Desenvolvido sob a égide da **TH Sistemas**, o software utiliza a biblioteca `Pygame` para interface gráfica e o protocolo `TCP/IP` para comunicação entre terminais.

O sistema foi forjado para operar em redes locais ou remotas, permitindo que até 4 alquimistas se enfrentem em uma arena de pixels e glória.

---

## 🏗️ 2. ARQUITETURA ALQUÍMICA
O projeto adota o modelo **Cliente/Servidor Autoritativo**, garantindo a integridade dos dados e evitando feitiços de trapaça (Hacks).

* **TH_SERVER**: O Cérebro. Processa colisões, tempo de detonação e estado do Grid.
* **TH_CLIENT**: Os Olhos. Renderiza os sprites e captura o input do usuário.



---

## 🛠️ 3. REQUISITOS DE AMBIENTE
Para a correta transmutação dos scripts, certifique-se de possuir os seguintes componentes:

| Componente | Versão Mínima | Observação |
| :--- | :--- | :--- |
| **Python** | 3.10.x | Interpretador principal |
| **Pygame-CE** | 2.5.2+ | Motor de renderização e som |
| **Rede** | TCP/IP | Porta 5555 liberada no Firewall |

---

## 📂 4. ESTRUTURA DO DIRETÓRIO (INVENTÁRIO)
```text
src/
├ settings.py # Constantes (GRID_SIZE, TICK_RATE)
|         
├── server/             # O Cérebro (Lógica Pura)
│   ├── main.py         # Loop do Servidor
│   └── engine.py       # Cálculos de colisão e explosão
├── client/             # A Visão (Interface)
│   ├── main.py         # Janela Pygame e Loop de Eventos
│   └── network.py      # Driver de Comunicação Socket
├── assets/             # Artefatos Visuais e Sonoros
|    ├── sprites.png     # Gráficos 16-bit
|   └── sfx.wav         # Sons de detonação
└── docs/
     ├── README.md # Voce está aqui! :)


🚀 5. PROCEDIMENTOS DE EXECUÇÃO
I. Iniciando o Servidor (O Mestre)

Navegue até a raiz do projeto e execute o comando abaixo. O servidor ficará em "Listening" aguardando conexões.
Bash

python server/main.py

II. Iniciando o Cliente (Os Jogadores)

Em um novo terminal, execute o cliente apontando para o endereço IP do servidor (use 127.0.0.1 para testes na mesma máquina):
Bash

python client/main.py --connect 127.0.0.1

⚠️ 6. NOTAS DO DESENVOLVEDOR (TH)

    Aviso de Isenção: A TH Sistemas não se responsabiliza por mouses arremessados na parede ou amizades desfeitas após uma bomba bem posicionada no canto do mapa.

    Status do Projeto: Versão Beta (Funcionalidades básicas de movimento e bomba).

    Limitação Conhecida: Latência acima de 200ms pode causar "Ghosting" nos sprites.
    
    Créditos ao Youtuber S3GA SOUNDS pelo remake da música "Mr. Crowley" do lendário Ozzy Ousbourne usado no projeto

© 2026 TH SISTEMAS - O CONHECIMENTO LIBERTA!
