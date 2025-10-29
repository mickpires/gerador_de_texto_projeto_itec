from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from itec import OPENROUTER_API_KEY
from itec.tool import WikipediaSearchTool
from itec.pydantic import  ReaderResults, ResearcherResults, WriterResults

llm = ChatOpenAI(
    model = 'openrouter/deepseek/deepseek-chat-v3.1:free',
    base_url = 'https://openrouter.ai/api/v1',
    openai_api_key = OPENROUTER_API_KEY
)

wikipedia_search_tool = WikipediaSearchTool()

reader = Agent(
    role = "Reader",
    goal = "Understand what are the topics the user is requesting to be searched on wikipedia and what language the user wants the result",
    backstory = 'you are an expert on analyze text' 
                'you understand what are the key topics the users wants to know about',
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
    goal = 'write an article with a title and a content which has more than 200 words and less than 2000 words',
    backstory = 'you are a senior writer who knows how to make engaging text'
                'You like to make the reader feels curious about the topics that you are writing',
    allow_delegation= False,
    llm = llm
)

reader_task = Task(
    name = 'reader_task',
    description="""
    Analyze the user prompt: {prompt}
    Identify and extract the main topics that need to be researched on Wikipedia.
    Return ONLY a JSON object with a single key "topics" containing an array of topic strings.
    """,
    expected_output="A JSON object with key 'topics' containing array of research topics",
    output_pydantic=ReaderResults,
    agent=reader
)
reader_task.output

researcher_task = Task(
    name="researcher_task",
    description="""
    Search EACH of the topics recognized by the reader_task on English Wikipedia using the wikipedia search tool separately:
    You're gonna use the tool on the topic, then you're gonna save text extracted by the tool on a python list called texts.
    You're gonna do this process for each topic.
    """,
    expected_output = """
    the expected output is a python list with each text extracted as follow:
    texts = [the text from topic 1, the text from topic 2, ..., the text from topic n]
""",
    output_pydantic = ResearcherResults,
    tools = [wikipedia_search_tool],
    agent = researcher
)

writer_task = Task(
    name = 'writer_task',
    description = 'Get all the texts found on the wikipedia by the researcher  in the researcher_task and use it to produce the article',
    expected_output= 'The article should have a title and a content with more than 200 words and less than 2000'
                      'The article must be wrote in {output_language}',
    output_pydantic= WriterResults,
    agent = writer
)

article_creater_crew = Crew(
    agents = [reader, researcher, writer],
    tasks = [reader_task, researcher_task, writer_task],
    verbose=True
)