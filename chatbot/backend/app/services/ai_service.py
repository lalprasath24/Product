# import logging
# import openai
# from typing import List, Tuple
# from app.core.config import settings

# logger = logging.getLogger("remo_ai")

# # Configure OpenRouter API
# openai.api_key = settings.OPENROUTER_API_KEY
# openai.api_base = "https://openrouter.ai/api/v1"

# async def generate_response(query: str, relevant_docs: List[Tuple[str, float]]) -> str:
#     """Generate AI response using OpenRouter API with relevant documents"""
    
#     try:
#         logger.info(f"Generating AI response for query: {query[:50]}...")
        
#         # Prepare context from relevant documents
#         context = "\n\n".join([doc[0] for doc in relevant_docs])
#         logger.info(f"Using context from {len(relevant_docs)} documents")
        
#         # Create prompt for milk delivery company
#         prompt = f"""You are Remo AI, an assistant for a fresh milk delivery company. 
# Use the following company information to answer the customer's question accurately.

# Company Information:
# {context}

# Customer Question: {query}

# Please provide a helpful and accurate response based on the company information above. 
# If the information is not available in the context, politely say so.

# Response:"""

#         response = openai.ChatCompletion.create(
#             model="openai/gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are Remo AI, a helpful assistant for a milk delivery company."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=200,
#             temperature=0.7
#         )
        
#         ai_response = response.choices[0].message.content.strip()
#         logger.info("AI response generated successfully")
#         return ai_response
        
#     except Exception as e:
#         logger.error(f"AI response generation failed: {str(e)}")
#         return "I'm having trouble processing your request right now. Please try again later."