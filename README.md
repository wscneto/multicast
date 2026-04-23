# Sistema Multicast (Aula de Sistemas Distribuidos)

Obs.: feito utilizando IA

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