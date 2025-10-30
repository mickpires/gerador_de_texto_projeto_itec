from pydantic import BaseModel, Field

class ReaderResults(BaseModel):
    """
    Modelo Pydantic para validar e estruturar os resultados do agente leitor.
    
    Esta classe define o formato esperado da saída do agente "Wikipedia Topic Extractor",
    garantindo que os dados estejam estruturados corretamente para as próximas etapas do processo.

    Fields:
        topics (list[str]): Lista Python contendo os tópicos que o pesquisador deve usar 
                           para buscar na Wikipedia. Cada tópico deve ser um título 
                           específico de artigo da Wikipedia em inglês.
        language (str): O idioma em que o resultado final deve ser escrito (ex: 'pt', 'en', 'es').

    Exemplo:
        >>> resultado_valido = ReaderResults(
        ...     topics=["Quantum mechanics", "Physics", "Albert Einstein"],
        ...     language="pt"
        ... )
        >>> print(resultado_valido.topics)  # ['Quantum mechanics', 'Physics', 'Albert Einstein']
        >>> print(resultado_valido.language)  # 'pt'

    Uso no contexto:
        - Valida a saída do reader_task (Wikipedia Topic Extractor)
        - Garante que os tópicos estejam no formato correto para pesquisa
        - Define o idioma para o writer_task produzir o artigo final
    """

    topics:list[str] = Field(description='a python list with the topics that the researcher must use to search on wikipedia')
    language:str = Field(description='the language that the final result must be written')

class WriterResults(BaseModel):
    """
    Modelo Pydantic para validar e estruturar os resultados do agente escritor.
    
    Esta classe define o formato esperado da saída do agente "Senior Writer",
    garantindo que o artigo gerado tenha a estrutura completa necessária.

    Fields:
        title (str): O título do artigo produzido pelo agente escritor.
        content (str): O conteúdo completo do artigo, que deve ter entre 300-2000 palavras.

    Exemplo:
        >>> artigo_valido = WriterResults(
        ...     title="Introdução à Mecânica Quântica",
        ...     content="A mecânica quântica é um dos pilares da física moderna... [texto completo]"
        ... )
        >>> print(artigo_valido.title)  # "Introdução à Mecânica Quântica"
        >>> print(len(artigo_valido.content.split()))  # Número aproximado de palavras

    Uso no contexto:
        - Valida a saída do writer_task (Senior Writer)
        - Garante que o artigo tenha título e conteúdo
        - Define a estrutura final retornada pela função principal gerar_texto()
    """
    title:str = Field(description='The title of the article made')
    content:str = Field(description='The content of the article')