import connection as cn
import socket
import numpy as np

def move(Q, exploration_proba, state_code):
    if np.random.uniform(0,1) < exploration_proba:
        return np.random.choice([0, 1, 2])
    return np.argmax(Q[state_code, :])

def main():
    # Connect
    c = cn.connect(2037)
    
    if isinstance(c, socket.socket):
        # Q-table
        try:
            Q = np.loadtxt('resultado.txt')
        except:
            Q = np.zeros([24 * 4, 3])
        
        #initialize the exploration probability to 1
        exploration_proba = 0.1

        #discounted factor
        gamma = 0.95

        #learning rate
        lr = 0.7
        
        moves = ["left", "right", "jump"]
        acao = 2

        state, reward = cn.get_state_reward(c, "")
        plataforma = int(state[2:6], 2)
        direction = int(state[-2:], 2)
        total_episode_reward = 0
        # Game
        print("\nInitial State: "+state+"\nPlataforma: " + str(plataforma)+"\nDireção: " + str(direction)+"\nreward: "+str(reward)+"\n")

        while(True):   
            # Converte o state em um número inteiro
            state_code = int(state, 2) 

            acao = move(Q, exploration_proba, state_code)
            
            # Executa ação e recebe state e reward
            next_state, reward = cn.get_state_reward(c, moves[acao])
            next_state_code = int(next_state, 2)            
            plataforma = int(next_state[2:6], 2)
            direction = int(next_state[-2:], 2)
            print("Ação efetuada: " + moves[acao] + "\nnew state: "+next_state+"\nPlataforma: " + str(plataforma)+"\nDireção: " + str(direction)+"\nreward: "+str(reward)+"\n")

            # Update Q-table
            Q[state_code, acao] = (1 - lr) * Q[state_code, acao] + lr * (reward + gamma * np.max(Q[next_state_code, :]))              
            np.savetxt('resultado.txt', Q)

            total_episode_reward = total_episode_reward + reward
            # Update state
            state = next_state
        
        # exploration_proba = max(min_exploration_proba, np.exp(-exploration_decreasing_decay*e))
    else:
        print('Connection failed!')
    
    

    
main()