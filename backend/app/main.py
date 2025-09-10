from chat_engine import load_chat_engine

chat_engine = load_chat_engine()

def generate_response(user_input: str) -> str:
    print(f"user input: {user_input}")
    response = chat_engine.chat(user_input).response
    print(f"response: {response}")
    return response

generate_response("你是誰？")
generate_response("我上一個問題是什麼？")