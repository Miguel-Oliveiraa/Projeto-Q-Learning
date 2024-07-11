def parse_analysis_file(filename):
    configurations = []
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    i = 0
    while i < len(lines) / 14:  # Itera a cada bloco de 14 linhas
        config = {}
        
        # Processa lr, gamma, exploration_proba
        line = lines[i * 14].strip()
        config['lr'] = float(line.split()[1])
        
        line = lines[i * 14 + 1].strip()
        config['gamma'] = float(line.split()[1])
        
        line = lines[i * 14 + 2].strip()
        config['exploration_proba'] = float(line.split()[1])
        
        # Calcula mean_reward
        mean_rewards = []
        for j in range(10):
            line = lines[i * 14 + 4 + j].strip()
            mean_rewards.append(float(line.split()[3]))
        
        mean_reward_avg = sum(mean_rewards) / 10
        config['mean_reward'] = mean_reward_avg
        
        configurations.append(config)
        i += 1
    
    # Ordena configurations por mean_reward
    configurations.sort(key=lambda x: x['mean_reward'])
    
    return configurations

def write_ordered_analysis(configurations, output_file):
    with open(output_file, 'w') as file:
        for config in configurations:
            file.write(f"lr: {config['lr']}\n")
            file.write(f"gamma: {config['gamma']}\n")
            file.write(f"exploration_proba: {config['exploration_proba']}\n")
            file.write(f"mean_reward: {config['mean_reward']}\n\n")

# Main script
if __name__ == "__main__":
    analysis_file = 'analysis.txt'
    ordered_output_file = 'ordered_analysis.txt'
    
    # Parse the analysis file
    configurations = parse_analysis_file(analysis_file)
    
    # Write ordered analysis to output file
    write_ordered_analysis(configurations, ordered_output_file)
    
    print(f"Ordered analysis saved to {ordered_output_file}")
