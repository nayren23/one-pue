import numpy as np

def accumulate(value, mu: float = 0, sigma: float = 1):
    """mu: moyenne du changement
       sigma: écart type du changement"""
    change = np.random.normal(mu, sigma)
    return value + change

if __name__ == "__main__":
    val = 100
    for _ in range(10):
        # mu: de cmb tend à augmenter ou diminuer le compteur par itération (par seconde du coup)
        # sigma: de cmb l'augmentation varie. Si parfois c'est +0.8 max, parfois +1.2 max alors sigma = 0.2
        val = accumulate(val, mu=0.9, sigma=0.3)
        print(f"{val:.2f}")