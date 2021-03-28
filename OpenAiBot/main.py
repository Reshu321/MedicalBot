import discord
import os
import openai
from keep_alive import keep_alive

openai.api_key = "sk-8KrCMtgTZlwtN3v7P5IrFqgYmhktS7ElnsInhAJC"
completion = openai.Completion()

start_chat_log = '''The following is a conversation with a medical bot assistant. The AI assistant is helpful, answers medical questions, and is very friendly.

Human: What is a blood cell?
Is this a medical question: Yes 
medical bot: A blood cell, also called a hematopoietic cell, hemocyte, or hematocyte, is a cell produced through hematopoiesis and found mainly in the blood
###
Human: What is a car?
Is this a medical question: No 
medical bot: I'm sorry I only answer medical questions
###
Human: Define virus
Is this a medical question: Yes 
medical bot: A virus is a small infectious agent that replicates only inside the living cells of other organisms
###
Human: Define medical
Is this a medical question: Yes 
medical bot: Medical is the science and art of healing
###
Human: Tell me about chocolate?
Is this a medical question: No 
medical bot: I'm sorry I only answer medical questions
###
Human:
'''

def ask(question, chat_log=None):
  if chat_log is None:
      chat_log = start_chat_log
  prompt = f'{chat_log} {question} \n:'
  response = completion.create(
    prompt=prompt, engine="davinci", temperature=0.15, 
      top_p=1, frequency_penalty=0, stop=['###', 'Human', '.'], presence_penalty=0.6, best_of=1,
      max_tokens=300)
  answer = response.choices[0].text.strip()

  answer = answer.split("\n")
  count = 0
  for i in answer:
    count+=1
  return answer[count- 1]

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if (message.content.startswith("#")):
      response = ask(message.content.split(" ", 1)[1])
      await message.channel.send(response)
 
 
 
 
keep_alive()     
client.run(os.getenv('TOKEN'))  