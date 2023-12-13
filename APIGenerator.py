import openai
import config

openai.api_key = "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"
print(f'openai.api_key :', {openai.api_key})


def openAIQuery(query):
    response = openai.Completion.create(
      engine="davinci-instruct-beta-v3",
      prompt=query,
      temperature=0.8,
      max_tokens=1000,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0)

    if 'choices' in response:
        if len(response.choices) > 0:
            answer = response.choices[0].text
        else:
            answer = 'Opps sorry, you beat the AI this time'
    else:
        answer = 'Opps sorry, you beat the AI this time'

    return answer


if __name__ == '__main__':
    if not openai.api_key:
        print(f'api_key is not set')
        exit(0)
        
    query = 'generate a Java Programming Questions bank of 20 question of hard level difficulty'
    try:
        response = openAIQuery(query)
        print(f'Response : {response}')
    except Exception as e:
        print(f'Exception : {str(e)}')