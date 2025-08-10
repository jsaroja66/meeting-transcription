from openai import OpenAI

client = OpenAI()

def transcribe_audio(file_path):
    """
    Transcribe the audio file at the given path using the Whisper API.

    Args:
        file_path (str): The path to the audio file to transcribe.

    Returns:
        str: The transcribed text from the audio file.
    """
    # Open the audio file
    with open(file_path, "rb") as audio_file:
        # Transcribe the audio using the Whisper API
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcription.text

def analyze_transcript_flow(text):
    """
    Analyze the flow of the transcript and create a natural split.

    Args:
        text (str): The transcribed text from the meeting.

    Returns:
        str: The organized transcript with a natural flow.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Organize the following text into a natural flow: {text}"}
        ]
    )
    return response.choices[0].message.content

def extract_key_points_and_action_items(text):
    """
    Extract key points and action items from the given text.

    Args:
        text (str): The organized transcript from the meeting.

    Returns:
        dict: A dictionary containing key points and action items.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Extract key points and action items from the following text: {text}"}
        ]
    )
    return response.choices[0].message.content

# Transcribe the audio file
audio_file_path = "audio_files/monday_meeting.mp3"
transcribed_text = transcribe_audio(audio_file_path)

# Analyze the transcript flow
organized_transcript = analyze_transcript_flow(transcribed_text)

# Save the organized transcript to a file
with open("sample_transcript.txt", "w") as file:
    file.write(organized_transcript)

# Extract key points and action items
key_points_and_action_items = extract_key_points_and_action_items(organized_transcript)
print("Key Points and Action Items:", key_points_and_action_items)


from fpdf import FPDF

def create_meeting_report(transcript, key_points_and_action_items, output_file):
    """
    Create a meeting report summarizing the key points and action items.

    Args:
        transcript (str): The organized transcript from the meeting.
        key_points_and_action_items (str): Extracted key points and action items.
        output_file (str): The path to save the generated report.

    Returns:
        None
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add title
    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(200, 10, txt="Meeting Report", ln=True, align='C')

    # Add transcript section
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt="Transcript", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, transcript)

    # Add key points and action items section
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt="Key Points and Action Items", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, key_points_and_action_items)

    # Save the PDF to the specified file
    pdf.output(output_file)

# Generate the meeting report
output_file = "meeting_report.pdf"
create_meeting_report(organized_transcript, key_points_and_action_items, output_file)
print(f"Meeting report saved to {output_file}")