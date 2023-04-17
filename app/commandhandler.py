import os
import openai
import numpy as np
import file_dbaccess
from loguru import logger
from datetime import datetime
from openai.embeddings_utils import get_embedding, cosine_similarity


EMBEDDING_MODEL = 'text-embedding-ada-002'
COMPLETIONS_MODEL = "text-davinci-003"
QUESTION_COMPLETIONS_API_PARAMS = {
    # We use temperature of 0.0 because it gives the most predictable, factual answer.
    "temperature": 0.0,
    "max_tokens": 200,
    "model": COMPLETIONS_MODEL,
}

REGULAR_COMPLETIONS_API_PARAMS = {
    "temperature": 0.5,
    "max_tokens": 500,
    "model": COMPLETIONS_MODEL,
}

class CommandHandler:
    def __init__(self):
        self.openai = openai
        self.openai.api_key = os.getenv("OPENAI_KEY")
        self.db = file_dbaccess.LocalFileDbAccess("database.csv")
        self.db.ensureExists()
        

    
    def execute_command(self, msg:str):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.df = self.db.get()
        """
        Check the message and exexute relevant command
        """
        if msg.startswith("/h"):
            return("Commands:\n\n/q [question] - Ask a question\n/s [message] - Save a message\n/f [message] - Find related messages\n/h - Show this help menu")

        # Question answering
        elif msg.startswith("/q "):
            # Get the question
            question = str(msg.split("/q ")[1])
            # Construct the prompt
            prompt = self.construct_prompt(question, self.df, top_n=3)
            # Get the answer
            response = openai.Completion.create(prompt=prompt, **QUESTION_COMPLETIONS_API_PARAMS)
            return response["choices"][0]["text"]

        elif msg.startswith("/s "):
            data_to_save = msg.split("/s ")[1]
            # Save the massage to the database
            text_embedding = get_embedding(data_to_save, engine='text-embedding-ada-002')
            self.df = self.df.append({"time":dt_string,"message":data_to_save, "ada_search": text_embedding},ignore_index=True)
            self.db.save(self.df)
            return "Message saved successfully!"

        # Find related messages
        elif msg.startswith("/f "):
            query = str(msg.split("/f ")[1])
            most_similar = self.return_most_similiar(query, self.df, top_n=3)
            msg_reply = ''
            for i in range(len(most_similar)):
                msg_reply += most_similar.iloc[i]['time'] + ': ' + most_similar.iloc[i]['message'] + '\n'
            return msg_reply

        # Placeholder for other commands
        elif msg.startswith("/"):
            return("Sorry, I don't understand the command")

        # Get a regular completion
        else:
            # Just get a regular completion from the model
            COMPLETIONS_API_PARAMS = {
                # We use temperature of 0.0 because it gives the most predictable, factual answer.
                "temperature": 0.0,
                "max_tokens": 200,
                "model": COMPLETIONS_MODEL,
            }
            response = openai.Completion.create(prompt=msg, **REGULAR_COMPLETIONS_API_PARAMS)
            print (response)
            return response["choices"][0]["text"]
            


    def construct_prompt(self,question, df, top_n=3):
        # Get the context
        context = self.generate_context(question, df, top_n)
        header =  header = """Answer the question in details, based only on the provided context and nothing else, and if the answer is not contained within the text below, say "w.", do not invent or deduce!\n\nContext:\n"""
        return header + "".join(context) + "Q: " + question + "\n A:"

    def generate_context(self,question, df, top_n=3):
        most_similiar = self.return_most_similiar(question, df, top_n)
        # Get the top 3 most similar messages
        top_messages = most_similiar["message"].values
        # Concatenate the top 3 messages into a single string
        context = '\n '.join(top_messages)
        return context

    def return_most_similiar(self,question, df, top_n=3):
        try:
            # Get the embedding for the question
            logger.warning(1)
            question_embedding = get_embedding(question, engine='text-embedding-ada-002')
            logger.warning(2)
            # Get the embedding for the messages in the database
            df["ada_search"] = df["ada_search"].apply(eval).apply(np.array)
            logger.warning(3)
            # Get the similarity between the question and the messages in the database
            df['similarity'] = df.ada_search.apply(lambda x: cosine_similarity(x, question_embedding))
            logger.warning(4)
            # Get the index of the top 3 most similar message
            most_similiar = df.sort_values('similarity', ascending=False).head(top_n)
            logger.warning(5)
            return most_similiar
        except Exception as e:
            logger.error(str(e))

