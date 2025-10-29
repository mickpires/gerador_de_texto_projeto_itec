from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import requests


class WikipediaSearchInput(BaseModel):
    topic:str = Field(description='the topic that will be used to search on wikipedia')

class WikipediaSearchTool(BaseTool):
    name:str = "wikipedia search tool"
    description:str = "It's to use to search topics on wikipedia"
    args_schema: Type[BaseModel] = WikipediaSearchInput

    def _run(self, topic:str):
        API_URL = "https://en.wikipedia.org/w/api.php"
        params = {
        "action": "query",
        "format": "json",
        "titles": topic,           # Artigo que queremos ler
        "prop": "extracts",           # Pede o conteúdo do artigo
        "explaintext": True           # Texto simples, sem HTML
        }

        headers = {'User-Agent': 'itec/1.0 (mickael.pires@outlook.com)'}
        response = requests.get(API_URL, params = params, headers=headers)
        if response.status_code == 200:
            dados = response.json()
        else:
            raise(f'erro. código {response.status_code} ')
        return dados