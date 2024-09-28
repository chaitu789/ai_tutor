from huggingface_hub import InferenceApi

api_key = "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"  # Replace with your Hugging Face API token
inference_api = InferenceApi(repo_id="eldestboom/ai_tutor", token=api_key)
import time
from huggingface_hub import InferenceApi


def send_query_get_response_hf(inference_api, user_question, repo_id):
    """
    Sends the user's query to the Hugging Face model and retrieves the response.

    :param inference_api: InferenceApi object initialized with the Hugging Face model.
    :param user_question: The query or question to ask the model.
    :param repo_id: Hugging Face repository ID containing educational materials (used to customize responses).
    :return: The model's response or an error message if the process takes too long.
    """
    # Customize the user question to include reference to relevant educational materials
    user_question += ' and tell me which file are the top results based on your similarity search (e.g., "Present Value Relations" in "Lec 2-3.pdf" under slides 20-34).'

    # Send the user question to the Hugging Face inference API and start a timer
    start_time = time.time()

    try:
        # Send the query to Hugging Face model
        response = inference_api(user_question)

        # Check if the response is taking too long (more than 60 seconds)
        if time.time() - start_time > 60:
            print("Took too long to get a response")
            return "The query took too long to process. Please try again."

        # Extract the text content from the model's response
        return response['generated_text'] if 'generated_text' in response else "No response available."

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Server issue, try again"
