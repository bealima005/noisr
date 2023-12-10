import random
import matplotlib.pyplot as plt


def random_walk(num_steps, prob_right, num_particles):

    particle_paths = []   # lista para guardar o caminho de todas as partículas

    for _ in range(num_particles):
        posição = [0]     # lista criada para cada partícula, que guarda a sua posição de acordo com o ciclo seguinte: (todas as partículas começam na posição 0)

        for _ in range(num_steps):
            x = random.uniform(0,1)  #número gerado aleatoriamente usado para a comparação com a probabilidade da partícula ir para a direita

            # se x for menor ou igual à probabilidade definida, a posição nova encontra-se à direita da anterior 
            if x <= prob_right:
                px_nova = posição[-1] + 1
                posição.append(px_nova)
            
            # se x for maior que probabilidade definida, a posição nova encontra-se à esquerda da anterior 
            else:
                px_nova = posição[-1] - 1
                posição.append(px_nova)

        particle_paths.append(posição) # guarda-se a nova posição na lista do caminho de cada partícula

    create_plot(num_steps, particle_paths)

    return particle_paths

def create_plot (num_steps, particle_paths):
            
    time = [x for x in range(len(particle_paths[0]))]

    for particle_path in particle_paths:
        plt.plot(particle_path, time)

    plt.title('Random Walk - N particles')
    plt.xlabel('Position')
    plt.ylabel('Time')
    plt.show()

num_steps = 456 # Número de passos das partículas
prob_right = 0.54 # Probabilidade de se mover para a direita
num_particles = 67 # Número of particulas que existe

random_walk (num_steps, prob_right, num_particles)
