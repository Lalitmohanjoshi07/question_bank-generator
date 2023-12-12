import openai
openai.api_key = "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"


def generateQuestion(topic, difficulty='variable'):
    messages = []
    
    # be as specific as possible in the behavior it should have
    system_content = '''you are a university teacher from technical field'''
    
    messages.append({"role": "system", "content": system_content})
    
    prompt_text = 'Make a question bank on '+topic+' with difficulty'+difficulty'
    
    messages.append({"role": "user", "content": prompt_text})
    
    response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=messages,
                            max_tokens=1000,
                            temperature=0.5)
    return (response.choices[0].message.content)

# topic-name and difficulty
topic= input('enter topic name: ')
difficulty= input('enter difficulty: ')

#calling the function to generate 
res= generateQuestion(topic, difficulty)
print(res)
