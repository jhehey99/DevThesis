import matplotlib.pyplot as plt
import numpy as np


def calculate_cost(theta, X, y):
    m = len(y)
    predictions = X.dot(theta)
    cost = (1/(2*m)) * np.sum(np.square(predictions - y))
    return cost


def apply_gradientDescent(X, y, theta, learning_rate = 0.01, iterations = 100):
    m = len(y)
    cost_history = np.zeros(iterations)
    theta_history = np.zeros((iterations, 2))

    for i in range(iterations):
        prediction = np.dot(X, theta)

        theta = theta - (1/m) * learning_rate * (X.T.dot((prediction - y)))
        theta_history[i,:] = theta.T
        cost_history[i] = calculate_cost(theta, X, y)

    return theta, cost_history, theta_history


def main():
    # initialize data
    np.random.seed(2)
    X = 2 * np.random.rand(100, 1)
    y = 4 + 3 * X + np.random.randn(100, 1)

    # apply
    lr = 0.1
    n_iter = 1000
    theta = np.random.randn(2, 1)

    X_b = np.c_[np.ones((len(X), 1)), X]
    theta, cost_history, theta_history = apply_gradientDescent(X_b, y, theta, lr, n_iter)

    theta0 = float("{:0.4f}".format(theta[0][0]))
    theta1 = float("{:0.4f}".format(theta[1][0]))
    
    theta0_str = str(theta0)
    theta1_str = str(theta1)

    eq_str = "y = " + theta0_str + " + " + theta1_str + "x"
    print("Theta 0: " + theta0_str)
    print("Theta 1: " + theta1_str)
    print("MSE: {:0.4f}".format(cost_history[-1]))
    print("Final Equation: " + eq_str)

    # plot cost function
    fig1 = plt.figure(1, figsize=(12,5))
    plt.subplot(121)
    plt.plot(cost_history)
    plt.ylabel("Cost History"); plt.xlabel("Iterations")

    # plot initial data and final equation
    plt.subplot(122)
    x_ = np.linspace(0, 2, 100)
    y_ = theta0 + theta1*x_
    plt.plot(x_, y_, 'r')
    plt.scatter(X, y)
    plt.title(eq_str)
    plt.grid()
    plt.tight_layout()
    plt.show()




if __name__ == "__main__":
    main()

    # TODO: input is from file
    # regression dito
    # TODO: output is sa file then read ng node js