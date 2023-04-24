def citire_automat(file_name):
    with open(file_name, "r") as file:
        states = file.readline().strip().split()  
        initial_state = file.readline().strip()  
        final_states = file.readline().strip().split() 
        alphabet = file.readline().strip().split()  
        stack_alphabet = file.readline().strip().split()  
        stack_symbol = file.readline().strip()  
        transitions = {}  


        for line in file:
            transition = line.strip().split()
            state = transition[0]
            symbol = transition[1]
            top_of_stack = transition[2]
            new_state = transition[3]
            new_top_of_stack = transition[4].split(',')
            if state not in transitions:
                transitions[state] = {}
            if symbol not in transitions[state]:
                transitions[state][symbol] = {}
            if top_of_stack not in transitions[state][symbol]:
                transitions[state][symbol][top_of_stack] = []
            transitions[state][symbol][top_of_stack].append((new_state, new_top_of_stack))

    return states, initial_state, final_states, alphabet, stack_alphabet, stack_symbol, transitions



def verifica_sir(automat, sir):
    states, initial_state, final_states, alphabet, stack_alphabet, stack_symbol, transitions = automat
    stack = [stack_symbol]  
    current_states = [initial_state]  

    for symbol in sir:
        new_current_states = []
        for state in current_states:
            if state in transitions and symbol in transitions[state] and stack[-1] in transitions[state][symbol]:
                for new_state, new_top_of_stack in transitions[state][symbol][stack[-1]]:
                    if new_state not in new_current_states:
                        new_current_states.append(new_state)
                    if new_top_of_stack != "lambda":
                        stack.extend(reversed(new_top_of_stack))
            if state in transitions and "lambda" in transitions[state] and stack[-1] in transitions[state]["lambda"]:
                for new_state, new_top_of_stack in transitions[state]["lambda"][stack[-1]]:
                    if new_state not in new_current_states:
                        new_current_states.append(new_state)
                    if new_top_of_stack != "lambda":
                        stack.extend(reversed(new_top_of_stack))
        current_states = new_current_states

    for state in current_states:
        if state in final_states and len(stack) == 1 and stack[-1] == stack_symbol:
            return "DA"  

    return "NU"  



states = ['q0', 'q1', 'q2', 'q3', 'q4']
initial_state = 'q0'
final_states = ['q4']
alphabet = ['a', 'b']
stack_alphabet = ['X', 'Y']
stack_symbol = 'Z'
transitions = {
    'q0': {
        'a': {
            'Z': [('qo', 'aZ')]  
        },
        'b': {
            'Z': [('q0', 'bZ')]  
        },
        'a': {
            'a': [('q0', 'aa')]  
        },
        'a': {
            'b': [('q0', 'ab')]  
        },
        'b': {
            'a': [('q0', 'ba')]  
        },
        'b': {
            'b': [('q0', 'bb')]  
        },
        'a': {
            'a': [('q1', 'a')]  
        },
        'b': {
            'b': [('q1', 'b')]  
        }
    },
    'q1': {
        'a': {
            'a': [('q2', 'a')] # X = a q1 --> q2 e a (Y) pe stiva si il pune pe a(Y)
        },
        'a': {
            'b': [('q2', 'a')] # X= a q1 --> q2 e b (Y) pe stiva si il pune pe a(Y)
        },
        'b': {
            'a': [('q2', 'a')] 
        },
        'b': {
            'b': [('q2', 'b')] 
        },
        'a': {
            'a': [('q3', 'a')] 
        },
        'b': {
            'b': [('q3', 'b')] 
        },
    },
    'q2': {
        'a': {
            'a': [('q2', 'a')] # X = a q1 --> q2 e a (Y) pe stiva si il pune pe a(Y)
        },
        'a': {
            'b': [('q2', 'a')] # X= a q1 --> q2 e b (Y) pe stiva si il pune pe a(Y)
        },
        'b': {
            'a': [('q2', 'a')] 
        },
        'b': {
            'b': [('q2', 'b')] 
        },
    },
    'q3': {
        'a': {
            'a': [('q3', 'lamba')]  
        },
        'a': {
            'b': [('q3', 'lambda')]  
        },
        'b': {
            'a': [('q3', 'lambda')]  
        },
        'b': {
            'b': [('q3', 'lambda')]  
        },
        'lambda': {
            'Z': [('q4', 'Z')]  
        },
        
    },
}
automat = (states, initial_state, final_states, alphabet, stack_alphabet, stack_symbol, transitions)

#siruri_test = ["bab","ab", "abb", "aabbb", "a", "b", "ba", "bbb", "bba" ]
siruri_test = ['bbbaaaaabbbb', 'bbbaaaabbb', 'aaaaba']
for sir in siruri_test:
    rezultat = verifica_sir(automat, sir)
    print("Pentru șirul '{}', rezultatul este: {}".format(sir, rezultat))
