# cleans up the text and prints it
def clean_text(part, text, type):
    # Get the text as a list
    text = str(text[0][part][0])
    text = text.split(',')[3: -2]

    # Turn the text back into a string to remove the brackets and quotes
    text = (str(text)).replace('[', '').replace(']', '')
    text = text.replace("'", '').replace('"', '').replace('result=', '')

    # Split the text into a list of sentences
    text_list = text.split('. ')

    if part == 'summary':
        print(f'\n{type} SUMMARY:')
    elif part == 'document':
        print('\nORIGINAL TEXT:')

    # Print the sentences in the text
    for i in range(len(text_list)):
        if i == len(text_list) - 1:
            print(f'{text_list[i].strip()}')
        else:
            print(f'{text_list[i].strip()}.')
    print()

    return text

# prints the original text and then the summary from the text
def make_summary(result, type):
    document = clean_text('document', result, type)
    summary = clean_text('summary', result, type)
    return summary