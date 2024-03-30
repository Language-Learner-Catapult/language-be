from openai import OpenAI
import io

client = OpenAI()

# TODO: Write prompt and functions
assistant = client.beta.assistants.create(
    name="Language Learner",
    instructions="",
    tools=[],
    model="gpt-3.5-turbo",
)


def run_assistant(thread_id):
    client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant.id,
        instructions=""
    )


def whisper_tts(text, voice="alloy"):
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )

    out = io.StringIO("")
    for data in response.iter_bytes():
        out.write(data)

    return out


def whisper_stt(audio_file):
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

    return transcription
