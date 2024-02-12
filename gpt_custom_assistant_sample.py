import os
import os.path
from openai import OpenAI
import time


def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )


def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")
    
def create_thread_and_run(user_input):
    custom_gpt_id = 'asst_eysn7gHx9SvlpYcYeTa2XLj8'
    thread = client.beta.threads.create()
    run = submit_message(custom_gpt_id, thread, user_input)
    return thread, run
    
# Pretty printing helper
def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()


# Waiting in a loop
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


if __name__ == "__main__":
  
  # Set your OpenAI API key

  client = OpenAI()
  OpenAI.api_key = os.getenv('OPENAI_API_KEY')
  custom_gpt_id = 'asst_id_here'

  completion = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Say this is a test",
    max_tokens=7,
    temperature=0
  )

  print(completion.choices[0].text)
  
  # Emulating concurrent user requests
  thread1, run1 = create_thread_and_run(
    "I need to solve the equation `3x + 11 = 14`. Can you help me?"
  )
  # Wait for Run 1
  run1 = wait_on_run(run1, thread1)
  pretty_print(get_response(thread1))
