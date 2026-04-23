# Sistema Multicast (Aula de Sistemas Distribuidos)

Este projeto implementa comunicacao **UDP multicast** simples:

- `sender.py`: envia mensagens para um grupo multicast.
- `receiver.py`: recebe mensagens desse grupo.

## Requisitos

- Linux no computador
- Celular Android na mesma rede Wi-Fi do computador
- Python 3.8+

## Como funciona

1. O emissor envia para um IP multicast (padrao: `239.255.10.10`) e porta UDP (`5007`).
2. Todo receptor que entrou nesse grupo recebe a mensagem.
3. Com `TTL=1`, o trafego fica restrito a rede local (ideal para demo em sala).

## Passo a passo rapido (computador + celular)

### 1) No celular (Android) com Termux

Instale o **Termux** (preferencialmente via F-Droid), depois:

```bash
pkg update -y
pkg install -y python
```

Copie o arquivo `receiver.py` para o celular (por Git, WhatsApp, Drive, cabo etc.) e rode:

```bash
python receiver.py --group 239.255.10.10 --port 5007
```

Quando aparecer `Listening on multicast group...`, o celular esta pronto para receber.

### 2) No computador (emissor)

No diretorio deste projeto, envie uma mensagem unica:

```bash
python sender.py --group 239.255.10.10 --port 5007 --message "Teste multicast para o celular"
```

Ou modo interativo (digite varias mensagens):

```bash
python sender.py --group 239.255.10.10 --port 5007
```

## Exemplos uteis

Enviar mensagem repetidamente a cada 2 segundos:

```bash
python sender.py --message "Heartbeat" --interval 2
```

Forcar interface de saida no emissor (util em algumas redes):

```bash
python sender.py --message "Teste" --interface 192.168.0.10
```

Escutar por uma interface especifica (quando necessario):

```bash
python receiver.py --interface 192.168.0.20
```

## Solucao de problemas (importante para apresentacao)

- Celular e computador precisam estar na **mesma Wi-Fi**.
- Alguns roteadores bloqueiam multicast em modo de economia/isolamento de cliente.
- Em algumas redes, desativar dados moveis no celular ajuda a forcar rota pelo Wi-Fi.
- Se nao receber nada, teste primeiro dois receptores no proprio notebook para validar o script.

## Roteiro de apresentacao (30-60s)

1. Abra `receiver.py` no celular e inicie a escuta.
2. No notebook, envie uma mensagem com `sender.py`.
3. Mostre a mesma mensagem aparecendo no celular em tempo real.
4. Explique: "Um emissor, varios receptores, sem conexao ponto-a-ponto".
