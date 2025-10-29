# Gerador de texto para o teste prático para a vaga de programador IA teste prático

## Sumário

- [Instalação](#instalação)
- [Exemplo de Uso](#exemplo-de-uso)


## Instalação

Para instalar o repositório, execute no terminal

   ```bash
   git clone https://github.com/mickpires/gerador_de_texto_projeto_itec.git
   ```

Para instalar as dependências do código, recomendo utilizar `uv` que é um gerenciador de projetos. Ele pode ser facilmente instalado usando `pip`

```bash
    pip install uv
```

Após ter feito a instalação do `uv`, é somente necessário entrar no diretório do projeto e executar

```bash
uv run run.py
```

Ele irá baixar as dependências contidas no arquivo `pyproject.toml` e executar o código. É necessário então colocar na sua barra de navegação do navegador

```bash
localhost:5000
```

e será apresentado a API

![alt text](imagens_readme/image.png)

## Exemplo de uso

Para a API funcionar é necessário que o usuário forneça uma _key_ do Gemini API que pode ser facilmente criada. A seguir um link do site do google ensinando como que faz para criar uma _key_. Não é necessário inserir nenhum cartão de crédito para criar https://ai.google.dev/gemini-api/docs/quickstart?hl=pt-br.
Após feita a _key_ e inserida no espaço demarcado, o usuário pode escrever sobre o que o artigo deve ser. Abaixo está uma execução e de como que deve ser esperado o resultado. O artigo tem um titulo e o conteúdo.

![alt text](imagens_readme/resultado.png)