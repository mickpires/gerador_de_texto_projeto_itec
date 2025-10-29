from pydantic import BaseModel, Field

class ReaderResults(BaseModel):
    topics:list[str] = Field(description='a python list with the topics that the researcher must use to search on wikipedia')

class ResearcherResults(BaseModel):
    contents:list[str] = Field(description='A python list of the texts extracted from the wikipedia for each topic')

class WriterResults(BaseModel):
    title:str = Field(description='The title of the article made')
    content:str = Field(description='The content of the article')