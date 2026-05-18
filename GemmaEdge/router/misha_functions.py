import ollama



def call_misha_stream(user_input, model_name):
    """Calls the model and respects EVERYTHING in the Modelfile."""
    messages = [{'role': 'user', 'content': user_input}]

    try:


        return ollama.chat(
            model=model_name,
            messages=messages,
            stream=True

        )
    except Exception as e:
        print(f"\n[RUNTIME ERROR]: Engine stalled: {e}")
        return None