from crewai import Agent, Task, Crew, LLM
from itec.tool import WikipediaSearchTool
from itec.pydantic import  ReaderResults, WriterResults

def gerar_texto(prompt, key):
    """
    Gera um artigo completo pesquisando e processando informações da Wikipedia.
    
    Esta função utiliza um sistema multiagente para:
    1. Identificar tópicos relevantes no prompt do usuário
    2. Pesquisar artigos correspondentes na Wikipedia
    3. Gerar um artigo original baseado no conteúdo pesquisado
    
    Args:
        prompt (str): O tópico ou solicitação do usuário para o artigo desejado.
                     Pode ser em qualquer idioma, mas os tópicos serão identificados
                     em inglês para pesquisa.
        key (str): Chave da API para o serviço de modelo de linguagem (LLM).
    
    Returns:
        tuple: Uma tupla contendo:
            - title (str): Título do artigo gerado
            - content (str): Conteúdo do artigo (entre 200-2000 palavras)
    
    Processo:
        1. Extração de Tópicos (Reader Agent):
           - Analisa o prompt e identifica títulos específicos de artigos da Wikipedia
           - Determina o idioma desejado para o artigo final
           - Retorna tópicos em inglês para pesquisa
        
        2. Pesquisa (Researcher Agent):
           - Busca cada tópico individualmente na Wikipedia
           - Coleta o conteúdo textual dos artigos encontrados
        
        3. Escrita (Writer Agent):
           - Sintetiza o conteúdo pesquisado em um artigo coeso
           - Gera texto no idioma original do prompt
           - Produz conteúdo entre 300-2000 palavras com título
    
    Exemplo:
        >>> titulo, conteudo = gerar_texto(
        ...     "Explique os conceitos básicos da física quântica",
        ...     "sua_chave_api"
        ... )
        >>> print(f"Título: {titulo}")
        >>> print(f"Conteúdo: {conteudo}")
    
    Notas:
        - Usa o modelo Gemini 2.5 Flash como LLM base
        - Temperatura configurada em 0.7 para equilíbrio entre criatividade e precisão
        - Requer conexão com internet para acesso à Wikipedia
        - O conteúdo gerado é baseado em fontes da Wikipedia mas reescrito originalmente
    """

    llm = LLM(
        model="gemini/gemini-2.5-flash",
        api_key=key,
        temperature=0.7
    )

    wikipedia_search_tool = WikipediaSearchTool()

    reader = Agent(
        role = "Wikipedia Topic Extractor",
        goal = "Extract specific Wikipedia article titles from user requests that can be directly searched in Wikipedia API",
        backstory = '''You are an expert at analyzing user requests and identifying the exact Wikipedia article titles 
        that would provide the most relevant information. You understand that Wikipedia articles have specific titles 
        and you extract only main concept titles, not descriptive phrases.''',
        allow_delegation=False,
        llm = llm
    )

    researcher = Agent(
        role = "Senior Researcher",
        goal = "Do excellent research on wikipedia",
        backstory= 
            "You're a Senior Researcher."
            "Who knows to search wikipedia using the tool provided",
        allow_delegation = False,
        tools=[wikipedia_search_tool],
        llm = llm
    )


    writer = Agent(
        role = 'senior writer',
        goal = 'write an article with a title and a content which has more than 300 words and less than 2000 words',
        backstory = 'you are a senior writer who knows how to make engaging text'
                    'You like to make the reader feels curious about the topics that you are writing',
        allow_delegation= False,
        llm = llm
    )

    reader_task = Task(
        name = 'wikipedia_topic_extraction',
        description="""
        Analyze the user prompt: {prompt}
        
        CRITICAL INSTRUCTIONS:
        - Extract ONLY main Wikipedia article titles, not descriptive phrases
        - Return concise article titles like "Physics", "Classical mechanics", "Quantum physics"
        - DO NOT return phrases like "Physics definition and scope" or "History of Physics concepts"
        - Each topic should be a direct Wikipedia article title
        - Focus on core concepts mentioned in the prompt
        - Identify the language that the user wants the final text by the prompt
        - guarantee that the topics are in english even though the prompt may be written in another language
        to be able to use to search on wikipedia
        
        Return ONLY a JSON object with a single key "topics" containing an array of Wikipedia article title strings
        and the language that the user wants the final text.
        """,
        expected_output="A JSON object with key 'topics' containing array of direct Wikipedia article titles and the language",
        output_pydantic=ReaderResults,
        agent=reader
    )

    researcher_task = Task(
        name="researcher_task",
        description="""
        Search EACH of the topics recognized by the reader_task on English Wikipedia using the wikipedia search tool separately:
        You're gonna use the tool on the topic, then you're gonna save text extracted by the tool on a python list called texts.
        You're gonna do this process for each topic.
        """,
        expected_output = """
        the expected output is a python list with each text extracted as follow:
        contents = [the text from topic 1, the text from topic 2, ..., the text from topic n]
    """,
        tools = [wikipedia_search_tool],
        agent = researcher
    )

    writer_task = Task(
        name = 'writer_task',
        description = 'Get all the texts found on the wikipedia by the researcher  in the researcher_task and use it to produce the article',
        expected_output= 'The article should have a title and a content with more than 200 words and less than 2000'
                        'The article must be wrote in the language identified on wikipedia_topic_extractor',
        output_pydantic= WriterResults,
        agent = writer
    )

    article_creater_crew = Crew(
        agents = [reader, researcher, writer],
        tasks = [reader_task, researcher_task, writer_task],
        verbose=False
    )

    inputs = {'prompt': prompt}
    results = article_creater_crew.kickoff(inputs = inputs)
    title, content = results['title'], results['content']
    return title, content