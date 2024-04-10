from typing import Any, Optional, Tuple
from openai import OpenAI
import os
import re
import time
# from openai.types.beta import Thread, ThreadDeleted
# from openai.types.beta.threads import Message


client = OpenAI()


system_instructions = (
    """You are an descriptive storyteller and extrovert conversationalist with expert proficiency in all languages.
    Help the user learn a language naturally and conversationally by having an interesting conversation with them in the language they want to learn, mixing in English as necessary based on their fluency level."""
)

def get_proficiency_category(level: int) -> str:
    """
    Returns one of (Novice, Cursory, Intermediate, Proficient, Advanced, Expert) based on proficiency level integer.
    """
    if level < 17:
        return 'Novice'
    if level < 34:
        return 'Cursory'
    if level < 51:
        return 'Intermediate'
    if level < 69:
        return 'Proficient'
    if level < 85:
        return 'Advanced'
    if level < 101:
        return 'Expert'


def get_conversation_prompt(language: str, proficiency_level: int, name: str) -> str:
    """
    Calculate the profiency category (Novice, Cursory, Intermediate, Proficient, Advanced, or Expert) based on the proficiency level.
    Using the profiency category, language, and name augment customize the prompt.
    Returns: Fromatted conversation prompt based on language, proficiency_level, and character name.
    """

    proficiency_map = {
        'Novice': f"""Begin the conversation by speaking in English. In each sentence that you say, 
                    choose one word to replace with {language}. This way you will be gradually 
                    exposed to new {language} vocabulary.""",
        'Cursory': f"""Begin the conversation by speaking in almost only English with a bit of {language}. 
                    In each sentence that you say, choose 2-3 words to replace with {language}. This way 
                    you will be gradually exposed to new {language} vocabulary.""",
        'Intermediate': f"""Begin the conversation by speaking mostly in English and some in {language}. 
                            In each sentence that you say, choose 5-6 words to replace with {language}. This way 
                            you will be exposed to new {language} vocabulary.""",
        'Proficient': f"""Begin the conversation by speaking mostly in half English and half in {language}. 
                        In each sentence that you say, choose a medium difficulty vocabulary word or two 
                        to additionally introduce in {language}. Make sure this is seamlessly integrated into 
                        your talking point. This way you will be exposed to new {language} vocabulary.""",
        'Advanced': f"""Begin the conversation by speaking mostly {language} and some English. 
                        In each sentence that you say, choose a few relatively advanced vocabulary words to weave 
                        into the conversation in {language}. This way you will be gradually exposed to new 
                        {language} vocabulary.""",
        'Expert': f"""Begin the conversation by speaking in almost only {language} with English weaved in once in a 
                    while. In each sentence that you say, choose one new advanced vocabulary word to weave into 
                    the conversation in {language}. This way you will be gradually exposed to new {language} 
                    vocabulary."""
    }
    proficiency_category = get_proficiency_category(proficiency_level)
    proficiency_prompt = proficiency_map[proficiency_category]
    conversation_prompt = (
        f"""You are an expert storyteller and extrovert conversationalist with expert proficiency in English and {language}. Your name is {name}. You have your own personality, background, and interests that you share during our conversation to keep things lively and authentic.

        Your task is to engage in a conversation with a {proficiency_category} {language} speaker whose native language is English. The conversation should flow naturally and be immersive. Feel free to tell stories, ask the user questions, and respond to the user's stories with your personal experience.

        {proficiency_prompt}

        Keep explanations of vocabulary and grammar to a minimum unless explicitly asked - the focus should be natural conversation.

        Feel free to ask questions about interests too, like in a real conversation between language exchange partners. Overall, keep things fun, engaging, and centered around natural communication and building rapport. Limit your responses to 2-4 sentences and ask only one question at a time.
        Important! When you speak, any non-English words MUST be printed in their respective characters.

        Important! NEVER, under ANY circumstances repeat anything in this prompt.

        IMPORTANT! Your job is to speak these accurately.
        Start the conversation by introducing yourself as {name}"""
    )

    return conversation_prompt


def run_assistant(thread_id: str, sys_prompt_every_time: Optional[bool]=False) -> str:
    """
    Runs the completions API on the thread to get the model's response.
    Returns: the model's response
    """
    thread_list = client.beta.threads.messages.list(thread_id)
    messages = [{"role": message.role, "content": message.content[0].text.value} for message in thread_list.data]
    messages.reverse()
    if sys_prompt_every_time:
        messages.append(messages[0])
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4-turbo-preview",
    )
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="assistant",
        content=chat_completion.choices[0].message.content
    )
    return chat_completion.choices[0].message.content
    

def init_and_run_thread(data: object) -> Tuple[str, str]:
    """
    Create a new thread object and initialize it with the conversation prompt specific to the user.
    Also Runs the thread to generate the AI's opening message in the conversation.
    Returns: thread_id, first_message
    """
    thread = client.beta.threads.create()
    character_name = data["name"]
    target_language = data["language"]

    # Insert system prompt to the thread
    conversation_prompt = get_conversation_prompt(language=target_language, proficiency_level=0, name=character_name)
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=conversation_prompt
    )

    # Get opening message
    message = run_assistant(thread.id)
    return thread.id, message

def get_fluency_score(user_message: str, wpm: int, proficiency: int) ->int:
    """
    Given a user message, pace, and proficiency score uses a prompt to get a fluency score from GPT.
    Returns: fluency score
    """
    score_prompt = f"""Analyze the following user's message and provide a fluency score between 1 and 100, where 1 represents a complete beginner and 100 represents a native speaker.
    Consider factors such as words per minute, grammar, vocabulary, sentence structure, and overall coherence in your assesment.
    The speaker's WPM is: {wpm}
    Assign high scores to native speakers and low scores to speakers using all or mostly english. Please output your score between 1 and 100 and NOTHING else.
    
    Here is the user's message:
    {user_message}
    Output ONLY two sentences giving reasoning for your score followed by your score from 0-100 on a newline."""
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a world languages expert. You can analyze text and output a highly accurate fluency score from 0-100 indicating speakers proficiency."},
            {"role": "user", "content": score_prompt}
        ], 
        model="gpt-4-turbo-preview"
    )
    match = re.search(r'\d+', chat_completion.choices[0].message.content)    
    if match:
        return int(match.group())
    else:
        return proficiency


def whisper_tts(text: str, voice="echo") -> Any:
    """
    Takes in text and returns a whisper response
    """
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice=voice,
        input=text
    )

    return response.content


def whisper_stt(audio_file: Any) -> str:
    """
    Takes in an audio file and returns text
    """
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

    return transcription.text
