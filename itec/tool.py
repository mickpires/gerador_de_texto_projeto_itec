from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import requests

def wikipedia_search(topic):
    """
    Realiza uma busca na Wikipedia em inglês e extrai o conteúdo textual de um artigo.
    
    Esta função consulta a API pública da Wikipedia para obter o conteúdo completo
    de um artigo específico em formato de texto simples (sem formatação HTML).
    
    Args:
        topic (str): O título do artigo da Wikipedia a ser pesquisado (em inglês)
    
    Returns:
        str: O conteúdo textual completo do artigo da Wikipedia
    
    Raises:
        TimeoutError: Quando a requisição excede o tempo limite de 10 segundos
        ConnectionError: Quando ocorrem problemas de conexão com a API
        ValueError: Quando o artigo não é encontrado ou não possui conteúdo extraível
        requests.HTTPError: Quando a API retorna um código de status HTTP inválido
    
    Exemplo:
        >>> conteudo = wikipedia_search("Quantum mechanics")
        >>> print(conteudo[:100])  # Primeiros 100 caracteres do artigo
    
    Processo:
        1. Configura os parâmetros da API Wikipedia para extrair texto simples
        2. Envia requisição com headers apropriados e timeout
        3. Processa a resposta JSON e extrai o conteúdo da primeira página
        4. Valida se a página existe e possui conteúdo
        5. Retorna o texto extraído ou levanta exceções específicas
    
    Notas:
        - Usa a Wikipedia em inglês (en.wikipedia.org)
        - Remove formatação HTML (explaintext=True)
        - Inclui User-Agent apropriado para identificação
        - Timeout de 10 segundos para evitar bloqueios
    """
        
    API_URL = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": topic,
        "prop": "extracts",
        "explaintext": True
    }

    headers = {'User-Agent': 'itec/1.0 (mickael.pires@outlook.com)'}
    
    try:
        response = requests.get(API_URL, params=params, headers=headers, timeout=10)
        
        if response.status_code != 200:
            raise requests.HTTPError(f"Erro HTTP {response.status_code} ao acessar Wikipedia para o tópico: '{topic}'")
        
        dados = response.json()
        paginas = dados.get('query', {}).get('pages', {})
        
        if not paginas:
            raise ValueError(f"Nenhuma página encontrada para o tópico: '{topic}'")
        
        primeira_pagina = list(paginas.values())[0]
        
        # Verifica se a página existe (não é uma página de desambiguação ou inexistente)
        if 'missing' in primeira_pagina:
            raise ValueError(f"Página não encontrada na Wikipedia: '{topic}'")
        
        if 'extract' not in primeira_pagina or not primeira_pagina['extract']:
            raise ValueError(f"Página encontrada mas sem conteúdo extraível para: '{topic}'")
        
        content = primeira_pagina['extract']
        
        return content
        
    except requests.Timeout:
        raise TimeoutError(f"Timeout ao buscar Wikipedia para: '{topic}'")
    except requests.RequestException as e:
        raise ConnectionError(f"Erro de conexão ao acessar Wikipedia: {str(e)}")
    except (KeyError, IndexError) as e:
        raise ValueError(f"Erro ao processar resposta da API para: '{topic}'. Estrutura inesperada.")
            


class WikipediaSearchInput(BaseModel):
    """
    Esquema Pydantic para validação do parâmetro de entrada da ferramenta.
    
    Fields:
        topic (str): O tópico que será usado para buscar na Wikipedia
                   com descrição explicativa para os agentes
    """
    topic:str = Field(description='the topic that will be used to search on wikipedia')

class WikipediaSearchTool(BaseTool):
    """
    Ferramenta de busca na Wikipedia para integração com framework CrewAI.
    
    Esta classe encapsula a funcionalidade de busca na Wikipedia em uma ferramenta
    padronizada que pode ser utilizada por agentes de IA no ecossistema CrewAI.
    
    Attributes:
        name (str): Nome identificador da ferramenta - "wikipedia search tool"
        description (str): Descrição da funcionalidade para os agentes
        args_schema (Type[BaseModel]): Esquema de validação dos parâmetros de entrada
    
    Métodos:
        _run(topic: str) -> str:
            Executa a busca na Wikipedia e retorna o conteúdo do artigo
            
    Exemplo de uso em um agente:
        >>> tool = WikipediaSearchTool()
        >>> resultado = tool._run("Artificial intelligence")
        >>> print(resultado)
    
    Herança:
        BaseTool: Classe base do CrewAI para criação de ferramentas
    """

    name:str = "wikipedia search tool"
    description:str = "It's to use to search topics on wikipedia"
    args_schema: Type[BaseModel] = WikipediaSearchInput

    def _run(self, topic:str):
        return wikipedia_search(topic)