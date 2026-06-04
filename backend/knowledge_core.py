CORE_KNOWLEDGE = [
    {
        "topic": "Accuracy Precision Recall",
        "aliases": ["accuracy", "precision", "recall", "metrics", "evaluation metrics"],
        "content": (
            "Accuracy is the fraction of total predictions that are correct. "
            "Precision measures how many predicted positives were actually positive. "
            "Recall measures how many actual positives were correctly found. "
            "Use precision when false positives are costly, and recall when false negatives are costly."
        ),
        "category": "core"
    },
    {
        "topic": "Confusion Matrix and F1 Score",
        "aliases": ["confusion matrix", "f1", "f1 score", "true positive", "false positive", "false negative"],
        "content": (
            "A confusion matrix summarizes prediction outcomes using true positives, true negatives, "
            "false positives, and false negatives. "
            "F1 score is the harmonic mean of precision and recall."
        ),
        "category": "core"
    },
    {
        "topic": "Bias vs Variance",
        "aliases": ["bias variance", "bias vs variance", "high bias", "high variance"],
        "content": (
            "Bias means the model is too simple and misses the real pattern, which often causes underfitting. "
            "Variance means the model is too sensitive to training data and may memorize noise, which often causes overfitting."
        ),
        "category": "core"
    },
    {
        "topic": "Overfitting and Underfitting",
        "aliases": ["overfitting", "underfitting", "generalization"],
        "content": (
            "Overfitting means the model memorizes training data and performs poorly on new data. "
            "Underfitting means the model is too simple to learn the pattern. "
            "Regularization, more data, and validation help control this."
        ),
        "category": "core"
    },
    {
        "topic": "Train Validation Test Split",
        "aliases": ["train test split", "validation set", "test set", "training set"],
        "content": (
            "The training set teaches the model, the validation set helps tune choices, and the test set measures final performance on unseen data."
        ),
        "category": "core"
    },
    {
        "topic": "Feature Engineering",
        "aliases": ["feature engineering", "features", "feature selection", "feature extraction"],
        "content": (
            "Feature engineering means creating or selecting useful input variables so the model can learn patterns more effectively. "
            "Good features often improve model performance more than changing the algorithm."
        ),
        "category": "core"
    },
    {
        "topic": "Hyperparameters and Tuning",
        "aliases": ["hyperparameter", "hyperparameters", "tuning", "hyperparameter tuning", "grid search", "random search"],
        "content": (
            "Hyperparameters are settings chosen before training, such as learning rate, batch size, or tree depth. "
            "Tuning means searching for values that improve validation performance."
        ),
        "category": "core"
    },
    {
        "topic": "Learning Rate",
        "aliases": ["learning rate", "step size", "lr"],
        "content": (
            "The learning rate controls how large each parameter update is during training. "
            "If it is too high, training can become unstable. If it is too low, learning becomes very slow."
        ),
        "category": "core"
    },
    {
        "topic": "Class Imbalance",
        "aliases": ["class imbalance", "imbalanced data", "imbalanced dataset", "minority class", "majority class"],
        "content": (
            "Class imbalance means one class appears much more often than another. "
            "In such cases, accuracy alone can be misleading, so precision, recall, F1, resampling, or class weighting become important."
        ),
        "category": "core"
    },
    {
        "topic": "Data Leakage",
        "aliases": ["data leakage", "leakage", "target leakage"],
        "content": (
            "Data leakage happens when information from validation, test, or future data accidentally reaches training. "
            "This makes performance look better than it really is."
        ),
        "category": "core"
    }
]
