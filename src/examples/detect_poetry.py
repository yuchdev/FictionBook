import json
import string
import argparse


def analyze_text(text):
    """
    Analyzes the given text by splitting it into lines and stanzas, and collecting
    metadata on the line lengths, punctuation counts, and stanzas.

    :param text: The text to be analyzed, provided as a string.
    :type text: str
    :return: A dictionary containing metadata about lines, stanzas, and overall analysis,
             including line length, punctuation counts, and stanza information.
    :rtype: dict
    """
    lines = text.split('\n')
    metadata = {
        'lines': [],
        'stanzas': []
    }
    stanza = []
    stanza_number = 0
    line_number = 0
    punctuation_set = set(string.punctuation)

    for idx, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line == '':
            # Empty line indicates stanza break
            if stanza:
                # Analyze the stanza
                stanza_metadata = analyze_stanza(stanza, stanza_number)
                metadata['stanzas'].append(stanza_metadata)
                stanza = []
                stanza_number += 1
        else:
            # Collect line metadata
            line_punctuation_counts = count_punctuation(line, punctuation_set)
            line_length = len(line)
            line_metadata = {
                'line_number': line_number,
                'stanza_number': stanza_number,
                'length': line_length,
                'punctuation_counts': line_punctuation_counts
            }
            metadata['lines'].append(line_metadata)
            stanza.append(line_metadata)
            line_number += 1

    # Add the last stanza if any
    if stanza:
        stanza_metadata = analyze_stanza(stanza, stanza_number)
        metadata['stanzas'].append(stanza_metadata)

    # After collecting all metadata, perform overall analysis
    overall_analysis = perform_overall_analysis(metadata)
    metadata['overall'] = overall_analysis

    return metadata


def count_punctuation(text, punctuation_set):
    """
    Count occurrences of punctuation characters in the given text.

    This function takes a string of text and a set of punctuation characters
    and returns a dictionary with the punctuation characters as keys and the
    count of their occurrences in the text as values.

    :param text: The input string to search for punctuation characters.
    :param punctuation_set: A set of punctuation characters to count in the text.
    :return: A dictionary with punctuation characters as keys and their counts as values.
    """
    punctuation_counts = {}
    for char in text:
        if char in punctuation_set:
            punctuation_counts[char] = punctuation_counts.get(char, 0) + 1
    return punctuation_counts


def analyze_stanza(stanza_lines, stanza_number):
    """
    Analyzes a stanza by aggregating line counts, total length, and punctuation
    statistics.

    :param stanza_lines: A list of dictionaries, where each dictionary represents
                         a line in the stanza with 'length' and 'punctuation_counts' keys.
    :type stanza_lines: list[dict]
    :param stanza_number: The position or number of the stanza in the poem.
    :type stanza_number: int
    :return: A dictionary containing metadata about the stanza including
             stanza number, line count, total length, and punctuation counts.
    :rtype: dict
    """
    stanza_line_count = len(stanza_lines)
    stanza_length = sum(line['length'] for line in stanza_lines)

    # Aggregate punctuation counts for the stanza
    stanza_punctuation_counts = {}
    for line in stanza_lines:
        for punc, count in line['punctuation_counts'].items():
            stanza_punctuation_counts[punc] = stanza_punctuation_counts.get(punc, 0) + count

    stanza_metadata = {
        'stanza_number': stanza_number,
        'line_count': stanza_line_count,
        'total_length': stanza_length,
        'punctuation_counts': stanza_punctuation_counts
    }
    return stanza_metadata


def perform_overall_analysis(metadata):
    """
    Analyzes textual metadata to compute various aggregate statistics.

    This function takes a dictionary containing metadata of a text, including details
    about lines, stanzas, and punctuations, and computes aggregate information like the
    total number of lines, total stanzas, total length, average line length, punctuation
    counts and stanza patterns.

    :param metadata:
        The metadata of the text to be analyzed. It should include 'lines' and 'stanzas',
        where 'lines' is a list of dictionaries with each dictionary containing 'length'
        and 'punctuation_counts', and 'stanzas' is a list of dictionaries with each dictionary
        containing 'line_count'.
    :type metadata: dict

    :return:
        A dictionary containing computed overall statistics which includes 'total_lines',
        'total_stanzas', 'total_length', 'average_line_length', 'total_punctuation_counts',
        'stanza_line_counts', and 'stanza_patterns'.
    :rtype: dict
    """
    total_lines = len(metadata['lines'])
    total_stanzas = len(metadata['stanzas'])
    total_length = sum(line['length'] for line in metadata['lines'])

    # Aggregate punctuation counts for the entire text
    total_punctuation_counts = {}
    for line in metadata['lines']:
        for punc, count in line['punctuation_counts'].items():
            total_punctuation_counts[punc] = total_punctuation_counts.get(punc, 0) + count

    # Calculate average line length
    if total_lines > 0:
        average_line_length = total_length / total_lines
    else:
        average_line_length = 0

    # Analyze stanza patterns
    stanza_line_counts = [stanza['line_count'] for stanza in metadata['stanzas']]
    stanza_patterns = {}
    for count in stanza_line_counts:
        stanza_patterns[count] = stanza_patterns.get(count, 0) + 1

    overall_metadata = {
        'total_lines': total_lines,
        'total_stanzas': total_stanzas,
        'total_length': total_length,
        'average_line_length': average_line_length,
        'total_punctuation_counts': total_punctuation_counts,
        'stanza_line_counts': stanza_line_counts,
        'stanza_patterns': stanza_patterns
    }
    return overall_metadata


def main():
    """
    :return: system exit code
    """
    parser = argparse.ArgumentParser(description="Poetry Analysis")
    parser.add_argument("input_file", help="Path to the input text file")
    parser.add_argument("output_file", help="Path to the output JSON file")
    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file

    # Read text from the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Perform analysis
    metadata = analyze_text(text)

    # Save results to a JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    print(f"Analysis complete. Results saved to '{output_file}'.")


if __name__ == '__main__':
    main()
