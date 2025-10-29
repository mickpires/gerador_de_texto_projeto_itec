from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import requests

# Para ajudar em testar se a ferramenta está correta. obtei por deixar separado assim
def wikipedia_search(topic):
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
        
        #title = primeira_pagina['title']
        content = primeira_pagina['extract']
        
        return content
        
    except requests.Timeout:
        raise TimeoutError(f"Timeout ao buscar Wikipedia para: '{topic}'")
    except requests.RequestException as e:
        raise ConnectionError(f"Erro de conexão ao acessar Wikipedia: {str(e)}")
    except (KeyError, IndexError) as e:
        raise ValueError(f"Erro ao processar resposta da API para: '{topic}'. Estrutura inesperada.")
            


class WikipediaSearchInput(BaseModel):
    topic:str = Field(description='the topic that will be used to search on wikipedia')

class WikipediaSearchTool(BaseTool):
    name:str = "wikipedia search tool"
    description:str = "It's to use to search topics on wikipedia"
    args_schema: Type[BaseModel] = WikipediaSearchInput

    def _run(self, topic:str):
        return wikipedia_search(topic)