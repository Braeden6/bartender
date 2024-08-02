from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from sqlalchemy import select
import openai
import csv
import openai
from app.core.database import get_db_session, async_engine, create_tables, AsyncSessionLocal, AsyncSession, Cocktail
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

async def generate_description_and_embeddings(cocktail_data):
    client = openai.AsyncClient()
    messages = [
        {
            "role": "system",
            "content": "write a description of this cocktail that will be used to be displayed to the user"
        },
        {
            "role": "user",
            "content": str(cocktail_data)
        }
    ]
    # gpt-4-turbo-preview // gpt-3.5-turbo-0125
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        max_tokens=250
    )
    description = response.choices[0].message.content.strip()
    
    embeddings_response = await client.embeddings.create(
        input=description,
        model="text-embedding-3-small"
    )
    embeddings = embeddings_response.data[0].embedding
    
    return description, embeddings

async def load_cocktails_from_csv(row):
    description, embeddings = await generate_description_and_embeddings(row)
    if description and embeddings:
        cocktail = Cocktail(
            name=row['Cocktail Name'],
            bartender=row['Bartender'],
            bar_company=row['Bar/Company'],
            location=row['Location'],
            ingredients=row['Ingredients'],
            garnish=row['Garnish'],
            glassware=row['Glassware'],
            preparation=row['Preparation'],
            notes=row['Notes'],
            description=description,
            drink_embeddings=embeddings
        )
    return cocktail
                
# @app.get('/upload')
async def upload(session: AsyncSession = Depends(get_db_session)):
    # await create_tables(engine=async_engine)
    path = 'C:/Users/bnorm/Desktop/repos/personal-projects/bartender-backend/hotaling_cocktails - Cocktails.csv'
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        done = 497
        # 684
        # 603
        for i, row in enumerate(reader):
            if i <= done:
                continue
            cocktail = await load_cocktails_from_csv(row)
            # print(cocktail.name)
            # raise Exception('stop')
            session.add(cocktail)
            await session.commit()
            print(i)
    return 'ok'

@app.get('/search')
async def search(query:str, session: AsyncSession = Depends(get_db_session)):
    client = openai.AsyncClient()
    embeddings_response = await client.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    )
    embeddings = embeddings_response.data[0].embedding
    stmt = select(
            Cocktail
        ).order_by(
            (1-Cocktail.drink_embeddings.cosine_distance(embeddings)).desc()
        ).limit(3)  
    results = await session.execute(stmt)
    final_results = [
        {
            'name': cocktail.name,
            'description': cocktail.description,
            'ingredients': cocktail.ingredients,
            'garnish': cocktail.garnish,
            'glassware': cocktail.glassware,
            'preparation': cocktail.preparation,
            'notes': cocktail.notes,
            'location': cocktail.location,
            'bar_company': cocktail.bar_company,
            'bartender': cocktail.bartender
        } for cocktail in results.scalars().all()
    ]
    return final_results



