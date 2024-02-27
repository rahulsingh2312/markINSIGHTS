from dotenv import load_dotenv
import os
# Load .env file
load_dotenv()
# Get OpenAI keys from .env file
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


from langchain import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def generate_brochure(product:str,age_group:str):
    product_schema=ResponseSchema(
        name="description",
        description="This is the description for the given product"
    )
    tagline_schema=ResponseSchema(
        name="tagline",
        description="This is the tagline for the given product"
    )
    response_schema=[product_schema,tagline_schema]
    output_parser=StructuredOutputParser.from_response_schemas(response_schema)
 
  
    from langchain_core.prompts import (
        ChatPromptTemplate,
        # MessagesPlaceholder,
        # HumanMessagePromptTemplate,
        # SystemMessagePromptTemplate,
    )

    
    format_instructions=output_parser.get_format_instructions()
    prompt_template="""
            Generate a brochure for the given product  {product} with a catchy tagline for the age group {age_group}.
            {format_instructions}
            """ 

    prompt =PromptTemplate(
    input_variables=["product","age_group"],
    template=prompt_template,
     partial_variables={"format_instructions": output_parser.get_format_instructions()},
)
   
    return model.invoke(prompt.format(product=product,age_group=age_group))
print(generate_brochure(product="car",age_group="18-25"))

