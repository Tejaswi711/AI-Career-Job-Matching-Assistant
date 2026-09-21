from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import LLMChain
from dotenv import load_dotenv
from prompt import system_prompt

load_dotenv()
llm=ChatOpenAI(model='gpt-4o-mini')
memory=ConversationBufferMemory(memory_key='history',return_messages=True)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{query}")
])
chatbot = LLMChain(llm=llm,prompt=prompt,memory=memory)


while True:
    question = input("You: ")

    if question.lower() == "bye":
        print("🤖: Thank you!")
        break

    response = chatbot.invoke(question)
    print("🤖:", response['text'])