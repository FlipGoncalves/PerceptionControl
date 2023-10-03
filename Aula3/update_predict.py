# measurement integration
def update(mean1, var1, mean2, var2):
    # mean1, var1 -> previous belief
    # mean2, var2 -> state we can derive from the measurement
    new_mean = (mean1*var2 + mean2*var1)/(var1 + var2)
    new_var = (var1*var2)/(var1 + var2)
    return [new_mean, new_var]

# motion forecast
def predict(mean1, var1, mean2, var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]