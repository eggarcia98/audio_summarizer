def merge_overlapping_transcripts(transcripts):
    """Merge overlapping transcripts to remove duplicates and adjust timings."""
    if not transcripts:
        return []

    merged_transcripts = []
    current_transcript = transcripts[0]

    for i in range(1, len(transcripts)):
        next_transcript = transcripts[i]

        # Check for overlapping transcripts
        if current_transcript['audio_end_time'] > next_transcript['audio_start_time']:
            current_transcript_text = current_transcript['transcript']
            next_transcript_text = next_transcript['transcript']

            # Find the index in next_transcript_text where the overlap ends
            overlap_index = next_transcript_text.find(current_transcript_text.split()[-1])
            if overlap_index != -1:
                # Remove the overlapping part from next_transcript
                next_transcript_text = next_transcript_text[overlap_index + len(current_transcript_text.split()[-1]):].strip()

                next_transcript['transcript'] = next_transcript_text
                next_transcript['audio_start_time'] = current_transcript['audio_end_time']

        # Append the current transcript to the merged list
        merged_transcripts.append(current_transcript)
        current_transcript = next_transcript

    # Append the last transcript
    merged_transcripts.append(current_transcript)
    return merged_transcripts
