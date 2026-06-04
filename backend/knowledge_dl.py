DL_KNOWLEDGE = [
    {
        "topic": "Neural Network Basics",
        "aliases": ["neural network", "neural networks", "ann", "artificial neural network", "deep learning"],
        "content": (
            "A neural network has layers of neurons that transform input step by step. "
            "Each connection has a weight, and activation functions add non-linearity. "
            "Deep learning means using many hidden layers to learn complex patterns."
        ),
        "category": "dl"
    },
    {
        "topic": "Activation Functions",
        "aliases": ["activation", "activation function", "relu", "sigmoid", "softmax", "tanh"],
        "content": (
            "Activation functions help neural networks learn non-linear relationships. "
            "ReLU is common in hidden layers, sigmoid is often used for binary outputs, "
            "and softmax is used for multi-class classification."
        ),
        "category": "dl"
    },
    {
        "topic": "Loss Function",
        "aliases": ["loss", "loss function", "objective function", "cost function"],
        "content": (
            "A loss function tells the model how wrong its prediction is. "
            "Training tries to reduce this value. "
            "Examples include cross-entropy for classification and mean squared error for regression."
        ),
        "category": "dl"
    },
    {
        "topic": "Cross Entropy",
        "aliases": ["cross entropy", "binary cross entropy", "categorical cross entropy"],
        "content": (
            "Cross-entropy loss compares predicted probabilities with the true class labels. "
            "It is widely used in classification because it strongly penalizes confident wrong predictions."
        ),
        "category": "dl"
    },
    {
        "topic": "Mean Squared Error",
        "aliases": ["mean squared error", "mse"],
        "content": (
            "Mean squared error measures the average squared difference between predicted and actual values. "
            "It is common in regression problems."
        ),
        "category": "dl"
    },
    {
        "topic": "Gradient Descent",
        "aliases": ["gradient descent", "optimizer", "optimization", "sgd", "adam"],
        "content": (
            "Gradient descent updates model parameters in the direction that reduces loss. "
            "The gradient shows which direction increases or decreases the loss fastest. "
            "Optimizers like SGD and Adam are practical ways to do these updates."
        ),
        "category": "dl"
    },
    {
        "topic": "Backpropagation",
        "aliases": ["backpropagation", "backprop", "chain rule"],
        "content": (
            "Backpropagation computes how much each weight contributed to the error. "
            "It uses the chain rule to pass gradients backward through the network. "
            "Those gradients are then used by an optimizer to update weights."
        ),
        "category": "dl"
    },
    {
        "topic": "Regularization",
        "aliases": ["regularization", "l1", "l2", "ridge", "lasso", "weight decay"],
        "content": (
            "Regularization reduces overfitting by discouraging overly complex models. "
            "L1 can push some weights toward zero, while L2 penalizes large weights smoothly."
        ),
        "category": "dl"
    },
    {
        "topic": "Dropout",
        "aliases": ["dropout"],
        "content": (
            "Dropout randomly turns off some neurons during training so the network does not depend too heavily on any single path. "
            "This improves generalization and helps reduce overfitting."
        ),
        "category": "dl"
    },
    {
        "topic": "Batch Size and Epochs",
        "aliases": ["batch size", "mini batch", "epoch", "epochs", "iteration", "iterations"],
        "content": (
            "Batch size is the number of examples used in one parameter update. "
            "An epoch means the model has seen the full training set once."
        ),
        "category": "dl"
    },
    {
        "topic": "CNN",
        "aliases": ["cnn", "convolutional neural network", "convolution"],
        "content": (
            "A CNN is a neural network designed for images and grid-like data. "
            "It uses convolution filters to detect local patterns such as edges and textures, "
            "then deeper layers combine them into higher-level features."
        ),
        "category": "dl"
    },
    {
        "topic": "RNN and LSTM",
        "aliases": ["rnn", "lstm", "gru", "recurrent neural network", "sequence model"],
        "content": (
            "RNNs process sequence data one step at a time while carrying hidden state. "
            "LSTMs improve this by using gates to preserve useful information over longer sequences."
        ),
        "category": "dl"
    },
    {
        "topic": "Transfer Learning",
        "aliases": ["transfer learning", "pretrained model", "pre-trained model"],
        "content": (
            "Transfer learning starts from a model already trained on a large dataset and adapts it to a new task. "
            "This often reduces training time and improves results when data is limited."
        ),
        "category": "dl"
    },
    {
        "topic": "Autoencoder",
        "aliases": ["autoencoder", "encoder decoder network"],
        "content": (
            "An autoencoder learns to compress data into a compact representation and reconstruct it again. "
            "It is often used for representation learning, denoising, and anomaly detection."
        ),
        "category": "dl"
    },
    {
        "topic": "GAN",
        "aliases": ["gan", "gans", "generative adversarial network", "generative adversarial networks"],
        "content": (
            "A GAN has two networks: a generator that creates samples and a discriminator that tries to distinguish real from fake. "
            "They train against each other to produce realistic outputs."
        ),
        "category": "dl"
    },
    {
        "topic": "Vanishing and Exploding Gradients",
        "aliases": ["vanishing gradient", "exploding gradient", "vanishing gradients", "exploding gradients"],
        "content": (
            "Vanishing gradients make parameter updates too small in deep networks, while exploding gradients make them too large and unstable. "
            "Good initialization, normalization, gating, and residual connections help reduce these problems."
        ),
        "category": "dl"
    },
    {
        "topic": "Residual Connections",
        "aliases": ["residual connection", "skip connection", "resnet", "residual network"],
        "content": (
            "Residual connections let information skip layers directly, making deep networks easier to train and helping gradients flow better."
        ),
        "category": "dl"
    },
    {
        "topic": "Batch Normalization",
        "aliases": ["batch normalization", "batchnorm", "batch norm", "layer normalization", "layer norm"],
        "content": (
            "Normalization layers stabilize training by controlling activation distributions. "
            "Batch normalization is common in CNNs, while layer normalization is common in transformers."
        ),
        "category": "dl"
    }
]
