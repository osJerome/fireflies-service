def parse_transcript(transcript_data):
    """
    Parses transcript JSON data into a readable format maintaining the sequence of speakers.
    """
    sentences = transcript_data["data"]["transcript"]["sentences"]
    parsed_data = []

    for sentence in sentences:
        speaker_name = sentence["speaker_name"]
        text = sentence["text"]
        parsed_data.append(f"{speaker_name}: {text}")

    readable_format = "\n".join(parsed_data)

    return readable_format
