from crewai import Agent, Task, Crew, LLM
from langchain_openai import ChatOpenAI
#from itec import OPENROUTER_API_KEY
from itec import GOOGLE_API_KEY
from itec.tool import WikipediaSearchTool
from itec.pydantic import  ReaderResults, ResearcherResults, WriterResults
from langchain_google_genai import ChatGoogleGenerativeAI

# llm = ChatOpenAI(
#     model = 'gemini-2.0-flash-live',
#     #base_url = 'https://openrouter.ai/api/v1',
#     base_url = 'https://generativelanguage.googleapis.com/v1beta/openai/',
#     openai_api_key = GOOGLE_API_KEY
#     #openai_api_key = OPENROUTER_API_KEY
# )

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=GOOGLE_API_KEY,
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
    goal = 'write an article with a title and a content which has more than 200 words and less than 2000 words',
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
    
    Return ONLY a JSON object with a single key "topics" containing an array of Wikipedia article title strings.
    """,
    expected_output="A JSON object with key 'topics' containing array of direct Wikipedia article titles",
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