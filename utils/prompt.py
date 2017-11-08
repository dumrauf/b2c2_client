def is_allowed_to_proceed():
    question = 'Proceed?: [Y/n] '
    answer = raw_input(question)
    if answer and answer[0] == 'Y':
        return True
    return False
