import random

def main():

    real_value = 5
    Px = 5
    Fx = 0
    Rt = 1.1666
    Qt = 0

    values = []
    covariance = []

    for i in range(2000):
        # real_value += 0.0002
        kalman_gain = Px/(Px+Rt)
        noise = (random.random()-0.5)
        value = real_value+noise
        estimated_value = Fx+kalman_gain*(value-Fx)
        estimated_covariance = (1-kalman_gain)*Px
        Fx = estimated_value
        Px = estimated_covariance + Qt
        values.append(estimated_value)
        covariance.append(estimated_covariance)

    print(f"Real Value {real_value}")
    print(f"Average Measure: {sum(values)/len(values)}")
    print(f"Average Covariance: {sum(covariance)/len(covariance)}")

if __name__ == "__main__":
    main()