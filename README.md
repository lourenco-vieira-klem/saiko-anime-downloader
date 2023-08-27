# SAIKO ANIMES DOWNLOADER

Script de download dos episódios semanais dos animes transmitidos no japão.

## Criação do ambiente virtual.

```bash
pipenv install -r requirements.txt
```
```bash
pipenv shell
```

## Execute o comendo abaixo para realizar o download do titulo desejado.

```bash
python main.py <url>

```
## Conforme o download for ocorrendo, uma barra de progresso exibira a taxa de download e tempo gasto.

```bash
anime em exibição [Saiko-Animes]_Liar_Liar_-_09_[WEB-1080p]_[Oficial].mp4
 57%|████████████████████████████████                                                        | 295M/514M [00:24<00:17, 12.2MiB/s]

```
## Todos os animes são salvos na pasta padrão downloads criada na raiz do projeto.
## Os episódios são salvos em pastas de acordo com a temporada ex: S1. S2 ....
