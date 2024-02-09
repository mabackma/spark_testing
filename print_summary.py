def print_text(part, text, type):

    # Get the text as a list
    text = str(text[0][part][0])
    text = text.split(',')[3: -2]

    # Turn the text back into a string to remove the brackets and quotes
    text = (str(text)).replace('[','').replace(']','')
    text = text.replace("'", '').replace('"', '').replace('result=', '')

    # Split the text into a list of sentences
    text = text.split('. ')

    if part == 'summary':
        print(f'\n{type} SUMMARY:')
    elif part == 'document':
        print('\nORIGINAL TEXT:')

    # Print the sentences in the text
    for i in range(len(text)):
        if i == len(text) - 1:
            print(f'{text[i].strip()}')
        else:
            print(f'{text[i].strip()}.')
    print()

def print_summary(result, type):
    print_text('document', result, type)
    print_text('summary', result, type)