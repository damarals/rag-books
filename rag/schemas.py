from langchain_core.pydantic_v1 import BaseModel, Field


class Module(BaseModel):
    title: str = Field(description="Título do módulo")
    quote: str = Field(
        description="Frase engraçada/filosófica para o módulo, entre aspas. Caso já exista a frase, cite quem disse, se foi você mesmo coloque 'IA' como fonte."
    )
    content: str = Field(description="Conteúdo do módulo")


class Section(BaseModel):
    title: str = Field(description="Título da seção")
    content: str = Field(description="Conteúdo da seção")


class Subsection(BaseModel):
    title: str = Field(description="Título da subseção")
    content: str = Field(description="Conteúdo da subseção")
